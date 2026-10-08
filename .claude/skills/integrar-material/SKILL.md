---
name: integrar-material
description: Transforma qualquer material que o Mike mandar (link de vídeo, áudio, transcrição, PDF, imagem, texto colado, resumo de outra IA, anotação solta) numa nota de estudo completa da Base CIBS, na profundidade e no formato da base, e integra ao grafo (conceitos, fontes, parashá, índices, commit). Use SEMPRE que chegar conteúdo novo nesta pasta ou no chat para a base, mesmo sem o prompt de extração, e quando o Mike disser "subi um material", "coloca na base", "integra isso", "olha esse vídeo", ou só mandar um link ou arquivo.
---

# /integrar-material

O material quase nunca chega pronto. Pode ser um link, uma transcrição crua, um resumo raso de outra IA
ou três linhas de anotação. Seu trabalho é sempre o mesmo: **extrair tudo o que o material contém, na
profundidade da base, e conectar ao que já existe.** O formato e as regras estão no `CLAUDE.md`. Este
arquivo diz como chegar lá a partir de qualquer entrada. O padrão de profundidade está em
`padrao-de-profundidade.md`, nesta pasta: leia antes de escrever.

## 0. Preparar (toda vez)
1. Leia o `CLAUDE.md` da raiz, o `WIKI/000 - Índice Central CIBS.md` e os três Fundamentos em
   `WIKI/00 - Fundamentos da Beit Shalom/`.
2. Leia `padrao-de-profundidade.md` (nesta pasta).
3. `git pull` se houver internet, para trabalhar sobre a versão mais nova.

## 1. Obter o conteúdo bruto completo
Nunca trabalhe só com um resumo se a fonte original estiver ao alcance.

| Entrada | O que fazer |
|---|---|
| Link de vídeo (YouTube, Instagram, TikTok) | Skill `transcrever-video`. Use também a legenda e a descrição do post. Extraia frames se a fala apontar para algo na tela (slide, texto hebraico, gráfico). |
| Vídeo ou áudio em `RAW/_midia/` | `ffmpeg` + `whisper-cli` (comandos no `CLAUDE.md`). Depois mova o original para `RAW/_midia/_processados/`. |
| Transcrição (.txt, .srt) | Leia inteira. Corrija termos mal transcritos pelo contexto (ver "Correção de transcrição" no padrão). |
| PDF, DOCX | Leia inteiro, em blocos de páginas. Tabelas e notas de rodapé também são conteúdo. |
| Imagem, print, slide | Transcreva todo o texto, incluindo hebraico e grego, antes de qualquer outra coisa. |
| Site ou artigo | Busque a página inteira (WebFetch ou skill `firecrawl`). |
| Texto colado ou anotação curta | Processe direto. Se for raso, aprofunde com a própria base (ver passo 3). |
| Rascunho pronto de outra IA (`kb-*.md` com `status: aguardando-integracao`) | Siga "Material novo no RAW" do `CLAUDE.md`. Ainda assim confira a profundidade pelo padrão. |
| Resumo genérico de outra IA, sem o formato da base | Trate como fonte bruta: extraia, reorganize e complete. Se o original (vídeo, PDF) estiver disponível, volte a ele. |

Trabalhe no scratchpad ou em `/tmp`. Nada de mídia dentro de `WIKI/`.

## 2. Inventário antes de escrever
Antes da nota, faça uma lista de trabalho (só para você) com tudo que o material traz:
- a tese central e as subteses;
- **cada** versículo citado (com livro, capítulo e versículo; deduza a referência quando o estudo cita
  o texto sem dar o endereço);
- cada palavra hebraica, aramaica ou grega, com a explicação dada;
- números, datas, cálculos, guematria, cronologias;
- analogias, exemplos, histórias e imagens usadas para explicar;
- pessoas, obras e fontes citadas (Talmud com fólio, Midrash com seção, Zohar, comentaristas,
  historiadores, estudos científicos com autores e ano);
