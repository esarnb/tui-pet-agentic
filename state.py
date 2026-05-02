import json
import os
import tempfile
import time
from datetime import datetime, timezone

STATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pet_state.json")

EVOLUTION_THRESHOLDS = {"egg": 0, "hatchling": 50, "drake": 200, "dragon": 500}
STAGE_ORDER = ["egg", "hatchling", "drake", "dragon"]
COOLDOWNS = {"pet": 30, "play": 60}


def default_state():
    now = datetime.now(timezone.utc).isoformat()
    return {
        "name": "Companion",
        "created_at": now,
        "last_update": now,
        "hunger": 80,
        "happiness": 80,
        "energy": 100,
        "xp": 0,
        "stage": "egg",
        "mood": "idle",
        "last_fed": now,
        "last_petted": now,
        "last_played": now,
        "interactions": 0,
    }


def load_state(path=STATE_PATH):
    for _ in range(5):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return default_state()
        except json.JSONDecodeError:
            time.sleep(0.05)
    raise RuntimeError("state file unreadable after 5 attempts")


def save_state(state, path=STATE_PATH):
    dir_ = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=dir_, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _derive_mood_from_stats(state):
    if state["energy"] < 20:
        return "sleeping"
    if state["hunger"] < 30:
        return "hungry"
    if state["happiness"] < 30:
        return "sad"
    if state["happiness"] > 80:
        return "happy"
    return "idle"


def apply_decay(state):
    now = datetime.now(timezone.utc)
    last = datetime.fromisoformat(state["last_update"])
    elapsed = (now - last).total_seconds()

    sleeping = state.get("mood") == "sleeping"

    if sleeping:
        state["energy"] = min(100, state["energy"] + elapsed * (16 / 3600))
        if state["energy"] >= 100:
            sleeping = False
    else:
        state["energy"] = max(0, state["energy"] - elapsed * (4 / 3600))

    state["hunger"] = max(0, state["hunger"] - elapsed * (5 / 3600))
    state["happiness"] = max(0, state["happiness"] - elapsed * (3 / 3600))
    state["last_update"] = now.isoformat()
    state["mood"] = "sleeping" if sleeping else _derive_mood_from_stats(state)
    return state


def check_cooldown(state, action):
    if action == "pet":
        last = datetime.fromisoformat(state["last_petted"])
    elif action == "play":
        last = datetime.fromisoformat(state["last_played"])
    else:
        return None
    elapsed = (datetime.now(timezone.utc) - last).total_seconds()
    remaining = COOLDOWNS.get(action, 0) - elapsed
    return int(remaining) if remaining > 0 else None


def apply_action(state, action, name=None):
    now = datetime.now(timezone.utc).isoformat()

    if action == "feed":
        prev = state["hunger"]
        state["hunger"] = min(100, state["hunger"] + 30)
        state["happiness"] = min(100, state["happiness"] + 5)
        state["xp"] += 5
        state["last_fed"] = now
        state["interactions"] += 1
        return {"hunger_before": prev, "hunger_after": state["hunger"]}

    elif action == "pet":
        prev = state["happiness"]
        state["happiness"] = min(100, state["happiness"] + 10)
        state["xp"] += 2
        state["last_petted"] = now
        state["interactions"] += 1
        return {"happiness_before": prev, "happiness_after": state["happiness"]}

    elif action == "play":
        ph, pp, pe = state["happiness"], state["hunger"], state["energy"]
        state["happiness"] = min(100, state["happiness"] + 20)
        state["hunger"] = max(0, state["hunger"] - 10)
        state["energy"] = max(0, state["energy"] - 5)
        state["xp"] += 10
        state["last_played"] = now
        state["interactions"] += 1
        return {
            "happiness_before": ph, "happiness_after": state["happiness"],
            "hunger_before": pp, "hunger_after": state["hunger"],
            "energy_before": pe, "energy_after": state["energy"],
        }

    elif action == "sleep":
        state["mood"] = "sleeping"
        state["interactions"] += 1
        return {}

    elif action == "wake":
        state["mood"] = _derive_mood_from_stats(state)
        state["interactions"] += 1
        return {}

    elif action == "rename":
        old = state["name"]
        state["name"] = name
        return {"old_name": old}

    return {}


def check_evolution(state):
    current_idx = STAGE_ORDER.index(state["stage"])
    for i in range(current_idx + 1, len(STAGE_ORDER)):
        next_stage = STAGE_ORDER[i]
        if state["xp"] >= EVOLUTION_THRESHOLDS[next_stage]:
            state["stage"] = next_stage
        else:
            break
    return state


def get_age_string(state):
    created = datetime.fromisoformat(state["created_at"])
    now = datetime.now(timezone.utc)
    delta = now - created
    days = delta.days
    hours = delta.seconds // 3600
    mins = (delta.seconds % 3600) // 60
    if days > 0:
        return f"{days} day{'s' if days != 1 else ''}, {hours}h"
    if hours > 0:
        return f"{hours}h {mins}m"
    return f"{mins}m"


def get_time_ago(timestamp):
    dt = datetime.fromisoformat(timestamp)
    now = datetime.now(timezone.utc)
    elapsed = (now - dt).total_seconds()
    if elapsed < 60:
        return f"{int(elapsed)}s ago"
    elif elapsed < 3600:
        return f"{int(elapsed / 60)}m ago"
    elif elapsed < 86400:
        return f"{int(elapsed / 3600)}h ago"
    return f"{int(elapsed / 86400)}d ago"
