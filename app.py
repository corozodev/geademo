import streamlit as st
import pandas as pd

from auto import assign_codes
from email_service import generate_email

# --------------------------------------------------
# Configuración general
# --------------------------------------------------
st.set_page_config(
    page_title="Automatización RRHH – Códigos de Cine",
    layout="centered"
)

st.title("🎬 Automatización de entrega de códigos de cine")
st.markdown(
    """
    Demo de automatización para RRHH.
    Permite asignar y enviar códigos de cine de forma **masiva** o **individual**,
    con trazabilidad y sin errores manuales.
    """
)

# --------------------------------------------------
# Cargar códigos (desde el repo)
# --------------------------------------------------
try:
    codes_df = pd.read_csv("data/codigos.csv")
except Exception as e:
    st.error("❌ No se pudo cargar el archivo de códigos.")
    st.stop()

# --------------------------------------------------
# Selección de modo
# --------------------------------------------------
modo = st.radio(
    "Selecciona el modo de operación:",
    ["📄 Carga masiva", "✉️ Prueba manual"]
)

st.divider()

# ==================================================
# MODO MASIVO
# ==================================================
if modo == "📄 Carga masiva":

    st.subheader("📄 Carga masiva de colaboradores")

    use_example = st.checkbox("Usar archivo de ejemplo incluido en la app")

    uploaded_file = st.file_uploader(
        "O sube tu propio archivo CSV de colaboradores",
        type=["csv"]
    )

    collaborators_df = None

    if use_example:
        try:
            collaborators_df = pd.read_csv("data/colaboradores.csv")
            st.info("Usando archivo de ejemplo del repositorio.")
            st.dataframe(collaborators_df)
        except Exception:
            st.error("❌ No se pudo cargar el archivo de ejemplo.")

    elif uploaded_file is not None:
        try:
            collaborators_df = pd.read_csv(uploaded_file)
            st.success("Archivo cargado correctamente.")
            st.dataframe(collaborators_df)
        except Exception:
            st.error("❌ Error al leer el archivo CSV.")

    st.divider()

    if collaborators_df is not None:
        if st.button("▶ Ejecutar automatización"):
            try:
                result_df, updated_codes_df = assign_codes(
                    collaborators_df,
                    codes_df
                )

                st.success("✅ Automatización ejecutada correctamente")

                st.subheader("📊 Resultados de la asignación")
                st.dataframe(result_df)

                st.subheader("📧 Correos generados (modo simulación)")
                for _, row in result_df.iterrows():
                    st.code(
                        generate_email(
                            correo=row["correo"],
                            codigo=row["codigo"]
                        )
                    )

            except Exception as e:
                st.error(f"❌ Error durante la automatización: {str(e)}")

    else:
        st.warning("Selecciona un archivo de ejemplo o sube un CSV para continuar.")

# ==================================================
# MODO PRUEBA MANUAL
# ==================================================
elif modo == "✉️ Prueba manual":

    st.subheader("✉️ Envío de código de prueba")

    correo = st.text_input("Correo del colaborador")

    if correo:
        if st.button("Enviar código de prueba"):
            try:
                available_codes = codes_df[codes_df["estado"] == "disponible"]

                if available_codes.empty:
                    st.error("❌ No hay códigos disponibles.")
                else:
                    codigo = available_codes.iloc[0]["codigo"]

                    st.success("Correo generado (modo simulación)")
                    st.code(generate_email(correo, codigo))

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.divider()
st.caption(
    "Demo desarrollada como prototipo de automatización de procesos RRHH. "
    "En producción, este flujo puede integrarse con Power Automate, Outlook y SharePoint."
)
