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
        text = file.read().lower()
        text = re.sub(f"[{string.punctuation}]", "", text)
    cleaned_text = remove_stopwords(text, stopwords)
    word_counts = Counter(cleaned_text)
    total = sum(word_counts.values())
    freq_relativa = {word: count / total for word, count in word_counts.items()}
    return word_counts, freq_relativa

# Função para exibir as 20 palavras mais frequentes com frequência relativa
def display_top_words(word_counts, freq_relativa, n=20):
    print(f"Top {n} palavras mais frequentes:")
    for i, (word, count) in enumerate(word_counts.most_common(n), start=1):
        print(f"{i}. {word} - {count} ({freq_relativa[word]:.4f})")

# Função para gerar o gráfico de barras com frequências relativas
def gerar_grafico_barras(freq_relativa, n=20):
    palavras = [word for word, _ in sorted(freq_relativa.items(), key=lambda x: x[1], reverse=True)[:n]]
    frequencias = [freq_relativa[word] for word in palavras]

    # Criar o gráfico
    plt.figure(figsize=(10, 6))
    plt.barh(palavras, frequencias, color='skyblue')
    plt.xlabel('Frequência Relativa')
    plt.ylabel('Palavras')
    plt.title(f'Top {n} Palavras Mais Frequentes - Frequência Relativa')
    plt.gca().invert_yaxis()  # Inverter a ordem para as mais frequentes ficarem no topo
    plt.show()

# Stopwords em português
stopwords = set([
    'a', 'o', 'e', 'é', 'de', 'em', 'para', 'que', 'com', 'não', 'os', 'as', 'uma', 'um', 'no', 'na',
    'eu', 'tu', 'ele', 'ela', 'nos', 'nosso', 'minha', 'meu', 'se', 'por', 'mais', 'mas', 'ou',
    'como', 'isso', 'à', 'nas', 'foi', 'também', 'tinha'
])

def main():
    B1_file = 'Entrevista_B1.txt'
    B2_file = 'Entrevista_B2.txt'

    # Calcular e exibir palavras frequentes para B1
    print("Palavras frequentes B1:")
    B1_counts, B1_freq_rel = count_frequent_words(B1_file, stopwords)
    display_top_words(B1_counts, B1_freq_rel)
    gerar_grafico_barras(B1_freq_rel)

    # Calcular e exibir palavras frequentes para B2
    print("\nPalavras frequentes João:")
    B2_counts, B2_freq_rel = count_frequent_words(B2_file, stopwords)
    display_top_words(B2_counts, B2_freq_rel)
    gerar_grafico_barras(B2_freq_rel)

if __name__ == "__main__":
    main()



