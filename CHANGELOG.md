# Changelog

## 2026-11-06 — Desktop layer + layout image

### Added
- DESK layer (hold Space, then hold Enter): home row = Gui+1…0, top row = Gui+Shift+1…0.
  Replaces the laptop's Arsenik number-row Gui+N shortcuts (the Totem has no number row).
  In NAV, the Enter thumb still taps Esc and now holds DESK.
- `docs/totem-layout.png`: colored one-page image of all layers in the Totem shape.
  Regenerate with `python3 docs/layout_png.py docs/totem-layout.png` (needs Pillow).

## 2026-11-05 — Qwerty-Lafayette + Arsenik

The Totem now matches the laptop setup: OS layout Qwerty-Lafayette + kanata Arsenik.

### Changed
- `config/totem.keymap`: base layout switched from the vylet-style layout to QWERTY + Arsenik.
  - Home-row mods: S/D/F = Gui/Ctrl/Alt, J/K/L = Alt/Ctrl/Gui (tap-preferred, 300 ms).
  - Inner thumbs: Bspc/Shift, Space/Nav, Enter/Sym (Arsenik timings).
  - SYM layer: Lafayette AltGr symbols (`RA(key)`).
  - NUM layer (Sym + Bspc): shifted digits, digits, Lafayette dead key + digit macros.
  - NAV layer: arrows, Home/End, PgUp/PgDn, Ctrl+A/Z/X/C/V on the left; numpad on the right.
  - Outer pinkies: `<` (ISO key) and `'`. Outer thumbs: Tab, Del, ADJ.
  - Kept: ADJ layer, TVPaint layers, Q+W = Esc combo, A+S+D = TVPaint toggle.
- `build.yaml`: board renamed `seeeduino_xiao_ble` → `xiao_ble//zmk` (required by current ZMK `main`).

### Notes
- Accents come from the OS layout (Qwerty-Lafayette), not from kanata. Any computer needs that layout; kanata is not needed for the Totem.
- On the laptop, kanata must ignore the Totem to avoid double home-row mods: `linux-dev-names-exclude ("TOTEM")` in the kanata `defcfg` (local change in `~/dev/arsenik`, not in this repo).
