# Terminal Pet — Visual Design Mockup

## 1. Live Window Display (Main UI)

### Layout Structure
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃           🐉 Blazer                  ┃
┃                                       ┃
┃              ▄▄▄▄▄▄▄▄               ┃
┃            ▄███████████▄             ┃
┃           ██  ●  ●  ●██              ┃
┃           ██  ▄▄▄▄▄  ██              ┃
┃            ▀██████████▀              ┃
┃              ▀▀▀▀▀▀▀▀               ┃
┃                                       ┃
┃  Hunger    ████████░░░░ 72/100      ┃
┃  Happiness █████░░░░░░░░ 56/100     ┃
┃  Energy    ██████████░░░░ 78/100    ┃
┃                                       ┃
┃  Stage: Dragon  •  XP: 542/500 ⭐  ┃
┃  Mood: Happy 😊                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## 2. Sprite Evolution — All Stages

### EGG (Idle) — Wobbling gently
```
        ╭─────────────╮
        │   ▄▄▄▄▄▄▄   │
        │  ██░░░░░██  │    Frame 1
        │ ██░░░░░░░██ │
        │ ██░░░░░░░██ │
        │  ██░░░░░██  │
        │   ▀▀▀▀▀▀▀   │
        ╰─────────────╯
        
        ╭─────────────╮
        │  ▄▄▄▄▄▄▄▄   │
        │ ██░░░░░░██  │    Frame 2
        │██░░░░░░░░██ │    (slight
        │██░░░░░░░░██ │     wobble)
        │ ██░░░░░░██  │
        │  ▀▀▀▀▀▀▀▀   │
        ╰─────────────╯
```

### HATCHLING (4 moods × 2 frames each)

#### Idle — Looking around
```
        ┌──────────────┐
        │   ╭────╮     │
        │  ╭┤● ● ├╮   │
        │  │ ╰────╯ │  │    (soft teal
        │  │  ▄▄▄▄  │  │     with peach
        │  │ ▀▀▀▀▀▀ │  │     belly)
        │  ╰────────╯  │
        └──────────────┘
```

#### Happy — Big smile
```
        ┌──────────────┐
        │   ╭────╮     │
        │  ╭┤◉ ◉ ├╮   │
        │  │ ╰────╯ │  │    Grinning
        │  │  ▄▄▄▄  │  │
        │  │ ▀▀▀▀▀▀ │  │
        │  ╰────────╯  │
        └──────────────┘
```

#### Hungry — Mouth wide open
```
        ┌──────────────┐
        │   ╭────╮     │
        │  ╭┤● ● ├╮   │
        │  │ ╱════╲ │  │    Starving!
        │  │  ▄▄▄▄  │  │
        │  │ ▀▀▀▀▀▀ │  │
        │  ╰────────╯  │
        └──────────────┘
```

#### Sleeping — Zzz
```
        ┌──────────────┐
        │   ╭────╮     │
        │  ╭┤- - ├╮   │    Snoozing
        │  │ ╰────╯ │  │
        │  │  ▀▀▀▀  │  │
        │  │ ▀▀▀▀▀▀ │  │
        │  ╰────────╯  │    💤 💤 💤
        └──────────────┘
```

### DRAKE (Leveled up) — More angular, blue/gold theme

#### Idle — Alert posture
```
        ┌────────────────┐
        │    ╱╲╲╲╲╲╲╱╱   │
        │   ╱█████████╲  │
        │  │ ●  ■  ● ││  │    Deep teal
        │  │ ╰────────╯│  │    Gold accents
        │   ╲████████╱   │    Amber eyes
        │    ╲╲╲╲╲╲╲╲    │
        └────────────────┘
```

#### Sad — Droopy
```
        ┌────────────────┐
        │    ╱╲  ╱╲      │
        │   ╱█████████╲  │    Unhappy
        │  │ ●  ■  ● ││  │
        │  │ ╰╲────╱╯│  │
        │   ╲████████╱   │
        │    ╲╲╲╲╲╲╲╲    │
        └────────────────┘
```

### DRAGON (Ultimate form) — Majestic with wings & flames

