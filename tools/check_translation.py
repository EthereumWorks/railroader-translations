#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_translation.py -- the acceptance gate for a Railroader translation.

Run it before you open a pull request. It is the same set of rules the maintainer
runs, so if this is quiet your translation is very likely to be merged as-is.

    python tools/check_translation.py            # every language in Translate/
    python tools/check_translation.py FR          # just one
    python tools/check_translation.py FR --pages  # ...and draw the notebook pages
                                                  # the way the game will draw them

Exit code 0 = no errors (warnings are allowed to stay). Exit code 1 = something
would be broken or invisible in-game.

Every rule below exists because the game does something specific:

  * The files are read with java.nio.Files.readString + org.json.JSONObject
    (zombie/core/Translator.java:247-266). readString is ALWAYS UTF-8, and a
    byte-order mark makes JSONObject throw -- which drops the whole file, not
    the one string. Hence: UTF-8, no BOM, valid JSON.
  * A key that is missing, or whose value is an empty string, falls back to
    English (the same function loads EN first and only overwrites with a
    non-empty value). So a partial translation is safe, and "" is the honest way
    to say "leave this one in English".
  * "%1" is a positional argument the game substitutes at runtime. Lose it and
    the sentence loses the number that was its point.
  * The engineer's notebook is drawn by the vanilla journal UI, which shows 15
    lines of one page and no more -- text past that is not scrolled to, it is
    simply never seen. We budget 14 lines x 50 columns.
  * The control stand (HUD) draws its labels at fixed positions inside dials and
    boxes. A label much longer than the English one runs into its neighbour.
