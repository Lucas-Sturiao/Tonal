import mido
from mido import Message, MidiFile, MidiTrack
import random

MIDI_BASE = {
    'C': 60, 'C#': 61, 'D': 62, 'D#': 63, 'E': 64, 'F': 65, 
    'F#': 66, 'G': 67, 'G#': 68, 'A': 69, 'A#': 70, 'B': 71
}

def obter_notas_midi(acorde_str):
    """Converte um acorde em formato de texto para uma lista de notas MIDI."""
    partes = acorde_str.split('/')
    acorde_base = partes[0]
    baixo = partes[1] if len(partes) > 1 else None

    raiz, sufixo = extrair_raiz_e_sufixo(acorde_base)
    nota_raiz = MIDI_BASE[raiz]

    # Mapeia os intervalos a partir da tônica com base no sufixo
    if sufixo == '':        intervalos = [0, 4, 7]         # Tríade Maior
    elif sufixo == 'm':     intervalos = [0, 3, 7]         # Tríade Menor
    elif sufixo == 'dim':   intervalos = [0, 3, 6]         # Tríade Diminuta
    elif sufixo == 'maj7':  intervalos = [0, 4, 7, 11]     # Tétrade Maior 7M
    elif sufixo == 'm7':    intervalos = [0, 3, 7, 10]     # Tétrade Menor 7m
    elif sufixo == '7':     intervalos = [0, 4, 7, 10]     # Tétrade Dominante
    elif sufixo == 'm7b5':  intervalos = [0, 3, 6, 10]     # Tétrade Meio Diminuta
    else:                   intervalos = [0, 4, 7]

    notas = [nota_raiz + i for i in intervalos]

    # Adiciona o baixo uma oitava abaixo (-12 semitons)
    if baixo:
        notas.insert(0, MIDI_BASE[baixo] - 12)
    else:
        # Sem inversão, duplica a tônica nos graves para dar peso
        notas.insert(0, nota_raiz - 12)

    return notas

def exportar_para_midi(progressao_str, nome_arquivo="progressao.mid"):
    """Gera um arquivo MIDI a partir da string de progressão."""
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    
    # Duração de cada acorde (4 batidas = 1 compasso inteiro)
    ticks_por_acorde = mid.ticks_per_beat * 4 
    acordes = [a.strip() for a in progressao_str.split('-')]

    for acorde in acordes:
        notas_midi = obter_notas_midi(acorde)
        
        # Liga todas as notas do acorde simultaneamente (time=0)
        for nota in notas_midi:
            track.append(Message('note_on', note=nota, velocity=80, time=0))
        
        # Desliga as notas. O primeiro 'note_off' define o tempo de duração do acorde.
        for i, nota in enumerate(notas_midi):
            delta_time = ticks_por_acorde if i == 0 else 0
            track.append(Message('note_off', note=nota, velocity=80, time=delta_time))

    mid.save(nome_arquivo)
    return nome_arquivo

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
        exportar = input("Exportar para MIDI? (s/n): ").strip().lower() == 's'
        
        try:
            graus_calculados = obter_graus(entrada, escala, tetrades)
            resultado = gerar_progressao(graus_calculados, escala, usar_inversoes)
            
            print(f"\nSua progressão na tônica de {entrada.upper()} {escala.capitalize()}:")
            print(f"-> {resultado}")
            
            if exportar:
                nome_arq = f"progressao_{entrada.upper()}_{escala}.mid"
                exportar_para_midi(resultado, nome_arq)
                print(f"✅ Arquivo MIDI salvo como: {nome_arq}")
                
        except ValueError as e:
            print(f"Erro: {e}")