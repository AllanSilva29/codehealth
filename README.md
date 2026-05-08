# Code Health Analysis Pipeline 🚀

Uma ferramenta para analisar a "saúde" do seu código Python, identificando **Hotspots** (áreas de alto risco de manutenção) através da combinação de métricas de churn (histórico Git) e complexidade estática.

## ✨ Funcionalidades

- **Métricas de Churn:** Identifica quais arquivos mudam com mais frequência.
- **Complexidade Ciclomática:** Analisa a dificuldade de leitura e teste das funções.
- **Análise de Dependências (Fan-out):** Mapeia o acoplamento entre módulos.
- **Detecção de Hotspots:** Algoritmo que cruza churn e complexidade para encontrar códigos críticos.
- **Relatórios JSON:** Gera dados estruturados para integração com outras ferramentas.
- **Interface Visual Detalhada:** Exibe tabelas de hotspots e diagnósticos acionáveis diretamente no terminal para orientar a refatoração.
- **Recomendações Acionáveis:** Sugere extração de métodos, serviços e resolução de acoplamento com base em métricas reais.

## 🛠️ Instalação

Certifique-se de estar com seu ambiente virtual ativo e instale as dependências:

```bash
pip install -e .
```

As principais bibliotecas utilizadas são:
- `PyDriller` (Mineração de Git)
- `Radon` (Métricas de código)
- `NetworkX` (Grafos de dependência)
- `Typer` & `Rich` (CLI moderna)

## 🚀 Como Usar

Para escanear um repositório, basta rodar o comando `scan` passando o caminho da pasta:

```bash
codehealth scan /caminho/do/seu/projeto
```

### Opções:

- `-o`, `--output`: Define o nome do arquivo JSON de saída (Padrão: `report.json`).

Exemplo:
```bash
codehealth scan . --output analise_maio.json
```

## 📊 Entendendo os Resultados

O pipeline classifica os arquivos em níveis de severidade baseados no **Hotspot Score**:

| Severidade | Descrição |
| :--- | :--- |
| 🔴 **Critical** | Alta complexidade + Alto churn. Requer refatoração imediata. |
| 🟠 **High** | Código instável ou muito complexo. Risco de bugs elevado. |
| 🟡 **Medium** | Atenção necessária. Pode se tornar um problema em breve. |
| ⚪ **Low** | Código estável e de baixa complexidade. |

## 📁 Estrutura do Projeto

- `src/codehealth/analyzers`: Lógica de análise de complexidade e dependências.
- `src/codehealth/collectors`: Extratores de dados do Git e carregamento de fontes.
- `src/codehealth/report`: Geração de relatórios estruturados.
- `src/codehealth/cli.py`: Ponto de entrada da aplicação.

---
Desenvolvido por **Allan Silva 29**.
