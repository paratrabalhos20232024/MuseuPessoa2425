# sentimento_paragrafos_melhorado.py
from transformers import pipeline
import sys
import re

classifier = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def extrair_falas_entrevistado(texto):
    padrao = re.compile(r'(?i)^.*entrevistado\s*:?\s*(.*)', re.MULTILINE)
    return padrao.findall(texto)

def analisar_sentimento(entrada, saida):
    try:
        with open(entrada, "r", encoding="utf-8") as f:
            texto = f.read()

        falas = extrair_falas_entrevistado(texto)
        if not falas:
            print(f"⚠️ Nenhuma fala de 'entrevistado' encontrada no arquivo {entrada}.")
            return

        with open(saida, "w", encoding="utf-8") as out:
            for i, fala in enumerate(falas, 1):
                fala = fala.strip()
                if not fala:
                    continue

                out.write(f"\n===== Resposta {i} =====\n")
                try:
                    resultado = classifier(fala[:512])[0]
                    label = resultado['label'].lower()
                    estrelas = int(re.search(r"\d", label).group())
                    tipo = (
                        "Muito negativa" if estrelas <= 2 else
                        "Neutra" if estrelas == 3 else
                        "Positiva"
                    )
                    out.write(f"Parágrafo (tipo: {tipo}, estrelas={estrelas}): {fala}\n")
                except Exception as e:
                    out.write(f"⚠️ Erro ao classificar resposta {i}: {e}\n")

        print(f"✅ Ficheiro de sentimentos criado com sucesso em: {saida}")

    except Exception as e:
        print(f"❌ Erro ao processar os arquivos: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python sentimento_paragrafos_melhorado.py <entrada.md> <saida.txt>")
        sys.exit(1)

    entrada = sys.argv[1]
    saída = sys.argv[2]
    analisar_sentimento(entrada, saída)
