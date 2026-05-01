# Terminal Pet — Development Tutorial

> **Purpose of this document:** A step-by-step build guide for an AI agent (or human developer) picking up this project from scratch. Each phase is independently testable. Follow the phases in order — earlier phases produce artifacts later ones depend on.

---

## 0. Project Overview

A persistent terminal companion that lives in a separate small terminal window snapped to a corner of your screen. The user interacts with it from any shell (PowerShell, CMD, Git Bash) using a `pet` CLI command. The pet is rendered as a colored blocky pixel-art sprite using Unicode half-block characters and 24-bit RGB terminal colors — not ASCII art.

The pet has stats (hunger, happiness, age, XP) that change over time and persist between sessions via a shared JSON state file. Both the display window and the CLI tool read and write the same file, so they stay in sync without sockets, servers, or IPC.

### Design constraints (must respect these)

1. **Cross-shell** — must work in PowerShell, CMD, and Git Bash on Windows 10/11.
2. **Non-blocking** — the pet runs in a separate window so the user's normal terminal stays usable.
3. **No external services** — fully local, no network, no databases.
4. **Single dependency** — only `rich` (Python). Avoid pulling in heavy frameworks.
5. **Colored pixel art, not ASCII** — sprites use Unicode block chars + RGB color.
6. **Atomic state writes** — the CLI and window both touch the same file; reads/writes must not corrupt it.

---

## 1. Architecture

### 1.1 File layout

```
tui-pet/
├── template.md              # this document
├── pet_window.py            # live animated display loop
├── pet.py                   # CLI tool dispatcher
├── sprites.py               # sprite definitions (color block art)
├── state.py                 # state load/save/decay logic
├── pet_state.json           # generated on first run; do not commit hand-edited copies
├── launch.bat               # Windows Terminal launcher for pet_window.py
├── launch.ps1               # PowerShell launcher (alt)
├── setup.bat                # one-time setup: PATH + Python deps
├── pet.bat                  # tiny shim so `pet ...` works in CMD/PowerShell
├── pet                      # tiny shim so `pet ...` works in Git Bash (no extension)
└── requirements.txt         # rich>=13.0
```

### 1.2 Process model

```
┌────────────────────┐         ┌────────────────────┐
│  pet_window.py     │         │   any shell        │
│  (long-running)    │         │   `pet feed`       │
│                    │         │   `pet pet`        │
│  Reads state every │         │   `pet status`     │
│  1 second, redraws │         └─────────┬──────────┘
└─────────┬──────────┘                   │
          │ reads                writes  │
          ▼                              ▼
        ┌──────────────────────────────────┐
        │      pet_state.json              │
        │  (single source of truth)        │
        └──────────────────────────────────┘
```

### 1.3 Why this architecture

- **No tmux** — tmux doesn't work natively in PowerShell or CMD. Spawning a separate small window works in all three shells.
- **File-based state** — avoids socket/server complexity. Easy to debug (`cat pet_state.json`), easy to reset (delete the file).
- **Polling at 1Hz** — fast enough to feel responsive after a CLI action, slow enough to be invisible in CPU usage.
- **`rich`** — handles RGB color, cursor positioning, and live refresh without us reinventing terminal control codes.

---

## 2. Tech Stack & Dependencies

| Concern | Choice | Why |
|---|---|---|
| Language | Python 3.10+ | Cross-shell, batteries-included, the user already has it |
| Rendering | `rich` | Best-in-class terminal rendering with RGB + live updates |
| Block art | Unicode `█ ▀ ▄ ▌ ▐` | Full-cell + half-cell glyphs let us approximate square pixels |
| State store | JSON file | Trivial, debuggable, cross-shell |
| CLI parsing | `argparse` (stdlib) | No extra deps |
| File locking | `msvcrt.locking` (Windows stdlib) | Prevents torn writes; see §6 |

### 2.1 requirements.txt

```
rich>=13.0
```

---

## 3. Data Model

### 3.1 `pet_state.json` schema

```json
{
  "name": "Blob",
  "created_at": "2026-04-30T10:00:00Z",
  "last_update": "2026-04-30T10:00:00Z",
  "hunger": 80,
  "happiness": 80,
  "energy": 100,
  "xp": 0,
  "stage": "egg",
  "mood": "idle",
  "last_fed": "2026-04-30T10:00:00Z",
  "last_petted": "2026-04-30T10:00:00Z",
  "last_played": "2026-04-30T10:00:00Z",
  "interactions": 0
}
```

### 3.2 Stat ranges & semantics

