TEXT1 = a1.txt
TEXT2 = a2.txt
STOPWORDS = stopwords.txt

all: t1 t2 t3 t4 t5 t6 t7 t8

$(STOPWORDS):
	# Criação de um arquivo de stopwords, se necessário
	echo -e "a\no\ne\nde\ndo\nda\nem\nque\num\numa\nos\nas\npor\ncom\npara\nna\nno\nse" > $(STOPWORDS)

t1: \
	a1.conll \
	a2.conll

%conll: %.txt
	# Verifique se o comando avdconll está funcionando corretamente
	avdconll $< > $@

t2: \
    a1-ent.txt \
    a2-ent.txt

%-ent.txt: %conll
	grep PROPN $< | sort | uniq -c | sort -nr > $@
t3: \
	a1-entidades.csv \
	a2-entidades.csv

%-entidades.csv: %-ent.txt
	py entidades_tabela.py $< 

t4: \
	a1-keywords.txt \
	a2-keywords.txt

%-keywords.txt: %.txt
	keyterms $< > $@

t5: summary.txt

summary.txt: $(TEXT1) $(TEXT2)
	@echo "Contagem de palavras e linhas para $(TEXT1) e $(TEXT2)" > $@
	@echo "$(TEXT1): Palavras = $$(wc -w < $(TEXT1) | awk '{print $$1}'), Linhas = $$(wc -l < $(TEXT1) | awk '{print $$1}')" >> $@
	@echo "$(TEXT2): Palavras = $$(wc -w < $(TEXT2) | awk '{print $$1}'), Linhas = $$(wc -l < $(TEXT2) | awk '{print $$1}')" >> $@

t6: \
	a1-topwords.txt \
	a2-topwords.txt

%-topwords.txt: %.txt $(STOPWORDS)
	# Contar as 20 palavras mais comuns, sem as stopwords
	LC_ALL=C.UTF-8 grep -o -E '\w+' $< | tr A-Z a-z | grep -v -x -F -f $(STOPWORDS) | sort | uniq -c | sort -nr | head -n 20 > $@

t7: \
	a1-topwords.png \
	a2-topwords.png

%-topwords.png: %-topwords.txt
	py grafico_topwords.py $<

t9: a1-chunks.txt a2-chunks.txt

%-chunks.txt: %.txt $(STOPWORDS)
	py extract_chunks.py $< --count $@


t10: freqrel.txt

freqrel.txt: $(TEXT1) $(TEXT2) $(STOPWORDS)
	@py freq_relativa.py $(TEXT1) $(STOPWORDS) > $@.tmp1
	@py freq_relativa.py $(TEXT2) $(STOPWORDS) > $@.tmp2
	@echo "Frequencias relativas das top 20 palavras ($(TEXT1)):" > $@
	@cat $@.tmp1 >> $@
	@echo "" >> $@
	@echo "Frequencias relativas das top 20 palavras ($(TEXT2)):" >> $@
	@cat $@.tmp2 >> $@
	@rm -f $@.tmp1 $@.tmp2

t11: \
	a1-freqrel.png \
	a2-freqrel.png

%-freqrel.png: %-freqrel.txt
	py grafico_freqrel.py $<



t12: 
	py sentimento_paragrafos.py entrevista_a1.md a1-sentimento.txt
	py sentimento_paragrafos.py entrevista_a2.md a2-sentimento.txt


t13: 
	py sentimento_conjuntospalavras.py entrevista_a1.md a1-sentianalise.txt
	py sentimento_conjuntospalavras.py entrevista_a2.md a2-sentianalise.txt

t14:
	py sentimento_tabela.py entrevista_a1.md a1-sentimento.csv 
	py sentimento_tabela.py entrevista_a2.md a2-sentimento.csv
	
t15:
	py sentimento_linhas.py a1-sentimento.csv a2-sentimento.csv ./grafico

t16:
	txtfreq -r a1.txt > racio-a1.csv
	gsort -k6n racio-a1.csv > A1_racio.csv

	txtfreq -r a2.txt > racio-a2.csv
	gsort -k6n racio-a2.csv > A2_racio.csv

t17:
	py interjeicoes.py a1.txt > interjeicao-a1.txt
	py interjeicoes.py a2.txt > interjeicao-a2.txt

	py coesao.py a1.txt > coesao-a1.txt
	py coesao.py a2.txt > coesao-a2.txt

	py tempos.py a1.txt > tempos-a1.txt
	py tempos.py a2.txt > tempos-a2.txt


# ---------- LIMPEZA ----------
clean:
	# Limpeza dos arquivos gerados
	del /Q *.conll *.txt
