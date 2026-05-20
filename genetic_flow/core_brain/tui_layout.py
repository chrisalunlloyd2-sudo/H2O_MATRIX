from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.syntax import Syntax
from rich.console import Console

console = Console()

def generate_dashboard(gen, fitness, code_str, stuck_count, max_stuck):
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=4),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3)
    )
    layout["body"].split_row(
        Layout(name="feed", ratio=1),
        Layout(name="code", ratio=1)
    )
    
    hdr_text = f"[bold green]MODE:[/bold green] Hybrid PRoot Loop  |  [bold cyan]RAM FENCE:[/bold cyan] Active (256MB)\n[bold green]BRAIN:[/bold green] Qwen2:1.5b (Local) | [bold green]CLEANER:[/bold green] Danube3:500m"
    layout["header"].update(Panel(hdr_text, title="SYSTEM MONITOR", border_style="cyan"))
    
    feed_text = f"Generation: [bold yellow]{gen}[/bold yellow]\nLast Computed Fitness Score: [bold green]{fitness:.4f}[/bold green]"
    layout["feed"].update(Panel(feed_text, title="EVOLUTION PIPELINE FEED", border_style="yellow"))
    
    code_syntax = Syntax(code_str, "python", theme="monokai", line_numbers=True)
    layout["code"].update(Panel(code_syntax, title="CURRENT RUNNING GENETIC BASELINE", border_style="green"))
    
    ftr_text = f"[bold red]WATCHDOG STATUS:[/bold red] Nominal | Stuck Rounds: [bold yellow]{stuck_count}/{max_stuck}[/bold yellow] | Cloud Escalation: [bold cyan]IDLE[/bold cyan]"
    layout["footer"].update(Panel(ftr_text, title="WATCHDOG CIRCUIT BREAKER", border_style="red"))
    
    return layout