| Field | Type | Range | Semantics |
|---|---|---|---|
| `hunger` | int | 0–100 | 100 = full. Decays at ~5/hr. <30 → mood becomes `hungry`. |
| `happiness` | int | 0–100 | 100 = thrilled. Decays at ~3/hr. <30 → mood becomes `sad`. |
| `energy` | int | 0–100 | 100 = wide awake. Decays at ~4/hr. <20 → mood becomes `sleeping`. |
| `xp` | int | 0+ | Earned per interaction; gates evolution. |
| `stage` | enum | `egg` / `hatchling` / `drake` / `dragon` | Drives sprite selection. |
| `mood` | enum | `idle` / `happy` / `hungry` / `sad` / `sleeping` | Drives sprite frame selection. Derived, not user-set. |

### 3.3 Decay model

When the state is loaded, compute `elapsed = now - last_update` in seconds, then:

```python
hunger    = max(0, hunger    - elapsed * (5/3600))
happiness = max(0, happiness - elapsed * (3/3600))
energy    = max(0, energy    - elapsed * (4/3600))
last_update = now
```

This way the pet ages even when the window is closed — state catches up the next time it's loaded.

### 3.4 Mood derivation

```python
def derive_mood(state):
    if state["energy"] < 20:    return "sleeping"
    if state["hunger"] < 30:    return "hungry"
    if state["happiness"] < 30: return "sad"
    if state["happiness"] > 80: return "happy"
    return "idle"
```

### 3.5 Evolution thresholds

| Stage | XP required |
|---|---|
| `egg` | 0 |
| `hatchling` | 50 |
| `drake` | 200 |
| `dragon` | 500 |

Stage upgrades are sticky: once promoted, a pet does not regress.

---

## 4. Sprite System

### 4.1 Sprite encoding

Each sprite is a 2D grid of palette indices. A `0` is transparent. Each non-zero index maps to an RGB color in the sprite's palette. Each grid "cell" is rendered as **two characters wide** so it looks square in a terminal (terminal cells are ~2:1 tall:wide).

```python
EGG_IDLE = {
    "palette": {
        1: "#f5e6d3",   # shell base
        2: "#d4a574",   # shell speckle
        3: "#8b6f47",   # shell shadow
    },
    "frames": [
        # frame 0
        [
            [0,0,1,1,1,1,0,0],
            [0,1,1,2,1,1,1,0],
            [1,1,2,1,1,2,1,1],
            [1,2,1,1,1,1,1,1],
            [1,1,1,2,1,1,2,1],
            [1,1,1,1,1,1,1,1],
            [0,1,3,1,1,3,1,0],
            [0,0,1,3,3,1,0,0],
        ],
        # frame 1 (slight wobble)
        # ...
    ],
}
```

### 4.2 Rendering a sprite

```python
from rich.text import Text

def render_sprite(sprite, frame_idx):
    frame = sprite["frames"][frame_idx]
    palette = sprite["palette"]
    text = Text()
    for row in frame:
        for cell in row:
            if cell == 0:
                text.append("  ")  # transparent: two spaces
            else:
                color = palette[cell]
                text.append("██", style=f"{color}")
        text.append("\n")
    return text
```

`██` (two full blocks) per pixel gives a chunky, square pixel-art look in any modern terminal.

### 4.3 Required sprites (deliverables for `sprites.py`)

| Stage | Moods needed | Frames per mood |
|---|---|---|
| egg | idle | 2 (wobble) |
| hatchling | idle, happy, hungry, sleeping | 2 each |
| drake | idle, happy, hungry, sad, sleeping | 2 each |
| dragon | idle, happy, hungry, sad, sleeping | 3 each (idle includes flame puff) |

Total: ~36 frames. Keep each 8×8 to start; can expand to 12×12 later.

### 4.4 Palette guidance

Use a cohesive 4–6 color palette per stage so each evolution feels distinct:

- **Egg** — warm cream + tan speckles
- **Hatchling** — soft teal body, peach belly, dark eyes
- **Drake** — deeper teal/blue body, gold accents, amber eyes
- **Dragon** — saturated indigo + magenta wings, flame orange, bright cyan highlights

---

## 5. CLI Spec

### 5.1 Commands

```
pet                 # default — same as `pet status`
pet status          # rich table of stats + ASCII bar
pet feed            # +30 hunger, +5 happiness, +5 xp
pet pet             # +10 happiness, +2 xp, cooldown 30s
pet play            # +20 happiness, -10 hunger, -5 energy, +10 xp, cooldown 60s
pet sleep           # set mood=sleeping; restores energy at 4× rate while sleeping
pet wake            # exit sleep state early
pet rename <name>   # change pet's name
pet evolve          # show current stage + xp progress to next
pet reset           # delete pet_state.json (with y/N confirmation)
pet help            # list all commands
```

