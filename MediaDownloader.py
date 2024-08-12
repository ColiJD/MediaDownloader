import streamlit as st
import os
from funciones import setup_session_state, validate_url_and_format, handle_download, check_and_warn_changes, YouTubeDownloader
from pathlib import Path

def main():
    st.title("Descargador de Videos de YouTube")
    # Inicializar el estado de la sesión
    setup_session_state()

    # Entrada para la URL del video de YouTube
    url = st.text_input("Ingrese la URL del video de YouTube:", value=st.session_state.url)

    # Selección del formato de descarga
    format_type = st.selectbox("Selecciona el formato de descarga:", ["video", "audio"], index=["video", "audio"].index(st.session_state.format_type))
    
     # Ruta temporal para almacenamiento en Streamlit Cloud
    ruta_temporal = Path("/tmp/descargas_streamlit")
    try:
        # Verificar si la ruta temporal existe, si no, crearla
        if not ruta_temporal.exists():
            ruta_temporal.mkdir(parents=True, exist_ok=True)
            st.write(f"Se ha creado la ruta temporal: {ruta_temporal}")
        else:
            st.write(f"Se utilizará la ruta temporal: {ruta_temporal}")
    except Exception as e:
        st.error(f"Error al crear la ruta temporal: {e}")
        return

    # Verificar cambios y advertir al usuario si es necesario
    check_and_warn_changes(url, format_type)
    
    # Validar URL y formato
    if st.button("Validar"):
        validate_url_and_format(url, format_type)

    # Manejo del estado de validación y del botón de descarga
    if st.session_state.validated:
        downloader = YouTubeDownloader(st.session_state.url, st.session_state.format_type)
        handle_download(downloader)
    else:
        st.info("Por favor, valide la URL y el formato antes de descargar.")
        

if __name__ == "__main__":
    main()
