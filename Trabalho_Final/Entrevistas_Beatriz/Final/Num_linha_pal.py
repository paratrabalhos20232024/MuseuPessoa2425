def contar_linhas_e_palavras(arquivo):
    num_linhas = 0
    num_palavras = 0

    # Abrir o arquivo e processar linha por linha
    with open(arquivo, 'r', encoding='utf-8') as file:
        for linha in file:
            num_linhas += 1
            num_palavras += len(linha.split())  # Conta palavras separadas por espaços

    return num_linhas, num_palavras

def main():
    # Defina os nomes dos arquivos de entrada
    arquivos = ['Entrevista_B1.txt', 'Entrevista_B2.txt']
    
    # Processa cada arquivo
    for arquivo in arquivos:
        num_linhas, num_palavras = contar_linhas_e_palavras(arquivo)
        print(f"O arquivo '{arquivo}' tem {num_linhas} linhas e {num_palavras} palavras.")

# Executando o script
if __name__ == "__main__":
    main()
