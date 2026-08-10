# S5proj_Bromelia_distribuition
# Dashboard Bromeliaceae do Brasil

Aplicativo web interativo para explorar os registros de coleta da família **Bromeliaceae**
no Brasil, cruzando as ocorrências do GBIF com a distribuição por bioma da
Flora e Funga do Brasil.

## Objetivos do projeto:
## Para que serve

Bromeliaceae é uma das famílias mais diversas do Brasil e um grupo de interesse
para conservação, com muitas espécies endêmicas e restritas a um único bioma.
Este dashboard permite responder, de forma visual, perguntas como:

- Quando as bromélias brasileiras foram coletadas? Houve períodos de maior
  esforço de coleta?
- Quais espécies têm ampla distribuição mas poucos registros — ou seja, onde
  estão as lacunas de amostragem?
- Como a riqueza de espécies se compara ao número de registros em cada bioma?
## Funcionalidades

- **Histograma** do ano de coleta dos registros, mostrando a evolução do esforço
  de coleta ao longo do tempo.
- **Gráfico de dispersão** por espécie, cruzando o número de registros no GBIF
  com a amplitude geográfica segundo a Flora do Brasil, colorido por bioma.
- **Caixas de seleção** para escolher quais gráficos exibir.
- **Filtro por intervalo de anos**, que atualiza os dois gráficos.

## Fontes de dados

| Fonte | O que fornece | Referencia |
|---|---|---|
| GBIF | Ocorrências: nome aceito, ano de coleta, coordenadas, estado | GBIF.org (10 August 2026) GBIF Occurrence Download https://doi.org/10.15468/dl.qvrga3|
| Flora e Funga do Brasil (JBRJ) | Distribuição por bioma e por estado das espécies aceitas |Flora e Funga do Brasil (Constantly updated): Flora e Funga do Brasil project - Projeto Flora e Funga do Brasil. Instituto de Pesquisas Jardim Botânico do Rio de Janeiro.|

A divisão entre as duas fontes é intencional: o GBIF já entrega os nomes com
sinônimos resolvidos e as datas de coleta, enquanto o bioma é uma informação que
só a Flora do Brasil disponibiliza.

## Origem e preparo dos dados

Os dados brutos (GBIF e Flora e Funga do Brasil) foram baixados e processados
em um repositório separado (`[nome-do-repo-de-preparo]`), responsável apenas
pela extração, limpeza e agregação. Este repositório consome apenas as
saídas já processadas, em `data/processed/`:

| Arquivo | Granularidade | Usado em |
|---|---|---|
| `especies_resumo.csv` | 1 linha por espécie | Gráfico de dispersão |
| `ocorrencias_por_ano.csv` | 1 linha por ano | Histograma |
| `bioma_riqueza_vs_registros.csv` | 1 linha por bioma | — |
| `ocorrencias_por_estado.csv` | 1 linha por UF | — |

O código de preparo (coleta via GBIF, cruzamento com biomas da Flora e Funga
do Brasil, limpeza e agregação) está documentado em `[link ou caminho do
repositório de preparo]`.

## Uso de IA no desenvolvimento

Parte dos scripts de preparação e limpeza de dados foi desenvolvida com
apoio de um assistente de IA (Claude, Anthropic), sob minha supervisão e
revisão. Isso incluiu: estruturação inicial dos scripts de coleta/limpeza,
sugestões de tratamento de erros e correção de problemas de tipagem
identificados pelo linter (Pylance).

Todas as decisões metodológicas — quais colunas usar, como tratar
sinonímia taxonômica, quais critérios de limpeza aplicar (ex: faixa de anos
válida, remoção de coordenadas (0,0), reconciliação de nomes entre GBIF e
Flora do Brasil) — foram definidas e revisadas por mim, com base no meu
conhecimento de botânica e do problema.

## Limitações dos dados

Dados de biodiversidade como os do GBIF **não são um censo**: refletem
esforço de coleta, não necessariamente a distribuição real das espécies.
Isso implica algumas limitações importantes para a interpretação dos
resultados:

- **Viés de amostragem geográfico**: áreas de mais fácil acesso (perto de
  cidades, universidades, estradas) tendem a ter mais registros, o que pode
  inflar artificialmente a "amplitude de distribuição" de espécies nessas
  regiões.
