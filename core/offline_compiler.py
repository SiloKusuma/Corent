import json
from pathlib import Path
from datetime import datetime, timezone
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table
from . import json_store

console = Console()
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

def compile_dataset(agent_name: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    console.print("\n[bold yellow]=== PHASE 6: OFFLINE COMPILER / RAG PREP ===[/bold yellow]")
    raw = json_store.export_all_turns()

    if not raw:
        console.print("[bold red]Tidak ada data percakapan untuk dikompilasi![/bold red]")
        return OUTPUT_DIR / "empty.json"

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    dataset = {
        "agent_name": agent_name,
        "compiled_at": datetime.now(timezone.utc).isoformat(),
        "total_turns": len(raw),
        "statistics": json_store.get_session_summary(),
        "conversations": raw
    }

    json_path = OUTPUT_DIR / f"dataset_{agent_name}_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    rag_path = OUTPUT_DIR / f"rag_{agent_name}_{timestamp}.jsonl"
    with open(rag_path, "w", encoding="utf-8") as f:
        for turn in raw:
            entry = {
                "id": turn["id"],
                "text": f"{turn['role']}: {turn['content']}",
                "model": turn["model"],
                "category": turn["category"],
                "turn": turn["turn"],
                "topic": turn["topic"]
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    summary_path = OUTPUT_DIR / f"summary_{agent_name}_{timestamp}.json"
    summary = {
        "agent_name": agent_name,
        "total_turns": len(raw),
        "category_distribution": json_store.get_category_counts(),
        "files": {
            "dataset": str(json_path),
            "rag_ready": str(rag_path)
        }
    }
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    table = Table(title="📦 Output Files", header_style="bold cyan")
    table.add_column("File", style="green")
    table.add_column("Path")
    table.add_row("Dataset (JSON)", str(json_path))
    table.add_row("RAG-Ready (JSONL)", str(rag_path))
    table.add_row("Summary", str(summary_path))
    console.print(table)

    cat_counts = json_store.get_category_counts()
    cat_table = Table(title="📊 Category Distribution", header_style="bold magenta")
    cat_table.add_column("Category", style="cyan")
    cat_table.add_column("Turns")
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        if count > 0:
            cat_table.add_row(cat.capitalize(), str(count))
    console.print(cat_table)

    console.print(f"\n[bold green]✔ AI Agent [bold yellow]{agent_name}[/bold yellow] siap digunakan secara OFFLINE![/bold green]")
    return json_path
