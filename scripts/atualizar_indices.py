#!/usr/bin/env python3
"""Reconstrói os índices da WIKI CIBS e verifica a integridade da base.

Uso (a partir da raiz do projeto):
    python3 scripts/atualizar_indices.py            # atualiza índices + verifica
    python3 scripts/atualizar_indices.py --checar   # só verifica, não grava

Atualiza (só as seções geradas; escopo e "Ver também" ficam como estão):
- `WIKI/NN - Categoria/000 - Índice Categoria.md`: `## Notas desta categoria` e `## Conceitos desta categoria`
- `WIKI/Escrituras/000 - Índice Escrituras.md`: `## Passagens` (ordem do cânon)
- `WIKI/Fontes/000 - Índice Fontes.md`: `## Obras e referências` (por grupo)
- `WIKI/000 - Índice Central CIBS.md`: categorias, referências e lista alfabética de notas

Verifica (erros fazem o script sair com código 1):
- wikilink entre crases, colchetes desbalanceados, `|` extra, `:` `/` ou `\\` no alvo
- link sem nota (link cinza), nota/conceito/passagem/fonte fora dos índices
- arquivo vazio em WIKI ou RAW (stub criado pelo Obsidian)
- frontmatter da nota kb- (campos obrigatórios, topic_category igual à pasta)
- nota kb- sem link para outra nota kb- ("Notas relacionadas na base")
- rascunho vindo do RAW que não foi finalizado (status, categoria_sugerida, bloco de integração)
- frases proibidas ("o palestrante", "fonte não confiável" etc.)
Avisos (não bloqueiam): notas de conceito, passagem ou fonte curtas demais.
"""
import glob
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI = os.path.join(RAIZ, "WIKI")
RAW = os.path.join(RAIZ, "RAW")
CENTRAL = os.path.join(WIKI, "000 - Índice Central CIBS.md")
ESCRITURAS = os.path.join(WIKI, "Escrituras")
FONTES = os.path.join(WIKI, "Fontes")
nfc = lambda s: unicodedata.normalize("NFC", s)

CAMPOS_KB = ["title", "origem", "creator_channel", "autor_do_estudo", "source_url", "source_type",
             "date_captured", "topic_category", "tags", "type", "knowledge_depth"]
FRASES_PROIBIDAS = [r"\bo palestrante\b", r"\ba palestrante\b", r"\bo pregador\b", r"\bnesta live\b",
                    r"\bneste vídeo\b", r"não verificad", r"carece de fonte", r"merece verificação",
                    r"fonte (não confiável|duvidosa|questionável)", r"verifique a fonte"]
MIN_PALAVRAS = {"concept": 160, "escritura": 100, "fonte": 120}

CANON = [
    ("Torá", ["Gênesis", "Êxodo", "Levítico", "Números", "Deuteronômio"]),
    ("Nevi'im", ["Josué", "Juízes", "1 Samuel", "2 Samuel", "1 Reis", "2 Reis", "Isaías", "Jeremias",
                 "Ezequiel", "Oseias", "Joel", "Amós", "Obadias", "Jonas", "Miqueias", "Naum",
                 "Habacuque", "Sofonias", "Ageu", "Zacarias", "Malaquias"]),
    ("Ketuvim", ["Salmo", "Provérbios", "Jó", "Cântico dos Cânticos", "Rute", "Lamentações",
                 "Eclesiastes", "Ester", "Daniel", "Esdras", "Neemias", "1 Crônicas", "2 Crônicas"]),
    ("Berit Hadashah", ["Mateus", "Marcos", "Lucas", "João", "Atos", "Romanos", "1 Coríntios",
                        "2 Coríntios", "Gálatas", "Efésios", "Filipenses", "Colossenses",
                        "1 Tessalonicenses", "2 Tessalonicenses", "1 Timóteo", "2 Timóteo", "Tito",
                        "Filemom", "Hebreus", "Tiago", "1 Pedro", "2 Pedro", "1 João", "2 João",
                        "3 João", "Judas", "Apocalipse"]),
]
ORDEM_LIVRO = {nfc(l): (g, i) for g, (_, ls) in enumerate(CANON) for i, l in enumerate(ls)}


def ler(caminho):
    return open(caminho, encoding="utf-8").read()


def frontmatter(texto):
    m = re.match(r"---\n(.*?)\n---", texto, re.S)
    return dict(re.findall(r'^(\w+):\s*"?(.*?)"?\s*$', m.group(1), re.M)) if m else {}


def titulo(caminho):
    t = frontmatter(ler(caminho)).get("title")
    return (t or os.path.basename(caminho)[:-3]).replace("|", "—")


def base(caminho):
    return nfc(os.path.basename(caminho)[:-3])


def categorias():
    return sorted(d for d in os.listdir(WIKI) if re.match(r"^\d\d - ", d) and os.path.isdir(os.path.join(WIKI, d)))


def nome(cat):
    return cat.split(" - ", 1)[1]


