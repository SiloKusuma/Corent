import subprocess, sys, time, shutil
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

REQUIRED_PY_PACKAGES = ["requests", "rich", "python-dotenv"]
REQUIRED_NODE_PACKAGES = ["express", "cors", "dotenv"]

def _run_pip(pkg: str):
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", pkg, "--quiet"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

def _run_npm(pkg: str, cwd: str):
    subprocess.check_call(
        ["npm", "install", pkg, "--save"],
        cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

def check_python():
    console.print(f"[bold green]✔ Python[/bold green] {sys.version.split()[0]}")
    return True

def check_node():
    try:
        ver = subprocess.check_output(["node", "--version"], text=True).strip()
        console.print(f"[bold green]✔ Node.js[/bold green] {ver}")
        return True
    except FileNotFoundError:
        console.print("[bold red]✘ Node.js not found. Install from https://nodejs.org[/bold red]")
        return False

def check_npm():
    try:
        ver = subprocess.check_output(["npm", "--version"], text=True).strip()
        console.print(f"[bold green]✔ npm[/bold green] {ver}")
        return True
    except FileNotFoundError:
        console.print("[bold red]✘ npm not found.[/bold red]")
        return False

def install_python_deps():
    console.print("\n[bold cyan]▸ Installing Python packages...[/bold cyan]")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as p:
        for pkg in REQUIRED_PY_PACKAGES:
            task = p.add_task(f"  Installing {pkg}...", total=None)
            try:
                _run_pip(pkg)
            except subprocess.CalledProcessError:
                p.update(task, description=f"  [red]Failed {pkg}[/red]")
                return False
            p.update(task, description=f"  [green]✔ {pkg} installed[/green]")
            time.sleep(0.2)
    return True

def install_node_deps(web_dir: str):
    console.print("\n[bold cyan]▸ Installing Node.js packages...[/bold cyan]")
    if not Path(web_dir).exists():
        Path(web_dir).mkdir(parents=True)
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as p:
        base = p.add_task("  Initializing package.json...", total=None)
        subprocess.check_call(["npm", "init", "-y"], cwd=web_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p.update(base, description="  [green]✔ package.json ready[/green]")
        for pkg in REQUIRED_NODE_PACKAGES:
            task = p.add_task(f"  Installing {pkg}...", total=None)
            try:
                _run_npm(pkg, web_dir)
            except subprocess.CalledProcessError:
                p.update(task, description=f"  [red]Failed {pkg}[/red]")
                return False
            p.update(task, description=f"  [green]✔ {pkg} installed[/green]")
            time.sleep(0.2)
    return True

def run_installation(web_dir: str):
    console.print("\n[bold yellow]=== PHASE 1: INSTALLATION WIZARD ===[/bold yellow]\n")
    ok = True
    for fn, label in [(check_python, "Python"), (check_node, "Node.js"), (check_npm, "npm")]:
        if not fn():
            ok = False
    if not ok:
        console.print("[bold red]Prerequisites missing. Aborting.[/bold red]")
        sys.exit(1)
    if not install_python_deps():
        sys.exit(1)
    if not install_node_deps(web_dir):
        sys.exit(1)
    console.print("\n[bold green]✔ All dependencies installed successfully![/bold green]\n")
    return True
