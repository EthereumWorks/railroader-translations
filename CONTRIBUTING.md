# How to translate Railroader

*[По-русски](CONTRIBUTING.ru.md)*

Read this once before you start. Most of it is not style advice — it is what the
game does to your file, and each rule is here because breaking it produces a bug you
cannot see in a text editor.

---

## 1. Say which language you are taking

[Open an issue](../../issues/new/choose) first — "I am translating Railroader into
Polish". Two people translating the same language on the same weekend is the one
waste this process can actually prevent, and it also lets the author tell you if
strings are about to change.

Use the **language folder name Project Zomboid itself uses**: `AR CA CH CN CS DA DE
EN ES ES_CL ES_MX FI FR HU ID IT JP KO NL NO PL PT PTBR RO RU TH TR UA`. A folder
outside that list is one the game never loads, so if your language is not there,
say so in the issue — it needs a `language.txt` of its own and that is a decision
before it is work.

## 2. Copy the English folder

    Translate/EN/  ->  Translate/<YOUR CODE>/

Six files, 118 strings. Translate the **values**, never the keys:

```json
    "IGUI_RR_NoFuel": "No fuel - the engine won't fire",
     ^^^^^^^^^^^^^^^  key: leave it exactly as it is
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ this is yours
```

[**KEYS.md**](KEYS.md) lists every string with the English and the Russian side by
side and a note on what it is for and where it is drawn. Keep it open while you
work; a lot of these strings are two words long and mean nothing out of context.

Two ways to send the work, both fine:

* **git** — fork, branch, commit, pull request;
* **no git** — attach the folder (or the six files) to your issue. The author will
  open the pull request for you and you will still be credited as the translator.

## 3. The rules the game imposes

**UTF-8, and no BOM.** The game reads these files with `Files.readString`, which is
UTF-8 and nothing else, and hands them to a JSON parser that throws on a
byte-order mark — and a file that throws is dropped *whole*, so one invisible
character at the front costs you the entire file. In VS Code the status bar must say
`UTF-8`, not `UTF-8 with BOM` and not `Windows-1251`/`GBK`.

**It must stay valid JSON.** No trailing comma after the last line, every value in
double quotes, a literal `"` inside a value written `\"`.

**Keep `%1`.** It is a number the game substitutes at runtime — `"RUN %1"` becomes
`RUN 5`. Move it where your grammar wants it, but do not drop it and do not
translate it.

**Write a line break as `\n`** — two characters, backslash and n, inside the string.
Never press Enter inside a value. (In the file that looks like `\\n`, because JSON
also uses the backslash; copy the shape you see in the English file.)

**An empty value means "use the English".** If a string genuinely has no good
translation, `""` is the honest answer and nothing breaks: the game falls back to
English per string. A key you delete does the same thing — but then the checker
cannot tell it from a mistake, so prefer the empty string.

**Do not add keys.** A key the mod does not use is dead weight nothing reads, and it
usually means a typo in a key you meant to translate.

## 4. The rules the mod imposes

**Letters in brackets are keys on the player's keyboard.** `[E]`, `[W]`, `[S]`,
`[R]`, `[Q]`, `[L]`, `[F]`, `[Shift+F]` — translate the sentence around them, never
the letter. (`[Space]` is the *name* of the long key, not an engraved letter, so
that one may be translated.)

**The control stand has fixed-size boxes.** Everything whose key starts with
`IGUI_RR_Hud` or `IGUI_RR_Hint` is painted inside a dial, a lamp or a quadrant on
the driving panel. A word much longer than the English one runs into its neighbour,
and the checker will tell you the exact column budget. Russian solves this the way a
real driver's panel does — with abbreviations (`СОСТ` for condition, `ПРОЖ` for the
headlight). Do the same.

**`GP7` is a locomotive model, not a word.** It stays `GP7` in every language.

