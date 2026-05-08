import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
import os
import json

from .models import FileMetrics, RepositoryReport
from .collectors.git_history import collect_git_metrics, get_total_commits
from .collectors.source_loader import list_python_files, load_source, is_generated_code, is_migration_code, is_test_code
from .analyzers.complexity import analyze_complexity, get_cyclomatic_sum
from .analyzers.dependencies import analyze_dependencies, get_fan_out
from .analyzers.hotspots import calculate_hotspots
from .graph.analyzer import build_project_graph
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

    historical_data = {}
    if os.path.exists(output):
        try:
            with open(output, 'r', encoding='utf-8') as f:
                prev_report = json.load(f)
                historical_data = prev_report.get("files", {})
        except Exception:
            pass

    # 1. Coleta do Git
    console.print("  [yellow]>>[/yellow] Coletando histórico Git e Contribuidores...")
    churn_data, contributors_data, co_changes_data = collect_git_metrics(repo_path)
    total_commits = get_total_commits(repo_path)

    # 2. Análise de Arquivos
    console.print("  [yellow]>>[/yellow] Analisando arquivos Python...")
    python_files = list_python_files(repo_path)
    report = RepositoryReport(total_commits=total_commits)

    for rel_path in python_files:
        source = load_source(repo_path, rel_path)
        is_gen = is_generated_code(source)
        is_mig = is_migration_code(rel_path, source)
        is_test = is_test_code(rel_path)
        
        # Métricas estáticas
        functions = analyze_complexity(source)
        imports = analyze_dependencies(source)
        
        hist = historical_data.get(rel_path, {})
        
        metrics = FileMetrics(
            path=rel_path,
            churn=churn_data.get(rel_path, 0),
            loc=len(source.splitlines()),
            fan_out=get_fan_out(imports),
            cyclomatic_sum=get_cyclomatic_sum(functions),
            functions=functions,
            imports=imports,
            is_generated=is_gen,
            is_migration=is_mig,
            is_test=is_test,
            contributors=contributors_data.get(rel_path, set()),
            co_changes=co_changes_data.get(rel_path, {}),
            historical_churn=hist.get("churn", 0),
            historical_complexity=hist.get("cyclomatic_sum", 0)
        )
        report.files[rel_path] = metrics

    # 3. Grafo de Dependências
    console.print("  [yellow]>>[/yellow] Construindo Grafo de Dependências...")
    fan_in_map, in_cycles = build_project_graph(report.files)
    for path, metrics in report.files.items():
        metrics.fan_in = fan_in_map.get(path, 0)
        metrics.in_cycles = path in in_cycles

    # 4. Agregação e Scores
    console.print("  [yellow]>>[/yellow] Calculando Hotspots Contextuais...")
    calculate_hotspots(report.files)

    # Arredondar scores para o JSON ficar mais limpo
    for f in report.files.values():
        f.hotspot_score = round(f.hotspot_score, 2)

    # Calcular complexidade média
    if report.files:
        total_complexity = sum(f.cyclomatic_sum for f in report.files.values())
        report.avg_complexity = round(total_complexity / len(report.files), 2)

    # 5. Emissão do Relatório
    console.print(f"  [yellow]>>[/yellow] Gerando relatório JSON: [green]{output}[/green]")
    emit_json(report, output)

    # Exibição básica no terminal
    _display_summary(report)

def _display_summary(report: RepositoryReport):
    table = Table(title="Hotspots Detectados (Top 10)")
    table.add_column("Arquivo", style="cyan")
    table.add_column("Score", justify="right")
    table.add_column("Severidade", style="bold")
    table.add_column("Confiança", style="bold")
    table.add_column("Categorias", style="dim")

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

    # Relatório detalhado de problemas
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

if __name__ == "__main__":
    app()
