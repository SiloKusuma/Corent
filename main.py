#!/usr/bin/env python3
import sys, os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich import print as rprint

from core.installer import run_installation
from core.config import load_config, save_config, save_env
from core.provider import select_provider, select_model
from core.json_store import get_session_summary
from core.offline_compiler import compile_dataset
from ai.discussion import run_discussion

console = Console()
BASE_DIR = Path(__file__).parent
WEB_DIR = BASE_DIR / "web"

BANNER = """
[bold cyan]
   ██████╗ ██████╗ ██████╗ ███████╗███╗   ██╗████████╗
  ██╔════╝██╔═══██╗██╔══██╗██╔════╝████╗  ██║╚══██╔══╝
  ██║     ██║   ██║██████╔╝█████╗  ██╔██╗ ██║   ██║
  ██║     ██║   ██║██╔══██╗██╔══╝  ██║╚██╗██║   ██║
  ╚██████╗╚██████╔╝██║  ██║███████╗██║ ╚████║   ██║
   ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝
[/bold cyan]
[bold yellow]Auto-Discussion AI Builder — Synthetic Data Generation[/bold yellow]
"""

def phase2_agent_name() -> str:
    console.print("\n[bold yellow]=== PHASE 2: IDENTIFIKASI NAMA AGENT ===[/bold yellow]")
    name = Prompt.ask("[bold]Masukkan nama AI Agent kamu[/bold]", default="CorentAI")
    console.print(f"[green]✔ Nama agent: [bold]{name}[/bold][/green]\n")
    return name

def phase4_config(provider: str):
    console.print(f"\n[bold yellow]=== PHASE 4: KONFIGURASI DUAL-MODEL & API KEY ===[/bold yellow]")
    console.print(Panel(f"[bold]Provider: {provider}[/bold]", border_style="blue"))

    api_key = Prompt.ask("[bold]Masukkan API Key[/bold]", password=True)
    main_model = select_model(provider, "Model Utama")
    partner_model = select_model(provider, "Model Partner (Teman Bicara)")

    save_env(api_key)
    return api_key, main_model, partner_model

def main():
    rprint(BANNER)

    step = 0

    config = load_config()
    config["DISCUSSION_ROUNDS"] = config.get("DISCUSSION_ROUNDS", 10)
    config["TOPIC"] = config.get("TOPIC", "general")

    run_installation(str(WEB_DIR))

    config["AGENT_NAME"] = phase2_agent_name()

    config["PROVIDER"] = select_provider()

    api_key, main_model, partner_model = phase4_config(config["PROVIDER"])
    config["API_KEY"] = api_key
    config["MAIN_MODEL"] = main_model
    config["PARTNER_MODEL"] = partner_model

    save_config(config)

    run_discussion(config)

    compile_dataset(config["AGENT_NAME"])

    summary = get_session_summary()
    console.print("\n[bold green]========================================[/bold green]")
    console.print(f"[bold green]  ✔ Corent AI Agent [yellow]{config['AGENT_NAME']}[/yellow] selesai dibuat![/bold green]")
    console.print(f"[bold green]  ✔ {summary['total_turns']} percakapan tersimpan[/bold green]")
    console.print(f"[bold green]  ✔ Data siap di /output dan /data[/bold green]")
    console.print(f"[bold green]========================================[/bold green]\n")

    console.print("[bold]Jalankan web dashboard:[/bold]")
    console.print(f"  [cyan]cd web && npm start[/cyan]")
    console.print(f"  [cyan]cd web && node server.js[/cyan]\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Corent dihentikan oleh pengguna.[/bold yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/bold red]")
        sys.exit(1)
