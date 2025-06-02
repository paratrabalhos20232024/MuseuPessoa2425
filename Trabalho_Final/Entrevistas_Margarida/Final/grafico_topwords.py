import sys
import os
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    print("Uso: python grafico_topwords.py <ficheiro-topwords.txt>")
    sys.exit(1)

entrada = sys.argv[1]
basename = os.path.splitext(entrada)[0]
saida = f"{basename}.png"

palavras = []
frequencias = []

# Ler o arquivo e coletar palavras e frequências
with open(entrada, "r", encoding="utf-8") as f:
    for linha in f:
        partes = linha.strip().split()
        if len(partes) >= 2:
            freq = int(partes[0])
            palavra = ' '.join(partes[1:])
            frequencias.append(freq)
            palavras.append(palavra)

# Selecionar as top 20 palavras (ordenar por frequência, se necessário)
if len(palavras) > 20:
    # Combinar palavras e frequências, ordenar por frequência (decrescente)
    pares = sorted(zip(frequencias, palavras), reverse=True)[:20]
    frequencias, palavras = zip(*pares)
    frequencias = list(frequencias)
    palavras = list(palavras)

# Calcular a soma total das frequências (considerando apenas as top 20)
total_frequencias = sum(frequencias)

# Calcular frequências relativas
frequencias_relativas = [freq / total_frequencias for freq in frequencias]

# Criar gráfico
plt.figure(figsize=(12, 6))
plt.bar(palavras, frequencias_relativas, color="skyblue")
plt.xticks(rotation=45, ha='right')
plt.xlabel("Palavras")
plt.ylabel("Frequência Relativa")
plt.title(f"Top 20 Palavras (Frequência Relativa) - {basename}")
plt.tight_layout()
plt.savefig(saida)
print(f"✅ Gráfico guardado em: {saida}")