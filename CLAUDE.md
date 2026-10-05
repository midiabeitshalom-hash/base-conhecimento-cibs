# Base de Conhecimento CIBS — instruções do projeto

Second brain em Markdown para o Obsidian com os estudos da Congregação Israelita Beit Shalom (CIBS):
escatologia, mesianologia, Torá e alianças, mística judaica, festas bíblicas, história e identidade
judaica. A base é da Beit Shalom, e o autor da maior parte dos estudos é o Rav Yosef. Tudo que o Mike
mandar vira nota `.md` conectada ao grafo e registrada nos índices. A base cresce por acúmulo: cada nota
nova cria conexões com o que já existe e segue a linha de pensamento registrada em `00 - Fundamentos`.

## Estrutura de pastas

```
RAW/                    caixa de entrada: rascunhos e kb-*.md ainda não organizados
RAW/_midia/             vídeos, áudios, PDFs e imagens a processar (fora do Git)
WIKI/
  000 - Índice Central CIBS.md
  00 - Fundamentos da Beit Shalom/     método do Rav Yosef, pilares doutrinários, guia de voz
  01 - <Categoria>/
    000 - Índice <Categoria>.md
    kb-<slug>.md                 notas de estudo (uma por fonte)
    Conceitos/<Conceito>.md      notas de conceito, pessoa ou lugar (uma por wikilink)
  Escrituras/
    000 - Índice Escrituras.md
    <Livro>/<Livro Cap.Vers>.md  uma nota por passagem bíblica linkada
  Fontes/
    000 - Índice Fontes.md
    <Obra>.md                    Talmud, Midrash, Zohar, Josefo, 1 Enoque, estudos acadêmicos…
scripts/atualizar_indices.py
```

Notas `kb-*.md` soltas em `RAW/` estão pendentes: mova cada uma para a categoria certa e rode o script.
Arquivos vazios em `RAW/` são stubs criados pelo Obsidian ao clicar num link cinza. Depois de criada a
nota real em `WIKI/`, apague o stub (o script acusa arquivos vazios).

## Antes de escrever qualquer nota

Leia as três notas de `WIKI/00 - Fundamentos da Beit Shalom/`:
- `kb-metodo-e-linha-de-pensamento-rav-yosef.md`: como o Rav Yosef pensa, argumenta e ensina;
- `kb-pilares-doutrinarios-beit-shalom.md`: as posições da Beit Shalom, cada uma ligada às notas que a sustentam;
- `kb-guia-de-voz-e-linguagem-beit-shalom.md`: vocabulário, termos hebraicos, grafias e tom.

Toda nota nova precisa ser coerente com elas. Se um estudo novo acrescentar algo ao método ou aos
pilares (uma posição nova, um argumento novo, uma ferramenta nova), acrescente nos Fundamentos com link
para a nota nova. Só acrescente, nunca reescreva.

## Categorias (taxonomia atual)

| Pasta | Escopo |
|---|---|
| `00 - Fundamentos da Beit Shalom` | método e linha de pensamento do Rav Yosef, pilares doutrinários, guia de voz e linguagem |
| `01 - Escatologia e Profecia` | tempo do fim, profecias, cronologia profética (semanas de Daniel, jubileus, 6.000 anos), marca da besta, arrebatamento, Nefilim |
| `02 - Mesianologia e Natureza do Messias` | identidade e natureza do Messias, Mashiach ben Yosef e ben David, monoteísmo estrito, Trindade, Yeshua × "Jesus" romano, prostração e adoração |
| `03 - Torá Lei e Aliança` | lei e graça, alianças, Nova Aliança, exegese paulina, mitzvot, kashrut, Shabat |
| `04 - Mística e Cosmogonia Judaica` | criação, Ein Sof, Tzimtzum, Or HaGanuz, Adam Kadmon, os 4 mundos, sefirot, Tikkun Olam, Éden |
| `05 - Festas e Ritos Bíblicos` | moedim (Pessach, Shavuot, Sucot…), imersão (tevilá), calendário bíblico, ressurreição |
| `06 - História Arqueologia e Identidade Judaica` | Segundo Templo, grupos judaicos do 1º século, Bnei Anussim, DNA abraâmico, identidade |

`Escrituras/` e `Fontes/` são áreas de referência, fora da numeração.

