from transformers import pipeline
import sys
import re

# Pipeline de análise de sentimento
classifier = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Ler argumentos de entrada e saída
entrada = sys.argv[1]
saida = sys.argv[2]

# Tamanho da janela de palavras
WINDOW_SIZE = 10

with open(entrada, "r", encoding="utf-8") as f:
    text = f.read()

# Regex robusto para capturar texto entre <interviewee>...</interviewee>, multiline
interviewee_texts = re.findall(r"<interviewee>([\s\S]*?)</interviewee>", text, re.IGNORECASE)

# Limpeza básica e normalização de espaços
paragraphs = [re.sub(r'\s+', ' ', p.strip()) for p in interviewee_texts if p.strip()]

with open(saida, "w", encoding="utf-8") as out:
    for i, p in enumerate(paragraphs, 1):
        out.write(f"\n===== Trecho {i} =====\n")
        words = p.split()
        scores = []

        # Criar janelas de n palavras
        for j in range(0, len(words), WINDOW_SIZE):
            chunk = ' '.join(words[j:j+WINDOW_SIZE])
            if not chunk.strip():
                continue
            result = classifier(chunk[:512])[0]
            label = result['label']
            stars = int(label[0])
            tipo = (
                "Muito negativa" if stars <= 2 else
                "Neutra" if stars == 3 else
                "Positiva"
            )
            scores.append(stars)
            out.write(f"Bloco de palavras {j//WINDOW_SIZE + 1} ({tipo}, estrelas={stars}): {chunk}\n")

        media = sum(scores) / len(scores) if scores else 0
        out.write(f"\nClassificação média do trecho (por blocos): {media:.2f} estrelas\n")

print(f"✅ Ficheiro '{saida}' criado com sucesso com análise por blocos de palavras.")
