# dashboard.py
"""Arquivo principal que renderiza o dashboard Streamlit."""

import streamlit as st
import database
import data_loader
import components

st.set_page_config(layout="wide", page_title="Dashboard de Temperaturas IoT")

def main():
    """Função principal que executa a aplicação do dashboard."""
    st.title('Dashboard de Temperaturas IoT')

    # 1. Obter a conexão com o banco e inicializar a tabela
    engine = database.get_engine()
    database.init_db(engine)

    # 2. Sincronizar os dados do CSV com o banco
    data_loader.sync_csv_to_db("dados.csv", engine)
    
    st.divider() # Adiciona uma linha divisória

    # 3. Carregar dados das views e exibir os componentes do dashboard
    df_avg_temp = database.load_data_from_view('avg_temp_por_dispositivo')
    components.display_avg_temp_chart(df_avg_temp)

    df_leituras_hora = database.load_data_from_view('leituras_por_hora')
    components.display_readings_by_hour_chart(df_leituras_hora)

    df_temp_max_min = database.load_data_from_view('temp_max_min_por_dia')
    components.display_temp_range_chart(df_temp_max_min)

if __name__ == "__main__":
    main()