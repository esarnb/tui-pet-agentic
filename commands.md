# Terminal Pet — Commands

## Running the pet window

```
python pet_window.py
```

Opens the live animated display in the current terminal. Keep it running in a corner window. Use `Ctrl+C` to close.

**Launcher shortcuts:**
- `launch.bat` — opens a new Windows Terminal window sized for the pet
- `launch.ps1` — PowerShell fallback if Windows Terminal isn't installed

---

## CLI commands

All commands are run as `python pet.py <command>` (or just `pet <command>` after running `setup.bat`).

| Command | Effect |
|---|---|
| `pet` | Same as `pet status` |
| `pet status` | Show a stats table (hunger, happiness, energy, XP, mood, last actions) |
| `pet feed` | +30 hunger · +5 happiness · +5 XP |
| `pet pet` | +10 happiness · +2 XP · 30s cooldown |
| `pet play` | +20 happiness · −10 hunger · −5 energy · +10 XP · 60s cooldown |
| `pet sleep` | Put pet to sleep — energy restores 4× faster |
| `pet wake` | Wake the pet early |
| `pet rename <name>` | Rename your pet |
| `pet evolve` | Show evolution path and XP progress |
| `pet reset` | Delete pet state (asks for confirmation) |
| `pet help` | List all commands |

---

## Stats

| Stat | Range | Decays at | Bad threshold |
|---|---|---|---|
| Hunger | 0–100 | −5 / hour | < 30 → mood: hungry |
| Happiness | 0–100 | −3 / hour | < 30 → mood: sad |
| Energy | 0–100 | −4 / hour | < 20 → mood: sleeping |

Stats decay even while the window is closed. The next time state is loaded, decay catches up automatically.

---

## Evolution

XP is earned from interactions. Stages unlock permanently once the XP threshold is reached.

| Stage | XP required |
|---|---|
| Egg | 0 |
| Hatchling | 50 |
| Drake | 200 |
| Dragon | 500 |

---

## One-time setup

```
setup.bat
```

Installs `rich` and adds the project folder to your user PATH so `pet` works from any directory. Restart your terminal after running it.
