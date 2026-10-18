// Aspect Math engine - simplest aspect ratio, resize by one side, and fit inside a box.
// Mirrored by oracle.py; keep the op order identical.
// All sizes are whole pixels from 1 to 100000; results are rounded half up.

function _px(x, label) {
  if (typeof x !== "number" || !isFinite(x) || Math.floor(x) !== x || x < 1 || x > 100000) {
    throw new Error(label + " must be a whole number from 1 to 100000");
  }
  return x;
}

function _gcd(a, b) {
  while (b !== 0) { var t = a % b; a = b; b = t; }
  return a;
}

function _div(n, d) {
  return Math.floor((2 * n + d) / (2 * d));
}

function _fmt(h) {
  var whole = Math.floor(h / 100), frac = h % 100;
  if (frac === 0) return String(whole);
  var f = (frac < 10 ? "0" : "") + frac;
  if (f.charAt(1) === "0") f = f.charAt(0);
  return whole + "." + f;
}

// The ratio truth: the simplest whole-number ratio and the decimal width per unit of height.
function ratioTruth(width, height) {
  var w = _px(width, "width"), h = _px(height, "height");
  var g = _gcd(w, h);
  var dec = _div(w * 100, h);
  var per = dec === 0 ? "under 0.01" : _fmt(dec);
  return w + " x " + h + " is " + (w / g) + ":" + (h / g) + " (" + per + " wide for each 1 tall).";
}

// The resize truth: keep the shape, change the width.
function resizeTruth(width, height, newWidth) {
  var w = _px(width, "width"), h = _px(height, "height"), nw = _px(newWidth, "new width");
  var nh = _div(h * nw, w);
  var exact = (h * nw) % w === 0;
  var head = "Scaling " + w + " x " + h + " to " + nw + " wide gives " + nw + " x " + nh;
  if (exact) return head + ".";
  return head + " (exact height " + _fmt(_div(h * nw * 100, w)) + ", rounded).";
}

// The fit truth: the largest size with the same shape that fits inside a box.
function fitTruth(width, height, boxWidth, boxHeight) {
  var w = _px(width, "width"), h = _px(height, "height");
  var bw = _px(boxWidth, "box width"), bh = _px(boxHeight, "box height");
  var fw, fh, spare, exact, side;
  if (bw * h <= bh * w) {
    fw = bw; fh = _div(h * bw, w);
    spare = bh - fh;
    exact = (h * bw) % w === 0;
    side = "height";
  } else {
    fh = bh; fw = _div(w * bh, h);
    spare = bw - fw;
    exact = (w * bh) % h === 0;
    side = "width";
  }
  var head = "Fitting " + w + " x " + h + " inside " + bw + " x " + bh + " gives " + fw + " x " + fh + (exact ? "" : " after rounding to whole pixels");
  if (spare === 0) return head + ", which fills the box.";
  return head + ", with " + spare + (spare === 1 ? " pixel" : " pixels") + " spare on the " + side + ".";
}