### 5.2 Cooldowns

Prevent stat-spamming. Store last-action timestamps in state. If a cooldown is active, print a friendly message:

```
$ pet pet
Blob is still enjoying the last pet (12s left)
```

### 5.3 Output style

Use `rich` for output too:

- Stats as a table with colored progress bars
- Success messages in green
- Cooldown / error messages in yellow
- Errors (state file unreadable, etc.) in red

---

## 6. State Persistence (Critical)

Both `pet.py` and `pet_window.py` touch `pet_state.json`. Without care, a CLI write during a window read could produce corrupt JSON. Solution:

### 6.1 Atomic write

```python
import json, os, tempfile

def save_state(state, path):
    dir_ = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=dir_, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        os.replace(tmp, path)  # atomic on Windows + POSIX
    except Exception:
        os.unlink(tmp)
        raise
```

### 6.2 Tolerant read

```python
def load_state(path):
    for attempt in range(5):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError,):
            return default_state()
        except json.JSONDecodeError:
            time.sleep(0.05)  # writer mid-replace; retry
    raise RuntimeError("state file unreadable")
```

### 6.3 First-run defaults

If `pet_state.json` doesn't exist, create it on first action (CLI or window) using `default_state()` with `created_at = now`.

---

## 7. Step-by-Step Build Plan

> Each phase ends with a verifiable demo. Don't move on until the demo works.

### Phase 1 — Bootstrap

1. Confirm `python --version` is 3.10+.
2. Create `requirements.txt` with `rich>=13.0`.
3. Run `pip install -r requirements.txt`.
4. Create empty stubs: `pet.py`, `pet_window.py`, `sprites.py`, `state.py`.
5. **Demo:** `python pet.py` runs without error (prints nothing).

### Phase 2 — State module (`state.py`)

1. Implement `default_state()` returning the schema in §3.1.
2. Implement `load_state(path)` and `save_state(state, path)` per §6.
3. Implement `apply_decay(state)` per §3.3.
4. Implement `derive_mood(state)` per §3.4.
5. Implement `apply_action(state, action)` for `feed`, `pet`, `play`, `sleep`, `wake`. Each updates stats, sets `last_*`, and bumps `xp` + `interactions`.
6. Implement `check_evolution(state)` to bump `stage` when XP threshold met.
7. **Demo:** Write a tiny test script that loads default state, calls `apply_action(state, "feed")`, saves, reloads, prints — verify hunger went up.

### Phase 3 — Sprite module (`sprites.py`)

1. Define a `Sprite` dataclass with `palette: dict[int, str]` and `frames: list[list[list[int]]]`.
2. Hand-paint at least the **egg idle** sprite (2 frames). Use a grid editor in your head — start small (8×8).
3. Implement `render_sprite(sprite, frame_idx) -> rich.text.Text` per §4.2.
4. Implement `get_sprite(stage, mood) -> Sprite` lookup.
5. **Demo:** Standalone script `python -c "from rich import print; from sprites import get_sprite, render_sprite; print(render_sprite(get_sprite('egg','idle'), 0))"` shows a colored egg.
6. Iterate: add hatchling sprites, then drake, then dragon. This is the time-consuming part — budget several hours just on sprite art.

### Phase 4 — CLI (`pet.py`)

1. Use `argparse` with subcommands per §5.1.
2. Each subcommand: `load_state` → `apply_decay` → `apply_action` → `check_evolution` → `save_state` → print confirmation.
3. Implement `pet status` with a `rich.table.Table` of stats and colored bars (`█` for filled, `░` for empty).
4. Implement cooldown check before mutating stats.
5. **Demo:**
   ```
   python pet.py status      # shows stats table
   python pet.py feed        # confirms feed
   python pet.py status      # hunger bar visibly higher
   ```

### Phase 5 — Live window (`pet_window.py`)

1. Use `rich.live.Live` with `refresh_per_second=2`.
2. On each tick: `load_state` → `apply_decay` → `save_state` (so decay persists) → render layout.
3. Layout (use `rich.layout.Layout`):
   ```
   ┌────────────────────────┐
   │      <pet name>        │
   │                        │
   │      [ sprite ]        │
   │                        │
   │  Hunger    ████░░ 65   │
   │  Happy     █████░ 82   │
   │  Energy    ███░░░ 50   │
   │  Stage: drake          │
   │  XP: 245 / 500         │
   └────────────────────────┘
   ```
4. Animate: cycle frame index every 800ms regardless of state changes.
5. Handle `KeyboardInterrupt` cleanly (close `Live` context manager).
6. **Demo:** Run `python pet_window.py` in one terminal; in another run `python pet.py feed`; the window's hunger bar should jump within 1s.

