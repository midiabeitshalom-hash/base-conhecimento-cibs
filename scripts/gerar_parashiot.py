"""Gera WIKI/Parashiot/ a partir da planilha. Rodar com cwd = raiz da base."""
import zipfile, re, os, glob, unicodedata, xml.etree.ElementTree as ET
nfc = lambda s: unicodedata.normalize("NFC", s)
XLSX = "RAW/_midia/_processados/Parashiot_Haftarot_BeritChadasha_v3.xlsx"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

z = zipfile.ZipFile(XLSX)
linhas = []
for r in ET.fromstring(z.read("xl/worksheets/sheet1.xml")).iter(NS + "row"):
    vals = []
    for c in r.findall(NS + "c"):
        is_ = c.find(NS + "is")
        v = c.find(NS + "v")
        vals.append("".join(t.text or "" for t in is_.iter(NS + "t")) if is_ is not None else (v.text if v is not None else ""))
    linhas.append([nfc(x.strip()) for x in vals])
linhas = linhas[1:]
assert len(linhas) == 54

PASTA_LIVRO = {"Gênesis": "1 - Bereshit (Gênesis)", "Êxodo": "2 - Shemot (Êxodo)", "Levítico": "3 - Vayikra (Levítico)",
               "Números": "4 - Bamidbar (Números)", "Deuteronômio": "5 - Devarim (Deuteronômio)"}

