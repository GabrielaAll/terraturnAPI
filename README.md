# 🌱 TerraTurn - Motor de Rotação Agronômica e API

O **TerraTurn** é uma plataforma e motor de decisão agronômica voltado para a análise, harmonização e recomendação de rotação de culturas agrícolas. O sistema integra dados de múltiplas fontes geoespaciais e estatísticas de uso do solo (como USDA CDL, MapBiomas e EuroCrops HCAT4) para gerar métricas avançadas de diversidade agrícola, índices de sustentabilidade e previsões para planejamento de safras.

---

## 🚀 Funcionalidades Principais

* **Harmonização Multi-Fonte:** Padronização de nomenclaturas e códigos agronômicos entre diferentes bases de dados globais e nacionais (USDA Crop Sequence Boundaries, MapBiomas Coleção 10 e EuroCrops v2.0).
* **Motor Biológico de Rotação:** Algoritmo que avalia a viabilidade de culturas candidatas com base no histórico de plantio do talhão, penalidades por monocultura consecutiva e alertas de estresse hídrico (integração conceitual com dados de umidade do solo SMAP).
* **Engenharia de Features para Machine Learning:** Geração automatizada de métricas por unidade/talhão, incluindo índice de diversidade de Shannon, proporção de cereais e leguminosas, contagem de anos de safra dupla e variáveis de defasagem temporal (*lags* para modelos preditivos).
* **API RESTful (FastAPI):** Endpoints seguros para cadastro de usuários (JWT), gerenciamento de propriedades agrícolas e consultas ao motor de rotação.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.13+
* **Framework Web:** FastAPI & Uvicorn
* **Banco de Dados & ORM:** SQLite / PostgreSQL com SQLAlchemy
* **Manipulação e Análise de Dados:** Pandas, NumPy, PyArrow e GeoPandas / Rasterio / Pyogrio
  
---
## 📂 Estrutura do Projeto

```text
terraturn/
├── api/                  # Aplicação FastAPI (Rotas, Models, Schemas, Database)
├── rotacao/              # Matedata, conversores e motores de harmonização (USDA, MapBiomas, EuroCrops)
├── dados/                # Diretório de dados brutos, intermediários e processados (Parquet)
├── pipeline.py           # Orquestração dos pipelines de dados e extrações
├── gerar_json.py         # Exportador da base consolidada em JSON
├── requirements.txt      # Dependências do projeto
└── README.md             # Documentação oficial

