import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
import os

from .models import FileMetrics, RepositoryReport
from .collectors.git_history import collect_file_churn, get_total_commits
from .collectors.source_loader import list_python_files, load_source, is_generated_code
from .analyzers.complexity import analyze_complexity, get_cyclomatic_sum
from .analyzers.dependencies import analyze_dependencies, get_fan_out
from .analyzers.hotspots import calculate_hotspots
from .report.emit_json import emit_json

app = typer.Typer(help="Code Health Analysis Pipeline")
console = Console()

@app.command()
def scan(
    repo_path: str = typer.Argument(..., help="Caminho para o repositório Git"),
    output: str = typer.Option("report.json", "--output", "-o", help="Arquivo de saída JSON")
):
    """
    Executa o pipeline completo de análise de saúde de código.
    """
    if not os.path.exists(repo_path):
        console.print(f"[red]Erro:[/red] Caminho {repo_path} não encontrado.")
        raise typer.Exit(code=1)

    console.print(f"[bold blue]Iniciando scan no repositório:[/bold blue] {repo_path}")

    # 1. Coleta do Git
    console.print("  [yellow]>>[/yellow] Coletando histórico Git (Churn)...")
    churn_data = collect_file_churn(repo_path)
    total_commits = get_total_commits(repo_path)

    # 2. Análise de Arquivos
    console.print("  [yellow]>>[/yellow] Analisando arquivos Python...")
    python_files = list_python_files(repo_path)
    report = RepositoryReport(total_commits=total_commits)

    for rel_path in python_files:
        source = load_source(repo_path, rel_path)
        is_gen = is_generated_code(source)
        
        # Métricas estáticas
        functions = analyze_complexity(source)
        imports = analyze_dependencies(source)
        
        metrics = FileMetrics(
            path=rel_path,
            churn=churn_data.get(rel_path, 0),
            loc=len(source.splitlines()),
            fan_out=get_fan_out(imports),
            cyclomatic_sum=get_cyclomatic_sum(functions),
            functions=functions,
            imports=imports,
            is_generated=is_gen
        )
        report.files[rel_path] = metrics

    # 3. Agregação e Scores
    console.print("  [yellow]>>[/yellow] Calculando Hotspots...")
    calculate_hotspots(report.files)

    # Arredondar scores para o JSON ficar mais limpo
    for f in report.files.values():
        f.hotspot_score = round(f.hotspot_score, 2)

    # Calcular complexidade média
    if report.files:
        total_complexity = sum(f.cyclomatic_sum for f in report.files.values())
        report.avg_complexity = round(total_complexity / len(report.files), 2)

    # 4. Emissão do Relatório
    console.print(f"  [yellow]>>[/yellow] Gerando relatório JSON: [green]{output}[/green]")
    emit_json(report, output)

    # Exibição básica no terminal
    _display_summary(report)

def _display_summary(report: RepositoryReport):
    table = Table(title="Hotspots Detectados (Top 10)")
    table.add_column("Arquivo", style="cyan")
    table.add_column("Churn", justify="right")
    table.add_column("Complex.", justify="right")
    table.add_column("Fan-out", justify="right")
    table.add_column("Score", justify="right")
    table.add_column("Severidade", style="bold")

    # Ordena por hotspot_score desc
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
        
        table.add_row(
            f.path, 
            str(f.churn), 
            str(f.cyclomatic_sum), 
            str(f.fan_out),
            f"{f.hotspot_score:.1f}",
            f"[{severity_style}]{f.severity}[/{severity_style}]"
        )

    console.print("\n")
    console.print(table)

    # Relatório detalhado de problemas
    console.print("\n[bold underline]Diagnóstico Detalhado:[/bold underline]")
    for f in sorted_files:
        if f.notes:
            # Cor baseada na severidade
            color = "white"
            if f.severity == "Critical": color = "red"
            elif f.severity == "High": color = "orange"
            elif f.severity == "Medium": color = "yellow"
            
            console.print(f"\n[bold]{f.path}[/bold] ({f.severity})")
            for note in f.notes:
                console.print(f"  [dim]- {note}[/dim]")

    console.print(f"\n[bold green]Scan concluído![/bold green] Total de arquivos analisados: {len(report.files)}")
    console.print(f"[bold blue]Complexidade Média do Projeto:[/bold blue] {report.avg_complexity}")

if __name__ == "__main__":
    app()