"""

import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TRANSLATE = os.path.join(ROOT, "Translate")

SOURCE_LANG = "EN"
FILES = ["IG_UI", "ItemName", "Tooltip", "Recipes", "UI", "Fluids"]

# The folder names Project Zomboid itself ships (media/lua/shared/Translate).
# A language outside this list needs its own language.txt to even appear in the
# options screen (zombie/core/Languages.java:69) -- open an issue first.
PZ_LANGUAGES = {
    "AR", "CA", "CH", "CN", "CS", "DA", "DE", "EN", "ES", "ES_CL", "ES_MX",
    "FI", "FR", "HU", "ID", "IT", "JP", "KO", "NL", "NO", "PL", "PT", "PTBR",
    "RO", "RU", "TH", "TR", "UA",
}

# The journal page budget (mirrors RR_Manual.MAX_LINES / MAX_COLS in the mod).
PAGE_LINES = 14
PAGE_COLS = 50

# Keys that must be copied verbatim: a locomotive model is a model designation,
# not a word.
KEEP_VERBATIM = {"IGUI_RR_Model_GP7"}

# Display-width ceilings for text drawn inside the control stand. Measured
# against the widest thing English and Russian already put there (RU "ПРОКРУТКА"
# is 9, "СОСТ" is 4), with a little slack.
WIDTH_LIMITS = [
    (re.compile(r"^IGUI_RR_HudRev[FNR]$"), 2),
    (re.compile(r"^IGUI_RR_HudLamp"), 6),
    (re.compile(r"^IGUI_RR_Hud(Throttle|Starter|Reverser|Idle|Run|Prime|Crank"
                r"|Warming|Start|Dead|Range)$"), 10),
    (re.compile(r"^IGUI_RR_Hint"), 12),
]

# The supporters' page carries people's handles. A handle is spelled the way its
# owner spells it, in every language.
SUPPORTERS_KEY = "IGUI_RR_Note_Supporters"

# The translator's own credit page: empty in EN and RU (the mod's own text), one
# page in your language if you want the credit in-game. See CONTRIBUTING.
CREDIT_KEY = "IGUI_RR_Note_Translation"

NOTE_PREFIX = "IGUI_RR_Note_"

RE_ARG = re.compile(r"%(\d+)")
# A bracketed single letter is a KEY ENGRAVED ON THE KEYBOARD -- "[W]",
# "[Shift+F]". Those are the same in every language and must survive translation.
# A bracketed WORD is a word: "[Space]" is the name of the long key and may be
# translated, "[debug]" is ordinary text.
RE_BRACKET = re.compile(r"\[((?:Shift\+)?[A-Z])\]")


# --------------------------------------------------------------------------
# display width -- an East Asian wide character occupies two columns of the
# journal page, a combining mark none.
# --------------------------------------------------------------------------
def width(s):
    n = 0
    for ch in s:
        if unicodedata.combining(ch):
            continue
        n += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return n


def wrap(text, cols=PAGE_COLS):
    """The lines the journal will really draw. Mirrors RR_Manual.wrap():
    authored breaks first, then greedy word wrap; a word with no space in it is
    left alone and reported as too wide (which is what happens on screen)."""
    lines = []
    for para in text.split("\n"):
        if width(para) <= cols:
            lines.append(para)
            continue
        cur = None
        for word in para.split():
            if cur is None:
                cur = word
            elif width(cur) + 1 + width(word) <= cols:
                cur = cur + " " + word
            else:
                lines.append(cur)
                cur = word
        if cur is not None:
            lines.append(cur)
    return lines


class Report(object):
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, lang, where, msg):
        self.errors.append("%s  %-22s %s" % (lang, where, msg))

    def warn(self, lang, where, msg):
        self.warnings.append("%s  %-22s %s" % (lang, where, msg))


def load_json(path, lang, fname, rep):
    """Read one file the way the game reads it, and say what the game would say."""
    with open(path, "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        rep.error(lang, fname + ".json",
                  "starts with a UTF-8 BOM -- JSONObject throws and the WHOLE file "
                  "is dropped in-game. Save as UTF-8 without BOM.")
        raw = raw[3:]
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        rep.error(lang, fname + ".json",
                  "is not UTF-8 (byte %d: %s). The game reads these files as UTF-8 "
                  "only -- ANSI/Cp1251/GBK will not load." % (e.start, e.reason))
        return None

    seen = {}

    def pairs(items):
        out = {}
        for k, v in items:
            if k in out:
                seen[k] = True
            out[k] = v
        return out

    try:
        data = json.loads(text, object_pairs_hook=pairs)
    except ValueError as e:
        rep.error(lang, fname + ".json", "is not valid JSON: %s" % e)
        return None
    for k in sorted(seen):
        rep.error(lang, fname + ".json",
                  "key '%s' is defined twice -- the second one silently wins" % k)
    if not isinstance(data, dict):
        rep.error(lang, fname + ".json", "must be one JSON object")
        return None
    for k, v in data.items():
        if not isinstance(v, str):
            rep.error(lang, fname + ".json",
                      "'%s' is not a string (every value must be quoted text)" % k)
            return None
    return data


def check_value(lang, fname, key, en, tr, rep):
    where = "%s/%s" % (fname, key)

    if tr == "":
        # The translator's own credit page is empty in English too, and empty there
        # means "there is no such page", not "fall back to the English".
        if key != CREDIT_KEY:
            rep.warn(lang, where, "empty -- the game will show the English text here")
        return

    # A JSON "\n" escape does render as a break in-game, but it is not this mod's
    # convention and it breaks the tooling around it: the suite reads these files a
    # line at a time, so a value that spans lines is a value it cannot see. Write
    # "\\n" (backslash, n) in the file, the way the English does.
    if "\n" in tr:
        rep.error(lang, where,
                  "spans more than one line in the file. Write a break as \\\\n "
                  "(backslash, n) inside the string, exactly as the English does -- "
                  "not as a JSON \\n escape and never by pressing Enter.")

    if key in KEEP_VERBATIM:
        if tr != en:
            rep.error(lang, where, "must stay exactly %r (it is a model designation)" % en)
        return

    # %1 / %2 -- positional arguments the game fills in.
    a_en, a_tr = sorted(RE_ARG.findall(en)), sorted(RE_ARG.findall(tr))
    if a_en != a_tr:
        rep.error(lang, where,
                  "argument mismatch: English has %s, this has %s. Keep every %%N."
                  % (["%" + a for a in a_en] or "none", ["%" + a for a in a_tr] or "none"))

    # [W] [E] [V] ... are physical keyboard keys. Translate the sentence, keep
    # the letter.
    missing = [t for t in RE_BRACKET.findall(en) if ("[" + t + "]") not in tr]
    if missing:
        rep.error(lang, where,
                  "lost the key name(s) %s -- W/S/R/E/V/Q/L/F are the keys on the "
                  "player's keyboard and are the same in every language"
                  % ", ".join("[" + m + "]" for m in missing))

    # "PRESS W" -- the word is translated, the letter is a key on the keyboard. It
    # has no brackets to recognise it by, so the rule is by key prefix.
    if key.startswith("IGUI_RR_Hint"):
        lost = [c for c in re.findall(r"\b([A-Z])\b", en) if c not in tr]
        if lost:
            rep.error(lang, where,
                      "lost the key %s. The player presses that letter on his "
                      "keyboard; translate the word, keep the letter."
                      % ", ".join(lost))

    if "<br>" in en and "<br>" not in tr:
        rep.warn(lang, where,
                 "English breaks this tooltip with <br> and this does not -- long "
                 "tooltips run off the screen")

    if tr == en and len(en) > 3 and key not in KEEP_VERBATIM:
        rep.warn(lang, where, "identical to the English text -- not translated yet?")

    for pattern, limit in WIDTH_LIMITS:
        if pattern.match(key):
            w = width(tr)
            if w > limit:
                rep.error(lang, where,
                          "is %d columns wide; the control stand has room for %d. "
                          "Use the shortest word or an abbreviation a driver would "
                          "recognise (English %r, Russian uses abbreviations)."
                          % (w, limit, en))
            break

    # The engineer's notebook: one key is one whole page.
    if key.startswith(NOTE_PREFIX):
        page = tr.replace("\\n", "\n")
        lines = wrap(page)
        widest = max([width(l) for l in lines] or [0])
        if len(lines) > PAGE_LINES:
            rep.error(lang, where,
                      "is %d lines long; the journal shows %d and the rest is never "
                      "seen. Cut it, or move a fact to another page."
                      % (len(lines), PAGE_LINES))
        if widest > PAGE_COLS:
            hint = ""
            if " " not in page.replace("\n", ""):
                hint = (" This text has no spaces to break on, so you must break the "
                        "lines yourself with \\\\n -- about %d characters per line."
                        % (PAGE_COLS // 2))
            rep.error(lang, where,
                      "has a line %d columns wide; the page is %d wide and the rest "
                      "is cut off.%s" % (widest, PAGE_COLS, hint))


def handles_of(source, reference):
    """The handles printed on the supporters' page, worked out rather than listed:
    a line that is character-for-character the same in English and in Russian is
    not prose, it is somebody's name."""
    en = source["IG_UI"].get(SUPPORTERS_KEY, "").replace("\\n", "\n").split("\n")
    ru = reference.get(SUPPORTERS_KEY, "").replace("\\n", "\n").split("\n")
    return [l for l in en if l and l in ru]


