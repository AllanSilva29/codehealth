from typing import Dict
from ..models import FileMetrics
from .classifier import classify_architectural_roles

def calculate_hotspots(files: Dict[str, FileMetrics]):
    if not files:
        return

    max_churn = max(max((f.churn for f in files.values()), default=1), 3)
    max_complexity = max(max((f.cyclomatic_sum for f in files.values()), default=1), 30)

    classify_architectural_roles(files)

    for metrics in files.values():
        _calculate_contextual_scores(metrics, max_churn, max_complexity)
        _generate_heuristics(metrics)
        _evaluate_confidence(metrics)
        _distinguish_risk(metrics)
        _apply_severity(metrics)
        _add_validation_questions(metrics)

def _calculate_contextual_scores(metrics: FileMetrics, max_churn: int, max_complexity: int):
    base_score = (metrics.churn / max_churn) * (metrics.cyclomatic_sum / max_complexity) * 100
    multiplier = _get_contextual_multiplier(metrics)
    metrics.hotspot_score = base_score * multiplier

def _get_contextual_multiplier(metrics: FileMetrics) -> float:
    multiplier = 1.0
    if metrics.in_cycles:
        multiplier *= 1.4
        metrics.reasons.append("Loop perigoso de imports: arquivos dependendo um do outro em círculo (+40% de risco).")
    if len(metrics.contributors) > 5:
        multiplier *= 1.2
        metrics.reasons.append(f"Muitas 'mãos' no código: {len(metrics.contributors)} desenvolvedores diferentes mexeram aqui (+20% de risco).")
    if metrics.is_generated:
        multiplier *= 0.3
        metrics.reasons.append("Código gerado automaticamente (-70% de risco).")
    if metrics.is_migration:
        multiplier *= 0.5
        metrics.reasons.append("Script de banco de dados/migração (-50% de risco).")
    if metrics.is_test:
        multiplier *= 0.6
        metrics.reasons.append("Arquivo exclusivo de teste (-40% de risco).")
    
    # Novos multiplicadores arquiteturais
    if metrics.is_config or metrics.is_enum_mapping:
        if metrics.cyclomatic_sum < 20:
            multiplier *= 0.5
            metrics.reasons.append("Configuração/Mapeamento estável e simples (-50% de risco).")
        else:
            multiplier *= 1.2
            metrics.reasons.append("Configuração com lógica complexa detectada (+20% de risco).")

    if metrics.is_gateway:
        if metrics.cyclomatic_sum < 15:
            multiplier *= 0.7
            metrics.reasons.append("Gateway/Maestro legítimo: muita orquestração, pouca lógica interna (-30% de risco).")
        else:
            multiplier *= 1.3
            metrics.reasons.append("Gateway 'Gordo': lógica de negócio vazando para o orquestrador (+30% de risco).")

    if metrics.is_serializer:
        if metrics.cyclomatic_sum > 25:
            multiplier *= 1.4
            metrics.reasons.append("Serializer complexo: possível vazamento de regras de domínio (+40% de risco).")

    return multiplier

def _generate_heuristics(metrics: FileMetrics):
    _check_complexity_density(metrics)
    _check_god_object(metrics)
    _check_fan_out(metrics)
    _check_temporal_coupling(metrics)
    _check_sociotechnical(metrics)

    if metrics.hotspot_score > 30 and "HOTSPOT" not in metrics.categories:
        metrics.categories.append("HOTSPOT")

def _check_complexity_density(metrics: FileMetrics):
    loc = max(metrics.loc, 1)
    complexity_density = metrics.cyclomatic_sum / loc
    if complexity_density > 0.15 and metrics.loc > 100:
        metrics.categories.append("COMPLEXITY")
        metrics.signals["high_density"] = True
        metrics.notes.append(f"Muito código complexo (ifs/loops) espremido em poucas linhas ({complexity_density:.2f} pontos por linha). O arquivo está denso e difícil de ler.")

def _check_god_object(metrics: FileMetrics):
    is_large = metrics.loc > 300
    is_complex = metrics.cyclomatic_sum > 50
    
    # Heurística de coesão simples: muitas funções com complexidade espalhada
    has_fragmented_logic = len([f for f in metrics.functions if f.complexity > 5]) > 5
    
    if is_large and is_complex:
        metrics.categories.append("GOD_OBJECT")
        metrics.signals["god_object"] = True
        
        if has_fragmented_logic:
            metrics.notes.append(f"Deus ex Machina: Arquivo gigante ({metrics.loc} linhas) com lógica muito fragmentada. Parece centralizar múltiplos domínios.")
            metrics.hotspot_score *= 1.2
        else:
            metrics.notes.append(f"Arquivo grande ({metrics.loc} linhas) fazendo coisas demais. Considere quebrar em serviços menores.")

