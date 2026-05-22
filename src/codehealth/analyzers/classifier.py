import os
from typing import Dict
from ..models import FileMetrics

def classify_architectural_roles(files: Dict[str, FileMetrics]):
    """
    Classifica cada arquivo em um papel arquitetural com base no caminho e nome.
    Isso ajuda a ajustar os scores de hotspot e fornecer diagnósticos melhores.
    """
    for rel_path, metrics in files.items():
        path_lower = rel_path.lower()
        filename = os.path.basename(path_lower)
        
        # 1. Config & Bootstrap
        if any(x in path_lower for x in ["settings.py", "config/", "configuration", "setup.py", "bootstrap"]):
            metrics.is_config = True
            
        # 3. Serializers & Schemas
        if any(x in path_lower for x in ["serializer", "schema", "dto", "marshmallow", "pydantic"]):
            metrics.is_serializer = True
            
        # 2. API Gateway / Orchestrators
        if any(x in path_lower for x in ["gateway", "proxy", "facade", "orchestrator", "api/"]):
            if not metrics.is_test and not metrics.is_serializer:
                metrics.is_gateway = True
            
        # 4. CLI & Management Commands
        if any(x in path_lower for x in ["cli.py", "commands/", "management/commands/", "task/"]):
            metrics.is_cli_command = True
            
        # 5. Shared Kernel / Utilities
        if any(x in path_lower for x in ["shared/", "common/", "utils/", "kernel/", "base/", "models.py"]):
            metrics.is_shared_kernel = True
            
        # 6. Registry & Cache
        if any(x in path_lower for x in ["registry", "cache_manager", "plugin_registry"]):
            metrics.is_registry = True
            
        # 7. Event Handlers / Messaging
        if any(x in path_lower for x in ["handler", "consumer", "subscriber", "event_bus", "rabbitmq", "kafka"]):
            if not metrics.is_gateway: # Evita sobreposição se for gateway
                metrics.is_event_handler = True
                
        # 8. Enums & Mappings
        if any(x in path_lower for x in ["constants.py", "mapping.py", "enums.py", "table.py"]):
            metrics.is_enum_mapping = True

        # 9. Reporting / Emitters
        if any(x in path_lower for x in ["report/", "emit", "output", "display"]):
            metrics.is_registry = True # Using Registry as a proxy for "infrastructure lookup/output" or I could add is_reporting

def get_role_name(metrics: FileMetrics) -> str:
    if metrics.is_config: return "Configuration"
    if metrics.is_gateway: return "API Gateway"
    if metrics.is_serializer: return "Serializer/Schema"
    if metrics.is_cli_command: return "CLI Command"
    if metrics.is_shared_kernel: return "Shared Kernel"
    if metrics.is_registry: return "Registry/Cache"
    if metrics.is_event_handler: return "Event Handler"
    if metrics.is_enum_mapping: return "Enum/Mapping"
    if metrics.is_migration: return "Migration"
    if metrics.is_test: return "Test"
    return "Domain/Logic"