def notas(cat):
    return sorted(glob.glob(os.path.join(WIKI, cat, "kb-*.md")))


def conceitos(cat):
    pasta = os.path.join(WIKI, cat, "Conceitos")
    return sorted((base(f) for f in glob.glob(os.path.join(pasta, "*.md"))), key=lambda s: s.lower())


def passagens():
    arqs = [f for f in glob.glob(os.path.join(ESCRITURAS, "**", "*.md"), recursive=True)
            if not os.path.basename(f).startswith("000 - ")]

    def chave(f):
        n = base(f)
        m = re.match(r"^(.*?)\s+(\d+)(?:\.(\d+))?", n)
        livro = nfc(m.group(1)) if m else n
        g, i = ORDEM_LIVRO.get(livro, (9, 0))
        return (g, i, livro, int(m.group(2)) if m else 0, int(m.group(3) or 0) if m else 0, n)
    return sorted(arqs, key=chave)


def fontes():
    return sorted((f for f in glob.glob(os.path.join(FONTES, "**", "*.md"), recursive=True)
                   if not os.path.basename(f).startswith("000 - ")), key=lambda f: base(f).lower())


def trocar_secao(texto, cabecalho, novo_corpo, antes_de=None):
    if not re.search(rf"^{re.escape(cabecalho)}$", texto, re.M):
        alvo = antes_de if antes_de and antes_de in texto else None
        texto = texto.replace(alvo, f"{cabecalho}\n\n{alvo}", 1) if alvo else texto.rstrip() + f"\n\n{cabecalho}\n"
    padrao = re.compile(rf"(^{re.escape(cabecalho)}\n)(.*?)(?=^## |\Z)", re.M | re.S)
    return padrao.sub(lambda m: m.group(1) + "\n" + novo_corpo + "\n\n", texto, count=1)


def atualizar():
    todas, total_conc = [], 0
    for cat in categorias():
        idx = os.path.join(WIKI, cat, f"000 - Índice {nome(cat)}.md")
        assert os.path.exists(idx), f"categoria sem índice: {cat}"
        lista = [(base(f), titulo(f)) for f in notas(cat)]
        todas += [(k, t, cat) for k, t in lista]
        t = ler(idx)
        t = trocar_secao(t, "## Notas desta categoria", "\n".join(f"- [[{k}|{ti}]]" for k, ti in lista) or "_Nenhuma nota ainda._", "## Ver também")
        conc = conceitos(cat)
        total_conc += len(conc)
        t = trocar_secao(t, "## Conceitos desta categoria", " · ".join(f"[[{c}]]" for c in conc) or "_Nenhum conceito ainda._", "## Ver também")
        open(idx, "w", encoding="utf-8").write(t)

    n_pass = n_font = 0
    idx_e = os.path.join(ESCRITURAS, "000 - Índice Escrituras.md")
    if os.path.exists(idx_e):
        ps = passagens()
        n_pass = len(ps)
        blocos, atual = [], None
        for f in ps:
            n = base(f)
            m = re.match(r"^(.*?)\s+\d", n)
            livro = nfc(m.group(1)) if m else n
            grupo = CANON[ORDEM_LIVRO[livro][0]][0] if livro in ORDEM_LIVRO else "Outros"
            if grupo != atual:
                blocos.append(f"\n### {grupo}\n")
                atual = grupo
            blocos.append(f"- [[{n}]]")
        t = trocar_secao(ler(idx_e), "## Passagens", "\n".join(blocos).strip() or "_Nenhuma passagem ainda._", "## Ver também")
        open(idx_e, "w", encoding="utf-8").write(t)

    idx_f = os.path.join(FONTES, "000 - Índice Fontes.md")
    if os.path.exists(idx_f):
        grupos = {}
        for f in fontes():
            grupos.setdefault(frontmatter(ler(f)).get("grupo", "Outros"), []).append(base(f))
        n_font = sum(len(v) for v in grupos.values())
        corpo = "\n\n".join(f"### {g}\n\n" + "\n".join(f"- [[{n}]]" for n in v) for g, v in sorted(grupos.items()))
        t = trocar_secao(ler(idx_f), "## Obras e referências", corpo or "_Nenhuma fonte ainda._", "## Ver também")
        open(idx_f, "w", encoding="utf-8").write(t)

    t = ler(CENTRAL)
    cats = categorias()
    linhas = []
    for c in cats:
        n, nc = len(notas(c)), len(conceitos(c))
        linhas.append(f"- [[000 - Índice {nome(c)}|{c}]] — {n} {'nota' if n == 1 else 'notas'} · {nc} conceitos")
    cab = f"## Categorias ({len(cats)} categorias · {len(todas)} notas · {total_conc} conceitos)"
    if re.search(r"^## Categorias.*$", t, re.M):
        t = re.sub(r"^## Categorias.*$", cab, t, count=1, flags=re.M)
    t = trocar_secao(t, cab, "\n".join(linhas))
    refs = []
    if os.path.exists(idx_e):
        refs.append(f"- [[000 - Índice Escrituras|Escrituras]] — {n_pass} passagens")
    if os.path.exists(idx_f):
        refs.append(f"- [[000 - Índice Fontes|Fontes]] — {n_font} obras e referências")
    t = trocar_secao(t, "## Referências", "\n".join(refs) or "_Nenhuma ainda._", "## Todas as notas (ordem alfabética)")
    t = trocar_secao(t, "## Todas as notas (ordem alfabética)",
                     "\n".join(f"- [[{k}|{ti}]] · _{nome(c)}_" for k, ti, c in sorted(todas)))
    open(CENTRAL, "w", encoding="utf-8").write(t)
    print(f"índices atualizados: {len(cats)} categorias, {len(todas)} notas, {total_conc} conceitos, {n_pass} passagens, {n_font} fontes")


