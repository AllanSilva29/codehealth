import typer
from rich.console import Console
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
from .report.terminal import display_summary

app = typer.Typer(rich_markup_mode="rich")
console = Console()

@app.command(
    help="""
Executa o pipeline completo de análise de saúde de código.

Esta ferramenta investiga o repositório em busca de gargalos arquiteturais e sócio-técnicos.

[bold]Conceitos Chave:[/bold]
• [bold cyan]Score[/bold cyan]: Pontuação final de risco do arquivo (baseada em complexidade e histórico de alterações multiplicada por fatores contextuais).
• [bold cyan]Severidade[/bold cyan]: Classificação do risco geral (Low, Medium, High, Critical) baseada no Score.
• [bold cyan]Confiança[/bold cyan]: Certeza do diagnóstico (Low, Medium, High). Aumenta quando múltiplos sinais negativos corroboram o problema e diminui em arquivos como testes e código gerado.
[bold cyan]Diagnósticos Arquiteturais:[/bold cyan]
• [bold cyan]API Gateway[/bold cyan]: Orquestradores que podem esconder complexidade ou centralizar lógica indevida.
• [bold cyan]Serializer/Schema[/bold cyan]: Transformadores de dados onde a lógica de domínio costuma vazar.
• [bold cyan]Shared Kernel[/bold cyan]: Núcleos compartilhados que exigem alta estabilidade.
• [bold cyan]Config/Mapping[/bold cyan]: Arquivos de infraestrutura com scores ajustados para evitar falsos positivos.

[bold cyan]Categorias de Risco:[/bold cyan]
  - [dim]COMPLEXITY[/dim]: Código muito denso (muita lógica espremida em poucas linhas).
  - [dim]GOD_OBJECT[/dim]: Arquivos gigantescos centralizando responsabilidades demais.
  - [dim]ARCHITECTURE[/dim]: Arquivos "maestros" ou orquestradores legítimos.
  - [dim]COUPLING[/dim]: Alto acoplamento com dependências externas.
  - [dim]TEMPORAL[/dim]: Dependências ocultas detectadas via histórico Git.
  - [dim]SOCIO_TECHNICAL[/dim]: Gargalos de equipe e fragmentação de conhecimento.

[bold]Complexidade Média do Projeto:[/bold]
Representa o "peso" cognitivo médio para entender um arquivo no projeto.
• [bold green]Baixa (menor que 10)[/bold green]: Projeto saudável. O código é simples, modular e fácil de testar.
• [bold yellow]Moderada (10 até 20)[/bold yellow]: Alerta. Algumas áreas estão ficando densas; a manutenção exige mais atenção.
• [bold red]Alta (maior que 20)[/bold red]: Perigo. O projeto possui lógica muito ramificada, difícil de debugar e com alto risco de bugs em novas alterações.
"""
)
def scan(
    repo_path: str = typer.Argument(..., help="Caminho para o repositório Git"),
    output: str = typer.Option("report.json", "--output", "-o", help="Arquivo de saída JSON")
):
    if not os.path.exists(repo_path):
        console.print(f"[red]Erro:[/red] Caminho {repo_path} não encontrado.")
        raise typer.Exit(code=1)

    console.print(f"[bold blue]Iniciando scan no repositório:[/bold blue] {repo_path}")

    historical_data = _load_historical_data(output)

    # 1. Coleta do Git
    console.print("  [yellow]>>[/yellow] Coletando histórico Git e Contribuidores...")
    churn_data, contributors_data, co_changes_data = collect_git_metrics(repo_path)
    total_commits = get_total_commits(repo_path)

    # 2. Análise de Arquivos
    console.print("  [yellow]>>[/yellow] Analisando arquivos Python...")
    report = RepositoryReport(total_commits=total_commits)
    _analyze_python_files(repo_path, report, historical_data, churn_data, contributors_data, co_changes_data)

    # 3. Grafo de Dependências
    console.print("  [yellow]>>[/yellow] Construindo Grafo de Dependências...")
    _build_and_apply_graph(report)

    # 4. Agregação e Scores
    console.print("  [yellow]>>[/yellow] Calculando Hotspots Contextuais...")
    calculate_hotspots(report.files)
    _finalize_report_metrics(report)

    # 5. Emissão do Relatório
    console.print(f"  [yellow]>>[/yellow] Gerando relatório JSON: [green]{output}[/green]")
    emit_json(report, output)

    # Exibição no terminal
    display_summary(report)

def _load_historical_data(output_path: str) -> dict:
    if os.path.exists(output_path):
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                prev_report = json.load(f)
                return prev_report.get("files", {})
        except Exception:
            pass
    return {}

def _analyze_python_files(repo_path: str, report: RepositoryReport, hist_data: dict, churn_data: dict, contributors_data: dict, co_changes_data: dict):
    python_files = list_python_files(repo_path)
    for rel_path in python_files:
        source = load_source(repo_path, rel_path)
        functions = analyze_complexity(source)
        imports = analyze_dependencies(source)
        hist = hist_data.get(rel_path, {})
        
        metrics = FileMetrics(
            path=rel_path,
            churn=churn_data.get(rel_path, 0),
            loc=len(source.splitlines()),
            fan_out=get_fan_out(imports),
            cyclomatic_sum=get_cyclomatic_sum(functions),
            functions=functions,
            imports=imports,
            is_generated=is_generated_code(source),
            is_migration=is_migration_code(rel_path, source),
            is_test=is_test_code(rel_path),
            contributors=contributors_data.get(rel_path, set()),
            co_changes=co_changes_data.get(rel_path, {}),
            historical_churn=hist.get("churn", 0),
            historical_complexity=hist.get("cyclomatic_sum", 0)
        )
        report.files[rel_path] = metrics

def _build_and_apply_graph(report: RepositoryReport):
    fan_in_map, in_cycles = build_project_graph(report.files)
    for path, metrics in report.files.items():
        metrics.fan_in = fan_in_map.get(path, 0)
        metrics.in_cycles = path in in_cycles

def _finalize_report_metrics(report: RepositoryReport):
    for f in report.files.values():
        f.hotspot_score = round(f.hotspot_score, 2)
    if report.files:
        total_complexity = sum(f.cyclomatic_sum for f in report.files.values())
        report.avg_complexity = round(total_complexity / len(report.files), 2)

if __name__ == "__main__":
    app()
