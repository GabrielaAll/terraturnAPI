import json
from rotacao.legenda import LEGENDA, CDL, MAPBIOMAS, REGRAS_HCAT4

def exportar_base_completa():
    # 1. Legenda Comum Completa
    legenda_comum = [
        {
            "cultura": cultura,
            "grupo": grupo,
            "lavoura_temporaria": lavoura_temp
        }
        for cultura, (grupo, lavoura_temp) in LEGENDA.items()
    ]

    # 2. Tabela USDA CDL (Crop Data Layer)
    cdl_tabela = [
        {
            "codigo_cdl": codigo,
            "nome_original": nome,
            "cultura": cultura,
            "cultura_2": cultura_2,
            "estacao": estacao
        }
        for codigo, (nome, cultura, cultura_2, estacao) in CDL.items()
    ]

    # 3. Tabela MapBiomas Coleção 10
    mapbiomas_tabela = [
        {
            "codigo_mapbiomas": codigo,
            "nome_original": nome,
            "cultura": cultura
        }
        for codigo, (nome, cultura) in MAPBIOMAS.items()
    ]

    # 4. Regras HCAT4 (EuroCrops v2.0)
    hcat4_regras = [
        {
            "prefixo_codigo": prefixo,
            "cultura_mapeada": cultura
        }
        for prefixo, cultura in REGRAS_HCAT4
    ]

    # 5. Estrutura Global Consolidada
    base_completa = {
        "projeto": "TerraTurn - Motor de Rotação Agronômica",
        "versao": "3.0.0-completa",
        "descricao": "Base de dados e regras de harmonização agronômica oficial para integração multi-fonte (USDA CSB, EuroCrops v2.0, MapBiomas Coleção 10).",
        "parametros_metricas_ml": {
            "descricao_features": "Métricas calculadas por talhão/pixel na série temporal",
            "indicadores": [
                "Sequência completa de culturas (ex: soja>milho>soja)",
                "Número de culturas distintas e índice de diversidade de Shannon",
                "Proporção de monocultura e proporção de cereais/leguminosas",
                "Contagem de anos de safra dupla e anos de pousio",
                "Dataset de Machine Learning com variáveis de lag (t-1 até t-k) e contagem de monocultura recente"
            ]
        },
        "legenda_comum": legenda_comum,
        "conversoes": {
            "usda_cdl": cdl_tabela,
            "mapbiomas_colecao10": mapbiomas_tabela,
            "eurocrops_hcat4": hcat4_regras
        }
    }

    # Gravação do ficheiro JSON final
    nome_arquivo = "base_consolidada_rotacao.json"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(base_completa, f, ensure_ascii=False, indent=4)
    
    print(f"[sucesso] Base completa gerada em '{nome_arquivo}' com {len(legenda_comum)} culturas, {len(cdl_tabela)} códigos CDL, {len(mapbiomas_tabela)} classes MapBiomas e {len(hcat4_regras)} regras HCAT4.")

if __name__ == "__main__":
    exportar_base_completa()