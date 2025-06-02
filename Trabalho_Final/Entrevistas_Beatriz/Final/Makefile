t1: Entrevista.conll Entrevista-ent.txt Entrevista-keywords.txt

Entrevista.conll : Entrevista_B1.txt Entrevista_B2.txt
	avdconll Entrevista_B1.txt > Entrevista_B1.conll
	avdconll Entrevista_B2.txt > Entrevista_B2.conll	

Entrevista-ent.txt: 
	rg PROPN Entrevista_B1.conll | sort | uniq -c | sort -n > Entrevista_B1-ent.txt
	rg PROPN Entrevista_B2.conll | sort | uniq -c | sort -n > Entrevista_B2-ent.txt


#entidades mas sem as repetições
Entrevista_B1-ent-agr.txt: Entrevista_B1-ent.txt
	awk '{print $$2, $$4}' Entrevista_B1-ent.txt | sort | uniq -c | sort -nr > Entrevista_B1-ent-agr.txt
	awk '{print $$2, $$4}' Entrevista_B2-ent.txt | sort | uniq -c | sort -nr > Entrevista_B2-ent-agr.txt

Entrevista-keywords.txt: 
	keyterms Entrevista_B1.txt > Entrevista_B1-keywords.txt
	keyterms Entrevista_B2.txt > Entrevista_B2-keywords.txt

t2: Entrevista-chunks.txt Entrevista-nomes-absoluta.txt

Entrevista-chunks.txt: 
	py extract_chunks.py Entrevista_B1.txt --count > Entrevista_B1-chunks.txt
	py extract_chunks.py Entrevista_B2.txt --count > Entrevista_B2-chunks.txt


Entrevista-nomes-absoluta.txt: 
	py freq_absoluta.py Entrevista_B1.conll Entrevista_B2.conll > Entrevista_freq.txt

Palavras_linhas: 
	py Num_linha_pal.py Entrevista_B1-ent.txt Entrevista_B2-ent.txt > Entrevista_linhas_pal.txt

palavras_frequentes.txt: 
	python top_20_pal.py Entrevista_B1.txt Entrevista_B2.txt > palavras_frequentes.txt


t3: analise_sentimento sentimento_pal tabela sentimento_pal grafico novo_grafico 

analise_sentimento:
	py sentimento.py Entrevista_B1.md sentimento_B1.txt
	py sentimento.py Entrevista_B2.md  sentimento_B2.txt

# Sentimento Palavras para a analise ser mais específica
sentimento_pal:
	py sentimento_pal.py Entrevista_B1.md sentimento_pal_B1.txt
	py sentimento_pal.py Entrevista_B2.md  sentimento_pal_B2.txt

tabela:
	py tabela.py Entrevista_B1.md tabela_B1.txt
	py tabela.py Entrevista_B2.md tabela_B2.txt

grafico:
	py grafico.py tabela_B1.txt grafico_barras_B1.png grafico_linhas_B1.png
	py grafico.py tabela_B2.txt grafico_barras_B2.png grafico_linhas_B2.png

#foi necessário fazer outro grafico porque no anterior não se conseguia ler porque
#nos trechos onde havia agradecimentos ou despedidas, o número de palavras era muito baixo
# e por isso a analise era sempre super positiva e não se via bem os outros trechos por 
#estes serem mais baixos e terem mais palavras
novo_grafico:
	py graf.py tabela_B1.txt graf_B1.png  
	py graf.py tabela_B2.txt graf_B2.png


t4: racio coesao interjeicoes tempos
#racio-- word	occu	freq-per-mill	usual	rank	racio
racio:
	txtfreq -r Entrevista_B1.txt > Entrevista_B1_racio.csv
	gsort -k6n Entrevista_B1_racio.csv > B1_racio.csv

	txtfreq -r Entrevista_B2.txt > Entrevista_B2_racio.csv
	gsort -k6n Entrevista_B2_racio.csv > B2_racio.csv

coesao:
	py analise_coesao.py Entrevista_B1.txt > coesao_B1.txt
	py analise_coesao.py Entrevista_B2.txt > coesao_B2.txt


interjeicoes:
	py interjeicoes.py Entrevista_B1.txt > interjeicoes_B1.txt
	py interjeicoes.py Entrevista_B2.txt > interjeicoes_B2.txt


tempos:
	python tempos_txt.py Entrevista_B1.txt > tempos_B1.txt
	python tempos_txt.py Entrevista_B2.txt > tempos_B2.txt
