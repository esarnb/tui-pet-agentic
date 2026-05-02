import argparse
import sys

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box

from state import (
    load_state, save_state, apply_decay, check_cooldown,
    apply_action, check_evolution, get_age_string, get_time_ago,
    STAGE_ORDER, EVOLUTION_THRESHOLDS,
)

console = Console()

STAGE_EMOJI = {"egg": "🥚", "hatchling": "🐣", "drake": "🦎", "dragon": "🐉"}
MOOD_EMOJI  = {"idle": "😐", "happy": "😊", "hungry": "😫", "sad": "😢", "sleeping": "😴"}


def _bar(value, width=12):
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


def _load_and_advance():
    state = load_state()
    apply_decay(state)
    check_evolution(state)
    return state


def cmd_status(args):
    state = _load_and_advance()
    save_state(state)

    stage = state["stage"]
    name = state["name"]
    age = get_age_string(state)
    mood = state["mood"]

    tbl = Table(box=box.ROUNDED, show_header=False, padding=(0, 1))
    tbl.add_column(justify="left", style="bold")
    tbl.add_column(justify="left", min_width=14)
    tbl.add_column(justify="right", min_width=7)

    title = Text()
    title.append(f" {STAGE_EMOJI.get(stage, '')} {name}", style="bold")
    title.append(f" — {stage.capitalize()} (Age: {age})")
    tbl.title = title

    for label, key in [("Hunger", "hunger"), ("Happiness", "happiness"), ("Energy", "energy")]:
        v = state[key]
        bar = _bar(v)
        bar.append(f"  {v:.0f}%", style="dim")
        tbl.add_row(label, bar, "")

    tbl.add_section()

    xp = state["xp"]
    idx = STAGE_ORDER.index(stage)
    if idx + 1 < len(STAGE_ORDER):
        next_stage = STAGE_ORDER[idx + 1]
        xp_next = EVOLUTION_THRESHOLDS[next_stage]
        xp_str = f"{xp} / {xp_next} (→ {next_stage.capitalize()})"
    else:
        xp_str = f"{xp} (⭐ Maxed!)"

    tbl.add_row("Stage", Text(stage.capitalize(), style="cyan"), "")
    tbl.add_row("XP", Text(xp_str, style="yellow"), "")
    tbl.add_row("Interactions", Text(str(state["interactions"]), style="dim"), "")
    tbl.add_row("Mood", Text(f"{MOOD_EMOJI.get(mood, '')} {mood.capitalize()}"), "")

    tbl.add_section()
    tbl.add_row("Fed", Text(get_time_ago(state["last_fed"]), style="dim"), "")
    tbl.add_row("Petted", Text(get_time_ago(state["last_petted"]), style="dim"), "")
    tbl.add_row("Played", Text(get_time_ago(state["last_played"]), style="dim"), "")

    console.print(tbl)

    tips = {
        "hungry":   f"[yellow]💡 {name} looks hungry! Try [bold]pet feed[/bold].[/yellow]",
        "sad":      f"[yellow]💡 {name} seems sad. Try [bold]pet pet[/bold] or [bold]pet play[/bold].[/yellow]",
        "sleeping": f"[dim]💡 {name} is sleeping. Try [bold]pet wake[/bold] to wake up.[/dim]",
        "happy":    f"[green]💡 {name} is happy! Try [bold]pet play[/bold] for more XP.[/green]",
    }
    if mood in tips:
        console.print(tips[mood])
    elif stage == "egg" and state["interactions"] == 0:
        console.print(f"[dim]💡 New pet! Try [bold]pet feed[/bold] to build a bond.[/dim]")


def _print_evolution(name, old_stage, new_stage):
    if new_stage != old_stage:
        console.print(f"\n[bold yellow]⭐ {name} evolved into {new_stage.capitalize()}![/bold yellow]")


def cmd_feed(args):
    state = _load_and_advance()
    old_stage = state["stage"]
    result = apply_action(state, "feed")
    check_evolution(state)
    save_state(state)

    name = state["name"]
    h_before = result["hunger_before"]
    h_after = result["hunger_after"]
    console.print(f"[green]🍖 {name} is munching! +30 hunger, +5 xp[/green]")
    ln = Text("   Hunger: ")
    ln.append_text(_bar(h_before)); ln.append(f" {h_before:.0f}  →  ")
    ln.append_text(_bar(h_after)); ln.append(f" {h_after:.0f}")
    console.print(ln)
    console.print(f"[dim]✨ Interactions: {state['interactions']}[/dim]")
    _print_evolution(name, old_stage, state["stage"])


