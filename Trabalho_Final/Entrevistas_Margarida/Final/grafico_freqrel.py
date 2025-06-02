import sys
import matplotlib.pyplot as plt
import os

if len(sys.argv) < 2:
    print("Uso: python grafico_freqrel.py <arquivo-freqrel.txt>")
    sys.exit(1)

entrada = sys.argv[1]
palavras = []
valores = []

# Ler o arquivo ignorando erros de codificação
with open(entrada, "r", encoding="utf-8", errors="ignore") as f:
    for linha in f:
        partes = linha.strip().split("\t")  # Usar tabulação como separador
        if len(partes) == 3:  # Espera <palavra>\t<frequência>\t<frequência relativa>
            palavra, _, valor = partes  # Ignorar a coluna de frequência absoluta
            try:
                valor = float(valor.replace(",", "."))  # Suporte a vírgulas
                palavras.append(palavra)
                valores.append(valor)
            except ValueError:
                continue

if not palavras:
    print("⚠️ Nenhum dado válido foi encontrado no arquivo.")
    sys.exit(1)

# Limitar às top 20 palavras
if len(palavras) > 20:
    pares = sorted(zip(valores, palavras), reverse=True)[:20]
    valores, palavras = zip(*pares)
    valores = list(valores)
    palavras = list(palavras)

# Gera gráfico de barras verticais
plt.figure(figsize=(12, 6))
plt.bar(palavras, valores, color="cornflowerblue")
plt.title("Top 20 Frequências Relativas de Palavras (Barras Verticais)")
plt.xlabel("Palavras")
plt.ylabel("Frequência Relativa")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

saida_vertical = entrada.replace(".txt", "-vertical.png")
plt.savefig(saida_vertical)
print(f"✅ Gráfico vertical salvo em: {saida_vertical}")
plt.close()

# Gera gráfico de barras horizontais
plt.figure(figsize=(10, 8))
plt.barh(palavras, valores, color="lightseagreen")
plt.title("Top 20 Frequências Relativas de Palavras (Barras Horizontais)")
plt.xlabel("Frequência Relativa")
plt.ylabel("Palavras")
plt.tight_layout()

saida_horizontal = entrada.replace(".txt", "-horizontal.png")
plt.savefig(saida_horizontal)
print(f"✅ Gráfico horizontal salvo em: {saida_horizontal}")
plt.close()