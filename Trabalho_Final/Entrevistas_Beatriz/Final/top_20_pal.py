from collections import Counter
import re
import string
import matplotlib.pyplot as plt

# Função para remover stopwords
def remove_stopwords(text, stopwords):
    return [word for word in text.split() if word.lower() not in stopwords]

# Função para tratar e contar palavras frequentes
def count_frequent_words(filename, stopwords):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read().lower()  # Converte para minúsculas para padronizar
        text = re.sub(f"[{string.punctuation}]", "", text)  # Remove pontuação
    
    # Remove stopwords do texto
    cleaned_text = remove_stopwords(text, stopwords)
    
    # Conta a frequência das palavras
    word_counts = Counter(cleaned_text)
    
    return word_counts

# Função para exibir as 20 palavras mais frequentes
def display_top_words(word_counts, n=20):
    print(f"Top {n} palavras mais frequentes:")
    for i, (word, count) in enumerate(word_counts.most_common(n), start=1):
        print(f"{i}. {word} - {count}")

# Função para gerar o gráfico de barras
def gerar_grafico_barras(word_counts, n=20):
    palavras = [word for word, _ in word_counts.most_common(n)]
    frequencias = [count for _, count in word_counts.most_common(n)]

    # Criar o gráfico
    plt.figure(figsize=(10, 6))
    plt.barh(palavras, frequencias, color='skyblue')
    plt.xlabel('Frequência Absoluta')
    plt.ylabel('Palavras')
    plt.title(f'Top {n} Palavras Mais Frequentes - Frequência Absoluta')
    plt.gca().invert_yaxis()  # Inverter a ordem para as mais frequentes ficarem no topo
    plt.show()

# Stopwords em português
stopwords = set([
    'a', 'o', 'e', 'é', 'de', 'em', 'para', 'que', 'com', 'não', 'os', 'as', 'uma', 'um', 'no', 'na', 
    'eu', 'tu', 'ele', 'ela', 'nos', 'nosso', 'minha', 'meu', 'se', 'por', 'mais', 'mas', 'ou', 
    'como', 'isso', 'à', 'nas', 'foi', 'também', 'tinha'
])

def main():
    # Defina o nome dos arquivos de entrada
    B1_file = 'Entrevista_B1.txt'
    B2_file = 'Entrevista_B2.txt'

    # Contar as palavras frequentes para B1
    print("Palavras frequentes B1:")
    B1_counts = count_frequent_words(B1_file, stopwords)
    display_top_words(B1_counts)
    gerar_grafico_barras(B1_counts)

    # Contar as palavras frequentes para B2
    print("\nPalavras frequentes João:")
    B2_counts = count_frequent_words(B2_file, stopwords)
    display_top_words(B2_counts)
    gerar_grafico_barras(B2_counts)

# Executando o script
if __name__ == "__main__":
    main()

