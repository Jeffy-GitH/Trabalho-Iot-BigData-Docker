import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine, Table, Column, String, Integer, DateTime, MetaData

# ========================
# 0. Configuração da Página
# ========================
# Usar o modo "wide" e dar um título para a aba do navegador
st.set_page_config(layout="wide", page_title="Dashboard de Temperaturas IoT")

# ========================
# 1. Conexão com o banco de dados
# ========================
@st.cache_resource
def get_engine():
    return create_engine('postgresql://postgres:postgres@localhost:5432/iot')

engine = get_engine()

# ========================
# 2. Garantir que a tabela exista
# ========================
meta = MetaData()
temperature_table = Table(
   'temperature_readings', meta,
   Column('id', String(255), primary_key=True),
   Column('room_id', String(255)),
   Column('noted_date', DateTime),
   Column('temp', Integer),
   Column('in_out', String(10))
)
meta.create_all(engine)

# ========================
# 3. Carregar CSV e inserir dados (agora na Sidebar)
# ========================
with st.sidebar:
    st.header("⚙️ Controle de Dados")
    st.subheader("Status da Carga de Dados")
    csv_file = "IOT-temp.csv"
    df = pd.read_csv(csv_file)

    df = df.rename(columns={
        "room_id/id": "room_id",
        "out/in": "in_out"
    })

    df["noted_date"] = pd.to_datetime(df["noted_date"], errors="coerce")
    df.dropna(subset=['noted_date'], inplace=True)

    try:
        with engine.connect() as connection:
            existing_ids_df = pd.read_sql("SELECT id FROM temperature_readings", connection)
            existing_ids = set(existing_ids_df['id'])

        st.write(f"Linhas lidas do CSV: `{len(df)}`")
        st.write(f"Registros no banco: `{len(existing_ids)}`")

        df_new = df[~df['id'].isin(existing_ids)]
        
        st.write(f"Novos registros: `{len(df_new)}`")

        if not df_new.empty:
            st.toast(f"Inserindo {len(df_new)} novos registros...")
            df_new.to_sql("temperature_readings", engine, if_exists="append", index=False)
        else:
            st.toast("Nenhum registro novo para inserir.")
            
    except Exception as e:
        st.error(f"Erro ao inserir dados: {e}")

# ========================
# 4. Função para carregar dados de views
# ========================
@st.cache_data
def load_data(view_name):
    _engine = get_engine()
    try:
        # Carrega todos os dados da view
        return pd.read_sql(f"SELECT * FROM {view_name}", _engine)
    except Exception as e:
        st.error(f"Não foi possível carregar a view '{view_name}': {e}")
        return pd.DataFrame()

# ========================
# 5. Dashboard
# ========================
st.title('🌡️ Dashboard de Análise de Temperaturas IoT')
st.markdown("Use o menu no canto superior direito para alterar o tema para **Dark**.")

# Carregar todos os dados necessários
df_avg_temp = load_data('avg_temp_por_dispositivo')
df_leituras_hora = load_data('leituras_por_hora')
df_temp_max_min = load_data('temp_max_min_por_dia')
total_readings = existing_ids_df.shape[0] if not existing_ids_df.empty else 0
num_devices = df_avg_temp.shape[0] if not df_avg_temp.empty else 0

st.divider()

# --- Métricas Principais (KPIs) ---
st.header("📊 Métricas Gerais", divider='rainbow')
col1, col2, col3 = st.columns(3)

with col1:
    avg_temp_geral = df_avg_temp['avg_temp'].mean() if not df_avg_temp.empty else 0
    st.metric(label="Temperatura Média Geral", value=f"{avg_temp_geral:.1f} °C")

with col2:
    st.metric(label="Total de Leituras no Banco", value=f"{total_readings}")
    
with col3:
    st.metric(label="Nº de Dispositivos", value=f"{num_devices}")

st.divider()

# --- Layout dos Gráficos em Colunas ---
col_graf1, col_graf2 = st.columns([2, 3]) # Coluna 1 é 2/5 e a Coluna 2 é 3/5 da largura

with col_graf1:
    # Gráfico 1: Média de temperatura por dispositivo
    st.header('📈 Média por Dispositivo')
    if not df_avg_temp.empty:
        # Usar template="streamlit" faz o gráfico se adaptar ao tema
        fig1 = px.bar(df_avg_temp, x='device_id', y='avg_temp', template="streamlit",
                      labels={'device_id': 'Dispositivo', 'avg_temp': 'Temperatura Média'})
        st.plotly_chart(fig1, use_container_width=True)

with col_graf2:
    # Gráfico 2: Contagem de leituras por hora
    st.header('🕒 Leituras por Hora')
    if not df_leituras_hora.empty:
        fig2 = px.line(df_leituras_hora, x='hora', y='contagem', template="streamlit",
                       labels={'hora': 'Hora do Dia', 'contagem': 'Nº de Leituras'}, markers=True)
        st.plotly_chart(fig2, use_container_width=True)

    # Gráfico 3: Temperaturas máximas e mínimas por dia
    st.header('☀️ Variação Diária')
    if not df_temp_max_min.empty:
        fig3 = px.line(df_temp_max_min, x='data', y=['temp_max', 'temp_min'], template="streamlit",
                       labels={'data': 'Data', 'value': 'Temperatura'})
        st.plotly_chart(fig3, use_container_width=True)