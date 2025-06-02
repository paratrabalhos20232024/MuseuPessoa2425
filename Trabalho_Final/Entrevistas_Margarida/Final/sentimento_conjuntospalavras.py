# sentimento_conjuntospalavras_melhorado.py
from transformers import pipeline
import sys
import re

classifier = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
WINDOW_SIZE = 10

def extrair_falas_entrevistado(texto):
    padrao = re.compile(r'(?i)^.*entrevistado\s*:?\s*(.*)', re.MULTILINE)
    return padrao.findall(texto)

def analisar_sentimentos(entrada, saida):
    try:
        with open(entrada, "r", encoding="utf-8") as f:
            texto = f.read()

        falas = extrair_falas_entrevistado(texto)
        if not falas:
            print(f"⚠️ Nenhuma fala de 'entrevistado' encontrada no arquivo {entrada}.")
            return

        with open(saida, "w", encoding="utf-8") as out:
            for idx, fala in enumerate(falas, 1):
                fala = fala.strip()
                if not fala:
                    continue

                out.write(f"\n===== Resposta {idx} =====\n")
                palavras = fala.split()
                scores = []

                for j in range(0, len(palavras), WINDOW_SIZE):
                    trecho = ' '.join(palavras[j:j+WINDOW_SIZE])
                    if not trecho.strip():
                        continue
                    try:
                        resultado = classifier(trecho[:512])[0]
                        label = resultado['label'].lower()
                        estrelas = int(re.search(r"\d", label).group())
                        tipo = (
                            "Muito negativa" if estrelas <= 2 else
                            "Neutra" if estrelas == 3 else
                            "Positiva"
                        )
                        scores.append(estrelas)
                        out.write(f"Bloco {j//WINDOW_SIZE + 1} ({tipo}, estrelas={estrelas}): {trecho}\n")
                    except Exception as e:
                        out.write(f"⚠️ Erro ao classificar bloco {j//WINDOW_SIZE + 1}: {e}\n")

                media = sum(scores) / len(scores) if scores else 0
                out.write(f"\nClassificação média da resposta: {media:.2f} estrelas\n")

        print(f"✅ Análise concluída. Resultado salvo em: {saida}")

    except Exception as e:
        print(f"❌ Erro ao processar os arquivos: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: py sentimento_conjuntospalavras_melhorado.py <entrada.md> <saida.txt>")
        sys.exit(1)

    entrada = sys.argv[1]
    saída = sys.argv[2]
    analisar_sentimentos(entrada, saída)
