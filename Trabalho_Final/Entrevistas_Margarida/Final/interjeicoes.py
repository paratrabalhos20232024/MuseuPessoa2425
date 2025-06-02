import sys
from collections import Counter
import re

# Lista de marcadores do português europeu
marcadores = list(set([
    'ah', 'eh', 'hã', 'hum', 'pois', 'ora', 'bem', 'tipo', 'pronto', 'então', 'lá está',
    'pois é', 'enfim', 'olha', 'veja', 'não é', 'vá', 'mas pronto', 'coisa', 'coisas',
    'assim', 'portanto', 'certo', 'claro', 'realmente', 'basicamente', 'literalmente',
    'se calhar', 'quer dizer', 'isto é', 'está bem', 'tá bem', 'é assim', 'prontos',
    'ok', 'digo', 'logo', 'isto', 'pronto pronto', 'tipo assim'
]))

def main():
    if len(sys.argv) != 2:
        print("Uso: python marcadores.py <ficheiro.txt>")
        sys.exit(1)

    with open(sys.argv[1], encoding='utf-8') as f:
        texto = f.read().lower()

    tokens = re.findall(r'\b[\wáéíóúâêôãõç]+\b', texto)
    contagem = Counter(token for token in tokens if token in marcadores)

    if contagem:
        for termo, freq in contagem.items():
            print(f"{termo}: {freq}")
    else:
        print("Nenhum marcador encontrado.")

if __name__ == '__main__':
    main()