def cmd_pet(args):
    state = _load_and_advance()
    remaining = check_cooldown(state, "pet")
    if remaining:
        console.print(f"[yellow]⏱️  {state['name']} is still enjoying the last pet ({remaining}s left)[/yellow]")
        console.print(f'[dim]💬 "...I\'m still happy!"[/dim]')
        return
    old_stage = state["stage"]
    result = apply_action(state, "pet")
    check_evolution(state)
    save_state(state)

    name = state["name"]
    h_before = result["happiness_before"]
    h_after = result["happiness_after"]
    console.print(f"[green]👋 {name} enjoyed that! +10 happiness, +2 xp[/green]")
    ln = Text("   Happiness: ")
    ln.append_text(_bar(h_before)); ln.append(f" {h_before:.0f}  →  ")
    ln.append_text(_bar(h_after)); ln.append(f" {h_after:.0f}")
    console.print(ln)
    console.print(f'[dim]💬 "...more please?"[/dim]')
    console.print(f"[dim]✨ Interactions: {state['interactions']}[/dim]")
    _print_evolution(name, old_stage, state["stage"])


def cmd_play(args):
    state = _load_and_advance()
    remaining = check_cooldown(state, "play")
    if remaining:
        console.print(f"[yellow]⏱️  {state['name']} needs a rest before playing again ({remaining}s left)[/yellow]")
        return
    old_stage = state["stage"]
    result = apply_action(state, "play")
    check_evolution(state)
    save_state(state)

    name = state["name"]
    console.print(f"[green]🎮 {name} had fun! +20 happiness, -10 hunger, -5 energy, +10 xp[/green]")
    for label, bk, ba in [
        ("Happiness", result["happiness_before"], result["happiness_after"]),
        ("Hunger",    result["hunger_before"],    result["hunger_after"]),
        ("Energy",    result["energy_before"],    result["energy_after"]),
    ]:
        ln = Text(f"   {label}: ")
        ln.append_text(_bar(bk)); ln.append(f" {bk:.0f}  →  ")
        ln.append_text(_bar(ba)); ln.append(f" {ba:.0f}")
        console.print(ln)
    console.print(f"[dim]✨ Interactions: {state['interactions']}[/dim]")
    _print_evolution(name, old_stage, state["stage"])


def cmd_sleep(args):
    state = _load_and_advance()
    apply_action(state, "sleep")
    save_state(state)
    name = state["name"]
    console.print(f"[blue]😴 {name} is now sleeping (energy restores 4x faster)[/blue]")
    console.print("[dim]   Zzz...  zzz...  zzz...[/dim]")
    console.print(f"[dim]   Type [bold]pet wake[/bold] to wake up.[/dim]")


def cmd_wake(args):
    state = _load_and_advance()
    apply_action(state, "wake")
    save_state(state)
    name = state["name"]
    energy = state["energy"]
    console.print(f"[green]🌅 {name} woke up refreshed![/green]")
    ln = Text("   Energy: ")
    ln.append_text(_bar(energy)); ln.append(f" {energy:.0f}%")
    console.print(ln)


def cmd_rename(args):
    if not args.name:
        console.print("[red]Usage: pet rename <new_name>[/red]")
        sys.exit(1)
    new_name = " ".join(args.name)
    state = _load_and_advance()
    result = apply_action(state, "rename", name=new_name)
    save_state(state)
    console.print(f"[green]✏️  Renamed your pet from [bold]{result['old_name']}[/bold] to [bold]{new_name}[/bold]![/green]")


