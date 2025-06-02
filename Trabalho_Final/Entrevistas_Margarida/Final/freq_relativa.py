import sys
import re
from collections import Counter

def carregar_stopwords(caminho_stopwords):
    try:
        with open(caminho_stopwords, encoding='utf-8') as f:
            return set(p.strip().lower() for p in f if p.strip())
    except FileNotFoundError:
        return set()

def calcular_freq_relativa(arquivo_txt, stopwords=set(), arquivo_saida=None):
    with open(arquivo_txt, encoding='utf-8') as f:
        texto = f.read().lower()
        palavras = re.findall(r'\w+', texto)
        palavras = [p for p in palavras if p not in stopwords]

    total = len(palavras)
    if total == 0:
        print(f"Nenhuma palavra válida encontrada em {arquivo_txt}")
        return

    contagem = Counter(palavras)
    top_20 = contagem.most_common(20)  # Limitar às top 20 palavras

    output_lines = [f"{palavra}\t{freq}\t{(freq/total):.4f}" for palavra, freq in top_20]

    if arquivo_saida:
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write("\n".join(output_lines))
        print(f"✅ Frequências relativas salvas em {arquivo_saida}")
    else:
        print("\n".join(output_lines))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python freq_relativa.py arquivo.txt [stopwords.txt] [saida.txt]")
        sys.exit(1)

    arquivo_txt = sys.argv[1]
    stopwords = carregar_stopwords(sys.argv[2]) if len(sys.argv) > 2 else set()
    arquivo_saida = sys.argv[3] if len(sys.argv) > 3 else None
    calcular_freq_relativa(arquivo_txt, stopwords, arquivo_saida)