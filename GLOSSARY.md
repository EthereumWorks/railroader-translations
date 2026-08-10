# The words

Railroad English is a trade language. Machine translation renders most of it
confidently and wrongly, and a wrong word here is not a stylistic problem — it is a
player who cannot start the locomotive because the panel told him to move something
that does not exist.

Every term below is described by **what it actually does in the machine**. Translate
the *thing*, using whatever your country's railwaymen call it. If your railways
never had that thing, choose the nearest working description and say so in your pull
request — that is a normal answer and it is better than a false friend.

The Russian column is what the shipped Russian file uses, as a worked example.

---

## The controls

| Term | What it is | Russian used here |
|---|---|---|
| **reverser** | The handle that selects the direction of travel: **F**orward, **N**eutral, **R**everse. Not a gearbox and not a reverse gear — there is no gearbox on a diesel-electric. Mechanically interlocked: with it centred the throttle will not open at all, and the engine can only be started with it in N. | реверс, реверсор |
| **throttle** | Not a pedal. A lever with **eight notches** plus idle; each notch is a fixed engine speed, and it is moved one notch at a time. "Run 5" means notch 5. | тяга, позиция |
| **notch** | One detented position of the throttle. `RUN 5` is the fifth. | позиция |
| **independent brake** | The air brake that holds **the locomotive only**. This is the brake the mod has, on the space bar. | тормоз |
| **automatic brake / brake pipe** | The brake that reaches down the train through every car. It is what the second book teaches, and the reason a light-engine driver still needs that book. Nothing in the game uses it yet. | автотормоз, тормозная магистраль |
| **horn** | The air horn. Held, not tapped. Runs off the compressor, so it needs the engine running. | тифон |
| **bell** | The warning bell. Toggled on and rings by itself. Also air. | колокол |
| **headlight** | The forward light, which burns on the end the reverser selects. **Dim** is a genuinely shorter beam — the real "meeting another train" position — not a dimmer bulb. | прожектор |

## Starting her

| Term | What it is | Russian used here |
|---|---|---|
| **cold** | The engine has not run and is at air temperature. A cold start is harder and drains more battery. | холодная |
| **prime** | Filling the fuel system before cranking. Roughly a second and a half, and a failed start **keeps** it, so the next attempt goes straight to the starter. | прокачка |
| **crank** | The starter motor turning the engine over. | прокрутка |
| **catch / fire** | The moment the diesel starts running on its own. A roll of the dice, not a certainty. | схватить, завестись |
| **warm-up** | The few seconds after it catches, during which it will not give full power. | прогрев |
| **stall** | The engine stopping on its own — out of fuel, or overloaded. | заглохнуть |
| **jump-start** | Reviving a flat battery from a **running generator** stood near the locomotive. | прикурить, запуск от генератора |

## The panel

| Term | What it is | Russian used here |
|---|---|---|
| **control stand** | The whole driving desk: six dials, the throttle quadrant, the reverser, the lamps. | пульт |
| **ammeter** | The load meter. It reads **actual tractive current** — throttle open and the needle at zero means she is not going to move, which is how the panel reports a fault before anything says so in words. | амперметр |
| **BATT / GEN / COND lamps** | Battery, main generator (lit = the diesel is running), and condition. Abbreviated on the panel in every language, because the lamp is 30 pixels wide. | АКК / ГЕН / СОСТ |
| **water** | Cooling-water temperature. A GP7 had no cab thermometer but it did have a water gauge, and in this mod that gauge is also how warm the cab is. It is a **temperature, not a quantity** — do not translate it as a water level. | вода |
| **condition** | How worn the machine is. It only ever goes down. At zero she is **OUT OF ORDER**: sitting on the rails, engine dead, and there is no repair. | состояние |

## Out on the road

| Term | What it is | Russian used here |
|---|---|---|
| **switch** *(also turnout, points)* | The moving rails that send a train onto one road or another. **Not an electrical switch.** In this mod you right-click it and choose which road it is set for. | стрелка |
| **main line** | The through road at a switch. | главный путь |
| **diverging track** | The other road at a switch. | боковой путь |
| **light engine** | A locomotive running **on her own, with nothing coupled to her**. Not "a light locomotive". This is everything the mod does today. | резервом, одиночный локомотив |
| **consist** *(and "train handling")* | A locomotive with cars coupled behind, and the craft of moving one. The second book is about this; there is no rolling stock in the game yet, so **do not promise it** anywhere the player reads before he can have it. | состав, вождение поездов |
| **derail** | To come off the rails. In this mod it is permanent: she is off the spline, dead, and does not go back. | сход с рельсов |
| **truck** *(bogie)* | The swivelling four-wheel assembly under each end of the locomotive. | тележка |
| **depot / engine shed / stall** | Where she is found: a covered stall in the Muldraugh yard. | депо, стойло |
| **roadkill** | What is left of an animal after a locomotive has been over it. Vanilla has the word; use vanilla's. | сбитое животное |

## Names that are not words

* **GP7**, **EMD**, **K&L 800** — a model, its builder, and a road number painted on
  the hood. They stay as they are in every language.
* **Knox County**, **Muldraugh**, **Louisville** — places. Use whatever **Project
  Zomboid's own translation** into your language uses for them; the game ships a
  file per town (`media/lua/shared/Translate/<LANG>/Muldraugh, KY.json`) and a
  player who reads two spellings of the same town assumes they are two towns.
* Handles on the supporters' page — copied character for character. See
  [CONTRIBUTING](CONTRIBUTING.md#4-the-rules-the-mod-imposes).

## Traps

* **`switch` is a turnout**, never a toggle.
* **`light engine` is about having no cars**, not about weight.
* **`consist` is a noun** — the cars, coupled, as one thing.
* **`reverser` selects direction only.** It has no bearing on speed and there are no
  gears to change.
* **`water` on the gauge is a temperature.**
* **`condition` is not health and not fuel** — it is wear, and it never goes up.
* **`prime` is fuel, not ignition.** A diesel has no spark; nothing here is ever
  "sparked", "ignited by a plug" or affected by rain.
* **The independent brake is not the automatic brake.** Getting these two the same
  word makes the second book look pointless, which is the exact confusion its
  tooltip exists to prevent.
