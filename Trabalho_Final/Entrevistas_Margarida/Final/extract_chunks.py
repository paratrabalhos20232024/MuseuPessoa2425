#!/usr/bin/env python3

import spacy
import sys
from collections import Counter

def clean_chunk(chunk):
    # Remove tokens de pontuação no início e fim
    tokens = [token for token in chunk if not token.is_punct]
    return tokens

def main():
    if len(sys.argv) < 2:
        print("Uso: python extract_chunks.py entrada.txt [--count] [saida.txt]")
        sys.exit(1)

    infile = sys.argv[1]
    count_mode = "--count" in sys.argv
    outfile = None
    for arg in sys.argv[2:]:
        if arg != "--count":
            outfile = arg

    nlp = spacy.load("pt_core_news_lg")

    with open(infile, encoding="utf8") as f:
        text = f.read()

    doc = nlp(text)

    chunks = []
    for chunk in doc.noun_chunks:
        clean_tokens = clean_chunk(chunk)
        # Ignora se vazio depois de limpar pontuação
        if not clean_tokens:
            continue
        # Ignora se todos os tokens são stopwords
        if all(token.is_stop for token in clean_tokens):
            continue
        # Ignora se só tem uma palavra que é stopword
        if len(clean_tokens) == 1 and clean_tokens[0].is_stop:
            continue
        clean_text = " ".join(token.text for token in clean_tokens)
        chunks.append(clean_text)

    output_lines = []
    if count_mode:
        counter = Counter(chunks)
        for chunk, freq in counter.most_common():
            output_lines.append(f"{freq}\t{chunk}")
    else:
        output_lines = chunks

    if outfile:
        with open(outfile, "w", encoding="utf8") as f:
            f.write("\n".join(output_lines))
        print(f"Resultado guardado em {outfile}")
    else:
        print("\n".join(output_lines))

if __name__ == "__main__":
    main()