def check_language(lang, source, rep, handles):
    langdir = os.path.join(TRANSLATE, lang)

    if lang not in PZ_LANGUAGES:
        rep.error(lang, "-",
                  "Project Zomboid has no '%s' language folder of its own, so the game "
                  "will never load this one. Open an issue before starting." % lang)

    for fname in FILES:
        path = os.path.join(langdir, fname + ".json")
        en = source[fname]
        if not os.path.exists(path):
            rep.error(lang, fname + ".json",
                      "missing -- its %d strings will all stay English" % len(en))
            continue
        data = load_json(path, lang, fname, rep)
        if data is None:
            continue

        for key in en:
            if key not in data:
                rep.error(lang, "%s/%s" % (fname, key),
                          "missing (the game falls back to English for it)")
        for key in data:
            if key not in en:
                rep.error(lang, "%s/%s" % (fname, key),
                          "is not a key of this mod -- a typo, or a leftover from an "
                          "older version. Nothing reads it.")

        for key, value in data.items():
            if key in en:
                check_value(lang, fname, key, en[key], value, rep)

        # Handles are not translatable: a name is spelled the way its owner spells
        # it. Translate the heading and the thank-you line, copy the names.
        if fname == "IG_UI" and data.get(SUPPORTERS_KEY):
            page = data[SUPPORTERS_KEY].replace("\\n", "\n")
            for name in handles:
                if name not in page:
                    rep.error(lang, "IG_UI/" + SUPPORTERS_KEY,
                              "does not contain the handle %r. Translate the heading "
                              "and the thank-you; copy the names exactly." % name)


