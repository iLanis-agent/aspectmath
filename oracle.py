#!/usr/bin/env python3
# Aspect Math oracle - mirrors engine.js.
import json, math

def _px(x, label):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or math.floor(x) != x or x < 1 or x > 100000:
        raise ValueError(f"{label} must be a whole number from 1 to 100000")
    return int(x)

def _div(n, d):
    return (2 * n + d) // (2 * d)

def _fmt(h):
    whole, frac = divmod(h, 100)
    if frac == 0:
        return str(whole)
    f = f"{frac:02d}"
    if f[1] == "0":
        f = f[0]
    return f"{whole}.{f}"

def ratio_truth(width, height):
    w = _px(width, "width"); h = _px(height, "height")
    g = math.gcd(w, h)
    dec = _div(w * 100, h)
    per = "under 0.01" if dec == 0 else _fmt(dec)
    return f"{w} x {h} is {w // g}:{h // g} ({per} wide for each 1 tall)."

def resize_truth(width, height, new_width):
    w = _px(width, "width"); h = _px(height, "height"); nw = _px(new_width, "new width")
    nh = _div(h * nw, w)
    exact = (h * nw) % w == 0
    head = f"Scaling {w} x {h} to {nw} wide gives {nw} x {nh}"
    if exact:
        return head + "."
    return head + f" (exact height {_fmt(_div(h * nw * 100, w))}, rounded)."

def fit_truth(width, height, box_width, box_height):
    w = _px(width, "width"); h = _px(height, "height")
    bw = _px(box_width, "box width"); bh = _px(box_height, "box height")
    if bw * h <= bh * w:
        fw = bw; fh = _div(h * bw, w); spare = bh - fh; exact = (h * bw) % w == 0; side = "height"
    else:
        fh = bh; fw = _div(w * bh, h); spare = bw - fw; exact = (w * bh) % h == 0; side = "width"
    head = f"Fitting {w} x {h} inside {bw} x {bh} gives {fw} x {fh}" + ("" if exact else " after rounding to whole pixels")
    if spare == 0:
        return head + ", which fills the box."
    return head + f", with {spare} {'pixel' if spare == 1 else 'pixels'} spare on the {side}."

FNS = {"ratioTruth": ratio_truth, "resizeTruth": resize_truth, "fitTruth": fit_truth}

CASES = [
    ("ratioTruth", [1920, 1080]), ("ratioTruth", [1080, 1920]), ("ratioTruth", [1000, 1000]), ("ratioTruth", [1366, 768]),
    ("ratioTruth", [4, 3]), ("ratioTruth", [1, 100000]), ("ratioTruth", [100000, 1]), ("ratioTruth", [2560, 1080]),
    ("ratioTruth", [0, 5]), ("ratioTruth", [5, 0]), ("ratioTruth", [100001, 5]), ("ratioTruth", [5.5, 5]), ("ratioTruth", [-5, 5]),
    ("resizeTruth", [1920, 1080, 1280]), ("resizeTruth", [1920, 1080, 1000]), ("resizeTruth", [1000, 1000, 1]),
    ("resizeTruth", [3, 2, 1]), ("resizeTruth", [3, 2, 2]), ("resizeTruth", [1920, 1080, 100000]), ("resizeTruth", [1, 1, 100000]),
    ("resizeTruth", [1920, 1080, 0]), ("resizeTruth", [0, 1080, 5]), ("resizeTruth", [1920, 0, 5]), ("resizeTruth", [1920, 1080, 100001]),
    ("resizeTruth", [1920, 1080, 640.5]),
    ("fitTruth", [1920, 1080, 1000, 1000]), ("fitTruth", [1920, 1080, 1920, 1080]), ("fitTruth", [1920, 1080, 3840, 2160]),
    ("fitTruth", [1080, 1920, 1000, 1000]), ("fitTruth", [1000, 1000, 500, 800]), ("fitTruth", [1000, 1000, 800, 500]),
    ("fitTruth", [4, 3, 16, 9]), ("fitTruth", [3, 2, 1, 1]), ("fitTruth", [1, 1, 100000, 100000]), ("fitTruth", [1920, 1080, 960, 540]),
    ("fitTruth", [0, 1080, 5, 5]), ("fitTruth", [1920, 1080, 0, 5]), ("fitTruth", [1920, 1080, 5, 100001]), ("fitTruth", [1920, 1080, 5, 2.5]),
    ("fitTruth", [1921, 1080, 1000, 563]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