### Phase 6 — Launchers

1. **`launch.bat`**:
   ```bat
   @echo off
   start "Terminal Pet" wt -w 0 nf -d "%~dp0" --title "Pet" --size 42,22 python pet_window.py
   ```
   (Uses Windows Terminal `wt.exe`; falls back gracefully if not present.)

2. **`launch.ps1`** (alt for users without WT):
   ```powershell
   Start-Process powershell -ArgumentList "-NoProfile","-Command","cd '$PSScriptRoot'; python pet_window.py"
   ```

3. **`pet.bat`** (CLI shim for CMD/PowerShell):
   ```bat
   @echo off
   python "%~dp0pet.py" %*
   ```

4. **`pet`** (CLI shim for Git Bash, no extension):
   ```bash
   #!/usr/bin/env bash
   exec python "$(dirname "$0")/pet.py" "$@"
   ```

5. **Demo:** Double-click `launch.bat` — small window appears showing the pet. From any other terminal in the project dir, `pet status` works.

### Phase 7 — Setup script (`setup.bat`)

1. Run `pip install -r requirements.txt`.
2. Append the project directory to user PATH using:
   ```bat
   setx PATH "%PATH%;%~dp0"
   ```
3. Print success + remind user to restart their terminal.
4. **Demo:** Open a fresh terminal — `pet status` works without `cd`-ing into the project dir.

### Phase 8 — Polish

- Add a `pet help` ASCII banner.
- Add a one-line tip in `pet status` based on mood ("Blob looks hungry, try `pet feed`").
- Add a low-stat warning in the live window (red border when any stat <20).
- Sound? Skip — keeps deps minimal.
- Save a daily snapshot to `history.jsonl` for future stat graphs.

### Phase 9 — Optional: Auto-start on login

Document in README how to put a `launch.bat` shortcut in `shell:startup`.

---

## 8. Testing Checklist

Before declaring done, verify:

- [ ] `pet feed` works in PowerShell, CMD, and Git Bash.
- [ ] Closing the pet window does not lose state (reopen → stats are correct).
- [ ] Running CLI while window is open updates the window within 1s.
- [ ] Running `pet feed` 100 times in a tight loop never produces a JSON parse error in the window (atomic write test).
- [ ] Leaving the window open overnight: stats decay correctly, pet doesn't crash.
- [ ] Deleting `pet_state.json` and rerunning starts a fresh pet.
- [ ] Sprite renders without distortion in Windows Terminal, ConHost (legacy CMD), and Git Bash.
- [ ] Resizing the pet window does not crash `Live`.

---

## 9. Known Gotchas

1. **Legacy ConHost (old CMD)** — does not support 24-bit color by default. Mitigation: detect via `os.environ.get("WT_SESSION")` or `colorama.init()`; document that Windows Terminal is recommended.
2. **Git Bash and `\r\n`** — Python on Windows handles this correctly when using `open(..., encoding="utf-8")`. Don't open in binary mode.
3. **PATH changes via `setx`** — only take effect in *new* terminals. Don't expect the same shell that ran `setup.bat` to see `pet` immediately.
4. **`rich.Live` flicker** — set `transient=False`, `screen=False`, `refresh_per_second=2`. Higher refresh rates flicker on Windows.
5. **Sprites look stretched** — terminal cells are ~2:1 tall:wide. Always use *two characters* per pixel (`██`), never one.
6. **Time math** — store all timestamps as ISO 8601 UTC strings. Convert to/from `datetime` objects only at boundaries.

---

## 10. Future Ideas (Out of Scope for v1)

- Multi-pet support (`pet list`, `pet switch <name>`)
- Mini-games (`pet play guess` for extra XP)
- Cosmetics shop (spend XP on hat sprites)
- Stat graphs from `history.jsonl` via `pet graph`
- Sync state via a Gist or Dropbox folder for cross-machine pets
- Sound effects (would require `playsound` or `winsound`)
- Web dashboard (overkill — defeats the "lives in a terminal" charm)

---

## 11. Acceptance Criteria for v1

Project is "done" when:

1. A new user can `git clone` (or copy the folder), run `setup.bat`, double-click `launch.bat`, and see a colored animated pet in a corner window.
2. From any other shell on the same machine, `pet feed` / `pet status` / `pet pet` work.
3. The pet survives a reboot — state persists, decay catches up correctly.
4. At least the `egg` and `hatchling` stages have full sprite sets across all moods.
5. No exception escapes either process during a 24-hour soak test.

Once those five hold, ship v1 and iterate on sprites + features.
