import json, uuid, time
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CONV_DIR = DATA_DIR / "conversations"
CAT_DIR = DATA_DIR / "categories"

CONV_DIR.mkdir(parents=True, exist_ok=True)
CAT_DIR.mkdir(parents=True, exist_ok=True)

CATEGORIES = [
    "general", "technology", "science", "philosophy",
    "creative", "coding", "analysis", "reasoning",
    "planning", "qa"
]

def _classify_turn(text: str) -> str:
    text_lower = text.lower()
    keywords = {
        "coding": ["code", "python", "javascript", "function", "bug", "api", "html", "css", "programming", "debug"],
        "technology": ["tech", "computer", "software", "hardware", "ai", "data", "algorithm", "digital"],
        "science": ["science", "experiment", "theory", "physics", "biology", "chemistry", "research"],
        "philosophy": ["philosophy", "meaning", "consciousness", "ethics", "moral", "existence"],
        "creative": ["story", "write", "poem", "creative", "imagine", "design", "art"],
        "analysis": ["analyze", "compare", "contrast", "evaluate", "assessment", "examine"],
        "reasoning": ["reason", "logic", "deduce", "infer", "conclusion", "argument", "premise"],
        "planning": ["plan", "strategy", "step", "goal", "timeline", "roadmap", "schedule"],
        "qa": ["question", "answer", "explain", "what is", "how to", "why does", "define"]
    }
    scores = {}
    for cat, words in keywords.items():
        scores[cat] = sum(1 for w in words if w in text_lower)
    best_cat = max(scores, key=lambda c: scores[c])
    if scores[best_cat] > 0:
        return best_cat
    return "general"

def save_turn(
    agent_name: str,
    role: str,
    model: str,
    content: str,
    turn_number: int,
    topic: str = "general",
    category: Optional[str] = None
) -> dict:
    if category is None:
        category = _classify_turn(content)
    timestamp = datetime.now(timezone.utc).isoformat()
    turn_id = str(uuid.uuid4())[:8]
    record = {
        "id": turn_id,
        "agent_name": agent_name,
        "role": role,
        "model": model,
        "content": content,
        "turn": turn_number,
        "topic": topic,
        "category": category,
        "timestamp": timestamp
    }
    fname = CONV_DIR / f"turn_{turn_number:04d}_{role}_{turn_id}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    cat_file = CAT_DIR / f"{category}.jsonl"
    with open(cat_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record

def get_conversation_count() -> int:
    return len(list(CONV_DIR.glob("*.json")))

def get_category_counts() -> dict:
    counts = {}
    for cat in CATEGORIES:
        f = CAT_DIR / f"{cat}.jsonl"
        if f.exists():
            with open(f) as fh:
                counts[cat] = sum(1 for _ in fh)
        else:
            counts[cat] = 0
    return counts

def export_all_turns() -> list[dict]:
    records = []
    for f in sorted(CONV_DIR.glob("*.json")):
        with open(f, encoding="utf-8") as fh:
            records.append(json.load(fh))
    return records

def get_turns_by_category(category: str) -> list[dict]:
    f = CAT_DIR / f"{category}.jsonl"
    if not f.exists():
        return []
    records = []
    with open(f, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                records.append(json.loads(line))
    return records

def get_session_summary() -> dict:
    return {
        "total_turns": get_conversation_count(),
        "categories": get_category_counts(),
        "data_dir": str(DATA_DIR.resolve())
    }
