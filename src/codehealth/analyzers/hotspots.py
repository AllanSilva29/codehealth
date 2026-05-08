from typing import Dict
from ..models import FileMetrics

def calculate_hotspots(files: Dict[str, FileMetrics]):
    """
    Orquestra o cálculo de hotspots e diagnósticos.
    """
    if not files:
        return

    # Usamos limiares mínimos de referência equilibrados 
    # para projetos de pequeno/médio porte.
    max_churn = max(max((f.churn for f in files.values()), default=1), 3)
    max_complexity = max(max((f.cyclomatic_sum for f in files.values()), default=1), 30)

    for metrics in files.values():
        _calculate_scores(metrics, max_churn, max_complexity)
        _generate_diagnostics(metrics)
        _apply_severity(metrics)

def _calculate_scores(metrics: FileMetrics, max_churn: int, max_complexity: int):
    norm_churn = metrics.churn / max_churn
    norm_complexity = metrics.cyclomatic_sum / max_complexity
    metrics.hotspot_score = (norm_churn * norm_complexity) * 100
    
    if metrics.is_generated:
        metrics.hotspot_score *= 0.5
        metrics.notes.append("Código gerado detectado: Severidade reduzida.")

def _generate_diagnostics(metrics: FileMetrics):
    # 1. Funções Complexas
    for func in metrics.functions:
        if func.complexity > 20:
            metrics.notes.append(f"Alto Risco: Refatoração Necessária na função '{func.name}' (Complexidade: {func.complexity})")
        elif func.complexity > 10:
            metrics.notes.append(f"Risco Moderado: Considere Extrair Métodos da função '{func.name}' (Complexidade: {func.complexity})")

    # 2. Acoplamento
    if metrics.fan_out > 15:
        metrics.notes.append(f"Acoplamento Excessivo: O módulo depende de {metrics.fan_out} componentes. Extraia serviços ou isole preocupações.")

    # 3. Tamanho
    if metrics.loc > 200:
        metrics.notes.append(f"God Object: Arquivo muito grande ({metrics.loc} linhas). Considere dividir em submódulos.")

    # 4. Ciclos
    if metrics.cycles > 0:
        metrics.notes.append(f"Dependência Circular: Detectados {metrics.cycles} ciclos. Resolva para evitar efeitos colaterais.")

def _apply_severity(metrics: FileMetrics):
    score_display = f"{metrics.hotspot_score:.1f}"
    
    if metrics.hotspot_score >= 80:
        metrics.severity = "Critical"
        metrics.notes.append(f"CRITICAL: Hotspot crítico (Score: {score_display}). A complexidade total de {metrics.cyclomatic_sum} aliada ao churn torna este arquivo um ponto de falha provável.")
    elif metrics.hotspot_score >= 51:
        metrics.severity = "High"
        metrics.notes.append(f"HIGH: Risco elevado (Score: {score_display}). A complexidade de {metrics.cyclomatic_sum} está acima da média, dificultando manutenções futuras.")
    elif metrics.hotspot_score >= 21:
        metrics.severity = "Medium"
        metrics.notes.append(f"MEDIUM: Ponto de atenção (Score: {score_display}). Complexidade moderada que pode se tornar um hotspot se o churn aumentar.")
    else:
        metrics.severity = "Low"

    # Escalação por acoplamento
    if metrics.hotspot_score > 40 and metrics.fan_out > 15:
        metrics.severity = "Critical"
        metrics.notes.append(f"ESCALATION: Severidade elevada para CRITICAL devido ao alto acoplamento (Fan-out: {metrics.fan_out}).")

    # Redução por orquestração
    avg_func_complexity = metrics.cyclomatic_sum / max(len(metrics.functions), 1)
    if metrics.fan_out > 10 and avg_func_complexity < 5:
        if metrics.severity in ["Critical", "High"]:
            metrics.severity = "Medium"
            metrics.notes.append(f"REDUCTION: Severidade reduzida para MEDIUM pois o módulo é um orquestrador com funções simples (Complexidade Média: {avg_func_complexity:.1f}).")
