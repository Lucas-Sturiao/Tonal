import random

notas = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def obter_graus_maiores(tonica):
    tonica = tonica.upper()
    if tonica not in notas:
        raise ValueError("Nota inválida. Use o formato padrão (ex: C, D#, F).")

    index = notas.index(tonica)
    
    # Retorna um dicionário com os graus do campo harmônico maior
    return {
        "I": notas[index],
        "IV": notas[(index + 5) % 12],
        "V": notas[(index + 7) % 12],
        "vi": notas[(index + 9) % 12] + "m"
    }

def gerar_progressao(graus):
    progressoes = [
        f"{graus['I']} - {graus['IV']} - {graus['V']}",           # Rock/Blues
        f"{graus['I']} - {graus['V']} - {graus['vi']} - {graus['IV']}",  # Pop clássico
        f"{graus['I']} - {graus['vi']} - {graus['IV']} - {graus['V']}",  # Doo-wop
        f"{graus['vi']} - {graus['IV']} - {graus['I']} - {graus['V']}"   # Pop moderno
    ]
    return random.choice(progressoes)

if __name__ == "__main__":
    print("--- Gerador de Progressões Harmônicas ---")
    print("Digite 'sair' a qualquer momento para encerrar.")
    
    while True:
        entrada = input("\nDigite a nota tônica (ex: C, G, A#): ").strip()
        
        if entrada.lower() == 'sair':
            print("Encerrando o gerador...")
            break
            
        try:
            graus_calculados = obter_graus_maiores(entrada)
            resultado = gerar_progressao(graus_calculados)
            print(f"Sua progressão sorteada na tônica de {entrada.upper()}:")
            print(f"-> {resultado}")
        except ValueError as e:
            print(f"Erro: {e}")