RESUMO = {
 "Bereshit": "A criação em seis dias e o Shabat; Adam e Chavah no Éden, a queda e a expulsão; Kayin e Hevel; as gerações de Adam até Noach e a corrupção que antecede o dilúvio.",
 "Noach": "Noach, justo na sua geração, constrói a arca; o dilúvio e a aliança do arco-íris com a humanidade; os filhos de Noach, a Torre de Babel e a genealogia de Shem até Avram.",
 "Lech Lecha": "O chamado de Avram para sair de Ur e de Charan rumo à Terra; a descida ao Egito, a guerra dos reis e o encontro com Malki-Tzedek; a aliança entre as partes, o nascimento de Yishmael e a aliança da circuncisão, com os nomes Avraham e Sarah.",
 "Vayera": "D'us aparece a Avraham em Mamre e anuncia o nascimento de Yitzchak; a intercessão por Sedom e a destruição das cidades; o nascimento de Yitzchak e a Akedá, a amarração de Yitzchak no monte Moriá.",
 "Chayei Sarah": "A morte de Sarah e a compra da caverna de Machpelá; o servo de Avraham encontra Rivká para Yitzchak; a morte de Avraham.",
 "Toledot": "O nascimento de Esav e Ya'akov; a venda da primogenitura; Yitzchak entre os filisteus e os poços; Ya'akov recebe a bênção do pai.",
 "Vayetze": "Ya'akov foge para Charan e sonha com a escada (Sulam Ya'akov) em Beit El; casa com Leah e Rachel; o nascimento dos filhos e o retorno com a família.",
 "Vayishlach": "Ya'akov prepara o encontro com Esav e luta com o anjo em Peniel, onde recebe o nome Israel; o episódio de Dinah em Shechem; a morte de Rachel e as gerações de Esav.",
 "Vayeshev": "Yosef e seus sonhos; vendido pelos irmãos e levado ao Egito; Yehudah e Tamar; Yosef na casa de Potifar e na prisão, interpretando os sonhos do copeiro e do padeiro.",
 "Miketz": "Os sonhos de Paraó e a ascensão de Yosef no Egito; a fome e a descida dos irmãos para comprar alimento; Binyamin levado ao Egito e o cálice na sacola.",
 "Vayigash": "Yehudah se oferece no lugar de Binyamin; Yosef se revela aos irmãos; Ya'akov desce ao Egito com toda a família e se estabelece em Goshen.",
 "Vayechi": "Os últimos anos de Ya'akov no Egito; a bênção de Efraim e Menashe; as bênçãos proféticas às doze tribos; a morte de Ya'akov e de Yosef.",
 "Shemot": "A escravidão de Israel no Egito; o nascimento de Moshe e sua fuga para Midiã; a sarça ardente e a revelação do Nome; o primeiro confronto com Paraó.",
 "Vaera": "D'us reafirma a promessa aos patriarcas e revela o Nome; Moshe e Aharon diante de Paraó; as sete primeiras pragas.",
 "Bo": "As três últimas pragas; a primeira mitzvá dada a Israel, a do calendário (este mês será o primeiro); o cordeiro de Pessach, a morte dos primogênitos e a saída do Egito.",
 "Beshalach": "A travessia do Mar de Juncos e o Cântico do Mar; o maná e o Shabat no deserto; a água da rocha; a guerra contra Amalek.",
 "Yitro": "Yitro aconselha Moshe a organizar os juízes; Israel chega ao Har Sinai; a revelação da Torá e os Dez Mandamentos (Aseret HaDibrot).",
 "Mishpatim": "As leis civis e sociais: servos, danos, justiça, proteção do estrangeiro, do órfão e da viúva; as três festas de peregrinação; a aliança selada com sangue (Na'asê veNishmá).",
 "Terumá": "A oferta voluntária para a construção do Mishkan; as instruções para a Arca, a mesa, a Menorá e a estrutura do Tabernáculo.",
 "Tetzaveh": "O azeite para a lâmpada perpétua; as vestes do Kohen Gadol e dos sacerdotes; a consagração de Aharon e seus filhos; o altar do incenso.",
 "Ki Tisa": "O censo com o meio shekel; o Shabat como sinal eterno; o bezerro de ouro, a intercessão de Moshe e as segundas tábuas; os treze atributos de misericórdia.",
 "Vayakhel": "Moshe reúne o povo e reafirma o Shabat; as ofertas e a construção do Mishkan por Betzalel e Oholiav.",
 "Pekudei": "A contagem dos materiais do Mishkan; a confecção das vestes sacerdotais; a montagem do Tabernáculo e a nuvem da glória que o enche.",
 "Vayikra": "D'us chama Moshe da Tenda do Encontro; as ofertas (corbanot): olá, minchá, shelamim, chatat e asham.",
 "Tzav": "As instruções aos sacerdotes sobre as ofertas; o fogo perpétuo do altar; os sete dias de consagração de Aharon e seus filhos.",
 "Shemini": "O oitavo dia e a inauguração do serviço; a morte de Nadav e Avihu; as leis dos animais puros e impuros (kashrut).",
 "Tazria": "A pureza depois do parto; as leis de tzaraat nas pessoas e nas roupas.",
 "Metzora": "A purificação de quem teve tzaraat; tzaraat nas casas; as impurezas por fluxos do corpo.",
 "Acharei Mot": "O serviço do Kohen Gadol em Yom Kippur e o bode para Azazel; a proibição de comer sangue; as relações proibidas.",
 "Kedoshim": "\"Sereis santos, porque Eu sou santo\": leis de santidade na vida diária, ética e justiça; \"amarás o teu próximo como a ti mesmo\".",
 "Emor": "As leis dos sacerdotes; o calendário dos moedim: Shabat, Pessach, Omer, Shavuot, Yom Teruá, Yom Kippur e Sucot; a lâmpada da Menorá e o pão da proposição.",
 "Behar": "O ano sabático (shemitá) e o jubileu (yovel); a terra pertence a D'us; o resgate da terra e do irmão empobrecido.",
 "Bechukotai": "As bênçãos pela obediência e as consequências da desobediência; a promessa de lembrar a aliança com os patriarcas; as leis dos votos e dízimos.",
 "Bamidbar": "O censo de Israel no deserto do Sinai; a disposição das tribos ao redor do Mishkan; os levitas no lugar dos primogênitos.",
 "Naso": "O censo dos levitas; a mulher sotá; o nazireu; a Bênção Sacerdotal (Birkat Kohanim); as ofertas dos príncipes na inauguração do altar.",
 "Behaalotecha": "O acendimento da Menorá; a consagração dos levitas; o Pessach Sheni; a nuvem que guia o acampamento; as queixas do povo, os 70 anciãos e a murmuração de Miriam.",
 "Shelach Lecha": "Os doze espias e o relatório negativo; o decreto dos quarenta anos no deserto; as ofertas, a chalá e o tzitzit.",
 "Korach": "A rebelião de Korach, Datan e Aviram; a vara de Aharon que floresce; os deveres e os direitos dos sacerdotes e levitas.",
 "Chukat": "A novilha vermelha (parah adumah); a morte de Miriam e de Aharon; a água da rocha e o pecado de Moshe; a serpente de bronze.",
 "Balak": "Balak contrata Bil'am para amaldiçoar Israel; a jumenta que fala; as bênçãos de Bil'am, com a profecia da estrela de Ya'akov; o pecado em Peor.",
 "Pinchas": "A aliança de paz com Pinchas; o novo censo; as filhas de Tzelofchad; Yehoshua designado sucessor de Moshe; as ofertas de cada Shabat, Rosh Chodesh e dos moedim.",
 "Matot": "As leis dos votos; a guerra contra Midiã; as tribos de Reuven e Gad pedem herança a leste do Jordão.",
 "Masei": "As quarenta e duas etapas da jornada no deserto; as fronteiras da Terra; as cidades dos levitas e as cidades de refúgio; a herança das filhas de Tzelofchad.",
 "Devarim": "Moshe começa seu discurso final às margens do Jordão e relembra a jornada desde o Sinai, os espias e as vitórias a leste do Jordão.",
 "Vaetchanan": "Moshe suplica para entrar na Terra; a repetição dos Dez Mandamentos; o Shemá Israel e o mandamento de amar a D'us de todo o coração.",
 "Ekev": "As bênçãos pela obediência; a lembrança do maná e do deserto; o bezerro de ouro relembrado; o segundo parágrafo do Shemá.",
 "Reê": "A bênção e a maldição; o lugar que D'us escolher; a proibição da idolatria e do falso profeta; as leis de kashrut, dízimo e shemitá; as três festas de peregrinação.",
 "Shoftim": "Juízes e justiça; o rei e seus limites; os sacerdotes e levitas; o profeta como Moshe; as cidades de refúgio e as leis da guerra.",
 "Ki Tetze": "Setenta e quatro mitzvot da vida familiar e social: a mulher cativa, o filho rebelde, o ninho, o parapeito, salários justos, pesos honestos e a lembrança de Amalek.",
 "Ki Tavo": "Os primeiros frutos (bikurim) e a declaração do agricultor; as bênçãos e maldições dos montes Guerizim e Eval.",
 "Nitzavim": "Todo Israel diante de D'us para entrar na aliança, incluindo as gerações futuras; a promessa da teshuvá; a Torá não está nos céus; escolhe a vida.",
 "Vayelech": "Moshe, aos 120 anos, passa a liderança a Yehoshua; a leitura pública da Torá a cada sete anos (Hakhel); a ordem de escrever o cântico.",
 "Haazinu": "O cântico de Moshe, testemunho perante céus e terra; D'us vê Moshe subir ao monte Nevo.",
 "Vezot Haberachah": "Moshe abençoa as tribos antes de morrer; a morte de Moshe no monte Nevo. É lida em Simchat Torá, quando o ciclo termina e recomeça em Bereshit.",
}

