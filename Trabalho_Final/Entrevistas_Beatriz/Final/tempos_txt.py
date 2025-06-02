import sys
import spacy
from collections import Counter

# Carregar o modelo do spaCy para português
nlp = spacy.load("pt_core_news_sm")

# Mapas de interpretação simplificada
tempo_map = {
    "PR": "Presente",
    "PS": "Pretérito Perfeito",
    "IM": "Pretérito Imperfeito",
    "F": "Futuro",
    "MQP": "Mais-que-perfeito",
}

modo_map = {
    "IND": "Indicativo",
    "SUBJ": "Subjuntivo",
    "IMP": "Imperativo",
}

def identificar_tempos(doc):
    tempos = Counter()
    for token in doc:
        if token.pos_ == "VERB":
            # Extraímos as features morfológicas, se disponíveis
            morph = token.morph
            tempo = morph.get("Tense")
            modo = morph.get("Mood")
            if tempo:
                tempos[tempo[0]] += 1
            if modo:
                tempos[modo[0]] += 1
    return tempos

def main():
    with open(sys.argv[1], encoding='utf-8') as f:
        texto = f.read()
    doc = nlp(texto)
    contagem = identificar_tempos(doc)

    print("=== Tempos Verbais e Modos Detetados ===")
    for key, count in contagem.items():
        nome = tempo_map.get(key, modo_map.get(key, key))
        print(f"{nome}: {count}")

if __name__ == "__main__":
    main()
