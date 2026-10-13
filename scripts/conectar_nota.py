"""Conecta uma nota kb- nova ao resto da base, só acrescentando.

Uso (da raiz da base):
    python3 scripts/conectar_nota.py <kb-slug> conexoes.json

conexoes.json:
{
  "relacionadas": {"kb-outra-nota": "frase sobre a relação (vai na nota antiga)"},
  "parashiot": {"Parashá Emor": "Torá: Levítico 23, ..."},
  "secoes": {"Nome do conceito": "## Título da seção\\nTexto (use {LINK} para o link da nota nova)"}
}

Faz:
1. acrescenta a nota nova em "## Aparece em" de todo conceito, fonte e passagem que ela linka;
2. acrescenta o link de volta em "Notas relacionadas na base" das notas listadas em "relacionadas";
3. acrescenta o estudo em "Estudos da base que citam versículos destas leituras" das parashiot;
4. insere as seções novas antes de "## Relacionados" nos conceitos listados em "secoes".
Nada é apagado nem reescrito. Rodar duas vezes não duplica.
"""
import glob
import json
import os
import re
import sys
import unicodedata

nfc = lambda s: unicodedata.normalize("NFC", s)
K, conf = sys.argv[1], json.load(open(sys.argv[2]))
arq = {nfc(os.path.basename(f)[:-3]): f for f in glob.glob("WIKI/**/*.md", recursive=True)}
nota = nfc(open(arq[K]).read())
T = re.search(r'^title: "(.*)"', nota, re.M).group(1)
LINK = f"[[{K}|{T}]]"

n = 0
for a in sorted({x.split("|")[0].strip() for x in re.findall(r"\[\[([^\]]+)\]\]", nota)}):
    if a.startswith(("kb-", "Parashá", "000 - ")) or a not in arq:
        continue
    t = nfc(open(arq[a]).read())
    if K in t or "## Aparece em" not in t:
        continue
    open(arq[a], "w").write(t.rstrip() + f"\n- {LINK}\n")
    n += 1
print("aparece em:", n)

for k, frase in conf.get("relacionadas", {}).items():
    t = open(arq[k]).read()
    if K in t:
        continue
    i = t.index("**Notas relacionadas na base:**")
    resto = t[i:]
    itens = list(re.finditer(r"^- \[\[[^\n]*$", resto, re.M))
    if itens and itens[0].start() < 400:
        fim = itens[0].end()
        for x in itens[1:]:
            if resto[fim:x.start()].strip():
                break
            fim = x.end()
        t = t[:i] + resto[:fim] + f"\n- {LINK} — {frase}" + resto[fim:]
    else:
        j = t.index("\n", i)
        t = t[:j] + f" · {LINK} ({frase.rstrip('.')})" + t[j:]
    open(arq[k], "w").write(t)
    print("relacionada:", k)

for p, motivo in conf.get("parashiot", {}).items():
    t = open(arq[p]).read()
    if K in t:
        continue
    t = t.replace("- Nenhum estudo ainda.\n", "")
    t = re.sub(r"(\*\*Estudos da base que citam versículos destas leituras:\*\*\n(?:- .*\n)*)",
               lambda m: m.group(1) + f"- {LINK} — {motivo}\n", t, count=1)
    open(arq[p], "w").write(t)
    print("parashá:", p)

for c, bloco in conf.get("secoes", {}).items():
    t = open(arq[c]).read()
    titulo = bloco.split("\n", 1)[0]
    if titulo in t:
        continue
    t = t.replace("\n## Relacionados", "\n" + bloco.replace("{LINK}", LINK).rstrip() + "\n\n## Relacionados", 1)
    open(arq[c], "w").write(t)
    print("seção:", c)
