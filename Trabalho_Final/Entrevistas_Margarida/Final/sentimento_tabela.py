# sentimento_tabela_melhorado.py
import os
import sys
import re
import pandas as pd
from transformers import pipeline

# Inicializa o pipeline de sentimento
try:
    classifier = pipeline(
        "sentiment-analysis",
        model="nlptown/bert-base-multilingual-uncased-sentiment",
        device=-1
    )
except Exception as e:
    print(f"Erro ao inicializar o pipeline de sentimento: {e}")
    sys.exit(1)

# Argumentos obrigatórios
if len(sys.argv) != 3:
    print("Uso: python sentimento_tabela_melhorado.py <entrada.md> <saida.csv>")
    sys.exit(1)

entrada_md = sys.argv[1]
saida_csv = sys.argv[2]

# Garante que o diretório de saída existe
os.makedirs(os.path.dirname(saida_csv) or '.', exist_ok=True)

# Lê o ficheiro markdown
try:
    with open(entrada_md, "r", encoding="utf-8") as f:
        conteudo = f.read()
except Exception as e:
    print(f"Erro ao ler {entrada_md}: {e}")
    sys.exit(1)

# Extrai falas entre <entrevistado>...</entrevistado>
blocos = re.findall(r"<entrevistado>([\s\S]*?)</entrevistado>", conteudo, re.IGNORECASE)
blocos = [re.sub(r"\s+", " ", b.strip()) for b in blocos if b.strip()]

if not blocos:
    print("❌ Nenhuma fala encontrada entre <entrevistado>...</entrevistado>.")
    sys.exit(1)

WINDOW_SIZE = 10
dados = []

# Analisa cada bloco
for i, bloco in enumerate(blocos, 1):
    palavras = bloco.split()
    positivos = negativos = 0
    estrelas = []

    for j in range(0, len(palavras), WINDOW_SIZE):
        trecho = ' '.join(palavras[j:j+WINDOW_SIZE])
        if not trecho.strip():
            continue
        try:
            resultado = classifier(trecho, truncation=True, max_length=512)[0]
            label = resultado['label'].lower()
            estrelas_valor = int(re.search(r"\d", label).group())
            estrelas.append(estrelas_valor)
            if estrelas_valor <= 2:
                negativos += 1
            elif estrelas_valor >= 4:
                positivos += 1
        except Exception as e:
            print(f"⚠️ Erro no bloco {i}, trecho {j//WINDOW_SIZE + 1}: {e}")
            continue

    if estrelas:
        media = round(sum(estrelas) / len(estrelas), 2)
        dados.append({
            "Bloco": f"Bloco {i}",
            "Nº de Trechos": len(estrelas),
            "Média de Estrelas": media,
            "Positivos": positivos,
            "Negativos": negativos
        })

# Guarda em CSV estruturado
if dados:
    df = pd.DataFrame(dados)
    try:
        df.to_csv(saida_csv, index=False, encoding="utf-8")
        print(f"✅ Análise guardada com sucesso em: {saida_csv}")
    except Exception as e:
        print(f"Erro ao guardar CSV: {e}")
        sys.exit(1)
else:
    print("❌ Nenhum dado válido para guardar.")
    sys.exit(1)
