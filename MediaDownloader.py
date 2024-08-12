import streamlit as st
from funciones import setup_session_state, select_folder_button, validate_url_and_format, handle_download, check_and_warn_changes, YouTubeDownloader

def main():
    st.title("Descargador de Videos de YouTube")

    # Inicializar el estado de la sesión
    setup_session_state()

    # Mostrar botón para seleccionar la carpeta de destino
    select_folder_button()

    if st.session_state.download_folder:
        # Entradas y opciones para la URL y formato de descarga
        url = st.text_input("Ingrese la URL del video de YouTube:", value=st.session_state.url)
        format_type = st.selectbox("Selecciona el formato de descarga:", ["video", "audio"], index=["video", "audio"].index(st.session_state.format_type))

        # Verificar cambios, desactivar validación y advertir al usuario
        check_and_warn_changes(url, format_type)

        # Validar URL y formato
        if st.button("Validar"):
            validate_url_and_format(url, format_type)

        # Manejo del estado de validación y del botón de descarga
        if st.session_state.validated:
            downloader = YouTubeDownloader(st.session_state.url, st.session_state.download_folder, st.session_state.format_type)
            handle_download(downloader)
        else:
            st.info("Por favor, valide la URL y el formato antes de descargar.")
if __name__ == "__main__":
    main()
