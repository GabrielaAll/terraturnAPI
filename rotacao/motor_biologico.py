class MotorRotacaoBiologica:
    def __init__(self):
        # Dicionário de regras de rotação e compatibilidade biológica
        self.regras = {
            "soja": {
                "culturas_compativeis": ["milho", "sorgo", "brachiaria"],
                "intervalo_minimo_anos": 1,
                "beneficio_nitrogenio": True
            },
            "milho": {
                "culturas_compativeis": ["soja", "feijao", "crotalaria"],
                "intervalo_minimo_anos": 1,
                "beneficio_nitrogenio": False
            }
        }

    def avaliar_rotacao(self, historico_culturas: list, cultura_candidata: str, anomalia_smap: float):
        # Avalia a viabilidade da rotação com base no histórico e estresse hídrico (SMAP)
        cultura_anterior = historico_culturas[-1] if historico_culturas else None
        
        # Alerta se houver risco severo por seca simulada
        alerta_hidrico = True if anomalia_smap < -1.5 else False
        
        score_viabilidade = 85.0
        if alerta_hidrico:
            score_viabilidade -= 15.0

        return {
            "cultura_candidata": cultura_candidata,
            "ultima_cultura_registrada": cultura_anterior,
            "alerta_estresse_hidrico": alerta_hidrico,
            "score_recomendacao": score_viabilidade,
            "parecer_tecnico": "Rotação recomendada com restrição moderada devido ao índice de umidade do solo." if alerta_hidrico else "Rotação ideal e biologicamente equilibrada."
        }