#### Idle — Breathing fire
```
        ┌──────────────────────┐
        │    ╱╲  ◈◈◈◈  ╱╲      │
        │   ╱████████████╲     │    Indigo body
        │  │ ●  ◈  ● ◈◈ ││     │    Magenta wings
        │  │ ╰════════════╯│    │    Flame orange
        │   ╲████████████╱     │    Cyan highlights
        │    ╲ ╲╲╲╲╲╲╲ ╲      │
        │     ≡≡ 🔥 🔥 ≡≡      │
        └──────────────────────┘
```

#### Happy — Wings spread
```
        ┌──────────────────────┐
        │  ◈◈╱╲  ◈◈◈◈  ╱╲◈◈   │
        │  ◈████████████████◈  │    Joyful!
        │  ◈│ ◉  ◈  ◉ ◈◈ │◈   │    Full wingspan
        │  ◈│ ╰════════════╯│◈  │
        │   ╲████████████╱     │
        │    ╲ ╲╲╲╲╲╲╲ ╲      │
        └──────────────────────┘
```

---

## 3. CLI Status Output

### `pet status` — Rich table format
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🐉 Blazer — Dragon (Age: 3 days, 4h)       ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Stat          Progress               Value │
├───────────────────────────────────────────┤
│ Hunger        ████████░░░░░░░░░░  72%    │
│ Happiness     █████░░░░░░░░░░░░░  56%    │
│ Energy        ██████████░░░░░░░░  78%    │
├───────────────────────────────────────────┤
│ Current Stage Dragon                      │
│ Total XP      542 / 500 (⭐ Maxed!)       │
│ Interactions  127 total                   │
│ Mood          Happy 😊                    │
├───────────────────────────────────────────┤
│ Last actions:                             │
│   Fed         2 minutes ago               │
│   Petted      5 minutes ago               │
│   Played      28 minutes ago              │
└───────────────────────────────────────────┘

💡 Tip: Blazer looks happy! Try `pet play` for more XP.
```

### `pet feed` — Success feedback
```
🍖 Blazer is munching! +30 hunger, +5 xp
   Hunger: ███░░░░ 45  →  ███████░░ 72
   
✨ Interactions: 128
```

### `pet pet` — Affection
```
👋 Blazer enjoyed that! +10 happiness, +2 xp
   Happiness: ████░░░░░░  56  →  █████░░░░░  62
   
💬 "...more please?"
✨ Interactions: 129
```

### `pet pet` — With cooldown
```
⏱️  Blazer is still enjoying the last pet (8s left)

💬 "...I'm still happy!"
```

### `pet play` — Energy spent
```
🎮 Blazer had fun! +20 happiness, -10 hunger, -5 energy, +10 xp
   Happiness: ██████░░░░░░ 68  →  █████████░░░░ 85
   Hunger:    ████████░░░░ 72  →  ██████░░░░░░░ 62
   Energy:    ██████████░░ 78  →  █████████░░░░ 73
   
✨ Interactions: 130
```

### `pet evolve` — Progress display
```
🌟 Blazer's Evolution Path:

   EGG        HATCHLING      DRAKE       DRAGON
   ✓ (50 xp)  ✓ (200 xp)     ✓ (500 xp)  ⭐ (maxed!)
   
💪 You've unlocked the ultimate form!
   Next in v2: Celestial Dragon at 1000 xp
```

### `pet evolve` — Pre-evolution
```
🌟 Blazer's Evolution Path:

   EGG        HATCHLING      DRAKE       DRAGON
   ✓ (50 xp)  ✓ (200 xp)     → 245/500xp  ○
   
📈 Drake is growing! 245 / 500 xp to Dragon
   (Need 255 more xp)
   
💡 Keep playing to evolve!
```

### `pet sleep` / `pet wake`
```
😴 Blazer is now sleeping (energy restores 4x faster)
   
   Zzz...  zzz...  zzz...
   
   Type `pet wake` to wake up, or Blazer will
   auto-wake when energy reaches 100.
```

```
🌅 Blazer woke up refreshed!
   Energy: ████████░░░░░░░░░░ 100
