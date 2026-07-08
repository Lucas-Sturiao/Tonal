import random

notas = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def obter_graus(tonica, tipo_escala='maior', usar_tetrades=False):
    tonica = tonica.upper()
    if tonica not in notas:
        raise ValueError("Nota inválida. Use o formato padrão (ex: C, D#, F).")

    idx = notas.index(tonica)
    
    # Define intervalos e sufixos baseados na escala e no tipo de acorde
    if tipo_escala == 'maior':
        intervalos = [0, 2, 4, 5, 7, 9, 11]
        sufixos = ['maj7', 'm7', 'm7', 'maj7', '7', 'm7', 'm7b5'] if usar_tetrades else ['', 'm', 'm', '', '', 'm', 'dim']
    else: # menor natural
        intervalos = [0, 2, 3, 5, 7, 8, 10]
        sufixos = ['m7', 'm7b5', 'maj7', 'm7', 'm7', 'maj7', '7'] if usar_tetrades else ['m', 'dim', '', 'm', 'm', '', '']

    # Mapeia os graus numéricos (1 a 7) para facilitar a montagem das progressões
    return {str(i+1): notas[(idx + intervalos[i]) % 12] + sufixos[i] for i in range(7)}


def extrair_raiz_e_sufixo(acorde):
    """Extrai a raiz (ex: 'C' ou 'C#') e o sufixo (ex: 'm', 'maj7') de um nome de acorde."""
    if len(acorde) >= 2 and acorde[1] == '#':
        raiz = acorde[:2]
        sufixo = acorde[2:]
    else:
        raiz = acorde[:1]
        sufixo = acorde[1:]
    return raiz, sufixo


def calcular_baixo(acorde, tipo='terca'):
    """Calcula o baixo na terça (terca) ou quinta (quinta) para um acorde.

    - usa a lista global `notas` e faz índice módulo 12
    - determina se a terça é maior(4) ou menor(3) observando o sufixo do acorde
    """
    if not acorde:
        raise ValueError('Acorde vazio')

    raiz, sufixo = extrair_raiz_e_sufixo(acorde)
    idx = notas.index(raiz)
    sfx = sufixo.lower()

    # determinar intervalo da terça: trate 'dim' como menor, 'm' (quando não 'maj') como menor
    if 'maj' in sfx:
        terceira_intervalo = 4
    elif 'dim' in sfx or ('m' in sfx and 'maj' not in sfx):
        terceira_intervalo = 3
    else:
        # padrão: maior
        terceira_intervalo = 4

    if tipo == 'terca':
        baixo_idx = (idx + terceira_intervalo) % 12
    else:
        baixo_idx = (idx + 7) % 12

    return notas[baixo_idx]

def gerar_progressao(graus, tipo_escala='maior', usar_inversoes=False):
    if tipo_escala == 'maior':
        progressoes = [
            f"{graus['1']} - {graus['4']} - {graus['5']}",                 # I-IV-V
            f"{graus['1']} - {graus['5']} - {graus['6']} - {graus['4']}",  # I-V-vi-IV
            f"{graus['1']} - {graus['6']} - {graus['4']} - {graus['5']}",  # I-vi-IV-V
            f"{graus['2']} - {graus['5']} - {graus['1']}"                  # ii-V-I (Clássico Jazz/Bossa)
        ]
    else:
        progressoes = [
            f"{graus['1']} - {graus['6']} - {graus['3']} - {graus['7']}",  # i-VI-III-VII
            f"{graus['1']} - {graus['4']} - {graus['5']}",                 # i-iv-v
            f"{graus['2']} - {graus['5']} - {graus['1']}",                 # ii°-v-i
            f"{graus['1']} - {graus['6']} - {graus['4']} - {graus['5']}"   # i-VI-iv-v
        ]

    progresso = random.choice(progressoes)

    # Se inversões habilitadas, substitui 1 ou 2 acordes aleatórios por suas inversões (terca/quinta)
    if usar_inversoes:
        acordes = [a.strip() for a in progresso.split(' - ')]
        num_inversions = min(len(acordes), random.choice([1, 2]))
        indices = random.sample(range(len(acordes)), k=num_inversions)
        for i in indices:
            acorde = acordes[i]
            tipo_baixo = random.choice(['terca', 'quinta'])
            baixo = calcular_baixo(acorde, tipo=tipo_baixo)
            acordes[i] = f"{acorde}/{baixo}"
        return ' - '.join(acordes)

    return progresso

if __name__ == "__main__":
    print("--- Gerador de Progressões Harmônicas ---")
    print("Digite 'sair' a qualquer momento para encerrar.")
    
    while True:
        entrada = input("\nDigite a nota tônica (ex: C, G, A#): ").strip()
        if entrada.lower() == 'sair':
            break
            
        escala = input("Escala (maior/menor): ").strip().lower()
        if escala not in ['maior', 'menor']: 
            escala = 'maior'
            
        tetrades = input("Usar tétrades? (s/n): ").strip().lower() == 's'
        usar_inversoes = input("Usar inversões? (s/n): ").strip().lower() == 's'
        
        try:
            graus_calculados = obter_graus(entrada, escala, tetrades)
            resultado = gerar_progressao(graus_calculados, escala, usar_inversoes)
            print(f"\nSua progressão na tônica de {entrada.upper()} {escala.capitalize()}:")
            print(f"-> {resultado}")
        except ValueError as e:
            print(f"Erro: {e}")