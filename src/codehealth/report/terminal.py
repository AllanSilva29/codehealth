from rich.console import Console
from rich.table import Table
from ..models import RepositoryReport

console = Console()

def display_summary(report: RepositoryReport):
    """Exibe o sumário dos resultados no terminal usando a biblioteca rich."""
    table = Table(title="Hotspots Detectados (Top 10)")
    table.add_column("Arquivo", style="cyan")
    table.add_column("Score", justify="right")
    table.add_column("Severidade", style="bold")
    table.add_column("Confiança", style="bold")
    table.add_column("Categorias", style="dim")

    sorted_files = sorted(
        report.files.values(), 
        key=lambda x: x.hotspot_score, 
        reverse=True
    )[:10]

    for f in sorted_files:
        severity_style = "white"
        if f.severity == "Critical":
            severity_style = "bold red"
        elif f.severity == "High":
            severity_style = "red"
        elif f.severity == "Medium":
            severity_style = "yellow"
            
        conf_style = "green" if f.confidence == "High" else "yellow" if f.confidence == "Medium" else "red"
        cats = ", ".join(f.categories) if f.categories else "None"
        
        table.add_row(
            f.path, 
            f"{f.hotspot_score:.1f}",
            f"[{severity_style}]{f.severity}[/{severity_style}]",
            f"[{conf_style}]{f.confidence}[/{conf_style}]",
            cats
        )

    console.print("\n")
    console.print(table)

    console.print("\n[bold underline]Diagnóstico Contextual Detalhado:[/bold underline]")
    for f in sorted_files:
        if f.reasons or f.notes:
            color = "white"
            if f.severity == "Critical": color = "red"
            elif f.severity == "High": color = "orange"
            elif f.severity == "Medium": color = "yellow"
            
            console.print(f"\n[{color}][bold]{f.path}[/bold] (Risco: {f.severity}, Confiança: {f.confidence})[/{color}]")
            if f.reasons:
                console.print("  [bold]Fatores de Risco (Razões):[/bold]")
                for reason in f.reasons:
                    console.print(f"    [dim]- {reason}[/dim]")
            if f.notes:
                console.print("  [bold]Notas Heurísticas:[/bold]")
                for note in f.notes:
                    console.print(f"    [dim]- {note}[/dim]")

    console.print(f"\n[bold green]Scan concluído![/bold green] Total de arquivos analisados: {len(report.files)}")
    console.print(f"[bold blue]Complexidade Média do Projeto:[/bold blue] {report.avg_complexity}")