```

### `pet rename <name>`
```
✏️  Renamed your pet from "Blazer" to "Phoenix"!
```

### `pet reset` — Confirmation
```
⚠️  This will delete your pet permanently!
    
    Pet name: Blazer
    Age: 3 days, 4h
    XP: 542
    
    Are you sure? (y/N): y
    
    🗑️  Blazer has been released into the wild.
        
        Create a new pet with `pet status` or `pet feed`.
```

---

## 4. Error States

### Pet not yet created
```
❌ No pet found! 🐣

   Create your first pet:
   
   $ pet feed
   
   Welcome to Terminal Pet! 🎉
   Your new companion "Companion" has hatched!
```

### Corrupted state file
```
⚠️  Could not read pet state (corrupted?)

   Recovered to checkpoint from 30 seconds ago.
   Last action from 3 minutes ago.
   
   If problems persist, delete `pet_state.json` to reset.
```

### State file inaccessible
```
❌ ERROR: Cannot access pet_state.json

   Location: /home/user/tui-pet/pet_state.json
   
   Check:
   • File permissions
   • Disk space
   • File not locked by another process
   
   Run `pet reset` to start fresh if needed.
```

---

## 5. Full Session Example

### Terminal 1: Launch window
```bash
$ python pet_window.py

[Small window opens in corner showing animated pet]
```

### Terminal 2: Multiple interactions
```bash
$ pet status
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🥚 Blob — Egg (Age: 1 sec)                 ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Hunger    █████████░░░░░░░░░░  50%         │
│ Happiness ██████████░░░░░░░░░░  55%        │
│ Energy    ██████████░░░░░░░░░░  100%       │
├───────────────────────────────────────────┤
│ Current Stage: Egg                        │
│ XP: 0 / 50 (→ Hatchling)                  │
│ Mood: Idle                                │
└───────────────────────────────────────────┘

💡 Tip: New pet! Try `pet feed` to build a bond.

$ pet feed
🍖 Blob is munching! +30 hunger, +5 xp
   Hunger: ████░░░░░░░░░░░░░░  50  →  ██████████░░░░░░░░░░  80

$ pet pet
👋 Blob enjoyed that! +10 happiness, +2 xp
   Happiness: ██████░░░░░░░░░░░░  55  →  ██████░░░░░░░░░░░░  62

$ pet play
🎮 Blob had fun! +20 happiness, -10 hunger, -5 energy, +10 xp
   Happiness: ███████░░░░░░░░░░░░  62  →  █████████░░░░░░░░░░  79
   Hunger:    ██████████░░░░░░░░░░  80  →  ████████░░░░░░░░░░░░  70
   Energy:    ██████████░░░░░░░░░░  100  →  █████████░░░░░░░░░░░░  95

$ pet evolve
🌟 Blob's Evolution Path:

   EGG        HATCHLING      DRAKE       DRAGON
   → 27/50xp  ○              ○           ○
   
📈 Blob is growing! 27 / 50 xp to Hatchling
   (Need 23 more xp)
```

### Terminal 1: Window updates in real-time
```
[Window shows Blob sprite, hunger bar changes, happiness bar changes]
[Sprite animates between 2 frames]
[Mood updates to "happy"]
```

---

## 6. Color Palette Examples

### Egg Stage
```
🎨 Palette:
   Cream base    #F5E6D3
   Tan speckle   #D4A574
   Dark shadow   #8B6F47
```

### Hatchling Stage
```
🎨 Palette:
   Teal body     #20B2AA
   Peach belly   #FFB87C
   Dark outline  #2C3E50
   Eye highlight #FFF8DC
```

### Drake Stage
```
🎨 Palette:
   Deep teal     #1E7F7F
   Gold accent   #FFD700
   Amber eye     #FF8C00
   Dark outline  #1A1A1A
```

### Dragon Stage
```
🎨 Palette:
   Indigo body   #4B0082
   Magenta wing  #FF1493
   Flame orange  #FF4500
   Cyan glow     #00FFFF
   Shadow        #000000
