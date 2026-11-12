# Prompt de extração da Beit Shalom

**Para que serve:** extrair, de um vídeo ou aula, TUDO o que o professor ensina **e como ele ensina**, para que a base guarde o
conteúdo completo e os estudos novos saiam no mesmo padrão de linguagem e de raciocínio do Rav Yosef.

**Como usar**
1. **Em outra IA (Gemini, ChatGPT):** cole o bloco abaixo, ponha o link do vídeo no fim, salve a resposta como `kb-<slug>.md` em
   `RAW/` e diga ao Claude Code "subi um material".
2. **Aqui, no Claude Code:** quando o Mike mandar um link, um vídeo ou uma transcrição para extrair, o Claude segue este
   mesmo roteiro (itens de conteúdo e de forma de ensinar) ao ler o material e ao escrever a nota, e termina a nota com as seções
   "Assinatura de ensino desta aula" e "Frases do Rav Yosef". O que for novo na forma de ensinar entra em
   `WIKI/00 - Fundamentos da Beit Shalom/kb-assinatura-de-ensino-do-rav-yosef.md`.

O bloco é a versão em vigor. Quando for melhorado, atualize este arquivo.

---

```
Assista ao vídeo do link abaixo INTEIRO, do primeiro ao último minuto, com áudio e imagem. Sua missão é uma só: extrair TUDO o que o estudo ensina, com toda a profundidade e COM A FORMA COMO O PROFESSOR ENSINA, sem perder nada. O resultado vai para a base de conhecimento da Congregação Israelita Beit Shalom, onde outra IA fará as conexões e usará o seu material para escrever novos estudos no mesmo padrão de linguagem e de raciocínio do professor. Você não precisa organizar a base, criar links ou categorias: precisa só não deixar nada para trás.

COMO ASSISTIR
- Assista ao vídeo completo. Não resuma pelo título nem pela descrição.
- Capture o que aparece na tela (slides, versículos, hebraico ou grego, mapas, gráficos, tabelas, números) e marque assim: [na tela: …].
- Use a descrição do vídeo como fonte complementar.

O QUE NÃO PODE SE PERDER (CONTEÚDO)
1. A tese central e cada subtese, na ordem em que aparecem.
2. O raciocínio passo a passo: como ele sai de um ponto e chega ao outro, com os "porquês" e os "então", e não só as conclusões.
3. Todos os versículos citados ou lidos, com livro, capítulo e versículo e o trecho como foi lido. Se ele citar o texto sem a referência, identifique a referência.
4. Toda palavra hebraica, aramaica ou grega: escrita original, transliteração, tradução e a explicação que ele dá (raiz, letra, sentido que a tradução perde).
5. Números, datas, cronologias, cálculos e guematria, com a conta mostrada exatamente como ele faz.
6. Analogias, imagens, histórias, exemplos e comparações, contados por inteiro.
7. Fontes citadas, com a referência que ele der: Talmud (tratado e fólio), Midrash, Zohar, Targum, comentaristas, Josefo, Qumran, livros, estudos, pesquisadores.
8. As críticas que ele faz a outras leituras ou doutrinas e os argumentos que usa contra elas.
9. As perguntas que ele faz à congregação, as respostas a perguntas do público e os chamados à ação.

O QUE NÃO PODE SE PERDER (A FORMA DE ENSINAR)
Observe e registre COMO ele ensina, além do que ensina. Quero poder reproduzir o padrão dele:
a) A ABERTURA: a saudação, como situa o público, como anuncia o tema, por que diz que importa, o que promete a quem ficar até o fim, que perguntas põe na mesa antes de responder. Copie as frases exatas.
b) A ORDEM DO RACIOCÍNIO: liste, na ordem real em que ele faz, os movimentos da aula (por exemplo: tese, versículo lido, pista no texto, ponte com outro texto, fonte judaica, analogia, refutação, aplicação). Diga em que minuto cada movimento começa.
c) COMO LÊ UM TEXTO: se lê o versículo inteiro, se dá o contexto (quem fala, a quem, quando), se mostra o hebraico, em que nível do PaRDeS diz estar (peshat, remez, derash ou sod), se usa kal vachomer ou guematria, e como anuncia cada ferramenta.
d) AS PERGUNTAS: as perguntas retóricas que ele faz e como as responde ("Qual é o receio dele? …").
e) AS TRANSIÇÕES E OS PEDIDOS DE ATENÇÃO: as expressões que ele usa para passar de um ponto a outro, chamar a atenção, verificar se entenderam, marcar o ponto central ("preste atenção", "olha que informação interessante", "consegue entender?"). Liste as que se repetirem, com o minuto de alguns exemplos.
f) AS ANALOGIAS: de onde ele as tira (cotidiano, ciência, objetos) e onde as coloca em relação ao versículo (antes ou depois de prová-lo).
g) COMO CONFRONTA UM ERRO: como descreve a leitura comum, como a desmonta, como aponta a origem do desvio e o tom que usa com quem pensa diferente.
h) O TOM: como fala com a congregação (nós, vocês), o que pede que façam, como mistura rigor e acolhida.
i) O FECHAMENTO: como retoma a tese, o que deixa em aberto, o que pede (curtir, compartilhar, inscrever, curso, discipulado, contribuição, próxima aula) e como se despede.
j) AS FRASES MARCANTES: as formulações dele que resumem uma ideia, entre aspas, com o minuto. Prefira citar a parafrasear.

COMO ESCREVER
- Escreva o conhecimento na voz da Beit Shalom: "Rav Yosef ensina que…", "Rav Yosef mostra pelo hebraico que…". Nunca "o palestrante", "o pregador", "o vídeo", "a live".
- Use os termos como ele usa (Yeshua, Torá, Shabat, D'us ou Hashem, teshuvá, kapará, Mashiach…) e respeite a grafia de Deus que ele usa.
- Registre o ensino como ele é. Não acrescente ressalvas, avisos, "nuances", "o outro lado" nem rótulos como "especulativo" ou "não verificado". Não corrija nem suavize as posições dele.
- Se o professor não for o Rav Yosef, use o nome do professor no lugar.

TAMANHO
A nota tem que ser do tamanho do conteúdo, nunca menor. Referência (sem contar a transcrição): até 3 min → 800 a 1.500 palavras; de 5 a 20 min → 1.800 a 3.000; live ou aula de 30 min a 2 h → 3.000 a 6.000. Se ficar abaixo, volte ao vídeo; não encha com texto genérico.

ENTREGA
Tudo num único bloco de código markdown, para eu copiar e salvar. Na primeira linha, fora do bloco, escreva o nome sugerido: kb-<slug>.md (minúsculas, sem acento, com hífen).

Dentro do bloco:

---
title: "Título descritivo em frase normal"
titulo_original: "Título exato do vídeo"
autor_do_estudo: "Rav Yosef"
programa: "Programa, série ou módulo do curso, se houver"
source_url: "link do vídeo"
duracao: "mm:ss"
date_captured: AAAA-MM-DD
status: aguardando-integracao
---

# Título descritivo

## Tese central
2 a 4 frases com o núcleo do estudo, como o Rav Yosef o formula.

## Desenvolvimento do estudo
### 1. <Tema> (a partir de mm:ss)
### 2. <Tema> (a partir de mm:ss)
Uma subseção para cada bloco, na ordem do vídeo, com tudo dos itens 1 a 9, na linguagem dele. É a parte mais longa.

## Assinatura de ensino desta aula
Os itens a) a i) acima, respondidos para este vídeo, com as frases exatas e os minutos. É aqui que fica registrado COMO ele ensinou.

## Frases do Rav Yosef
As formulações marcantes, entre aspas, com o minuto.

## Versículos citados
Lista completa, na ordem: referência, trecho lido e para que ele usou.

## Termos hebraicos e gregos
Lista completa: original, transliteração, tradução e a explicação dada.

## Fontes citadas
Lista completa, com a referência que ele deu e para que usou.

## Aplicação e chamados à congregação
O que ele pede que a congregação entenda, mude ou pratique.

## Dúvidas
Termos não identificados, referências incertas e trechos inaudíveis, com o minuto.

## Transcrição completa
Toda a fala, do início ao fim, com marcação de minuto a cada parágrafo, por exemplo [12:30], e [na tela: …] quando for relevante.

LINK DO VÍDEO:
[cole aqui]
```