def cmd_evolve(args):
    state = _load_and_advance()
    save_state(state)
    stage = state["stage"]
    xp = state["xp"]
    name = state["name"]

    console.print(f"[bold]🌟 {name}'s Evolution Path:[/bold]\n")

    stages_display = []
    for s in STAGE_ORDER:
        threshold = EVOLUTION_THRESHOLDS[s]
        if s == stage:
            idx = STAGE_ORDER.index(s)
            if idx + 1 < len(STAGE_ORDER):
                next_xp = EVOLUTION_THRESHOLDS[STAGE_ORDER[idx + 1]]
                stages_display.append(Text(f"→ {xp}/{next_xp}xp", style="bold cyan"))
            else:
                stages_display.append(Text("⭐ maxed!", style="bold yellow"))
        elif STAGE_ORDER.index(s) < STAGE_ORDER.index(stage):
            stages_display.append(Text(f"✓ ({threshold} xp)", style="green"))
        else:
            stages_display.append(Text(f"○ ({threshold} xp)", style="dim"))

    labels = "   ".join(s.upper() for s in STAGE_ORDER)
    console.print(f"   {labels}")
    progress = Text("   ")
    for i, d in enumerate(stages_display):
        progress.append_text(d)
        if i < len(stages_display) - 1:
            progress.append("   ")
    console.print(progress)
    console.print()

    idx = STAGE_ORDER.index(stage)
    if idx + 1 < len(STAGE_ORDER):
        next_stage = STAGE_ORDER[idx + 1]
        next_xp = EVOLUTION_THRESHOLDS[next_stage]
        needed = next_xp - xp
        console.print(f"[cyan]📈 {name} is growing! {xp} / {next_xp} xp to {next_stage.capitalize()}[/cyan]")
        console.print(f"[dim]   (Need {needed} more xp)[/dim]")
        console.print("[dim]💡 Keep playing to evolve![/dim]")
    else:
        console.print(f"[bold yellow]💪 You've unlocked the ultimate form![/bold yellow]")


def cmd_reset(args):
    import os
    from state import STATE_PATH

    state = load_state()
    if not os.path.exists(STATE_PATH):
        console.print("[dim]No pet found. Nothing to reset.[/dim]")
        return

    name = state["name"]
    age = get_age_string(state)
    xp = state["xp"]

    console.print(f"[bold red]⚠️  This will delete your pet permanently![/bold red]")
    console.print(f"\n    Pet name: [bold]{name}[/bold]")
    console.print(f"    Age: {age}")
    console.print(f"    XP: {xp}\n")

    try:
        answer = input("    Are you sure? (y/N): ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        console.print("\n[dim]Aborted.[/dim]")
        return

    if answer == "y":
        os.remove(STATE_PATH)
        console.print(f"\n[dim]🗑️  {name} has been released into the wild.[/dim]")
        console.print("[dim]   Create a new pet with [bold]pet status[/bold] or [bold]pet feed[/bold].[/dim]")
    else:
        console.print("[dim]Aborted. Your pet is safe.[/dim]")


def cmd_help(args):
    console.print("[bold]🐉 Terminal Pet — Commands[/bold]\n")
    cmds = [
        ("pet",             "Show status (same as pet status)"),
        ("pet status",      "Rich table of stats"),
        ("pet feed",        "+30 hunger, +5 happiness, +5 xp"),
        ("pet pet",         "+10 happiness, +2 xp  (30s cooldown)"),
        ("pet play",        "+20 happiness, -10 hunger, -5 energy, +10 xp  (60s cooldown)"),
        ("pet sleep",       "Put pet to sleep; energy restores 4x faster"),
        ("pet wake",        "Wake the pet early"),
        ("pet rename NAME", "Rename your pet"),
        ("pet evolve",      "Show evolution progress"),
        ("pet reset",       "Delete pet (confirmation required)"),
        ("pet help",        "Show this help"),
    ]
    for cmd, desc in cmds:
        console.print(f"  [bold cyan]{cmd:<20}[/bold cyan]  {desc}")


def main():
    parser = argparse.ArgumentParser(prog="pet", add_help=False)
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("status")
    sub.add_parser("feed")
    sub.add_parser("pet")
    sub.add_parser("play")
    sub.add_parser("sleep")
    sub.add_parser("wake")
    rename_p = sub.add_parser("rename")
    rename_p.add_argument("name", nargs="*")
    sub.add_parser("evolve")
    sub.add_parser("reset")
    sub.add_parser("help")

    args = parser.parse_args()

    dispatch = {
        None:      cmd_status,
        "status":  cmd_status,
        "feed":    cmd_feed,
        "pet":     cmd_pet,
        "play":    cmd_play,
        "sleep":   cmd_sleep,
        "wake":    cmd_wake,
        "rename":  cmd_rename,
        "evolve":  cmd_evolve,
        "reset":   cmd_reset,
        "help":    cmd_help,
    }

    handler = dispatch.get(args.cmd, cmd_status)
    handler(args)


if __name__ == "__main__":
    main()
