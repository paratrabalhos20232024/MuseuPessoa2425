import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Verifica os argumentos
if len(sys.argv) != 4:
    print("Uso: python sentimento_area_negativos_abaixo.py <arquivo_csv_a1> <arquivo_csv_b2> <diretorio_saida>")
    sys.exit(1)

# Recebe os arquivos de entrada e o diretório de saída
entrada_csv_a1 = sys.argv[1]
entrada_csv_b2 = sys.argv[2]
diretorio_saida = sys.argv[3]

# Cria o diretório de saída, se não existir
try:
    os.makedirs(diretorio_saida, exist_ok=True)
except Exception as e:
    print(f"Erro ao criar diretório de saída {diretorio_saida}: {e}")
    sys.exit(1)

# Carrega os dados dos arquivos CSV
try:
    df_a1 = pd.read_csv(entrada_csv_a1)
    df_b2 = pd.read_csv(entrada_csv_b2)
except FileNotFoundError as e:
    print(f"Erro: Arquivo não encontrado: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Erro ao carregar os arquivos CSV: {e}")
    sys.exit(1)

# Verifica se os DataFrames contêm as colunas necessárias
required_columns = ["Blocos", "Positivos", "Negativos"]
for df, name in [(df_a1, entrada_csv_a1), (df_b2, entrada_csv_b2)]:
    if not all(col in df.columns for col in required_columns):
        print(f"⚠️ O arquivo {name} não contém as colunas necessárias (Blocos, Positivos, Negativos).")
        sys.exit(1)

# Função para gerar gráfico de área com negativos abaixo de zero
def gerar_grafico(df, nome_arquivo):
    # Configurações do gráfico
    plt.figure(figsize=(14, 8), dpi=100)
    
    # Dados para o gráfico
    blocos = df["Blocos"]
    positivos = df["Positivos"]
    negativos = df["Negativos"]
    
    # Normaliza os sentimentos por palavra (assumindo WINDOW_SIZE=10 palavras por chunk)
    WINDOW_SIZE = 10
    positivos_por_palavra = positivos / WINDOW_SIZE
    negativos_por_palavra = -negativos / WINDOW_SIZE  # Negativos abaixo de zero
    
    # Cria gráfico de área
    plt.fill_between(
        blocos,
        positivos_por_palavra,
        label="Positivos (por palavra)",
        color="#2ecc71",
        alpha=0.8
    )
    plt.fill_between(
        blocos,
        negativos_por_palavra,
        label="Negativos (por palavra)",
        color="#e74c3c",
        alpha=0.8
    )
    
    # Adiciona linha em y=0 para referência
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    # Adiciona anotações nos pontos de pico (maior valor absoluto)
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
    
    # Configurações dos eixos e título
    plt.xlabel("Bloco do Entrevistado", fontsize=12, labelpad=10)
    plt.ylabel("Sentimentos por Palavra", fontsize=12, labelpad=10)
    plt.title(f"Análise de Sentimento por Palavra: {nome_arquivo}", fontsize=14, pad=15)
    
    # Personaliza a legenda
    plt.legend(fontsize=10, loc='upper right', frameon=True, shadow=True)
    
    # Configura os rótulos do eixo x
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    
    # Adiciona grade leve no eixo y
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Ajusta o layout
    plt.tight_layout()
    
    # Salva o gráfico
    output_path = os.path.join(diretorio_saida, f"{nome_arquivo}-grafico.png")
    try:
        plt.savefig(output_path, bbox_inches='tight', dpi=150)
        plt.close()
        print(f"✅ Gráfico guardado em: {output_path}")
    except Exception as e:
        print(f"Erro ao salvar o gráfico {output_path}: {e}")
        plt.close()
        sys.exit(1)

# Gera gráficos para os arquivos a1 e b2
gerar_grafico(df_a1, "a1")
gerar_grafico(df_b2, "b2")