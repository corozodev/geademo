import streamlit as st
import pandas as pd
from auto import assign_codes
from email_service import generate_email

st.set_page_config(page_title="Automatización RRHH - Cine", layout="centered")

st.title("🎬 Automatización de entrega de códigos de cine")

modo = st.radio("Selecciona el modo:", ["Masivo", "Prueba manual"])

codes_df = pd.read_csv("data/codigos.csv")

if modo == "Masivo":
    st.subheader("Carga masiva de colaboradores")
    uploaded = st.file_uploader("Sube el archivo de colaboradores", type=["csv"])

    if uploaded and st.button("Ejecutar automatización"):
        collaborators_df = pd.read_csv(uploaded)
        result, updated_codes = assign_codes(collaborators_df, codes_df)

        st.success("Automatización ejecutada correctamente")
        st.dataframe(result)

        st.subheader("Correos generados")
        for _, row in result.iterrows():
            st.code(generate_email(row["correo"], row["codigo"]))

elif modo == "Prueba manual":
    st.subheader("Prueba individual")
    correo = st.text_input("Correo del colaborador")

    if correo and st.button("Enviar código de prueba"):
        available = codes_df[codes_df["estado"] == "disponible"].iloc[0]
        codigo = available["codigo"]
        st.code(generate_email(correo, codigo))
        st.success("Correo generado (modo demo)")
