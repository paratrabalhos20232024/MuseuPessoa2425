import sys
import os
import pandas as pd

if len(sys.argv) != 2:
    print("Uso: python entidades_tabela.py <ficheiro-ent.txt>")
    sys.exit(1)

entrada = sys.argv[1]
basename = os.path.splitext(entrada)[0]
saida_csv = f"{basename}-entidades.csv"

dados = []

with open(entrada, "r", encoding="utf-8") as f:
    for linha in f:
        partes = linha.strip().split(maxsplit=1)
        if len(partes) == 2:
            freq = int(partes[0])
            entidade = partes[1]
            dados.append({"Entidade": entidade, "Frequência": freq})

df = pd.DataFrame(dados)
df.to_csv(saida_csv, index=False, encoding="utf-8")
print(f"✅ Tabela guardada em: {saida_csv}")