**The nine `IGUI_RR_Note_*` strings are whole pages of a paper notebook** — the
mod's in-game manual, and the biggest part of the job. The vanilla journal window
draws **14 usable lines of about 50 columns** and *silently swallows everything
past that*: a page that is one line too long simply loses its last fact, with no
error anywhere. So:

* keep the shape of the English page — one fact per line, shortest thing first;
* it is fine to be terser than the English. It is not fine to be longer;
* **if your language does not put spaces between words** (Chinese, Japanese, Thai),
  the wrapper has nothing to break on, so you must break every line yourself with
  `\n` — about 25 characters per line for double-width scripts;
* run the checker with `--pages` and it will draw each page as the game will.

**The supporters' page (`IGUI_RR_Note_Supporters`) contains people's handles.**
Translate the heading and the thank-you line. **Copy the names character for
character** — a handle is spelled the way its owner spells it, and transliterating
one is the single change here that would offend somebody.

**Do not promise coupling or train handling in the profession text.** The second
book teaches working a train, and rolling stock does not exist yet, so the
character-creation screen must not sell it. Where the English says
"train handling", say what the English says and no more.

## 5. The words

Railroad English is a trade language and machine translation gets it wrong
confidently. **A `reverser` is not a reverse gear, a `switch` is not an electrical
switch, and `light engine` does not mean the engine is light.**
[**GLOSSARY.md**](GLOSSARY.md) explains every term the mod uses, with what it does
in the machine — translate the *thing*, and use whatever your country's railwaymen
call it. If your language's railways never had that thing, say so in the pull
request and propose what you chose instead.

The voice: a 1990s Kentucky short line, written down by a working engineer. Terse,
concrete, no jokes and no marketing.

## 6. Your credit page

`IGUI_RR_Note_Translation` is empty in English and Russian and is **yours**. Write a
short page in your language — the convention is a heading, who translated it, and
nothing else — and it becomes the last page of the notebook every player of your
language carries. Leave it empty and no page is written at all.

Filling it in is how you agree to your name being written into other people's save
games. Nobody will add it for you.

```json
    "IGUI_RR_Note_Translation": "TŁUMACZENIE\\nPolskie tłumaczenie: <your name>",
```

## 7. Check it before you send

    python tools/check_translation.py PL
    python tools/check_translation.py PL --pages

Python 3 and nothing else. It checks everything above — encoding, JSON, the key
list, the `%1`s, the key letters, the panel widths, and every notebook page against
the real 14×50 budget — and it is the same script that runs on your pull request.
Warnings are allowed to stay; errors are things that would be broken or invisible
in-game.

**Then look at it in the game.** This is the part no script can do for you: copy
your folder into the installed mod at

    <Steam>\steamapps\workshop\content\108600\3774360904\mods\Railroader\42\media\lua\shared\Translate\

start the game with the language set to yours, and go and sit in the locomotive.
Read the notebook page by page — that is where a line that is one word too long
shows itself. Screenshots in the pull request are welcome and make review fast.

## 8. Open the pull request

One language per pull request. The template asks you to confirm the checklist and to
say how you tested. Then:

* the checker runs automatically;
* the author reads it — expect questions, especially about the notebook pages;
* if it is accepted, it goes into the mod's own repository and ships in the next
  release. Your name goes into the change notes, the Steam CREDITS block,
  [TRANSLATORS.md](TRANSLATORS.md), and the notebook page you wrote.

**Acceptance is the author's decision and it is final** — see [TERMS.md](TERMS.md)
for what you are agreeing to. Being declined is not a judgement of your language; a
translation may also be turned down because it promises something the mod does not
do yet, or because the author cannot find a second speaker to check it.

## 9. Afterwards

New features bring new strings. When that happens you will be pinged on your
language's issue, and it is usually five or ten lines. **If you go quiet, nothing
breaks** — a string with no translation falls back to English, so the language keeps
working and simply has a few English sentences in it until somebody adds them. There
is no obligation to maintain anything, and no deadline anywhere in this process.
