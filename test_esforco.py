import time
import numpy as np
import pandas as pd

def motor_avaliacao_sintetico(historico: list, candidata: str, anomalia_smap: float) -> dict:
    """Simulação do motor de rotação biológica para testes de carga."""
    cultura_anterior = historico[-1] if historico else None
    alerta_hidrico = bool(anomalia_smap < -1.5)
    score = 85.0
    if cultura_anterior == candidata:
        score -= 30.0  # Penalidade severa por monocultura consecutivo
    if alerta_hidrico:
        score -= 15.0  # Penalidade por estresse hídrico simulado (SMAP)
    return {
        "cultura_candidata": candidata,
        "score_recomendacao": max(0.0, score),
        "alerta_hidrico": alerta_hidrico
    }

def executar_testes_esforco():
    print("=" * 60)
    print("🚀 INICIANDO TESTES DE ESFORÇO - TERRATURN")
    print("=" * 60)

    rng = np.random.default_rng(42)
    culturas = ["soja", "milho", "sorgo", "brachiaria", "algodao"]

    # ----------------------------------------------------
    # TESTE 1: Carga Computacional do Motor Biológico (CPU)
    # ----------------------------------------------------
    n_iteracoes = 100_000
    print(f"\n[1/2] Executando teste de CPU: {n_iteracoes:,} avaliações de rotação...")
    
    inicio_cpu = time.time()
    for _ in range(n_iteracoes):
        hist = [rng.choice(culturas), rng.choice(culturas)]
        cand = rng.choice(culturas)
        smap = rng.uniform(-3.0, 1.0)
        motor_avaliacao_sintetico(hist, cand, smap)
    fim_cpu = time.time()

    tempo_cpu = fim_cpu - inicio_cpu
    ops_seg = n_iteracoes / tempo_cpu
    latencia_media_ms = (tempo_cpu / n_iteracoes) * 1000

    print(f"   ✔ Concluído em: {tempo_cpu:.4f} segundos")
    print(f"   📊 Throughput: {ops_seg:,.2f} operações/segundo")
    print(f"   ⚡ Latência Média: {latencia_media_ms:.4f} ms por avaliação")

    # ----------------------------------------------------
    # TESTE 2: Carga de Dados e Agregação (Pipeline / ML)
    # ----------------------------------------------------
    n_unidades = 50_000
    n_anos = 8
    total_linhas = n_unidades * n_anos
    print(f"\n[2/2] Executando teste de Dados: Processando DataFrame com {total_linhas:,} linhas ({n_unidades:,} unidades x {n_anos} anos)...")

    inicio_df = time.time()
    dados_simulados = {
        "unidade_id": [f"talhao_{i}" for i in range(n_unidades) for _ in range(n_anos)],
        "ano": [2018 + j for i in range(n_unidades) for j in range(n_anos)],
        "cultura": rng.choice(culturas, size=total_linhas),
        "lavoura_temporaria": rng.choice([True, False], size=total_linhas, p=[0.8, 0.2])
    }
    df_stress = pd.DataFrame(dados_simulados)

    # Agrupamentos pesados simulando o cálculo de features de rotação
    resumo = df_stress.groupby("unidade_id").agg(
        n_anos=("ano", "count"),
        anos_lavoura=("lavoura_temporaria", "sum"),
        cultura_mais_comum=("cultura", lambda s: s.mode()[0] if not s.empty else "desconhecido"),
        n_culturas_distintas=("cultura", "nunique")
    )
    fim_df = time.time()

    tempo_df = fim_df - inicio_df
    print(f"   ✔ Concluído em: {tempo_df:.4f} segundos")
    print(f"   📦 Unidades analisadas com sucesso: {len(resumo):,}")
    print(f"   📈 Taxa de processamento: {total_linhas / tempo_df:,.2f} linhas/segundo")

    print("\n" + "=" * 60)
    print("✅ TESTES DE ESFORÇO FINALIZADOS COM SUCESSO!")
    print("=" * 60)

if __name__ == "__main__":
    executar_testes_esforco()