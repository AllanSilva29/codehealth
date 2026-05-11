import os
from .base import BaseEngine
from .drivers.python import PythonEngine

class EngineFactory:
    @staticmethod
    def get_engine(repo_path: str) -> BaseEngine:
        # Lógica simples de detecção: 
        # Se houver pyproject.toml, requirements.txt ou arquivos .py, usa PythonEngine
        
        python_indicators = ["pyproject.toml", "requirements.txt", "setup.py", "manage.py"]
        
        for item in python_indicators:
            if os.path.exists(os.path.join(repo_path, item)):
                return PythonEngine()
                
        # Se encontrar qualquer arquivo .py recursivamente
        for root, dirs, files in os.walk(repo_path):
            if any(f.endswith('.py') for f in files):
                return PythonEngine()
            if '.git' in dirs:
                dirs.remove('.git')
                
        # Por padrão, se não detectar nada específico mas houver arquivos, 
        # poderíamos ter uma GenericEngine, mas por enquanto vamos de PythonEngine
        # ou levantar um erro se quisermos ser estritos.
        return PythonEngine()