- **Viés temporal**: o número de registros por ano reflete tanto mudanças
  reais quanto o aumento do esforço de digitalização de acervos ao longo do
  tempo (especialmente digitalização de herbários nas últimas décadas).
- **Qualidade variável dos registros**: nem todos os registros do GBIF são
  verificados por especialista; incluem observações de cidadãos-cientistas
  junto com material de herbário tradicional. O campo `basisOfRecord` foi
  usado para excluir alguns tipos não representativos de coleta em campo
  (ex: espécimes fósseis, material vivo em cultivo), mas isso não elimina
  todo ruído.
- **Reconciliação taxonômica imperfeita**: o cruzamento entre nomes do GBIF
  e da Flora e Funga do Brasil depende de correspondência de nome
  científico; sinônimos não completamente normalizados podem gerar
  espécies "órfãs" (sem bioma correspondente) — a taxa de cruzamento bem-
  sucedido está reportada no log do script de preparação.

Esses dados são adequados para uma análise **exploratória e descritiva**,
não para inferências causais sobre distribuição real de espécies sem
validação adicional.

## Estrutura do projeto

```
.
├── README.md
├── app.py                        # aplicativo Streamlit
├── requirements.txt
├── .streamlit/
│   └── config.toml               # configuração exigida pelo Render
├── scripts/
│   ├── 01_biomas_flora.py        # Flora  -> tabela espécie x bioma
│   └── 02_prepara_gbif.py        # GBIF   -> ocorrências limpas e agregados
├── notebooks/
│   └── EDA.ipynb                 # análise exploratória
└── data/
    ├── raw/                      # downloads originais (não versionados)
    └── processed/                # dados tratados, lidos pelo aplicativo
```

Os arquivos brutos ficam fora do repositório por causa do tamanho. O que é
versionado são os scripts que os transformam e os arquivos já tratados, de modo
que o resultado é reproduzível a partir dos downloads originais.

## Como reproduzir

Requer Python 3.10 ou superior.

```bash
# 1. Ambiente virtual
python -m venv .venv
source .venv/bin/activate        # no Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. Baixar os dados brutos para data/raw/
#    - Flora e Funga do Brasil: pacote Darwin Core Archive (DwC-A) do IPT
#    - GBIF: filtros Scientific name = Bromeliaceae, Country = Brazil,
#      Occurrence status = Present, Has coordinate = yes; formato "Simple" (CSV)

# 3. Preparar os dados
python scripts/01_biomas_flora.py --entrada data/raw/dwca_flora.zip
python scripts/02_prepara_gbif.py --fonte download --arquivo data/raw/gbif.zip

# 4. Rodar o aplicativo
streamlit run app.py
```

## Tratamento aplicado aos dados

Etapas executadas pelos scripts antes da visualização:

- Filtragem para a família Bromeliaceae, considerando apenas nomes aceitos.
- Extração do bioma a partir do campo `occurrenceRemarks` da Flora, que traz a
  informação em formato JSON dentro de uma única coluna.
- Remoção de registros sem ano de coleta ou sem coordenadas válidas, incluindo
  coordenadas em (0, 0) e pontos fora dos limites aproximados do Brasil.
- Descarte de registros que não representam coleta em campo (espécimes fósseis
  e material vivo cultivado).
- Padronização dos nomes de estado para siglas de UF.
- Cruzamento entre as espécies do GBIF e a tabela de biomas da Flora.

## Limitações conhecidas

- Nem toda espécie registrada no GBIF consta na tabela de biomas da Flora —
  espécies exóticas ou cultivadas aparecem como "Sem informação".
- O bioma é atribuído a partir da distribuição conhecida da espécie, e não das
  coordenadas de cada registro. Espécies presentes em mais de um bioma têm seus
  registros contabilizados em todos eles, por isso a tabela por bioma também traz
  uma contagem ponderada.
- O número de registros reflete o esforço histórico de coleta, não a abundância
  real das espécies. Regiões de acesso mais fácil tendem a estar
  sobrerrepresentadas.

## Tecnologias

`pandas` · `plotly-express` · `streamlit` · hospedagem no Render

---

Projeto desenvolvido para a Sprint 5 do curso de Ciência de Dados da TripleTen.