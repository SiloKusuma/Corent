from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt

console = Console()

PROVIDER_INFO = {
    "1": {
        "name": "OpenRouter",
        "desc": "Multi-model gateway — access 200+ models",
        "api_url": "https://openrouter.ai/api/v1/chat/completions",
        "models": [
            "openai/gpt-4o", "openai/gpt-4o-mini",
            "anthropic/claude-3.5-sonnet", "google/gemini-2.0-flash",
            "meta-llama/llama-3.1-8b-instruct", "mistralai/mistral-7b-instruct"
        ]
    },
    "2": {
        "name": "Groq",
        "desc": "Ultra-fast inference on open models",
        "api_url": "https://api.groq.com/openai/v1/chat/completions",
        "models": [
            "llama3-70b-8192", "llama3-8b-8192",
            "mixtral-8x7b-32768", "gemma2-9b-it",
            "llama-3.1-70b-versatile", "llama-3.1-8b-instant"
        ]
    }
}

def select_provider() -> str:
    console.print(Panel("[bold yellow]Pilih Provider Gateway[/bold yellow]", border_style="yellow"))
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("#", style="dim")
    table.add_column("Provider")
    table.add_column("Deskripsi")
    for key, info in PROVIDER_INFO.items():
        table.add_row(key, info["name"], info["desc"])
    console.print(table)
    choice = Prompt.ask("[bold]Pilih provider[/bold]", choices=["1", "2"])
    provider_name = PROVIDER_INFO[choice]["name"]
    console.print(f"[green]✔ Provider dipilih: {provider_name}[/green]\n")
    return provider_name

def select_model(provider: str, label: str) -> str:
    info = None
    for k, v in PROVIDER_INFO.items():
        if v["name"].lower() == provider.lower():
            info = v
            break
    if not info:
        console.print("[red]Provider tidak dikenal, gunakan model manual.[/red]")
        return Prompt.ask(f"[bold]{label}[/bold] (nama model)")
    console.print(Panel(f"[bold yellow]Pilih {label}[/bold yellow]", border_style="yellow"))
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("#", style="dim")
    table.add_column("Model")
    for i, m in enumerate(info["models"], 1):
        table.add_row(str(i), m)
    table.add_row(str(len(info["models"])+1), "[italic]Kustom (ketik manual)[/italic]")
    console.print(table)
    max_choice = len(info["models"]) + 1
    choice = IntPrompt.ask("[bold]Pilih model[/bold]", default=1)
    if 1 <= choice <= len(info["models"]):
        model = info["models"][choice - 1]
    else:
        model = Prompt.ask("[bold]Masukkan nama model[/bold]")
    console.print(f"[green]✔ {label}: {model}[/green]\n")
    return model
