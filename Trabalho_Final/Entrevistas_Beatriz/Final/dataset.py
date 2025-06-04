import pandas as pd
import json
import re

def parse_tabela_sentimento(path):
    return pd.read_csv(path)

def parse_entidades(path):
    entidades = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                entidades.append({
                    "frequencia": int(parts[0]),
                    "texto": " ".join(parts[1:-1]),
                    "tipo": parts[-1]
                })
    return entidades

def parse_keywords(path):
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def parse_freq_absoluta(path, participante):
    with open(path, encoding="utf-8") as f:
        linhas = f.readlines()
    metade = len(linhas) // 2
    return [line.strip() for line in (linhas[:metade] if participante == "B1" else linhas[metade:])]

def parse_linhas_palavras(path, participante):
    with open(path, encoding="utf-8") as f:
        linhas = f.readlines()
    metade = len(linhas) // 2
    return [line.strip() for line in (linhas[:metade] if participante == "B1" else linhas[metade:])]

def parse_interjeicoes(path):
    interjeicoes = {}
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(path, encoding="latin1") as f:
            lines = f.readlines()
    for line in lines:
        if ":" in line:
            k, v = line.strip().split(":")
            interjeicoes[k.strip()] = int(v.strip())
    return interjeicoes

def parse_palavras_frequentes(path, participante):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    nome_participante = "B1" if participante == "B1" else "João"
    blocos = re.split(r"Palavras frequentes\s+", content)
    for bloco in blocos:
        if nome_participante in bloco:
            matches = re.findall(r"\d+\.\s(.+?)\s-\s(\d+)", bloco)
            return {pal.strip(): int(freq) for pal, freq in matches}
    return {}

def parse_tempos(path):
    tempos = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                k, v = line.strip().split(":")
                tempos[k.strip()] = int(v.strip())
    return tempos

def montar_dado(participante):
    return {
        "participante": participante,
        "tabela_sentimento": parse_tabela_sentimento(f"tabela_{participante}.txt").to_dict(orient="records"),
        "entidades": parse_entidades(f"Entrevista_{participante}-ent-agr.txt"),
        "keywords": parse_keywords(f"Entrevista_{participante}-keywords.txt"),
        "frequencia_absoluta": parse_freq_absoluta("Entrevista_freq.txt", participante),
        "linhas_palavras": parse_linhas_palavras("Entrevista_linhas_pal.txt", participante),
        "interjeicoes": parse_interjeicoes(f"interjeicoes_{participante}.txt"),
        "palavras_frequentes": parse_palavras_frequentes("palavras_frequentes.txt", participante),
        "tempos_verbais": parse_tempos(f"tempos_{participante}.txt"),
    }

# === Geração do JSON final ===
dados = [montar_dado("B1"), montar_dado("B2")]

with open("dataset_completo.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, indent=4, ensure_ascii=False)

