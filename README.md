# Railroader — translations

*[По-русски](README.ru.md)*

This is the text of **[Railroader](https://steamcommunity.com/sharedfiles/filedetails/?id=3774360904)**,
a working railroad for Project Zomboid Build 42 — a drivable EMD GP7, the railroader
profession, and the books that teach a survivor to run her.

The mod ships in **English and Russian**, both written by the author. Every other
language has to come from somebody who speaks it. That is what this repository is
for: **anyone may translate Railroader into their language and send it here**, and
accepted translations ship inside the mod itself, with the translator credited.

## Why not just reupload the mod with your own language in it?

Because everyone loses that way. A reupload is a copy that stops at the version it
was copied from: it does not get the next locomotive, the next fix, or the save-game
migration that comes with it, and its players report bugs that were fixed months ago
against code nobody is maintaining. Meanwhile the Workshop fills up with four
half-dead Railroaders and nobody can tell which one to install.

Send the language here instead and it is in the mod — the real one, the one that
keeps getting updated — for every player who has it installed, in the next release.
You are credited in four places (below), and you never have to maintain anything.

## What is here

| | |
|---|---|
| `Translate/EN/` | the source text — **118 strings, about 24 KB** |
| `Translate/RU/` | Russian, as a worked example of how far you may go from the English |
| [`KEYS.md`](KEYS.md) | every string, what it is for, and what it has to fit inside |
| [`GLOSSARY.md`](GLOSSARY.md) | the railroad words, explained — read this before translating "reverser" |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | how to do it, and the rules the game imposes |
| [`TERMS.md`](TERMS.md) | who owns what, in two paragraphs |
| [`TRANSLATORS.md`](TRANSLATORS.md) | who translated what |
| `tools/check_translation.py` | run it before you send: it is the same check the author runs |

There is **no code, no model, no sound and no artwork here** — you do not need any
of it to translate the mod, and it stays where it is.

## How big is the job?

118 strings. Roughly a third of them are two or three words on the control stand
(`THROTTLE`, `BATT`, `RUN 5`); a third are one-line messages; and **nine of them are
whole pages of the engineer's notebook**, which is the mod's in-game manual and about
half of all the words. A careful translator with the game installed spends an evening
on it, not a week.

## Languages

| Language | State | Translator |
|---|---|---|
| English (`EN`) | ships with the mod | SlavaPo (author) |
| Russian (`RU`) | ships with the mod | SlavaPo (author) |

Want one that is not on this list? **[Open an issue](../../issues/new/choose) saying
which language you are taking**, so two people do not translate the same one on the
same evening. Then read [CONTRIBUTING.md](CONTRIBUTING.md).

## Where your name goes

If your translation is accepted, you are credited in four places:

1. the mod's change notes for the release that carries it;
2. the CREDITS block on the Steam Workshop page;
3. [`TRANSLATORS.md`](TRANSLATORS.md) here;
4. **inside the game** — the last page of the engineer's notebook, in your language,
   written by you. That one is optional and it is yours to write or leave empty; see
   `IGUI_RR_Note_Translation` in [KEYS.md](KEYS.md).

## The one rule

**Every contribution is accepted, edited or declined by the author, and that
decision is final.** A translation is text a player reads in a locomotive cab for
hours; being wrong in a way only a native speaker can see is exactly what this
process exists to catch, and being right is not always enough — a line may also have
to be shorter, or say a thing the mod does not promise yet. Expect a conversation on
your pull request, not a rubber stamp.

See [TERMS.md](TERMS.md) for what you are agreeing to when you send one.
