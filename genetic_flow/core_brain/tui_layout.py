from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.syntax import Syntax
from rich.console import Console
import os
import sys

# Add path for cluster and pyramid modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from genetic_flow.cluster import topology_mapper as topo

console = Console()
RULES_PATH = os.path.expanduser("~/genetic_flow/symbolic_brain/rules.sql")

def get_last_insight():
    if os.path.exists(RULES_PATH):
        try:
            with open(RULES_PATH, "r") as f:
                lines = f.readlines()
                if lines:
                    return lines[-1].strip().replace("-- ", "")
        except: pass
    return "Searching for patterns..."

def generate_dashboard(gen, fitness, code_str, stuck_count, max_stuck, sprite_status="IDLE"):
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=4),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=5)
    )
    layout["body"].split_row(
        Layout(name="feed", ratio=1),
        Layout(name="code", ratio=1)
    )

    insight = get_last_insight()
    hdr_text = f"[bold green]MODE:[/bold green] Hybrid PRoot Loop  |  [bold cyan]RAM FENCE:[/bold cyan] Active (256MB)\n[bold green]SYMBOLIC INSIGHT:[/bold green] [yellow]{insight}[/yellow]"
    layout["header"].update(Panel(hdr_text, title="SYSTEM MONITOR v3.0", border_style="cyan"))

    feed_text = f"Generation: [bold yellow]{gen}[/bold yellow]\nLast Computed Fitness Score: [bold green]{fitness:.4f}[/bold green]\n\n"
    feed_text += topo.get_cluster_topology()
    layout["feed"].update(Panel(feed_text, title="EVOLUTION PIPELINE FEED", border_style="yellow"))

    code_syntax = Syntax(code_str, "python", theme="monokai", line_numbers=True)
    layout["code"].update(Panel(code_syntax, title="CURRENT RUNNING GENETIC BASELINE", border_style="green"))

    ftr_text = f"[bold red]WATCHDOG STATUS:[/bold red] Nominal | Stuck Rounds: [bold yellow]{stuck_count}/{max_stuck}[/bold yellow]\n"
    ftr_text += f"[bold blue]SPRITE ENGINE:[/bold blue] {sprite_status} | [bold cyan]CLOUD ESCALATION:[/bold cyan] IDLE"
    layout["footer"].update(Panel(ftr_text, title="SYSTEM CONTROL & SAFETY LAYER", border_style="red"))

    return layout