CONCEITOS = {
 "Bereshit": ["Adam HaRishon", "Na'assê Adam", "Tzelem Elohim", "Shabat", "Kayin", "Hevel", "Chanoch", "Nefilim", "Yetzer HaRá"],
 "Noach": ["Noach", "Shem", "Torre de Babel", "Avraham Avinu"],
 "Lech Lecha": ["Avraham Avinu", "Malki-Tzedek"], "Vayera": ["Avraham Avinu", "Yitzchak Avinu"],
 "Chayei Sarah": ["Avraham Avinu", "Yitzchak Avinu"], "Toledot": ["Yitzchak Avinu", "Ya'akov Avinu", "Bechor"],
 "Vayetze": ["Ya'akov Avinu", "Sulam Ya'akov"], "Vayishlach": ["Ya'akov Avinu", "Binyamin"],
 "Vayeshev": ["Yosef HaTzaddik", "Ya'akov Avinu"], "Miketz": ["Yosef HaTzaddik", "Binyamin"],
 "Vayigash": ["Yosef HaTzaddik", "Binyamin", "Ya'akov Avinu"], "Vayechi": ["Ya'akov Avinu", "Yosef HaTzaddik", "Menashe", "Doze Tribos de Israel"],
 "Shemot": ["Moshe Rabenu", "Tetragrama"], "Vaera": ["Moshe Rabenu", "Aharon HaKohen", "Tetragrama"],
 "Bo": ["Pessach", "Corban Pessach", "Bechor", "Erev Rav", "Moedim"], "Beshalach": ["Moshe Rabenu", "Shabat"],
 "Yitro": ["Har Sinai", "Torá", "Mitzvot", "Shabat", "Zachor e Shamor"], "Mishpatim": ["Mitzvot", "Halachá", "Shalosh Regalim"],
 "Terumá": ["Menorá"], "Tetzaveh": ["Kohen Gadol", "Aharon HaKohen", "Menorá"], "Ki Tisa": ["Shabat", "Moshe Rabenu", "Teshuvá"],
 "Vayakhel": ["Shabat"], "Pekudei": ["Kohen Gadol", "Shechinah"],
 "Vayikra": ["Corbanot", "Asham", "Kapará"], "Tzav": ["Corbanot", "Aharon HaKohen"], "Shemini": ["Kashrut", "Aharon HaKohen"],
 "Tazria": ["Tzaraat", "Taharah", "Tum'ah"], "Metzora": ["Tzaraat", "Taharah", "Tum'ah", "Niddah"],
 "Acharei Mot": ["Yom Kippur", "Azazel", "Kohen Gadol", "Kapará"], "Kedoshim": ["Kedushá", "Mitzvot"],
 "Emor": ["Moedim", "Shabat", "Pessach", "Chag HaMatzot", "Shavuot", "Yom Teruá", "Yom Kippur", "Sucot", "Shemini Atzeret", "Menorá"],
 "Behar": ["Shemitá", "Yovel"], "Bechukotai": ["Mitzvot"],
 "Bamidbar": ["Doze Tribos de Israel", "Bechor"], "Naso": ["Kohen Gadol"], "Behaalotecha": ["Menorá", "70 Anciãos", "Pessach"],
 "Shelach Lecha": ["Yehoshua bin Nun"], "Korach": ["Aharon HaKohen"], "Chukat": ["Aharon HaKohen", "Moshe Rabenu", "Taharah"],
 "Balak": ["Bil'am"], "Pinchas": ["Pinchas", "Yehoshua bin Nun", "Moedim"], "Matot": ["Doze Tribos de Israel"],
 "Masei": ["Doze Tribos de Israel"], "Devarim": ["Moshe Rabenu"], "Vaetchanan": ["Shemá Israel", "Monoteísmo Estrito", "Moshe Rabenu"],
 "Ekev": ["Shemá Israel", "Circuncisão do Coração"], "Reê": ["Kashrut", "Shemitá", "Shalosh Regalim"],
 "Shoftim": ["Moshe Rabenu"], "Ki Tetze": ["Mitzvot"], "Ki Tavo": ["Bikurim"], "Nitzavim": ["Teshuvá", "Circuncisão do Coração"],
 "Vayelech": ["Yehoshua bin Nun"], "Haazinu": ["Moshe Rabenu"], "Vezot Haberachah": ["Moshe Rabenu", "Doze Tribos de Israel"],
}

