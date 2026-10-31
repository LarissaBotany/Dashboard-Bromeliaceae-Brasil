# S5proj_Bromelia_distribuition
# Dashboard Bromeliaceae do Brasil

Aplicativo web interativo para explorar os registros de coleta da família
**Bromeliaceae** no Brasil, a partir de dados de ocorrência do GBIF cruzados com
a distribuição por bioma da Flora e Funga do Brasil.

**Aplicativo online:** https://s5proj-bromelia-distribuition.onrender.com
**GitHub** https://github.com/LarissaBotany/Dashboard-Bromeliaceae-Brasil

## Para que serve

Bromeliaceae é uma das famílias mais diversas do Brasil e um grupo de interesse
para conservação, com muitas espécies endêmicas e restritas a um único bioma.
Este dashboard permite responder, de forma visual, perguntas como:

- Quando as bromélias brasileiras foram coletadas? Houve períodos de maior
  esforço de coleta?
- O aumento no número de registros ao longo do tempo corresponde a um aumento no
  número de espécies distintas coletadas, ou apenas à repetição das mesmas
  espécies?


## Funcionalidades

- **Visualizador de dados**: tabela com os registros que alimentam os gráficos.
- **Histograma** do ano de coleta, mostrando a evolução do esforço de coleta ao
  longo do tempo.
- **Gráfico de dispersão** cruzando, para cada ano, o número de registros com o
  número de espécies distintas coletadas.
- **Botões** que geram cada gráfico sob demanda.


## Fontes de dados

| Fonte | O que fornece | Referencia |
|---|---|---|
| GBIF | Ocorrências: nome aceito, ano de coleta, coordenadas, estado | GBIF.org (10 August 2026) GBIF Occurrence Download https://doi.org/10.15468/dl.qvrga3|
| Flora e Funga do Brasil (JBRJ) | Distribuição por bioma e por estado das espécies aceitas |Flora e Funga do Brasil (Constantly updated): Flora e Funga do Brasil project - Projeto Flora e Funga do Brasil. Instituto de Pesquisas Jardim Botânico do Rio de Janeiro. Dataset/Checklist. doi:10.15468/1mtkaw|


A divisão entre as duas fontes é intencional: o GBIF já entrega os nomes com sinônimos resolvidos e as datas de coleta, enquanto o bioma é uma informação que só a Flora do Brasil disponibiliza.

## Dados usados pelo aplicativo

O aplicativo consome um único arquivo já tratado,
`ocorrencias_bromeliaceae.csv.gz`, com um registro de coleta por linha:

| Coluna | Descrição |
|---|---|
| `nome_aceito` | Nome científico da espécie, com sinônimos já resolvidos |
| `genero` | Gênero da espécie |
| `ano` | Ano de coleta do registro |
| `uf` | Sigla do estado |
| `latitude`, `longitude` | Coordenadas do registro |

O arquivo é comprimido (`.gz`) para caber com folga no repositório e ser lido rapidamente no plano gratuito do Render. O `pandas` abre esse formato diretamente, sem necessidade de descompactar.

## Preparo dos dados

Os arquivos brutos do GBIF e da Flora e Funga do Brasil foram baixados e processados separadamente, em scripts de preparação responsáveis pela extração, limpeza e agregação. Este repositório contém apenas a saída já tratada, de modo que o aplicativo não precisa baixar nem processar dados brutos ao ser executado.Parte dos scripts de preparação e limpeza de dados foi desenvolvida com apoio de um assistente de IA (Claude, Anthropic), sob minha supervisão e revisão. Isso incluiu: estruturação inicial dos scripts de coleta/limpeza, sugestões de tratamento de erros e correção de problemas de tipagem identificados pelo linter (Pylance).

Etapas aplicadas antes da visualização:

- Filtragem para a família Bromeliaceae, considerando apenas nomes aceitos.
- Extração do bioma a partir do campo `occurrenceRemarks` da Flora, que traz a informação em formato JSON dentro de uma única coluna.
- Remoção de registros sem ano de coleta ou sem coordenadas válidas, incluindo   coordenadas em (0, 0) e pontos fora dos limites aproximados do Brasil.
- Descarte de registros que não representam coleta em campo (espécimes fósseis e  material vivo cultivado).
- Padronização dos nomes de estado para siglas de UF.
- Cruzamento entre as espécies do GBIF e a tabela de biomas da Flora.

## Limitações dos dados

Dados de biodiversidade como os do GBIF **não são um censo**: refletem esforço de coleta, não necessariamente a distribuição real das espécies. Isso implica limitações importantes para a interpretação dos resultados:

- **Viés de amostragem geográfico**: áreas de mais fácil acesso (perto de cidades, universidades e estradas) tendem a ter mais registros, o que pode inflar artificialmente a amplitude de distribuição de espécies nessas regiões.
- **Viés temporal**: o número de registros por ano reflete tanto mudanças reais  quanto o aumento do esforço de digitalização de acervos ao longo do tempo, especialmente a digitalização de herbários nas últimas décadas.
- **Qualidade variável dos registros**: nem todos os registros do GBIF são verificados por especialista; incluem observações de ciência cidadã junto com   material de herbário tradicional. O campo `basisOfRecord` foi usado para  excluir alguns tipos não representativos de coleta em campo, mas isso não  elimina todo o ruído.
- **Reconciliação taxonômica imperfeita**: o cruzamento entre nomes do GBIF e da Flora e Funga do Brasil depende de correspondência de nome científico; sinônimos não completamente normalizados podem gerar espécies sem bioma  correspondente.

Esses dados são adequados para uma análise **exploratória e descritiva**, não para inferências causais sobre distribuição real de espécies sem validação adicional.


## Estrutura do projeto

```
.
├── README.md
├── app.py                              # aplicativo Streamlit
├── ocorrencias_bromeliaceae.csv.gz     # dados tratados, lidos pelo aplicativo
├── requirements.txt
├── .streamlit/
│   └── config.toml                     # configuração exigida pelo Render
└── notebooks/
    └── EDA.ipynb                       # análise exploratória
```

## Como executar localmente

Requer Python 3.10 ou superior.

```bash
# 1. Clonar o repositório
git clone https://github.com/LarissaBotany/Dashboard-Bromeliaceae-Brasil.git
cd S5proj_Bromelia_distribuition

# 2. Criar e ativar o ambiente virtual
python -m venv bromelia_env
source bromelia_env/bin/activate    # no Windows: bromelia_env\Scripts\activate

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Rodar o aplicativo
streamlit run app.py
```

O aplicativo abre no navegador em `http://localhost:8501`.

## Tecnologias

`pandas` · `plotly-express` · `streamlit` · hospedagem no Render

---

Projeto desenvolvido para a Sprint 5 do curso de Ciência de Dados da TripleTen.