def draw_pages(lang, source):
    """Print every notebook page as the journal will lay it out."""
    path = os.path.join(TRANSLATE, lang, "IG_UI.json")
    if not os.path.exists(path):
        print("no IG_UI.json for " + lang)
        return
    with open(path, "rb") as f:
        data = json.loads(f.read().decode("utf-8-sig"))
    order = [k for k in source["IG_UI"] if k.startswith(NOTE_PREFIX)]
    for key in order:
        text = data.get(key, "")
        if not text:
            continue
        lines = wrap(text.replace("\\n", "\n"))
        print("+" + "-" * PAGE_COLS + "+  " + key)
        for i, line in enumerate(lines):
            pad = " " * max(0, PAGE_COLS - width(line))
            flag = "  <-- line %d, over the %d the journal draws" % (i + 1, PAGE_LINES) \
                if i >= PAGE_LINES else ""
            print("|" + line + pad + "|" + flag)
        print("+" + "-" * PAGE_COLS + "+  %d lines, widest %d\n"
              % (len(lines), max([width(l) for l in lines] or [0])))


def main(argv):
    show_pages = "--pages" in argv
    argv = [a for a in argv if not a.startswith("--")]

    source = {}
    for fname in FILES:
        path = os.path.join(TRANSLATE, SOURCE_LANG, fname + ".json")
        with open(path, "rb") as f:
            source[fname] = json.loads(f.read().decode("utf-8"))

    langs = argv or sorted(d for d in os.listdir(TRANSLATE)
                           if os.path.isdir(os.path.join(TRANSLATE, d))
                           and d != SOURCE_LANG)
    if not langs:
        print("nothing to check: Translate/ has only %s" % SOURCE_LANG)
        return 0

    # Russian is the second file the author writes himself, so it is the reference
    # for "which lines of the supporters' page are names".
    reference = {}
    ref_path = os.path.join(TRANSLATE, "RU", "IG_UI.json")
    if os.path.exists(ref_path):
        with open(ref_path, "rb") as f:
            reference = json.loads(f.read().decode("utf-8"))
    handles = handles_of(source, reference)

    rep = Report()
    for lang in langs:
        if not os.path.isdir(os.path.join(TRANSLATE, lang)):
            print("no such language folder: Translate/%s" % lang)
            return 1
        check_language(lang.upper(), source, rep, handles)
        if show_pages:
            draw_pages(lang, source)

    total = sum(len(v) for v in source.values())
    print("Railroader translation check -- %s, %d strings each\n"
          % (", ".join(langs), total))
    for line in rep.warnings:
        print("warning  " + line)
    if rep.warnings:
        print("")
    for line in rep.errors:
        print("ERROR    " + line)
    print("\n%d error(s), %d warning(s)." % (len(rep.errors), len(rep.warnings)))
    if not rep.errors:
        print("Nothing that would break in-game. Open the pull request.")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
