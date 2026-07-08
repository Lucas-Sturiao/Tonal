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

def gerar_progressao(graus, tipo_escala='maior'):
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
    return random.choice(progressoes)

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
        
        try:
            graus_calculados = obter_graus(entrada, escala, tetrades)
            resultado = gerar_progressao(graus_calculados, escala)
            print(f"\nSua progressão na tônica de {entrada.upper()} {escala.capitalize()}:")
            print(f"-> {resultado}")
        except ValueError as e:
            print(f"Erro: {e}")