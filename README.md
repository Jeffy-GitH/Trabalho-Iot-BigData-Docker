# Dashboard de Análise de Temperatura IoT

Este projeto consiste em um dashboard interativo construído com Streamlit para visualização e análise de dados de temperatura de sensores IoT. A aplicação lê dados de um arquivo CSV, os armazena em um banco de dados PostgreSQL e exibe as informações em gráficos dinâmicos.

## Funcionalidades

- **Dashboard Interativo**: Interface web criada com Streamlit para fácil visualização dos dados.
- **Sincronização de Dados**: Carrega dados de um arquivo `dados.csv` e os insere em um banco de dados PostgreSQL.
- **Carga de Dados Idempotente**: O script verifica registros existentes e insere apenas os dados novos, evitando duplicatas a cada execução.
- **Setup Automático de Tabela**: A tabela principal (`temperature_readings`) é criada automaticamente no banco na primeira execução.
- **Visualizações Claras**: Apresenta três gráficos principais para análise:
  1.  Temperatura média por dispositivo.
  2.  Contagem de leituras por hora do dia.
  3.  Temperaturas máximas e mínimas diárias.
- **Código Organizado**: O projeto é estruturado em módulos com responsabilidades separadas (conexão com banco, carga de dados, componentes de UI), seguindo boas práticas de desenvolvimento.

## Tecnologias Utilizadas

- **Backend**: Python 3.9+
- **Interface Web**: Streamlit
- **Manipulação de Dados**: Pandas
- **Banco de Dados**: PostgreSQL
- **Conexão com Banco (ORM)**: SQLAlchemy com Psycopg2
- **Gráficos**: Plotly Express

## Pré-requisitos

Antes de começar, você precisa ter instalado em sua máquina:
- [Python 3.9 ou superior](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/) (um servidor rodando localmente ou acessível pela rede)

## Como Configurar e Executar

Siga os passos abaixo para configurar o ambiente e executar o projeto.

### Banco de Dados

### 1. Server
Instale o PostgresSql e o PgAdmin ou executa o comando abaixo com o Docker Desktop instalado na máquina para criar um container do Postgres.

```bash
docker run --name postgres-iot -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=iot -p 5432:5432 -d postgres:16
```
Isso irá criar junto com o banco de dados configurado com o nome do banco, user e password. <br>
Nome do banco: iot <br>
User: postgres <br>
Password: postgres

### 2. Criar as Views
```bash

-- View 1: Média de temperatura por dispositivo
CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT
    room_id AS device_id,
    AVG(temp)::numeric(10,2) AS avg_temp
FROM
    temperature_readings
GROUP BY
    room_id;

-- View 2: Leituras por hora
CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT
    EXTRACT(HOUR FROM noted_date) AS hora,
    COUNT(*) AS contagem
FROM
    temperature_readings
GROUP BY
    hora
ORDER BY
    hora;

-- View 3: Temperaturas máxima e mínima por dia
CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT
    DATE(noted_date) AS data,
    MAX(temp) AS temp_max,
    MIN(temp) AS temp_min
FROM
    temperature_readings
GROUP BY
    data
ORDER BY
    data;
```

### 1. Clone o Repositório

Se o seu projeto estiver no Git, o primeiro passo seria cloná-lo.
```bash
git clone https://github.com/alancavalcante-dev/trabalho-iot-bigdata.git
cd trabalho-iot-bigdata
```

### 1. Ambiente Virtual

Executa o comando para criar e ativar o ambiente virtual do python
```bash
py -m venv venv
venv/scripts/activate
```

### 3. Instale as depedências

Executa o comando para criar e ativar o ambiente virtual do python
```bash
pip install -r requirements.txt
```


### 4. Executa o app (dashboard)

Executa o comando para criar e ativar o ambiente virtual do python
```bash
streamlit run dashboard.py
```

## Estrutura do Projeto

```bash
├── .gitignore
├── components.py         # Funções que criam os gráficos (UI)
├── dados.csv             # Arquivo com os dados brutos
├── dashboard.py          # Arquivo principal que executa a aplicação
├── data_loader.py        # Lógica para carregar e sincronizar dados do CSV
├── database.py           # Funções de conexão e queries com o banco
├── requirements.txt      # Dependências
└── README.md
```





