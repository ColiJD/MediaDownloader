import streamlit as st
import os
from funciones import setup_session_state, validate_url_and_format, handle_download, check_and_warn_changes, YouTubeDownloader

def main():
    st.title("Descargador de Videos de YouTube")
    # Inicializar el estado de la sesión
    setup_session_state()
    
    # Opciones del sistema operativo
    opciones = ["Windows", "macOS", "Linux", "Android"]
    # Rutas correspondientes a cada sistema operativo
    usuario = os.getlogin()
    rutas_descarga = {
        "Windows": f"C:\\Users\\{usuario}\\Downloads",
        "macOS": f"/Users/{usuario}/Downloads",
        "Linux": f"/home/{usuario}/Downloads",
        "Android": "storage/emulated/0/Download"
    }

    # Entrada para la URL del video de YouTube
    url = st.text_input("Ingrese la URL del video de YouTube:", value=st.session_state.url)

    # Selección del formato de descarga
    format_type = st.selectbox("Selecciona el formato de descarga:", ["video", "audio"], index=["video", "audio"].index(st.session_state.format_type))
    
    RutaFolder = st.selectbox("Selecciones la direccion para guardar el video", opciones)
    # Obtener la ruta correspondiente según la selección
    ruta_seleccionada = rutas_descarga.get(RutaFolder, "Ruta no disponible")
    try:
        # Verificar si la ruta existe, si no, crearla
        if not os.path.exists(ruta_seleccionada):
            os.makedirs(ruta_seleccionada)
            st.write(f"Se ha creado la ruta: {ruta_seleccionada}")
        else:
            st.write(f"La ruta seleccionada para guardar el video es: {ruta_seleccionada}")
    except Exception as e:
        st.error(f"Error al crear la ruta: {e}")
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
