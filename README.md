# Aspect Math

Aspect ratio arithmetic. Change one side and the other side has to follow.

## What it computes

- **The ratio truth** - the simplest whole-number ratio of a width and a height, plus the decimal width per 1 of height.
- **The resize truth** - keep the shape and change the width; the new height is rounded to a whole pixel, with the exact value shown when it is not whole.
- **The fit truth** - the largest size with the same shape that fits inside a box, and the pixels spare on the other side.

All sizes are whole pixels from 1 to 100000. Rounding is half up.

## Boundary

Arithmetic only. Aspect Math does not know the sizes, ratios or cropping rules a screen, platform or printer requires. Check those in its own specs.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (40 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/aspectmath/
Repo: https://github.com/iLanis-agent/aspectmath
