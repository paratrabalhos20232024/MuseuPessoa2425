# sentimento_linhas_melhorado.py
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

if len(sys.argv) != 4:
    print("Uso: python sentimento_linhas.py <arquivo_csv_a1> <arquivo_csv_a2> <diretorio_saida>")
    sys.exit(1)

entrada_csv_a1 = sys.argv[1]
entrada_csv_a2 = sys.argv[2]
diretorio_saida = sys.argv[3]
os.makedirs(diretorio_saida, exist_ok=True)

def carregar_csv_flexivel(caminho):
    try:
        try:
            df = pd.read_csv(caminho, encoding="ISO-8859-1", sep=",")
            if df.shape[1] < 4:
                raise ValueError("Separador vírgula incorreto")
        except:
            df = pd.read_csv(caminho, encoding="ISO-8859-1", sep=";")

        if df.shape[1] >= 4:
            df = df.iloc[:, :4]
            df.columns = ["Blocos", "Média de Estrelas", "Positivos", "Negativos"]
        else:
            raise Exception("O ficheiro não tem colunas suficientes (mínimo 4).")

        df["Positivos"] = pd.to_numeric(df["Positivos"], errors="coerce").fillna(0)
        df["Negativos"] = pd.to_numeric(df["Negativos"], errors="coerce").fillna(0)

        return df
    except Exception as e:
        print(f"❌ Erro ao carregar {caminho}: {e}")
        sys.exit(1)

def gerar_grafico(df, nome_arquivo):
    plt.figure(figsize=(14, 8), dpi=100)

    blocos = df["Blocos"]
    positivos = df["Positivos"]
    negativos = df["Negativos"]

    WINDOW_SIZE = 10
    positivos_por_palavra = positivos / WINDOW_SIZE
    negativos_por_palavra = -negativos / WINDOW_SIZE

    plt.plot(blocos, positivos_por_palavra, label="Positivos (por palavra)", marker='o', linewidth=2, color="#2ecc71")

    if negativos_por_palavra.abs().sum() > 0:
        plt.plot(blocos, negativos_por_palavra, label="Negativos (por palavra)", marker='s', linewidth=2, color="#e74c3c")
    else:
        plt.plot(blocos, [0]*len(blocos), label="Negativos (0)", linestyle='dotted', linewidth=1.5, color="#e74c3c")

    # Definir limites do eixo Y com margem dinâmica
    min_y = min(negativos_por_palavra.min(), positivos_por_palavra.min())
    max_y = max(negativos_por_palavra.max(), positivos_por_palavra.max())
    margem = (max_y - min_y) * 0.2 if max_y != min_y else 0.5
    plt.ylim(min_y - margem, max_y + margem)

    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

    for i, (pos, neg) in enumerate(zip(positivos_por_palavra, negativos_por_palavra)):
        max_abs = max(pos, -neg, key=abs)
        if abs(max_abs) == max(abs(val) for val in list(positivos_por_palavra) + list(negativos_por_palavra)):
            plt.annotate(
                f"{max_abs:.2f}",
                (i, max_abs),
                textcoords="offset points",
                xytext=(0, 10 if max_abs >= 0 else -15),
                ha='center',
                fontsize=9,
                color="#2ecc71" if max_abs >= 0 else "#e74c3c",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8)
            )

    plt.xlabel("Bloco do Entrevistado", fontsize=12)
    plt.ylabel("Sentimentos por Palavra", fontsize=12)
    plt.title(f"Análise de Sentimento por Palavra: {nome_arquivo}", fontsize=14)
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.legend(fontsize=10, loc='upper right', frameon=True, shadow=True)
    plt.tight_layout()

    output_path_linhas = os.path.join(diretorio_saida, f"{nome_arquivo}-grafico.png")
    plt.savefig(output_path_linhas, bbox_inches='tight', dpi=150)
    plt.close()
    print(f"✅ Gráfico de linhas guardado em: {output_path_linhas}")

    try:
        df["Dif/Palavras"] = (positivos - negativos) / WINDOW_SIZE
        df["Trecho"] = blocos

        cores = df["Dif/Palavras"].apply(lambda x: "purple" if x >= 0 else "crimson")
        saida_barras = os.path.join(diretorio_saida, f"{nome_arquivo}-barras.png")

        ax = df.set_index("Trecho")["Dif/Palavras"].plot(
            kind="bar", figsize=(10, 6), color=cores
        )

        for p in ax.patches:
            valor = p.get_height()
            ax.annotate(f"{valor:.2f}", (p.get_x() + p.get_width() / 2., valor),
                        ha='center', va='bottom' if valor >= 0 else 'top',
                        fontsize=9, color="black", xytext=(0, 5 if valor >= 0 else -8),
                        textcoords='offset points')

        patch_pos = mpatches.Patch(color='purple', label='Polaridade Positiva')
        patch_neg = mpatches.Patch(color='crimson', label='Polaridade Negativa')
        plt.legend(handles=[patch_pos, patch_neg], loc='upper right')

        plt.xlabel("Trecho")
        plt.ylabel("Polaridade Normalizada")
        plt.title("((Positivos - Negativos) / Nº Palavras) por Trecho")
        plt.axhline(0, color='black', linestyle='--')
        plt.tight_layout()
        plt.savefig(saida_barras)
        plt.close()
        print(f"✅ Gráfico de barras guardado em: {saida_barras}")
    except Exception as e:
        print(f"Erro ao gerar gráfico de barras: {e}")
        plt.close()

# Executar
df_a1 = carregar_csv_flexivel(entrada_csv_a1)
df_a2 = carregar_csv_flexivel(entrada_csv_a2)
gerar_grafico(df_a1, "a1")
gerar_grafico(df_a2, "a2")
