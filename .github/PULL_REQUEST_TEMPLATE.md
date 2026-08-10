<!--
One language per pull request, please. If you are fixing a line in a language that
is already in, ignore the parts of the checklist that do not apply and say what was
wrong -- a fix does not need the whole ceremony.
-->

**Language:** <!-- e.g. Polish (PL) -->
**Translator credit as:** <!-- exactly how you want your name spelled, everywhere -->

### How I checked it

- [ ] `python tools/check_translation.py <CODE>` — no errors
- [ ] `python tools/check_translation.py <CODE> --pages` — every notebook page fits
- [ ] I played the mod in this language and read the notebook in the cab
      <!-- screenshots welcome, especially of the notebook pages and the control stand -->

### The rules I know about

- [ ] UTF-8 without BOM; the keys are untouched; no keys added or removed
- [ ] every `%1` is still there
- [ ] letters in brackets — `[W]`, `[E]`, `[Shift+F]` — are still the same letters
- [ ] the handles on the supporters' page are copied character for character
- [ ] the profession and trait text does not promise coupling or train handling
- [ ] `GP7` is still `GP7`

### Machine translation

- [ ] None was used, **or**
- [ ] it was used as a draft and I read and corrected every line — say which tool:

### Anything you had to decide

<!--
Words your railways never had, a term you rendered differently from the glossary, a
page you had to shorten to make it fit. This is the most useful part of the pull
request: it is where review starts.
-->

---

By opening this pull request I agree to [TERMS.md](../TERMS.md).
