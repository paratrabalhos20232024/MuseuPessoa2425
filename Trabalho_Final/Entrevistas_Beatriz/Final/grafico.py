import sys
import pandas as pd
import matplotlib.pyplot as plt

# Argumentos: entrada CSV, saída barras, saída linhas
entrada_csv = sys.argv[1]
saida_barras = sys.argv[2]
saida_linhas = sys.argv[3]

# Lê os dados diretamente da tabela já calculada
df = pd.read_csv(entrada_csv)

# Gráfico de barras: Polaridade Normalizada (já calculada)
df.set_index("Trecho")["Dif/Palavras"].plot(
    kind="bar", figsize=(10, 6), color="purple"
)
plt.xlabel("Trecho")
plt.ylabel("Polaridade Normalizada")
plt.title("((Positivos - Negativos) / Número de Palavras) por Trecho")
plt.axhline(0, color='black', linestyle='--')
plt.tight_layout()
plt.savefig(saida_barras)
plt.close()

# Gráfico de linhas: evolução dos sentimentos
df.plot(
    x="Trecho",
    y=["Positivos", "Negativos"],
    kind="line",
    marker='o',
    figsize=(10, 6),
    color=["green", "red"]
)
plt.xlabel("Trecho")
plt.ylabel("Número de Blocos")
plt.title("Evolução de Sentimentos por Trecho")
plt.legend(loc="upper right")
plt.tight_layout()
plt.savefig(saida_linhas)
plt.close()