```

---

## 7. Animation Frames Per Mood

### Idle — Gentle 2-frame loop (800ms each)
```
Frame 1: neutral posture
Frame 2: slight sway/wobble (different for each stage)
```

### Happy — Bouncy 2-frame loop (600ms each)
```
Frame 1: body up
Frame 2: body down (jump)
```

### Hungry — Frantic 2-frame loop (400ms each)
```
Frame 1: mouth open, lean back
Frame 2: lean forward, wide eyes
```

### Sleeping — Static frame + floating ZZZ text
```
Frame: eyes closed, relaxed pose
Text: "💤 💤" floating up and fading
```

### Sad — Slow 2-frame loop (1200ms each)
```
Frame 1: drooped head
Frame 2: drooped head (nearly identical, very sad)
```

---

## 8. Low-stat Warning (in window)

When any stat drops below 20:
```
╭────────────────────────────────╮
│  ⚠️  URGENT CARE NEEDED         │
│  ┌──────────────────────────┐  │
│  │  Hunger  ██░░░░░░░░ 15   │  │  ← Redder
│  │  Happiness ░░░░░░░░░░ 5  │  │  ← Very red
│  │  Energy  ░░░░░░░░░░ 0    │  │  ← Frozen
│  └──────────────────────────┘  │
│                                 │
│  💬 "...help me..."             │
└────────────────────────────────┘
```

---

## 9. Window Resizing Behavior

### Comfortable (42×22) — Default
```
┌─────────────────────────────────────────┐
│            Pet Comfortable               │
│                                          │
│          [8×8 sprite]                   │
│                                          │
│  Hunger  ████░░░░░░░░░░░░░░ 45        │
│  Happy   █████░░░░░░░░░░░░░ 55        │
│  Energy  ██████░░░░░░░░░░░░ 60        │
│  Stage: Hatchling  XP: 120/200        │
└─────────────────────────────────────────┘
```

### Minimal (28×14) — Fits in corner
```
┌──────────────────────────┐
│    Pet Tiny              │
│  ████████░░░░ 45        │
│  █████░░░░░░░░ 55        │
│  ██████░░░░░░░░ 60       │
│  Hatchling  120/200      │
└──────────────────────────┘
```

### Expanded (60×30) — Fullscreen
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                    🐉 Blazer — Dragon                    ┃
┃                   Age: 3 days, 4 hours                  ┃
┃                                                           ┃
┃                     [12×12 sprite]                       ┃
┃                                                           ┃
┃  Hunger        ████████░░░░░░░░░░░░░░░░░░  72%         ┃
┃  Happiness     █████░░░░░░░░░░░░░░░░░░░░░░  56%        ┃
┃  Energy        ██████████░░░░░░░░░░░░░░░░░░  78%       ┃
┃                                                           ┃
┃  Current Stage: Dragon                                  ┃
┃  XP Progress: 542 / 500 (⭐ Maxed Out!)                 ┃
┃  Total Interactions: 127                                ┃
┃  Current Mood: Happy 😊                                 ┃
┃                                                           ┃
┃  Last interactions:                                      ┃
┃    • Fed 2 minutes ago                                  ┃
┃    • Petted 5 minutes ago                               ┃
┃    • Played 28 minutes ago                              ┃
┃                                                           ┃
┃  Created: 2026-04-28  •  Checkpoint: 2026-05-01         ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## 10. Desktop Integration (Mockup)

### Windows Taskbar
```
[Window menu] [🐉 Terminal Pet] [🌐 Edge] [📧 Outlook]
```

### Pinned to corner (Windows Terminal)
```
┌─────────────────────┐ ┌──────────────────────┐
│ C:\Users\Dev        │ │  🐉 Blazer           │
│ $ █                 │ │  ████░░ 72          │
│                     │ │  █████░░ 56          │
│                     │ │  ██████░░ 78         │
└─────────────────────┘ └──────────────────────┘
```

---

## Summary of Visual Features

✅ **Unicode block characters** for crisp pixel art
✅ **24-bit RGB colors** for rich, vibrant palette
✅ **Animated 2-3 frame sprites** for life-like movement
✅ **Rich tables** for stats with colored progress bars
✅ **Emoji** for quick visual recognition (food, sleep, play, etc.)
✅ **Responsive layout** that adapts to window size
✅ **Clear feedback** on all CLI actions
✅ **Warning states** for low stats
✅ **Mood-based visuals** (happy expressions, sad faces, sleeping poses)
✅ **Stage evolution** clearly visible in sprite and UI changes

