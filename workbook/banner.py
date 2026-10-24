"""Recolor the Canvas four-stages banner from purple to the textbook blue.

Removes the baked-in title and logo, shifts purple to #006EB6 in LCh (so perceived
lightness holds), brightens the halos, and turns the pink shirts and shoes white.
Only needed if the banner changes; build.py uses assets/banner-blue.png as-is.
Requires opencv-python and numpy."""
import cv2, numpy as np
import pathlib
HERE = pathlib.Path(__file__).parent
src = str(HERE / 'assets' / 'banner-original.png')   # the Canvas course banner (purple)
bgr = cv2.imread(src)[9:523, 9:687].copy()
H, W = bgr.shape[:2]

# --- 1. remove baked text / logo / sparkle (same masks as before) ---
g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
keep = np.zeros((H, W), np.uint8); keep[148:230, 385:480] = 255
mask = np.zeros((H, W), np.uint8)
for (x0, y0, x1, y1, thr) in [(15, 25, 470, 200, 72), (640, 0, W, 45, 85), (640, 465, W, H, 85)]:
    mask[y0:y1, x0:x1] = ((g[y0:y1, x0:x1] > thr) * 255).astype(np.uint8)
mask[30:72, 18:202] = 255
mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), 3); mask[keep > 0] = 0
clean = cv2.inpaint(bgr, mask, 12, cv2.INPAINT_TELEA)
zone = np.zeros((H, W), np.float32); zone[20:205, 10:475] = 1; zone[keep > 0] = 0
zone = cv2.GaussianBlur(zone, (0, 0), 12)[..., None]
clean = (clean * (1 - zone) + cv2.GaussianBlur(clean, (0, 0), 14) * zone).astype(np.uint8)
for (x0, y0, x1, y1) in [(640, 0, W, 45), (640, 465, W, H)]:
    z = np.zeros((H, W), np.float32); z[y0:y1, x0:x1] = 1; z = cv2.GaussianBlur(z, (0, 0), 6)[..., None]
    clean = (clean * (1 - z) + cv2.GaussianBlur(clean, (0, 0), 10) * z).astype(np.uint8)
m2 = np.zeros((H, W), np.uint8); m2[143:154, 382:437] = 255
clean = cv2.inpaint(clean, m2, 5, cv2.INPAINT_TELEA)

# --- 2. LCh recolor ---
lab = cv2.cvtColor(clean.astype(np.float32) / 255, cv2.COLOR_BGR2Lab)
L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
C = np.hypot(a, b); hue = (np.degrees(np.arctan2(b, a)) + 360) % 360
tgt = cv2.cvtColor(np.array([[[182, 110, 0]]], np.float32) / 255, cv2.COLOR_BGR2Lab)[0, 0]
th = (np.degrees(np.arctan2(tgt[2], tgt[1])) + 360) % 360
yy, xx = np.mgrid[0:H, 0:W]
heads = [(118, 352, 62), (290, 258, 64), (432, 176, 66), (588, 140, 106)]
halo = np.zeros((H, W), np.float32)
for cx, cy, r in heads:
    halo = np.maximum(halo, np.clip((r - np.hypot(xx - cx, yy - cy)) / 14, 0, 1))
# protect the girls' pink shirts/shoes and skin: only below-head areas of the two younger girls, plus skin hues
shirts = np.zeros((H, W), np.float32)
shirts[386:470, 80:152] = 1; shirts[445:482, 118:200] = 1; shirts[290:372, 262:313] = 1; shirts[452:480, 268:322] = 1
shirts = cv2.GaussianBlur(shirts, (0, 0), 3)
# purple/magenta band in Lab hue: roughly 285..355 deg; pinks near 0 only inside halos
d = np.abs(((hue - 318) + 180) % 360 - 180)
w_global = np.clip((42 - d) / 10, 0, 1)
d2 = np.abs(((hue - 332) + 180) % 360 - 180)
w_halo = np.clip((43 - d2) / 6, 0, 1) * halo * np.clip((L - 45) / 10, 0, 1)
w_shirt = np.clip((28 - np.abs(((hue - 300) + 180) % 360 - 180)) / 8, 0, 1)   # inside shirt zones: purples only, not pinks
w_g = w_global * (1 - shirts) + w_shirt * shirts
d3 = np.abs(((hue - 358) + 180) % 360 - 180)
w_fr = halo * np.clip((30 - d3) / 6, 0, 1) * np.clip((L - 66) / 6, 0, 1) * np.clip((28 - C) / 6, 0, 1)
w = np.maximum(np.maximum(w_g, w_halo * (1 - shirts)), w_fr * (1 - shirts)) * np.clip((C - 2) / 4, 0, 1)
# outer glow ring (outside each head): pull any pink/magenta/purple to blue, whatever its lightness
ring = np.zeros((H, W), np.float32)
faces = [(122, 364, 32, 38), (290, 268, 28, 36), (432, 190, 26, 40), (588, 160, 62, 75)]
for (cx, cy, r), (fx, fy, rx, ry) in zip(heads, faces):
    dist = np.hypot(xx - cx, yy - cy)
    e = np.hypot((xx - fx) / rx, (yy - fy) / ry)
    ring = np.maximum(ring, np.clip((r - dist) / 14, 0, 1) * np.clip((e - 1.0) / 0.15, 0, 1))