def palavras(texto):
    texto = re.sub(r"^---\n.*?\n---", "", texto, flags=re.S)
    texto = re.split(r"^## Aparece em", texto, flags=re.M)[0]
    return len(re.findall(r"\w+", texto))


def verificar():
    arquivos = glob.glob(os.path.join(WIKI, "**", "*.md"), recursive=True)
    nomes = {base(f) for f in arquivos}
    erros, avisos, total = [], [], 0
    for f in arquivos + glob.glob(os.path.join(RAW, "**", "*.md"), recursive=True):
        if os.path.getsize(f) == 0:
            erros.append(("arquivo vazio (stub do Obsidian)", os.path.relpath(f, RAIZ)))
    for f in arquivos:
        t = ler(f)
        rel = os.path.relpath(f, RAIZ)
        if re.search(r"`\[\[", t):
            erros.append(("wikilink entre crases", rel))
        corpo = re.sub(r"`[^`\n]*`", "", t)
        if corpo.count("[[") != corpo.count("]]"):
            erros.append(("colchetes desbalanceados", rel))
        for l in re.findall(r"\[\[([^\]]+)\]\]", corpo):
            total += 1
            alvo = l.split("|")[0].split("#")[0].strip()
            if l.count("|") > 1:
                erros.append(("| extra", rel, l))
            if re.search(r"[:/\\]", alvo):
                erros.append(("caractere proibido no alvo (: / \\)", rel, l))
            elif alvo and nfc(alvo) not in nomes:
                erros.append(("link sem nota (cinza)", rel, alvo))
        fm = frontmatter(t)
        tipo = fm.get("type", "")
        if os.path.basename(f).startswith("kb-"):
            for campo in CAMPOS_KB:
                if not fm.get(campo):
                    erros.append(("kb sem campo no frontmatter", rel, campo))
            pasta = os.path.basename(os.path.dirname(f))
            if re.match(r"^\d\d - ", pasta) and fm.get("topic_category") != nome(pasta):
                erros.append(("topic_category diferente da pasta", rel, fm.get("topic_category")))
            outras = {x.split("|")[0].strip() for x in re.findall(r"\[\[(kb-[^\]]+)\]\]", corpo)} - {base(f)}
            if not outras:
                erros.append(("kb sem link para outra nota kb-", rel))
            if fm.get("status") or "categoria_sugerida" in fm or re.search(r"^## Notas para a integração", t, re.M):
                erros.append(("rascunho não finalizado (status, categoria_sugerida ou bloco de integração)", rel))
            if os.path.basename(f) != os.path.basename(f).lower():
                erros.append(("nome de arquivo com maiúscula", rel))
        for p in FRASES_PROIBIDAS:
            if re.search(p, t, re.I):
                erros.append(("frase proibida", rel, p))
        if tipo in MIN_PALAVRAS and palavras(t) < MIN_PALAVRAS[tipo]:
            avisos.append((f"{tipo} curto ({palavras(t)} palavras, mínimo {MIN_PALAVRAS[tipo]})", rel))
    indices = nfc(" ".join(ler(f) for f in arquivos if os.path.basename(f).startswith("000 - ")))
    for n in nomes:
        if n.startswith("kb-") and f"[[{n}|" not in indices:
            erros.append(("nota fora dos índices", n))
    for padrao, rotulo in [(os.path.join(WIKI, "*", "Conceitos", "*.md"), "conceito"),
                           (os.path.join(ESCRITURAS, "**", "*.md"), "passagem"),
                           (os.path.join(FONTES, "**", "*.md"), "fonte")]:
        for f in glob.glob(padrao, recursive=True):
            n = base(f)
            if not n.startswith("000 - ") and f"[[{n}]]" not in indices:
                erros.append((f"{rotulo} fora dos índices", n))
    print(f"verificação: {len(arquivos)} arquivos, {total} wikilinks, {len(erros)} erros, {len(avisos)} avisos")
    for e in erros:
        print("   ERRO", e)
    for a in avisos:
        print("   aviso", a)
    return not erros


if __name__ == "__main__":
    if "--checar" not in sys.argv:
        atualizar()
    sys.exit(0 if verificar() else 1)