existentes = {nfc(os.path.basename(f)[:-3]): f for f in glob.glob("WIKI/**/*.md", recursive=True)}
UM_CAP = {"Judas", "Obadias", "Filemom", "2 João", "3 João"}

def faixas(s):
    s = re.sub(r"\(.*?\)", "", s)
    out, livro = [], None
    for parte in s.split(";"):
        parte = parte.strip()
        m = re.match(r"^((?:[123] )?\D+?)\s+(\d.*)$", parte)
        if m:
            livro, parte = m.group(1).strip(), m.group(2)
        cap = None
        for item in parte.split(","):
            item = item.strip().replace("–", "-")
            if livro in UM_CAP and ":" not in item:
                item = "1:" + item
            m = re.match(r"^(\d+):(\d+)(?:-(?:(\d+):)?(\d+))?$", item)
            if m:
                cap = int(m.group(1)); v1 = int(m.group(2))
                c2 = int(m.group(3)) if m.group(3) else cap
                v2 = int(m.group(4)) if m.group(4) else v1
            else:
                m = re.match(r"^(\d+)(?:-(\d+))?$", item)
                v1 = int(m.group(1)); v2 = int(m.group(2) or v1); c2 = cap
            out.append((livro, (cap, v1), (c2, v2)))
            cap = c2
    return out

