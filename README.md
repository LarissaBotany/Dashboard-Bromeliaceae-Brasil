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

## Escala dos dados
 
| Indicador | Valor |
|---|---|
| Registros de coleta | **66.722** |
| Espécies aceitas distintas | **1.268** |
| Gêneros | **60** |
| Estados (UF) com registros | **27** (todas as UFs) |
| Período coberto | **1768 a 2026** |
 
- **Concentração recente:** cerca de **80%** dos registros são de 2000 em diante. A década de 2010 tem 17.940 registros e 2020–2026 já soma 22.132.
- **Registros históricos:** 276 registros são anteriores a 1900 (o mais antigo é de 1768).
- **Registros sem UF:** 2.514 registros (3,8%) não têm estado informado, mas mantêm coordenadas e ano.

## Funcionalidades

- **Visualizador de dados**: tabela com os registros que alimentam os gráficos.
- **Histograma** do ano de coleta, mostrando a evolução do esforço de coleta ao
  longo do tempo.
- **Gráfico de dispersão** cruzando, para cada ano, o número de registros com o
  número de espécies distintas coletadas.
- **Botões** que geram cada gráfico sob demanda.

## O que o aplicativo permite interpretar
 
- **Histograma do ano de coleta:** mostra a evolução do esforço de coleta e permite identificar décadas de maior intensidade, além de picos que podem refletir a digitalização de acervos de herbário e não só coletas novas.
- **Dispersão registros × espécies por ano:** permite distinguir dois cenários. Se os pontos sobem juntos, mais coletas trouxeram mais espécies. Se os registros crescem e as espécies se estabilizam, o esforço extra está repetindo espécies já conhecidas, o que sugere saturação da amostragem ou concentração em locais já visitados. Nos dados, isso aparece com clareza: em 2025 há 4.875 registros para 416 espécies, enquanto em 2010 eram 3.469 registros para 333 espécies, ou seja, os registros crescem cerca de 40% e as espécies cerca de 25%.
- **Tabela de registros:** dá acesso direto aos dados que alimentam os gráficos, para conferir qualquer ponto observado.

## Fontes de dados

| Fonte | O que fornece | Referência |
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

## Validação taxonômica e preparo dos dados
 
A qualidade taxonômica foi tratada como etapa central do projeto, e não só como limpeza:
 
- **Nomes aceitos e sinônimos:** uso apenas de nomes aceitos, para que a mesma espécie não seja contada mais de uma vez sob nomes diferentes. Isso afeta diretamente a contagem de espécies distintas por ano, que é a base do gráfico de dispersão.
- **Cruzamento GBIF × Flora e Funga do Brasil:** as espécies do GBIF foram conferidas contra a lista oficial brasileira, que traz a distribuição por bioma. Espécies sem correspondência são sinal de sinonímia mal resolvida e foram tratadas como tal.
- **Extração do bioma** do campo `occurrenceRemarks` da Flora, que traz a informação em JSON dentro de uma única coluna.
- **Filtros de qualidade geográfica:** remoção de registros sem ano ou sem coordenadas válidas, incluindo coordenadas em (0, 0) e pontos fora dos limites aproximados do Brasil.
- **Filtro por tipo de registro:** descarte de espécimes fósseis e material vivo cultivado, que não representam coleta em campo.
- **Padronização** dos nomes de estado para siglas de UF.
Os arquivos brutos foram processados em scripts de preparação separados (extração, limpeza e agregação). Este repositório contém apenas a saída tratada, então o aplicativo não precisa baixar nem processar dados brutos ao ser executado.
 
Parte dos scripts de coleta e limpeza foi desenvolvida com apoio de um assistente de IA (Claude, Anthropic), sob minha supervisão e revisão. Isso incluiu a estruturação inicial dos scripts, sugestões de tratamento de erros e correção de problemas de tipagem apontados pelo linter (Pylance).

## Limitações dos dados
Dados de biodiversidade como os do GBIF **não são um censo**: refletem esforço de coleta, não necessariamente a distribuição real das espécies.
 
- **Viés de amostragem geográfico:** áreas de fácil acesso (perto de cidades, universidades e estradas) tendem a ter mais registros, o que pode inflar a amplitude de distribuição das espécies nessas regiões.
- **Viés temporal:** o número de registros por ano reflete mudanças reais e também o aumento da digitalização de acervos, especialmente de herbários nas últimas décadas.
- **Qualidade variável dos registros:** nem todos os registros do GBIF são verificados por especialista, e há observações de ciência cidadã junto com material de herbário. O campo `basisOfRecord` foi usado para excluir alguns tipos não representativos, mas isso não elimina todo o ruído.
- **Reconciliação taxonômica imperfeita:** o cruzamento depende da correspondência de nomes científicos; sinônimos não totalmente normalizados podem gerar espécies sem bioma correspondente.
Esses dados servem a uma análise **exploratória e descritiva**, não a inferências causais sobre a distribuição real das espécies sem validação adicional.
 
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
cd Dashboard-Bromeliaceae-Brasil
 
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


## Autora
 
Larissa Areal de Carvalho Muller
 
Projeto desenvolvido durante o bootcamp de Ciência de Dados.
