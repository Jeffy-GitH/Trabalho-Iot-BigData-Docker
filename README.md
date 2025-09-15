# Monitoramento Inteligente de Temperatura IoT

Este projeto apresenta uma solução completa para a visualização de dados de sensores IoT, transformando leituras de temperatura brutas em insights visuais e acionáveis. Através de um dashboard dinâmico, é possível acompanhar e analisar padrões de temperatura de forma intuitiva e em tempo real.

## Principais Capacidades

- Visualização Dinâmica: Uma interface web interativa, desenvolvida com Streamlit, que serve como um centro de comando para a análise de dados.

- Pipeline de Dados Automatizada: Ingestão de dados a partir de um arquivo IOT-temp.csv, com sincronização direta para um banco de dados PostgreSQL.

- Sincronização Inteligente: O sistema evita redundância ao inserir apenas registros novos, garantindo uma base de dados consistente e otimizada.

- Infraestrutura como Código: A tabela temperaturas é criada programaticamente, eliminando a necessidade de configuração manual do banco de dados.

- Análises Estratégicas: O dashboard expõe três perspectivas cruciais sobre os dados:

- Performance térmica por dispositivo (temperatura média).

- Padrões de atividade ao longo do dia (leituras por hora).

- Variações e extremos de temperatura diários (máximas e mínimas).

- Arquitetura Modular: Código limpo e organizado em módulos, facilitando a manutenção e a escalabilidade do projeto.

## Tecnologias

- **Linguagem**: Python+
- **Interface Web**: Streamlit
- **Manipulação de Dados**: Pandas
- **Banco de Dados**: PostgreSQL
- **Conexão com Banco (ORM)**: SQLAlchemy com Psycopg2
- **Gráficos**: Plotly Express



### Database

### 1. Server
Instale o PostgresSql e o PgAdmin ou executa o comando abaixo com o Docker Desktop instalado na máquina para criar um container do Postgres.

```bash
docker run --name postgres-iot -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=pipeline -p 5432:5432 -d postgres:16
```

### Sistema

### 1. Ambiente Virtual

Ative o ambiente virtual
```bash
py -m venv venv
venv/scripts/activate
```

### 2. Instale as bibliotecas

Instalar as bibliotecas e frameworks
```bash
pip install pandas psycopg2-binary sqlalchemy streamlit plotly
```


### 3. Executa o app 

Executa o comando para criar e ativar o ambiente virtual do python
```bash
streamlit run dashboard.py
```
