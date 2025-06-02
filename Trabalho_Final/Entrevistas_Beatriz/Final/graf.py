import sys
import pandas as pd
import matplotlib.pyplot as plt
import os

# Argumentos: entrada CSV, saída barras
entrada_csv = sys.argv[1]
saida_barras = sys.argv[2]

# Lê os dados diretamente da tabela já calculada
df = pd.read_csv(entrada_csv)

# Remove o primeiro trecho
df = df.iloc[1:]

# Ajustes específicos conforme o nome da tabela
nome_arquivo = os.path.basename(entrada_csv).lower()

if "b2" in nome_arquivo:
    df = df[~df["Trecho"].isin([14, 15])]
elif "b1" in nome_arquivo:
    df = df[~df["Trecho"].isin([18])]

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