def contem(fx, livro, cap, ver=None):
    for l, a, b in fx:
        if l != livro:
            continue
        if ver is None:
            if a[0] <= cap <= b[0]:
                return True
        elif a <= (cap, ver) <= b:
            return True
    return False

ponto = lambda s: s.replace(":", ".").replace("–", "-")

# notas de passagem existentes
pass_notas = []
for f in glob.glob("WIKI/Escrituras/**/*.md", recursive=True):
    n = nfc(os.path.basename(f)[:-3])
    m = re.match(r"^(.*?) (\d+)(?:\.(\d+))?$", n)
    if m:
        pass_notas.append((n, m.group(1), int(m.group(2)), int(m.group(3)) if m.group(3) else None, f))

# versículos citados em cada nota kb-
LIVROS = sorted({"Gênesis", "Êxodo", "Levítico", "Números", "Deuteronômio", "Josué", "Juízes", "1 Samuel", "2 Samuel", "1 Reis", "2 Reis", "Isaías", "Jeremias", "Ezequiel", "Oseias", "Joel", "Amós", "Obadias", "Jonas", "Miqueias", "Zacarias", "Malaquias", "Mateus", "Marcos", "Lucas", "João", "Atos", "Romanos", "1 Coríntios", "2 Coríntios", "Gálatas", "Efésios", "Filipenses", "Colossenses", "1 Timóteo", "2 Timóteo", "Hebreus", "Tiago", "1 Pedro", "2 Pedro", "1 João", "Judas", "Apocalipse"}, key=len, reverse=True)
RX = re.compile(r"(?<![\w])(" + "|".join(map(re.escape, LIVROS)) + r")\s+(\d+)[.:](\d+)")
kb = {}
for f in glob.glob("WIKI/0[1-9]*/kb-*.md"):
    t = nfc(open(f).read())
    tit = re.search(r'^title: "(.*)"', t, re.M).group(1)
    kb[nfc(os.path.basename(f)[:-3])] = (tit, {(m.group(1), int(m.group(2)), int(m.group(3))) for m in RX.finditer(t)})

dados = []
for row in linhas:
    num, livro, heb, tr, trad, tora, hasq, hsef, bh = row
    dados.append(dict(num=int(num), livro=livro, heb=heb, tr=tr, trad=trad, tora=tora, hasq=hasq, hsef=hsef, bh=bh))

