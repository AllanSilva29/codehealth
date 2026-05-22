import typer
from rich.console import Console
import os
import json

from .models import FileMetrics, RepositoryReport
from .collectors.git_history import collect_git_metrics, get_total_commits
from .collectors.source_loader import load_source
from .engines.factory import EngineFactory
from .engines.base import BaseEngine
from .analyzers.hotspots import calculate_hotspots
from .graph.analyzer import build_project_graph
from .report.emit_json import emit_json
from .report.terminal import display_summary

app = typer.Typer(rich_markup_mode="rich", help="Ferramenta de análise de saúde de código.")
console = Console()

@app.command(
    name="scan",
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
    repo_path: str = typer.Argument(None, help="Caminho para o repositório Git"),
    output: str = typer.Option("report.json", "--output", "-o", help="Arquivo de saída JSON"),
    guide: bool = typer.Option(False, "--guide", help="Mostra um guia de como investigar as perguntas de validação")
):
    if guide:
        _display_investigation_guide()
        raise typer.Exit()

    if not repo_path:
        console.print("[red]Erro:[/red] Você deve fornecer o caminho do repositório ou usar --guide.")
        raise typer.Exit(code=1)

    if not os.path.exists(repo_path):
        console.print(f"[red]Erro:[/red] Caminho {repo_path} não encontrado.")
        raise typer.Exit(code=1)

    console.print(f"[bold blue]Iniciando scan no repositório:[/bold blue] {repo_path}")

    # 0. Detecção de Engine
    engine = EngineFactory.get_engine(repo_path)
    console.print(f"  [yellow]>>[/yellow] Engine detectada: [bold cyan]{engine.__class__.__name__}[/bold cyan]")

    historical_data = _load_historical_data(output)

    # 1. Coleta do Git
    console.print("  [yellow]>>[/yellow] Coletando histórico Git e Contribuidores...")
    churn_data, contributors_data, co_changes_data = collect_git_metrics(repo_path)
    total_commits = get_total_commits(repo_path)

    # 2. Análise de Arquivos
    console.print(f"  [yellow]>>[/yellow] Analisando arquivos...")
    report = RepositoryReport(total_commits=total_commits)
    _analyze_files(engine, repo_path, report, historical_data, churn_data, contributors_data, co_changes_data)

    # 3. Grafo de Dependências
    console.print("  [yellow]>>[/yellow] Construindo Grafo de Dependências...")
    _build_and_apply_graph(report)

    # 4. Agregação e Scores
    console.print("  [yellow]>>[/yellow] Calculando Hotspots Contextuais...")
    engine.classify_roles(report.files)
    calculate_hotspots(report.files)
    _finalize_report_metrics(report)

    # 5. Emissão do Relatório
    console.print(f"  [yellow]>>[/yellow] Gerando relatório JSON: [green]{output}[/green]")
    emit_json(report, output)

    # Exibição no terminal
    display_summary(report, engine=engine)

def _load_historical_data(output_path: str) -> dict:
    if os.path.exists(output_path):
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                prev_report = json.load(f)
                return prev_report.get("files", {})
        except Exception:
            pass
    return {}

def _analyze_files(engine: BaseEngine, repo_path: str, report: RepositoryReport, hist_data: dict, churn_data: dict, contributors_data: dict, co_changes_data: dict):
    relevant_files = engine.list_files(repo_path)
    for rel_path in relevant_files:
        source = load_source(repo_path, rel_path)
        analysis = engine.analyze_source(rel_path, source)
        
        hist = hist_data.get(rel_path, {})
        
        metrics = FileMetrics(
            path=rel_path,
            churn=churn_data.get(rel_path, 0),
            loc=len(source.splitlines()),
            fan_out=analysis.get("fan_out", 0),
            cyclomatic_sum=analysis.get("cyclomatic_sum", 0),
            functions=analysis.get("functions", []),
            imports=analysis.get("imports", set()),
            is_generated=engine.is_generated_code(source),
            is_migration=engine.is_migration_code(rel_path, source),
            is_test=engine.is_test_code(rel_path),
            contributors=contributors_data.get(rel_path, set()),
            co_changes=co_changes_data.get(rel_path, {}),
            historical_churn=hist.get("churn", 0),
            historical_complexity=hist.get("historical_complexity", 0) or hist.get("cyclomatic_sum", 0)
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

@app.command(name="guide", help="Mostra o guia de investigação.")
def guide_cmd():
    _display_investigation_guide()

def _display_investigation_guide():
    """Exibe um guia detalhado sobre como responder às perguntas de investigação."""
    from rich.panel import Panel
    from rich.markdown import Markdown

    guide_text = """

Este guia ajuda você a responder às perguntas de validação geradas pelo scan.

---

### Gateways e Orquestradores
Gateways recebem uma requisição e a direcionam para os lugares certos, sem processar a lógica pesada sozinhos.
**Onde são usados:** Em Views de API (Django/FastAPI), Controllers, ou módulos que integram com serviços externos (ex: Gateway de Pagamento).

**P: Este arquivo contém regras de negócio ou ele só 'passa a bola'?**
- **O que checar:** Procure por `if/else` que decidem regras do produto (ex: cálculos de desconto, validação de status). Se houver muito disso, o código deveria estar em um *Service*.
- **O que é bom:** O arquivo apenas chama métodos de outros objetos e retorna o resultado.

**P: As coisas que este arquivo importa fazem sentido?**
- **O que checar:** Veja os `imports`. Se um Gateway importa modelos de banco de dados diretamente ou bibliotecas de baixo nível, ele está fazendo coisa demais.

---

### Serializers e Schemas
**P: Tem cálculos ou regras complicadas aqui?**
- **O que checar:** Serializers devem apenas transformar dados. Se houver métodos `.save()` ou `.create()` com muita lógica, ou validações que consultam o banco repetidamente, está errado.

**P: A validação é simples ou um labirinto?**
- **O que checar:** Se um método de validação tem mais de 10-15 linhas ou muitos `if` aninhados, a regra é complexa demais para morar no Serializer.

---

### Configurações
**P: Tem regra de negócio misturada com infraestrutura?**
- **O que checar:** Arquivos de config devem ter apenas variáveis e chaves. Se houver funções que decidem comportamentos baseados em permissões ou datas, retire de lá.

---

### God Objects (Arquivos Gigantes)
**P: Este arquivo está fazendo o trabalho de vários ao mesmo tempo?**
- **O que checar:** Se o arquivo lida com "Usuário", "Email" e "Pagamento" no mesmo lugar, ele tem responsabilidades demais.
- **Dica:** Tente agrupar as funções por tema. Se você conseguir criar 3 arquivos novos com nomes claros, a divisão é necessária.

---

### Dependência Temporal (Sempre mudam juntos)
**P: Eles estão 'copiando' a lógica um do outro?**
- **O que checar:** Veja se os arquivos têm trechos de código idênticos. Se você altera um e esquece o outro, o sistema quebra?
- **Solução:** Extraia a lógica repetida para um arquivo comum (utilitário ou base).
"""
    console.print(Panel(Markdown(guide_text), title="Guia de Investigação", expand=False))

if __name__ == "__main__":
    app()
