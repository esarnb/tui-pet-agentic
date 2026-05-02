import time

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich import box

from state import load_state, save_state, apply_decay, check_evolution, get_age_string, STAGE_ORDER, EVOLUTION_THRESHOLDS
from sprites import get_sprite, render_sprite

STAGE_EMOJI = {"egg": "🥚", "hatchling": "🐣", "drake": "🦎", "dragon": "🐉"}
MOOD_EMOJI  = {"idle": "😐", "happy": "😊", "hungry": "😫", "sad": "😢", "sleeping": "😴"}

_frame_idx = 0
_last_frame_tick = 0.0
_zzz_cycle = 0


def _bar(value, width=10):
    filled = int(value / 100 * width)
    empty = width - filled
    if value >= 70:
        color = "green"
    elif value >= 30:
        color = "yellow"
    else:
        color = "red"
    t = Text()
    t.append("█" * filled, style=color)
    t.append("░" * empty, style="dim")
    return t


def _stat_line(label, value):
    label_text = f"{label:<9}"
    bar = _bar(value)
    val_text = f" {value:3.0f}%"
    t = Text(label_text)
    t.append_text(bar)
    t.append(val_text, style="dim")
    return t


def _xp_line(state):
    stage = state["stage"]
    xp = state["xp"]
    idx = STAGE_ORDER.index(stage)
    if idx + 1 < len(STAGE_ORDER):
        next_stage = STAGE_ORDER[idx + 1]
        xp_next = EVOLUTION_THRESHOLDS[next_stage]
        return Text(f"XP: {xp} / {xp_next}  (→{next_stage.capitalize()})", style="yellow")
    return Text(f"XP: {xp}  (⭐ Maxed!)", style="bold yellow")


def _sleeping_zzz():
    global _zzz_cycle
    patterns = ["💤      ", "  💤    ", "    💤  ", "      💤"]
    return Text(patterns[_zzz_cycle % len(patterns)], style="blue")


def _make_renderable(state, frame_idx):
    stage = state["stage"]
    mood = state["mood"]
    name = state["name"]
    age = get_age_string(state)

    sprite = get_sprite(stage, mood)
    sprite_rows = render_sprite(sprite, frame_idx)

    any_critical = any(state[k] < 20 for k in ("hunger", "happiness", "energy"))

    content = Text()

    # title line
    title = Text()
    title.append(f"{STAGE_EMOJI.get(stage, '')} ", style="bold")
    title.append(name, style="bold white")
    title.append(f"  (age: {age})", style="dim")
    content.append_text(title)
    content.append("\n\n")

    # sprite — each row is a Text, indent with 2 spaces
    for row_text in sprite_rows:
        content.append("  ")
        content.append_text(row_text)
        content.append("\n")

    if mood == "sleeping":
        content.append("  ")
        content.append_text(_sleeping_zzz())
        content.append("\n")

    content.append("\n")

    # stats
    for label, key in [("Hunger", "hunger"), ("Happy", "happiness"), ("Energy", "energy")]:
        v = state[key]
        content.append("  ")
        content.append_text(_stat_line(label, v))
        content.append("\n")

    content.append("\n")

    # stage + xp
    content.append(f"  Stage: ", style="dim")
    content.append(stage.capitalize(), style="cyan")
    content.append("\n")
    content.append("  ")
    content.append_text(_xp_line(state))
    content.append("\n")

    # mood
    emoji = MOOD_EMOJI.get(mood, "")
    content.append(f"  Mood:  {emoji} {mood.capitalize()}", style="dim" if mood == "idle" else "")
    content.append("\n")

    border_style = "red bold" if any_critical else "bright_black"
    if any_critical:
        title_str = "⚠️  URGENT CARE NEEDED"
    else:
        title_str = "Terminal Pet"

    return Panel(
        content,
        title=title_str,
        border_style=border_style,
        box=box.ROUNDED,
        padding=(0, 1),
        width=38,
    )


def run():
    global _frame_idx, _last_frame_tick, _zzz_cycle

    console = Console()
    frame_interval = 0.8
    tick_interval = 0.5

    state = load_state()
    apply_decay(state)
    check_evolution(state)
    save_state(state)

    with Live(
        _make_renderable(state, _frame_idx),
        console=console,
        refresh_per_second=2,
        screen=False,
        transient=False,
        auto_refresh=False,
    ) as live:
        while True:
            try:
                now = time.monotonic()

                state = load_state()
                apply_decay(state)
                check_evolution(state)
                save_state(state)

                mood = state["mood"]
                sprite = get_sprite(state["stage"], mood)
                n_frames = len(sprite.frames)

                if now - _last_frame_tick >= frame_interval:
                    _frame_idx = (_frame_idx + 1) % n_frames
                    _zzz_cycle = (_zzz_cycle + 1) % 4
                    _last_frame_tick = now

                live.update(_make_renderable(state, _frame_idx), refresh=True)
                time.sleep(tick_interval)

            except KeyboardInterrupt:
                break
            except Exception:
                time.sleep(1.0)


if __name__ == "__main__":
    run()