nome_nota = lambda d: f"Parashá {d['tr']}"
por_passagem = {}
for i, d in enumerate(dados):
    leituras = [("Torá", d["tora"]), ("Haftará", d["hasq"] + "; " + d["hsef"]), ("Berit Hadashah", d["bh"])]
    fx = {k: faixas(v) for k, v in leituras}
    # passagens com nota
    pl = []
    for n, l, c, v, f in pass_notas:
        for k in fx:
            if contem(fx[k], l, c, v):
                pl.append((n, k)); por_passagem.setdefault(n, []).append((nome_nota(d), k)); break
    # estudos
    est = []
    for k_, (tit, vs) in sorted(kb.items()):
        hits = {}
        for (l, c, v) in vs:
            for k in fx:
                if contem(fx[k], l, c, v):
                    hits.setdefault(k, set()).add(f"{l} {c}.{v}")
        if hits.get("Torá") or sum(len(x) for x in hits.values()) >= 2:
            desc = "; ".join(f"{k}: " + ", ".join(sorted(x)) for k, x in hits.items())
            est.append(f"- [[{k_}|{tit}]] — {desc}")
    conc = [c for c in CONCEITOS.get(d["tr"], []) if c in existentes]
    falt = [c for c in CONCEITOS.get(d["tr"], []) if c not in existentes]
    if falt:
        print("conceito inexistente ignorado:", d["tr"], falt)
    ant = dados[i - 1] if i > 0 else dados[-1]
    prox = dados[i + 1] if i + 1 < len(dados) else dados[0]
    al = [f"Parashat {d['tr']}", f"{d['tr']} (parashá)", f"Parashá {d['num']}", f"פרשת {d['heb']}"]
    fm = (f'---\ntitle: "{nome_nota(d)}"\ntype: parasha\nnumero: {d["num"]}\nlivro: "{d["livro"]}"\nhebraico: "{d["heb"]}"\n'
          f'transliteracao: "{d["tr"]}"\ntraducao: "{d["trad"]}"\ntora: "{ponto(d["tora"])}"\n'
          f'haftara_asquenazita: "{ponto(d["hasq"])}"\nhaftara_sefaradita: "{ponto(d["hsef"])}"\n'
          f'berit_hadashah: "{ponto(d["bh"])}"\naliases: [{", ".join(chr(34)+a+chr(34) for a in al)}]\n'
          f'tags: [parasha, {unicodedata.normalize("NFD", d["livro"]).encode("ascii","ignore").decode().lower()}]\ndate_captured: 2026-10-05\n---\n')
    corpo = [f"# {nome_nota(d)} — {d['heb']}\n",
             f"**Parashá {d['num']} de 54** · livro de {d['livro']} · *{d['tr']}* ({d['heb']}), \"{d['trad']}\"\n",
             f"**Resumo:** {RESUMO[d['tr']]}\n",
             "## Leituras\n", "| Leitura | Trecho |", "|---|---|",
             f"| Torá | {ponto(d['tora'])} |",
             f"| Haftará (asquenazita) | {ponto(d['hasq'])} |",
             f"| Haftará (sefaradita) | {ponto(d['hsef'])} |",
             f"| Berit Hadashah | {ponto(d['bh'])} |", "",
             "## Na base CIBS\n",
             "**Passagens com nota nesta leitura:** " + (" · ".join(f"[[{n}]] ({k})" for n, k in pl) or "nenhuma ainda.") + "\n",
             "**Conceitos e pessoas da parashá:** " + (" · ".join(f"[[{c}]]" for c in conc) or "nenhum ainda.") + "\n",
             "**Estudos da base que citam versículos destas leituras:**", *(est or ["- Nenhum estudo ainda."]), "",
             "## Sequência do ciclo\n",
             f"← [[{nome_nota(ant)}]] · [[000 - Índice Parashiot|Todas as parashiot]] · [[{nome_nota(prox)}]] →", ""]
    pasta = f"WIKI/Parashiot/{PASTA_LIVRO[d['livro']]}"
    os.makedirs(pasta, exist_ok=True)
    open(f"{pasta}/{nome_nota(d)}.md", "w").write(fm + "\n" + "\n".join(corpo))

# passagens: seção "Na leitura semanal"
for n, l, c, v, f in pass_notas:
    t = open(f).read()
    t = re.sub(r"\n## Na leitura semanal\n.*?(?=\n## )", "", t, flags=re.S)
    if n in por_passagem:
        bloco = "\n## Na leitura semanal\n" + "\n".join(f"- {k} da [[{p}]]" for p, k in por_passagem[n]) + "\n"
        t = t.replace("\n## Aparece em", bloco + "\n## Aparece em", 1) if "\n## Aparece em" in t else t.rstrip() + "\n" + bloco
        open(f, "w").write(t)
print("parashiot:", len(dados), "· passagens marcadas:", len(por_passagem))
