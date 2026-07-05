import random

notas = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def gerar_progressao_completa(tonica):
    tonica = tonica.upper()
    if tonica not in notas:
        return "Nota inválida. Use o formato padrão (ex: C, D#, F)."

    index = notas.index(tonica)
    
    grau_I = notas[index]
    grau_IV = notas[(index + 5) % 12]
    grau_V = notas[(index + 7) % 12]
    grau_vi = notas[(index + 9) % 12] + "m"
    
    # Estruturas de progressões famosas
    progressoes = [
        f"{grau_I} - {grau_IV} - {grau_V}",           # I-IV-V (Rock/Blues básico)
        f"{grau_I} - {grau_V} - {grau_vi} - {grau_IV}",    # I-V-vi-IV (Pop clássico)
        f"{grau_I} - {grau_vi} - {grau_IV} - {grau_V}",    # I-vi-IV-V (Anos 50/Doo-wop)
        f"{grau_vi} - {grau_IV} - {grau_I} - {grau_V}"     # vi-IV-I-V (Pop moderno/Épico)
    ]
    
    return random.choice(progressoes)

if __name__ == "__main__":
    print("--- Gerador de Progressões Harmônicas ---")
    entrada = input("Digite a nota tônica (ex: C, G, A#): ")
    
    resultado = gerar_progressao_completa(entrada)
    print(f"\nSua progressão sorteada na tônica de {entrada.upper()}:")
    print(f"-> {resultado}")