ring[250:300, 256:286] = 0   # second girl's ponytail
d4 = np.abs(((hue - 340) + 180) % 360 - 180)
pinkish = np.clip((55 - d4) / 8, 0, 1)
d5 = np.abs(((hue - 60) + 180) % 360 - 180)
tan = np.clip((28 - d5) / 8, 0, 1) * np.clip((L - 48) / 6, 0, 1) * np.clip((32 - C) / 6, 0, 1)
w_ring = ring * np.maximum(pinkish, tan) * np.clip((C - 1.5) / 3, 0, 1) * (1 - shirts)
w = np.maximum(w, w_ring)
dh = ((th - hue + 180) % 360) - 180
hue2 = hue + dh * w
# halos: lift lightness of glow pixels (not skin/hair) and whiten slightly
glow = np.maximum(halo * np.clip((L - 35) / 15, 0, 1), ring) * (1 - shirts) * w
L2 = np.clip(L + 9 * glow, 0, 100)
C2 = C * (1 - 0.35 * glow)
# gentle extra chroma in the blue background
bg = (1 - halo) * w * np.clip((60 - L) / 20, 0, 1)
C2 = C2 * (1 + 0.15 * bg)
dark = halo * np.clip((42 - L) / 10, 0, 1) * np.clip((40 - np.abs(((hue - 325) + 180) % 360 - 180)) / 10, 0, 1)
C2 = C2 * (1 - 0.85 * dark)
# fill the gray fade band between glow and background with blue
ring2 = ring.copy(); ring2[165:250, 398:430] = 0; ring2[105:185, 505:548] = 0
lowc = ring2 * np.clip((20 - C2) / 6, 0, 1) * (1 - shirts)
dh2 = ((th - hue2 + 180) % 360) - 180
hue2 = hue2 + dh2 * lowc
C2 = np.maximum(C2, 19 * lowc * np.clip((70 - L2) / 15, 0.35, 1))
# soft additive glow around each head (outside the face), brighter for the dimmer young-girl halos
boost = np.zeros((H, W), np.float32)
for (cx, cy, r), (fx, fy, rx, ry), amt in zip(heads, faces, (16, 15, 10, 8)):
    dist = np.hypot(xx - cx, yy - cy)
    e = np.hypot((xx - fx) / rx, (yy - fy) / ry)
    prof = np.exp(-((dist - r * 0.45) / (r * 0.42)) ** 2) * np.clip((e - 1.0) / 0.2, 0, 1)
    boost = np.maximum(boost, amt * prof)
boost[250:300, 256:286] *= 0.3; boost[165:250, 398:430] *= 0.3; boost[105:185, 505:548] *= 0.3
boost *= (1 - shirts)
L2 = L2 + boost * (1 - L2 / 100)
# carry the background's blue saturation into each glow; only the bright core goes white
wide = np.zeros((H, W), np.float32)
for (cx, cy, r), (fx, fy, rx, ry) in zip(heads, faces):
    dist = np.hypot(xx - cx, yy - cy)
    e = np.hypot((xx - fx) / rx, (yy - fy) / ry)
    wide = np.maximum(wide, np.clip((r + 18 - dist) / 22, 0, 1) * np.clip((e - 1.0) / 0.2, 0, 1))
wide[250:300, 256:286] = 0; wide[165:250, 398:430] = 0; wide[105:185, 505:548] = 0
wide *= (1 - shirts)
outside = 1 - np.clip(wide * 3, 0, 1)
bgC = cv2.GaussianBlur((C2 * outside).astype(np.float32), (0, 0), 30) / np.maximum(cv2.GaussianBlur(outside.astype(np.float32), (0, 0), 30), 1e-3)
target = bgC * (1 - np.clip((L2 - 52) / 38, 0, 1))
raise_ = wide * np.clip((target - C2) / 3, 0, 1)
dh3 = ((th - hue2 + 180) % 360) - 180
hue2 = hue2 + dh3 * raise_
C2 = C2 + (np.maximum(C2, target) - C2) * wide
# pink shirts -> white (fabric only: pink hues, not skin/hands/backpack)
tops = np.zeros((H, W), np.float32); tops[389:474, 70:160] = 1; tops[284:376, 258:318] = 1; tops[442:486, 112:208] = 1; tops[448:484, 262:328] = 1
tops = cv2.GaussianBlur(tops, (0, 0), 2)
d6 = np.abs(((hue - 355) + 180) % 360 - 180)
d7 = np.abs(((hue - 44) + 180) % 360 - 180)
skin = np.clip((28 - d7) / 6, 0, 1) * np.clip((C - 7) / 3, 0, 1)      # saturated orange = skin, protect
pinkfab = tops * np.clip((52 - d6) / 7, 0, 1) * np.clip((C - 2.5) / 3, 0, 1) * np.clip((L - 18) / 8, 0, 1) * (1 - skin)
cool = ((th - hue2 + 180) % 360) - 180
hue2 = hue2 + cool * pinkfab
C2 = C2 * (1 - pinkfab) + 3.5 * pinkfab
L2 = L2 + 13 * pinkfab * (1 - L2 / 100)
a2 = C2 * np.cos(np.radians(hue2)); b2 = C2 * np.sin(np.radians(hue2))
out = cv2.cvtColor(np.dstack([L2, a2, b2]).astype(np.float32), cv2.COLOR_Lab2BGR)
out = np.clip(out * 255, 0, 255).astype(np.uint8)
up = cv2.resize(out, (W * 2, H * 2), interpolation=cv2.INTER_LANCZOS4)
cv2.imwrite(str(HERE / 'assets' / 'banner-blue.png'), cv2.addWeighted(up, 1.35, cv2.GaussianBlur(up, (0, 0), 2), -0.35, 0))
print('wrote assets/banner-blue.png')