- críticas que o estudo faz a outras leituras;
- aplicações práticas e chamados à ação.

Essa lista é o seu checklist. No fim, todo item dela precisa estar na nota.

## 3. Escrever a nota `kb-`
- Siga o modelo do `CLAUDE.md` ("Formato da nota de estudo"). As 5 seções, nessa ordem.
- **Decomposição Analítica Exaustiva**: uma subseção `###` por tema, na ordem do estudo, com o
  raciocínio passo a passo. É a parte mais longa da nota.
- Tamanho: a nota nunca é menor que o conteúdo útil da fonte. Uma aula de 1 hora costuma dar de 3.000 a
  6.000 palavras. Um reel de 1 minuto dá de 800 a 1.500 (com contexto e conexões da base). Veja as metas
  no padrão.
- Material raso (anotação, post curto): registre o que ele traz e **aprofunde com o que a base já
  ensina** (notas `kb-`, conceitos, Fundamentos), sempre deixando claro o que é do material e o que é
  conexão. Não invente posição que a base não tem.
- Voz: o conhecimento direto e "Rav Yosef ensina que…" quando for a posição dele. Material de fora:
  `origem: externa` e o autor real. Nada de rótulo de desconfiança (lista no `CLAUDE.md`).
- Português natural (skill `escrita-natural`). Termos hebraicos em itálico com tradução na primeira vez.

## 4. Conectar
1. **Categoria:** pelas regras do `CLAUDE.md` (onde o assunto já vive; senão o escopo; senão categoria
   nova, avisando o Mike).
2. **Wikilinks:** só com a grafia canônica (procure antes com `ls WIKI/*/Conceitos/ WIKI/Fontes/` e as
   "Formas canônicas"). Todo link de conceito, pessoa ou fonte precisa ter nota. Se não existir, **crie a
   nota** no modelo do `CLAUDE.md` (conceito: mínimo ~160 palavras; fonte: ~120). Se não valer uma nota,
   deixe em texto simples.
3. **Passagens bíblicas:** só linke as que já têm nota em `WIKI/Escrituras/`. As outras ficam em texto
   simples (`Isaías 9.6`). Se a passagem for central para a tese ou já aparecer em 3 ou mais notas `kb-`,
   crie a nota da passagem e passe a linkar.
4. **Parashá:** se o estudo trata de uma parashá, ou se a maioria dos versículos cai numa delas
   (veja as leituras em `WIKI/Parashiot/`), ponha `parasha: "Parashá <Nome>"` no frontmatter, linke
   `[[Parashá <Nome>]]` em "Notas relacionadas na base" e acrescente o estudo na nota da parashá.
5. **Notas relacionadas:** de 3 a 8 notas `kb-` reais, com uma frase sobre a relação. Acrescente o link
   de volta nas notas antigas (só acrescentar). Atualize "Aparece em" dos conceitos e fontes usados.
6. **Fundamentos:** se o estudo traz posição, argumento ou ferramenta nova, acrescente em
   `kb-pilares-doutrinarios-beit-shalom.md` ou `kb-metodo-e-linha-de-pensamento-rav-yosef.md`, com link.

## 5. Conferir e fechar
1. Releia o inventário do passo 2: marque cada item na nota. Faltou algo? Volte e inclua.
2. Passe o "Controle de qualidade" do `padrao-de-profundidade.md`.
3. `python3 scripts/atualizar_indices.py` precisa terminar com **0 erros e 0 avisos**.
4. Apague stubs vazios em `RAW/` que a nota resolveu. Mova os originais para `RAW/_midia/_processados/`.
5. Commit local: `Adiciona: <título>`. **Push só quando o Mike confirmar.**
6. Responda ao Mike em poucas linhas: nota criada (título e categoria), conceitos e fontes novos,
   parashá ligada, conexões novas e as dúvidas que ficaram (termo que não deu para identificar,
   referência incerta, possível conflito com os Pilares).
