import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.live import Live
from rich.layout import Layout
from rich.text import Text

from . import models, prompts
from core import json_store

console = Console()

def run_discussion(config: dict):
    agent_name = config["AGENT_NAME"]
    provider = config["PROVIDER"]
    api_key = config["API_KEY"]
    main_model = config["MAIN_MODEL"]
    partner_model = config["PARTNER_MODEL"]
    rounds = config.get("DISCUSSION_ROUNDS", 10)
    topic = config.get("TOPIC", "general")

    console.print(f"\n[bold yellow]=== PHASE 5: AUTO-DISCUSSION & DATA GATHERING ===[/bold yellow]")
    console.print(f"[cyan]Agent:[/cyan] {agent_name}")
    console.print(f"[cyan]Topic:[/cyan] {topic}")
    console.print(f"[cyan]Rounds:[/cyan] {rounds}")
    console.print(f"[cyan]Main Model:[/cyan] {main_model}")
    console.print(f"[cyan]Partner Model:[/cyan] {partner_model}\n")

    main_sys = prompts.SYSTEM_PROMPT_MAIN.format(agent_name=agent_name)
    partner_sys = prompts.SYSTEM_PROMPT_PARTNER.format(agent_name=agent_name)

    main_messages = [{"role": "system", "content": main_sys}]
    partner_messages = [{"role": "system", "content": partner_sys}]

    initial = prompts.build_initial_prompt(agent_name, topic)
    partner_messages.append({"role": "user", "content": initial})
    json_store.save_turn(agent_name, "partner", partner_model, initial, 0, topic)

    with Progress(
        BarColumn(bar_width=40),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("[bold]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(f"[cyan]Berdiskusi...", total=rounds)

        for turn in range(1, rounds + 1):
            progress.update(task, description=f"[cyan]Turn {turn}/{rounds} — Partner menulis...")

            partner_reply = models.chat_completion(
                provider, api_key, partner_model, partner_messages
            )
            if partner_reply and not partner_reply.startswith("[ERROR"):
                json_store.save_turn(agent_name, "partner", partner_model, partner_reply, turn, topic)
                main_messages.append({"role": "user", "content": partner_reply})

            progress.update(task, description=f"[cyan]Turn {turn}/{rounds} — {agent_name} merespon...")

            main_reply = models.chat_completion(
                provider, api_key, main_model, main_messages
            )
            if main_reply and not main_reply.startswith("[ERROR"):
                json_store.save_turn(agent_name, "main", main_model, main_reply, turn, topic)
                partner_messages.append({"role": "user", "content": main_reply})
                main_messages.append({"role": "assistant", "content": main_reply})

            progress.update(task, advance=1)

            topic_keywords = {
                "technology": ["tech", "komputer", "digital", "software", "programming"],
                "science": ["fisika", "biologi", "kimia", "alam", "eksperimen"],
                "philosophy": ["makna", "kesadaran", "eksistensi", "etika", "moral"],
                "creative_writing": ["cerita", "puisi", "imajinasi", "kreatif", "seni"],
                "coding": ["kode", "program", "algoritma", "aplikasi", "debug"],
                "problem_solving": ["solusi", "strategi", "rencana", "langkah", "tujuan"]
            }
            related = topic_keywords.get(topic, [])
            if related and (not partner_reply or not main_reply):
                injection = f"Bicara tentang {topic} ya, ini menarik! {', '.join(related[:3])}?"
                if partner_reply and partner_reply.startswith("[ERROR"):
                    partner_messages.append({"role": "user", "content": injection})

            time.sleep(0.3)

    cat_counts = json_store.get_category_counts()
    table = Table(title="📊 Hasil Diskusi", header_style="bold cyan")
    table.add_column("Metrik", style="green")
    table.add_column("Nilai")
    table.add_row("Total percakapan", str(json_store.get_conversation_count()))
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        if count > 0:
            table.add_row(f"  Kategori: {cat}", str(count))
    console.print(table)
    console.print(f"\n[bold green]✔ Diskusi selesai! {json_store.get_conversation_count()} percakapan tersimpan di data/[/bold green]\n")
