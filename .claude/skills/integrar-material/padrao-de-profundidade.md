# Padrão de profundidade da Base CIBS

Toda nota `kb-` precisa ficar no nível das 35 notas que já estão na base (hoje entre 2.200 e 3.500
palavras). Quem ler a nota deve conseguir dar a aula sem ter visto o vídeo. Use como referência de
qualidade, por exemplo, `WIKI/03 - Torá Lei e Aliança/kb-lei-x-graca.md` e
`WIKI/02 - Mesianologia e Natureza do Messias/kb-o-messias-e-a-serpente.md`.

## Metas de tamanho (nota `kb-`, sem contar o frontmatter)

| Fonte | Meta |
|---|---|
| Reel, short ou post de até 3 min | 800 a 1.500 palavras (o conteúdo do material mais contexto e conexões da base) |
| Vídeo de 5 a 20 min | 1.800 a 3.000 |
| Live ou aula de 30 min a 2 h | 3.000 a 6.000 |
| PDF ou artigo | proporcional: nada do argumento, dos dados ou das citações pode sumir |
| Anotação curta ou texto raso | o que ele traz, mais o aprofundamento com a base, sem inventar posição |

Se a nota ficar abaixo da meta, quase sempre faltou decompor o raciocínio, citar os versículos ou trazer
as analogias. Volte à fonte antes de "encher" com texto genérico.

## O que cada seção precisa ter

**Síntese Executiva e Tese Central**
- Tese em 2 a 4 frases, afirmativa, na voz da base.
- Contexto & Importância: que leitura comum o estudo corrige ou aprofunda e por que isso importa.
- Pré-requisitos: com links para as notas da base que ajudam a entender.

**Mapeamento de Entidades, Fontes e Referências Citadas** (7 grupos, nesta ordem)
- Autor do estudo · Figuras bíblicas e históricas · Escrituras (Torá · Nevi'im · Ketuvim · Berit
  Hadashah) · Literatura rabínica e judaica · Literatura do Segundo Templo e historiadores · Estudos
  acadêmicos e científicos · Ferramentas e modelos conceituais.
- Cada item com uma linha dizendo **para que** o estudo o usa.
- Talmud sempre com tratado e fólio (*Yoma 39b*), Midrash com seção (*Bereshit Rabá 8:1*), Josefo
  com obra, livro e seção, estudos com autores, ano, revista e números.
- Grupo vazio: `Sem referência específica citada.`
- Conexões que você conhece e que fortalecem o tema podem entrar, marcadas como conexão.

**Decomposição Analítica Exaustiva** (a parte mais longa)
- Uma subseção `### N. Tema` para cada bloco do estudo, na ordem em que aparece.
- Dentro de cada uma: o argumento passo a passo ("primeiro…, depois…, por isso…"), não só a conclusão.
- Todo versículo citado, com a referência e o trecho (tradução que o estudo usa).
- Toda palavra hebraica ou grega explorada: escrita original, transliteração em itálico, tradução e o
  ponto que o estudo tira dela. Ex.: *le'malei* (לְמַלֵּא), "cumprir, preencher", que em Mateus 5.17
  significa interpretar corretamente, e não abolir.
- Números e cálculos completos, mostrando a conta: guematria (נחש = 358 = משיח), cronologias (6.000
  anos, 70 semanas, jubileus de 50 anos), datas.
- Analogias e exemplos com a imagem inteira, porque são o que a congregação lembra (ex.: a serra
  elétrica de Lei × Graça).
- Citações de fontes judaicas com o que elas dizem e como o estudo as usa (ex.: *Yoma 39b*, os
  40 anos em que a fita escarlate deixou de embranquecer).
- As críticas que o estudo faz a outras doutrinas, na voz da Beit Shalom.

**Glossário e Rede de Conexões**
- Linha de wikilinks com os conceitos centrais do estudo (só grafias canônicas e com nota).
- Notas relacionadas na base: de 3 a 8 notas `kb-` reais, cada uma com uma frase de relação. Se houver
  parashá, `[[Parashá <Nome>]]` entra aqui.
- Mini-glossário: de 5 a 10 termos com hebraico ou grego, transliteração e significado.

**Síntese de Princípios e Aplicação Prática**
- De 4 a 8 princípios numerados, cada um com uma frase de justificativa.
- Checklist de aplicação com ações concretas (`- [ ]`).

## Aprofundar material raso (sem inventar)
Quando o material traz pouco (um post, um resumo genérico de outra IA, três parágrafos):
1. Registre tudo que ele traz.
2. Procure o tema na base: `grep -ril "<termo>" WIKI`. Leia as notas `kb-`, os conceitos e os Pilares.
3. Aprofunde com o que a base já ensina: hebraico, versículos, fontes, analogias que outras notas usam.
   Escreva como conexão ("A base já mostra em [[kb-…|…]] que…").
4. Complete o contexto bíblico e histórico com conhecimento sólido (hebraico, fontes judaicas com
   referência precisa), sempre coerente com os Fundamentos.
5. Não atribua ao Rav Yosef o que ele não disse no material. Na dúvida, escreva o conhecimento direto,
   sem atribuição, ou atribua à base ("a Beit Shalom ensina…") quando estiver nos Pilares.

## Correção de transcrição
O Whisper erra nomes e termos. Corrija pelo contexto e pelas grafias canônicas do `CLAUDE.md`:
- nomes: Yeshua, Rav Yosef, Beit Shalom, Moshe Rabenu, Sha'ul, Yosef, Avraham;
- termos: Torá, Shabat, teshuvá, kapará, mitzvot, kashrut, Mashiach ben Yosef, Adam Kadmon, Ein Sof,
  Tzimtzum, Or HaGanuz, sefirot, PaRDeS, guematria, Berit Hadashah, Ruach HaKodesh, moedim, tevilá;
- referências: confira livro, capítulo e versículo pelo texto citado. Se a fala diz "em Romanos dez"
  e cita "o fim da Lei é o Messias", é Romanos 10.4.
O que não der para identificar com segurança vai para as dúvidas da resposta ao Mike (com o trecho e o
minuto). Não chute.

## Controle de qualidade (antes do commit)
- [ ] Todos os itens do inventário (passo 2 da skill) estão na nota.
- [ ] A nota está dentro da meta de tamanho para o tipo de fonte.
- [ ] As 5 seções na ordem certa; o Mapeamento nos 7 grupos.
- [ ] Cada versículo tem referência; cada termo hebraico tem transliteração e tradução.
- [ ] Cálculos e guematria com a conta mostrada.
- [ ] Analogias e exemplos completos.
- [ ] Frontmatter completo (`title` descritivo, `titulo_original`, `origem`, `autor_do_estudo`,
      `source_url`, `source_type`, `date_captured`, `topic_category` exato, `tags`, `type`,
      `knowledge_depth`; `parasha` quando houver).
- [ ] Nenhum link cinza, nenhum link entre crases, nenhum `:` ou `/` no alvo.
- [ ] Voz da base, sem "o palestrante", "o vídeo" e sem rótulo de desconfiança.
- [ ] Coerente com os Pilares. Se houver conflito, ele vai para as dúvidas ao Mike.
- [ ] `python3 scripts/atualizar_indices.py` com 0 erros e 0 avisos.
