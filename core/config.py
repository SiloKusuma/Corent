import os, json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config.json"
DATA_DIR = BASE_DIR / "data"
ENV_FILE = BASE_DIR / ".env"

DEFAULT_CONFIG = {
    "AGENT_NAME": "",
    "PROVIDER": "",
    "API_KEY": "",
    "MAIN_MODEL": "",
    "PARTNER_MODEL": "",
    "DISCUSSION_ROUNDS": 10,
    "TOPIC": "general"
}

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    return dict(DEFAULT_CONFIG)

def save_config(updates: dict):
    cfg = load_config()
    cfg.update(updates)
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

def save_env(api_key: str):
    lines = []
    if ENV_FILE.exists():
        with open(ENV_FILE) as f:
            lines = f.readlines()
    found = False
    for i, line in enumerate(lines):
        if line.startswith("API_KEY="):
            lines[i] = f"API_KEY={api_key}\n"
            found = True
            break
    if not found:
        lines.append(f"API_KEY={api_key}\n")
    with open(ENV_FILE, "w") as f:
        f.writelines(lines)