def _check_fan_out(metrics: FileMetrics):
    if metrics.fan_out > 15:
        avg_func_complexity = metrics.cyclomatic_sum / max(len(metrics.functions), 1)
        if avg_func_complexity < 3:
            metrics.categories.append("ARCHITECTURE")
            metrics.notes.append(f"Arquivo atua como um 'maestro'. Ele importa muitos outros arquivos ({metrics.fan_out} dependências), mas suas funções são simples.")
        else:
            metrics.categories.append("COUPLING")
            metrics.signals["high_coupling"] = True
            metrics.notes.append(f"Arquivo muito dependente de outros ({metrics.fan_out} dependências) e com lógica muito complexa. É arriscado mexer aqui sem quebrar o sistema.")
            metrics.hotspot_score *= 1.3

def _check_temporal_coupling(metrics: FileMetrics):
    if metrics.co_changes:
        metrics.categories.append("TEMPORAL")
        metrics.signals["temporal_coupling"] = True
        coupled_with = ", ".join(f"{k} ({v*100:.0f}%)" for k, v in metrics.co_changes.items())
        metrics.notes.append(f"Sempre que esse arquivo muda, esses também mudam: {coupled_with}. Pode haver uma dependência oculta (código amarrado).")

def _check_sociotechnical(metrics: FileMetrics):
    if len(metrics.contributors) > 5 and metrics.churn > 20:
        metrics.categories.append("SOCIO_TECHNICAL")
        metrics.signals["high_fragmentation"] = True
        metrics.notes.append(f"Gargalo na equipe: o arquivo muda toda hora e tem {len(metrics.contributors)} pessoas diferentes mexendo. Risco alto de bugs e conflitos.")

def _evaluate_confidence(metrics: FileMetrics):
    score = sum([
        metrics.signals.get("high_density", False) or metrics.signals.get("god_object", False),
        metrics.signals.get("temporal_coupling", False),
        metrics.signals.get("high_fragmentation", False),
        metrics.in_cycles
    ])
    
    if metrics.is_test or metrics.is_migration or metrics.is_generated or metrics.is_config or metrics.is_enum_mapping:
        score -= 2
        
    if metrics.is_gateway or metrics.is_serializer:
        score -= 1 # Framework markers reduce confidence of "pure" hotspot
        
    metrics.confidence = "High" if score >= 2 else "Medium" if score == 1 else "Low"

def _distinguish_risk(metrics: FileMetrics):
    high_comp = metrics.cyclomatic_sum > 30 or metrics.signals.get("god_object", False)
    high_churn = metrics.churn > 15
    
    if high_comp and not high_churn:
        metrics.reasons.append("Risco Estrutural: Arquivo com código muito complexo, mas pelo menos ele quase não sofre alterações (estável).")
    elif high_churn and not high_comp:
        metrics.reasons.append("Risco Operacional: Arquivo muda com muita frequência. Pode indicar que esse código é um gargalo na equipe ou a regra nunca estabiliza.")
    elif high_comp and high_churn:
        metrics.reasons.append("Risco Crítico: Pior cenário possível. O código é muito difícil de entender e ainda por cima está sendo alterado o tempo todo.")

def _apply_severity(metrics: FileMetrics):
    if metrics.hotspot_score >= 80:
        metrics.severity = "Critical"
    elif metrics.hotspot_score >= 51:
        metrics.severity = "High"
    elif metrics.hotspot_score >= 21:
        metrics.severity = "Medium"
    else:
        metrics.severity = "Low"

def _add_validation_questions(metrics: FileMetrics):
    """Adiciona perguntas de investigação baseadas no papel do arquivo."""
    if metrics.is_gateway:
        metrics.validation_questions.extend([
            "A lógica de negócio está centralizada aqui ou apenas orquestração?",
            "As dependências importadas são coesas com o propósito do gateway?"
        ])
    if metrics.is_serializer:
        metrics.validation_questions.extend([
            "Existe lógica de domínio vazando para os serializers?",
            "A complexidade de validação é intrínseca ao domínio ou procedural?"
        ])
    if metrics.is_config:
        metrics.validation_questions.extend([
            "Existem regras de negócio misturadas com a infraestrutura?",
            "A inicialização está explícita ou baseada em efeitos colaterais mágicos?"
        ])
    if metrics.is_enum_mapping:
        metrics.validation_questions.extend([
            "A complexidade é algorítmica ou apenas dados declarativos?",
            "Este mapeamento é instável ou muda por razões externas?"
        ])
    if metrics.signals.get("god_object"):
        metrics.validation_questions.extend([
            "Quantas responsabilidades distintas este arquivo possui?",
            "Domínios não relacionados estão misturados aqui?",
            "A API pública é excessivamente ampla?"
        ])
    if metrics.signals.get("temporal_coupling"):
        metrics.validation_questions.extend([
            "O co-change é causado por fluxo de trabalho compartilhado ou duplicação de regras?",
            "Existe uma abstração faltando que unificaria essas mudanças?"
        ])
