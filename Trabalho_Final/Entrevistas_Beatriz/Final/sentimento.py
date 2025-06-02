import sys
import re
from transformers import pipeline

# Pipeline de análise de sentimento
classifier = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Ler argumentos de entrada e saída
entrada = sys.argv[1]
saida = sys.argv[2]

# Ler o arquivo de entrada
with open(entrada, "r", encoding="utf-8") as f:
    text = f.read()

# Regex robusto para capturar mesmo com quebras de linha e espaços
interviewee_texts = re.findall(r"<interviewee>([\s\S]*?)</interviewee>", text, re.IGNORECASE)

# Limpeza básica e separação
paragraphs = [re.sub(r'\s+', ' ', p.strip()) for p in interviewee_texts if p.strip()]

with open(saida, "w", encoding="utf-8") as out:
    for i, p in enumerate(paragraphs, 1):
        out.write(f"\n===== Trecho {i} =====\n")
        sentences = [s.strip() for s in re.split(r'[.!?]', p) if s.strip()]
        scores = []

        for j, sentence in enumerate(sentences, 1):
            result = classifier(sentence[:512])[0]
            label = result['label']
            stars = int(label[0])
            tipo = (
                "Muito negativa" if stars <= 2 else
                "Neutra" if stars == 3 else
                "Positiva"
            )
            scores.append(stars)
            out.write(f"Frase {j} ({tipo}, estrelas={stars}): {sentence}\n")

        media = sum(scores) / len(scores) if scores else 0
        out.write(f"\nClassificação média do trecho: {media:.2f} estrelas\n")

print(f"✅ Ficheiro '{saida}' criado com sucesso.")