- Cada nota tem **uma** categoria (a pasta). As outras conexões são feitas por wikilink, sem duplicar a nota.
- `topic_category` = nome exato da categoria, sem o número (ex.: `"Escatologia e Profecia"`).
- A taxonomia não é fechada. Para decidir a categoria de um conteúdo novo:
  1. O assunto já aparece na base (`grep -ril "<termo>" WIKI`)? Vai para a categoria onde ele já vive.
  2. Não aparece, mas cabe no escopo de uma categoria? Vai para ela.
  3. Não conecta com nenhuma? Crie a categoria nova sem pedir: um domínio próprio, com nome amplo
     (`Oração e Liturgia`, e não `Amidá de Shabat`), no próximo número livre. Crie a pasta e o índice,
     acrescente a linha nesta tabela e inclua a categoria no "Ver também" de 1 ou 2 vizinhas. Avise o Mike.
  4. Se uma categoria passar de ~30 notas e houver um subgrupo claro com 8 ou mais, **proponha** o
     desmembramento ao Mike. Não execute sozinho.

## Fluxo de ingestão por tipo de entrada

1. **Link de vídeo** (YouTube, Instagram…): use a skill `transcrever-video`. A legenda e a descrição do
   post também são fonte. Distinga o que vem da fala, da legenda e do texto na tela quando isso mudar o
   sentido. Se a fala se referir a algo visual (um slide, um gráfico, um texto hebraico na tela), extraia
   frames antes de limpar a mídia.
2. **Vídeo ou áudio em `RAW/_midia/`**: trabalhe no scratchpad e transcreva com
   `ffmpeg -y -i <arquivo> -ar 16000 -ac 1 -c:a pcm_s16le audio.wav` e
   `whisper-cli -m ~/whisper-models/ggml-large-v3-turbo-q8_0.bin -f audio.wav -l pt -otxt -osrt -of transcript`.
   Não apague o original: depois de processado, mova para `RAW/_midia/_processados/`.
3. **Documento** (PDF, DOCX, TXT): leia inteiro (PDF em blocos de páginas). Um documento longo com temas
   distintos pode virar mais de uma nota.
4. **Imagem**: transcreva todo o texto, incluindo hebraico e grego, antes de extrair o conhecimento.
5. **Site ou artigo**: busque a página (WebFetch ou `firecrawl`).
6. **Texto colado no chat**: processe direto.

Várias fontes numa mensagem viram uma nota por fonte, salvo se o Mike pedir para juntar. Dois estudos
sobre o mesmo tema continuam em notas separadas (uma por fonte) e se linkam nos dois sentidos.

## Formato da nota de estudo (`kb-<slug>.md`)

Nome do arquivo: `kb-<slug>.md`, em minúsculas, sem acento, com hífen, curto e descritivo.

```markdown
---
title: "Título descritivo do conteúdo (frase normal, sem caixa alta e sem hashtag)"
titulo_original: "Título exato como foi publicado"
origem: beit-shalom | externa
creator_channel: "Congregação Israelita Beit Shalom"
autor_do_estudo: "Rav Yosef"
programa: "Nome do programa ou série, quando houver"
source_url: "URL ou descrição da fonte"
source_type: video | live | documento | imagem | site | texto | sintese
date_captured: AAAA-MM-DD
topic_category: "Nome exato da categoria"
tags: [tag-um, tag-dois]
type: universal-knowledge-base
knowledge_depth: exhaustive-academic
---

# Título descritivo

## Síntese Executiva e Tese Central
**Tese Central:** o núcleo do estudo.
**Contexto & Importância:** por que importa e que leitura comum ele corrige ou aprofunda.
**Nível de Complexidade & Pré-requisitos:** o que ajuda saber antes, com links para notas da base.

---

## Mapeamento de Entidades, Fontes e Referências Citadas
**Autor do estudo:** Rav Yosef — Congregação Israelita Beit Shalom.
**Figuras bíblicas e históricas**
**Escrituras** (agrupadas: Torá · Nevi'im · Ketuvim · Berit Hadashah)
**Literatura rabínica e judaica** (Mishná, Talmud com tratado e fólio, Midrash com seção, Targum, Zohar, comentaristas)
**Literatura do Segundo Templo e historiadores** (1 Enoque, Jubileus, Qumran, Flávio Josefo…)
**Estudos acadêmicos e científicos** (autores, ano, revista, DOI/link, desenho, amostra, resultados com números)
**Ferramentas e modelos conceituais** (PaRDeS, guematria, ciclos jubilares, tipologia…)

---

## Decomposição Analítica Exaustiva
### 1. <Tema>
### 2. <Tema>
(na ordem do estudo: argumentos, passo a passo do raciocínio, textos em hebraico e grego com
transliteração e tradução, números, datas, cálculos, guematria, analogias e exemplos usados)

---

## Glossário e Rede de Conexões
[[Conceito]] · [[Conceito]] · ...

**Notas relacionadas na base:** [[kb-arquivo|Título]] (uma frase sobre a relação) · ...

**Mini-glossário:** 5 a 10 termos, com hebraico/grego, transliteração e significado.

---

## Síntese de Princípios e Aplicação Prática
**Princípios Fundamentais Extraídos**
**Checklist de Aplicação**
- [ ] ação prática
```

