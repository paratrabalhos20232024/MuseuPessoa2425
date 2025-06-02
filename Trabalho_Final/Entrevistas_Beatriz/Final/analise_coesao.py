import sys
from collections import Counter
import re

# Conectores discursivos comuns no português europeu, organizados por tipo
conectores = {
    'aditivos': [
        'e', 'também', 'ainda', 'além disso', 'bem como', 'inclusive'
    ],
    'adversativos': [
        'mas', 'porém', 'todavia', 'contudo', 'não obstante', 'no entanto', 'apesar disso'
    ],
    'conclusivos': [
        'portanto', 'logo', 'assim', 'por conseguinte', 'em conclusão', 'dessa forma'
    ],
    'explicativos': [
        'porque', 'pois', 'isto é', 'ou seja', 'nomeadamente', 'a saber'
    ],
    'temporais': [
        'depois', 'antes', 'quando', 'enquanto', 'assim que', 'logo que', 'desde que'
    ],
    'condicionais': [
        'se', 'caso', 'desde que', 'a menos que', 'contanto que'
    ],
    'concessivos': [
        'embora', 'ainda que', 'mesmo que', 'apesar de', 'por mais que'
    ],
    'causais': [
        'porque', 'como', 'visto que', 'já que', 'dado que'
    ]
}

def detectar_conectores(texto):
    contagem = Counter()
    texto = texto.lower()
    for tipo, lista in conectores.items():
        for c in lista:
            # Usa regex para encontrar conectores inteiros, mesmo os compostos
            padrao = r'\b' + re.escape(c) + r'\b'
            contagem[tipo] += len(re.findall(padrao, texto))
    return contagem

def main():
    with open(sys.argv[1], encoding='utf-8') as f:
        texto = f.read()
    contagem = detectar_conectores(texto)
    for tipo, count in contagem.items():
        print(f'{tipo}: {count}')

if __name__ == '__main__':
    main()