Uma nota do mesmo tema, mesmo que de outra categoria, sempre entra em "Notas relacionadas na base".

## Autoria, voz e fontes

- `creator_channel` é sempre `"Congregação Israelita Beit Shalom"`. `autor_do_estudo` é `"Rav Yosef"`,
  ou o nome de outro professor da Beit Shalom quando for o caso.
- No texto, escreva o conhecimento direto ("A Torá precede o Sinai…") e atribua ao Rav Yosef quando
  marcar a posição ou o argumento dele ("Rav Yosef ensina que…", "Rav Yosef mostra pelo hebraico
  que…"). Nunca "o palestrante", "o pregador", "o vídeo", "a live", "o autor".
- **Fontes entram com nome e referência precisa:** Talmud (tratado + fólio: *Yoma 39b*), Midrash
  (obra + seção: *Bereshit Rabá 8:1*), Zohar (parashá/volume e folha), Targum, comentaristas (Rashi
  sobre Gênesis 1:26), Josefo (*Antiguidades* livro e seção), Qumran (manuscrito), estudos (autores,
  ano, revista, DOI). Cada obra citada tem nota em `WIKI/Fontes/` e é linkada (`[[Talmud Bavli]]`).
- Sábios, comentaristas e pesquisadores citados entram pelo nome: são fontes. Conceitos com nome
  próprio ficam (PaRDeS, Seder Olam Rabbah, os 13 princípios de Rambam).
- Material de fora da Beit Shalom (livro, curso, outro canal) leva `origem: externa`, com
  `creator_channel` e `autor_do_estudo` preenchidos com o autor real. O conhecimento é registrado com
  essa autoria e nunca é atribuído ao Rav Yosef. Quando o tema já tem posição nos Fundamentos, a nota
  se liga a ela em "Notas relacionadas na base".

## Regras de conteúdo

- **Registre o conhecimento, não uma auditoria da fonte.** É proibido incluir:
  - seções do tipo "Nuances, riscos e o que a fonte não diz";
  - rótulos de desconfiança: "fonte duvidosa", "não verificado", "carece de fonte", "especulativo",
    "não sabemos a origem", "apócrifo" usado para desqualificar (prefira "literatura do Segundo Templo");
  - conselhos do tipo "verifique a fonte primária" ou "consulte seu líder";
  - julgamentos sobre a confiabilidade do autor ou do canal.
- As críticas que o próprio estudo faz a outras doutrinas são conteúdo da Beit Shalom e ficam, na voz dela.
- Sem referência: escreva só `Sem referência específica citada.` O conteúdo fica registrado como está.
- Referências que você conheça e que conectem o tema (um texto do Talmud, um achado de Qumran) podem
  entrar no Mapeamento como conexão.
- Extração exaustiva: versículos, palavras hebraicas, valores de guematria, datas, cálculos de
  cronologia, analogias (ex.: a serra elétrica de Lei × Graça) e exemplos não podem se perder.
- Português do Brasil, texto natural (skill `escrita-natural`). Termos hebraicos em itálico na primeira
  ocorrência, com tradução.
- Na grafia de Deus no texto corrido (Deus, D'us, Hashem, Elohim), respeite a forma usada no estudo.

## Higiene de wikilinks e terminologia

- O alvo do link (antes do `|`) nunca tem `:`, `/` ou `\`. Versículos usam ponto: `[[Gênesis 1.26]]`.
- O texto de exibição nunca tem `|` (use travessão —).
- Nunca coloque wikilink entre crases: vira código e some do grafo.
- **Uma grafia por conceito em toda a base.** Antes de criar um link, procure a grafia já usada:
  `ls WIKI/*/Conceitos/ WIKI/Fontes/ | grep -i "<termo>"` e
  `grep -rhoE '\[\[[^]|]+' WIKI | sort | uniq -c | sort -rn`.
  Para mostrar outra forma, use o texto de exibição: `[[Moshe Rabenu|Moisés]]`. Cada nota de conceito
  lista suas variações em `aliases:` no frontmatter, e o Obsidian sugere o nome canônico pela variação.
- **Versículos:** o alvo é sempre `Livro Cap.Vers` do primeiro versículo da passagem, e o intervalo vai
  no texto de exibição: `[[Mateus 5.17|Mateus 5.17-19]]`. Para capítulo inteiro, trechos não contíguos
  ou passagens com mais de ~10 versículos, linke o capítulo: `[[Daniel 7|Daniel 7.1-8, 13-14]]`. Nomes
  dos livros em português, por extenso (`Salmo 119.142`, `1 Coríntios 15.51`).
- Pessoas e entidades diferentes nunca se fundem, mesmo com nomes parecidos: `Yochanan HaShaliach`
  (o apóstolo João) é uma nota e `João, o Imersor` é outra; `Adam HaRishon` (o primeiro homem) é uma e
  `Adam Kadmon` (o homem primordial da mística) é outra.
- Só vira link o que é um nó útil de conhecimento (conceito, pessoa bíblica ou histórica relevante,
  lugar, obra, passagem). Menção de passagem a algo fora do tema (uma marca, uma pessoa moderna citada
  de relance) fica em texto simples.
- Tags: minúsculas, sem acento, com hífen. Reutilize as existentes.

### Formas canônicas

(complete com as decisões da Fase 2)
- `[[Yeshua]]` (exibição livre: Yeshua HaMashiach, Yeshua de Nazaré)
- `[[Moshe Rabenu]]` (Moisés) · `[[Avraham Avinu]]` (Abraão) · `[[David HaMelech]]` (Rei Davi, Davi)
- `[[Yosef HaTzaddik]]` (José do Egito) · `[[Sha'ul HaShaliach]]` (Paulo de Tarso)
- `[[Adam HaRishon]]` (Adão, Adam) · `[[Adam Kadmon]]` (não confundir)
- `[[Kapará]]` (Capará, Kaparrah, Kaparot quando significa expiação)
- `[[Mitzvot]]` (Mitzvah) · `[[Kashrut]]` (Kosher) · `[[Shavuot]]` (Chag Shavuot, Pentecostes)
- `[[Profeta Daniel]]`, `[[Profeta Jeremias]]` (um só padrão para profetas)
- `[[Torá]]` · `[[Tanakh]]` · `[[Berit Hadashah]]` · `[[Ruach HaKodesh]]` · `[[Teshuvá]]` · `[[PaRDeS]]`
- `[[Mashiach]]` · `[[Mashiach ben Yosef]]` · `[[Mashiach ben David]]`
- `[[Clínica…]]` não existe aqui: o nome da instituição é `[[Congregação Israelita Beit Shalom]]`
- Tags: `tora` (não `torah`), `yeshua`, `berit-hadashah`

## Notas de conceito (`WIKI/NN - Categoria/Conceitos/<Nome exato do link>.md`)

Todo wikilink de conceito, pessoa, lugar ou evento tem nota própria, na categoria onde é mais usado.
**Nenhum link cinza.** A explicação vem do que a própria base ensina (as notas `kb-` e os Fundamentos),
aprofundada com conhecimento sólido (hebraico, fontes judaicas, contexto histórico), sempre coerente
com a posição da Beit Shalom.

- **Profundidade obrigatória.** Não é verbete de dicionário. Os conceitos centrais (os mais linkados,
  como Torá, Teshuvá, PaRDeS, Adam Kadmon, Mashiach ben Yosef, Tzimtzum, Shabat) passam de 400 palavras.
  Nenhum fica abaixo de ~160.
- Se o conceito já existe, reutilize o nome exato, acrescente a nota nova em "Aparece em" e aprofunde
  com o que ela trouxer.

```markdown
---
title: "<Conceito>"
type: concept
topic_category: "<Categoria>"
aliases: [Variação 1, Variação 2]
hebraico: "תּוֹרָה"           # quando houver
tags: [conceito, tag-um]
date_captured: AAAA-MM-DD
---

# <Conceito>

**Definição:** 1 a 3 frases precisas. Termo original, transliteração e tradução literal.

## Raiz e significado
Etimologia, raiz hebraica/grega, nuances que a tradução perde.

## Na Escritura
Passagens-chave, com links para `Escrituras/`.

## Nas fontes judaicas
O que Talmud, Midrash, Zohar e comentaristas dizem, quando a base usa essas fontes (com referência precisa).

## Na visão da Beit Shalom
A leitura da Beit Shalom e do Rav Yosef, amarrada às notas `kb-` e aos Fundamentos.

## Leituras que a Beit Shalom corrige
(quando houver) a leitura comum e por que a base a considera equivocada.

## Como explicar à congregação
Uma analogia ou imagem simples, pronta para virar aula ou post.

## Relacionados
[[Conceito]] · [[Conceito]]

## Aparece em
- [[kb-arquivo|Título]]
```

Para **pessoas**, as seções são: Quem é · Na Escritura · Na tradição judaica · Na leitura da Beit
Shalom · Relacionados · Aparece em.

## Notas de passagem bíblica (`WIKI/Escrituras/<Livro>/<Livro Cap.Vers>.md`)

```markdown
---
title: "Mateus 5.17"
type: escritura
livro: "Mateus"
grupo: "Berit Hadashah"          # Torá | Nevi'im | Ketuvim | Berit Hadashah
aliases: ["Mt 5.17", "Mateus 5:17", "Mateus 5.17-19"]
tags: [escritura, mateus]
date_captured: AAAA-MM-DD
---

# Mateus 5.17

> Texto da passagem (o intervalo citado pela base). Use a tradução que a base já usa; se não houver,
> a Almeida Corrigida Fiel.

**Original:** hebraico ou grego com transliteração, quando a base explora as palavras (ex.: *le'malei*, "cumprir").

## Contexto
Quem fala, para quem, em que momento, o que vem antes e depois.

## Leitura da Beit Shalom
Como a base lê a passagem (peshat, remez, derash e sod quando a base usa o PaRDeS), com links para as `kb-`.

## Conexões
Outras passagens e conceitos ligados.

## Aparece em
- [[kb-arquivo|Título]]
```

Mínimo de ~100 palavras. Passagens centrais (as que sustentam teses da base) passam de 250.

## Notas de fonte (`WIKI/Fontes/<Obra>.md`)

```markdown
---
title: "Talmud Bavli"
type: fonte
grupo: "Talmud"   # Escrituras e Targum | Mishná e Talmud | Midrash | Mística judaica | Comentaristas e codificadores | Literatura do Segundo Templo | Historiadores | Estudos acadêmicos e científicos
aliases: [Talmud Babilônico]
tags: [fonte, talmud]
date_captured: AAAA-MM-DD
---

# Talmud Bavli

**O que é:** natureza da obra, época, local, língua, estrutura (ordens, tratados, fólios).

## Como a Beit Shalom usa esta fonte
## Passagens citadas na base
- *Yoma 39b* — o que diz e em que estudo aparece ([[kb-…|…]])
## Relacionados
## Aparece em
```

Mínimo de ~120 palavras. Um trecho específico (ex.: *Yoma 39b*) ganha nota própria em `Fontes/` quando
a base o explica em detalhe ou o cita em 2 ou mais notas. Caso contrário, fica listado na nota da obra.

## Integração com a base (toda nota nova)

1. Leia o Índice Central, o índice da categoria provável e os três Fundamentos.
2. Escreva a nota `kb-` com "Notas relacionadas na base" apontando para notas reais.
3. Crie ou atualize as notas de conceito, de passagem e de fonte de todos os wikilinks que ela usa.
4. Reforce as notas antigas quando fizer sentido: acrescente um link para a nova em "Notas relacionadas
   na base" (só acrescente, nunca reescreva o conteúdo antigo). Atualize os Fundamentos se o estudo
   trouxer algo novo sobre o método ou as posições.
5. Rode `python3 scripts/atualizar_indices.py`. Ele reconstrói os índices (categorias, conceitos,
   Escrituras, Fontes, Central) e verifica a base. Precisa terminar com **0 erros**. Os avisos de nota
   curta devem ser resolvidos aprofundando a nota. Só verificar: `--checar`.
6. Faça commit local ao fim de cada lote (`Adiciona: <títulos>`). Push só com confirmação do Mike.
7. Responda ao Mike de forma curta: que notas criou, em que categoria e que conexões novas surgiram.

## Material novo no RAW ("subi um novo material")

O Mike pode mandar o conteúdo de três formas: um link (vídeo, site), um arquivo bruto em
`RAW/_midia/` (PDF, áudio, transcrição) ou um **rascunho pronto** em `RAW/`, gerado por outra IA com o
prompt de extração. O rascunho é um `kb-<slug>.md` com `status: aguardando-integracao`,
`categoria_sugerida` e, no fim, o bloco `## Notas para a integração`.

Quando o Mike disser que subiu material novo, ou pedir para integrar:
1. Liste `RAW/` e `RAW/_midia/`. Ignore stubs vazios (0 bytes) e `_processados/`. Link e arquivo bruto
   seguem o "Fluxo de ingestão". Rascunho pronto segue os passos abaixo.
2. **Confira o rascunho.** Se o original estiver em `RAW/_midia/` (PDF, transcrição), compare e
   complete o que faltar: versículos, termos hebraicos, números, analogias. Corrija termos mal
   transcritos e resolva o que estiver listado como dúvida. O que não der para resolver vai para a
   resposta ao Mike.
3. **Decida a categoria** pelas regras da seção "Categorias". `categoria_sugerida` é só uma sugestão.
   Se for preciso criar uma categoria nova, crie (pasta, índice, tabela deste arquivo, "Ver também")
   e avise o Mike.
4. **Normalize:** frontmatter completo e `topic_category` exato; grafias canônicas com texto de
   exibição; versículos no formato da base; nenhum link entre crases; título descritivo.
5. **Conecte:** preencha "Notas relacionadas na base" com notas reais. Leve o conteúdo de
   "Aporte à linha de pensamento" para os Fundamentos (só acrescentando, com link para a nota nova).
6. **Finalize:** apague `status`, `categoria_sugerida` e o bloco `## Notas para a integração`. Mova a
   nota para `WIKI/NN - Categoria/` e siga a "Integração com a base" (notas de conceito, passagens e
   fontes, reforço das notas antigas, script com 0 erros, commit). Mova o original de `RAW/_midia/`
   para `RAW/_midia/_processados/`.
7. Responda ao Mike de forma curta: nota criada, categoria (e se é nova), conexões novas e dúvidas
   que ficaram.

O script acusa erro se uma nota na `WIKI/` ainda tiver `status`, `categoria_sugerida` ou o bloco de
integração.

## Formato dos índices

Índice de categoria (`000 - Índice <Categoria>.md`). O script gera as seções de notas e de conceitos.
O escopo e o "Ver também" são escritos à mão.

```markdown
---
title: "Índice <Categoria>"
type: index-node
topic_category: "<Categoria>"
tags: [indice, moc, <tag-da-categoria>]
date_captured: AAAA-MM-DD
---

# <NN> — <Categoria>

Uma frase de escopo.

## Notas desta categoria

## Conceitos desta categoria

## Ver também
- [[000 - Índice <Categoria vizinha>|<Categoria vizinha>]]
- [[000 - Índice Central CIBS|Índice Central]]
```

`Escrituras/000 - Índice Escrituras.md` tem a seção `## Passagens` (gerada na ordem do cânon:
Torá, Nevi'im, Ketuvim, Berit Hadashah). `Fontes/000 - Índice Fontes.md` tem `## Obras e referências`
(gerada por grupo). O Índice Central tem `## Categorias (...)`, `## Referências` e
`## Todas as notas (ordem alfabética)`, todas geradas pelo script.
