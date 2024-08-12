import streamlit as st
import subprocess
import os
import yt_dlp as ytdlp

class YouTubeDownloader:
    def __init__(self, url,format_type):
        self.url = url
        # self.download_folder = download_folder
        self.format_type = format_type
        self.progress_bar = st.progress(0)
        self.ytdlp = ytdlp.YoutubeDL({
            # 'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
            'format': 'bestaudio/best' if format_type == 'audio' else 'best',
            'progress_hooks': [self._progress_hook]
        })

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            percentage = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1)
            self.progress_bar.progress(int(percentage * 100))
        elif d['status'] == 'finished':
            self.progress_bar.progress(100)  # Descarga completa al 100%
            st.success("¡Descarga completada!")
        elif d['status'] == 'error':
            st.error("Error durante la descarga.")

    def show_title(self):
        try:
            info_dict = self.ytdlp.extract_info(self.url, download=False)
            st.write(f"*Título:* {info_dict['title']}")
        except Exception as e:
            st.error(f"Error al acceder al video: {e}")

    def download(self):
        try:
            self.ytdlp.download([self.url])
        except Exception as e:
            st.error(f"Error durante la descarga: {e}")

# def get_folder_path():
#     try:
#         result = subprocess.run(["python", "select_folder.py"], capture_output=True, text=True)
#         return result.stdout.strip()
#     except Exception as e:
#         st.error(f"Error al seleccionar la carpeta: {e}")
#         return None

# def select_folder_button():
#     if st.session_state.download_folder is None:
#         if st.button("Seleccionar Carpeta de Destino"):
#             st.session_state.download_folder = get_folder_path()
#             st.write(f"Ruta de la carpeta de destino: {st.session_state.download_folder}" 
#                      if st.session_state.download_folder 
#                      else "No se seleccionó ninguna carpeta.")

def validate_url_and_format(url, format_type):
    if url:
        st.session_state.url = url
        st.session_state.format_type = format_type
        st.session_state.validated = True
        st.success(f"URL: {url}\nFormato: {format_type}")
    else:
        st.error("Por favor, ingrese una URL válida.")
        st.session_state.validated = False

def handle_download(downloader):
    downloader.show_title()

    if st.button("Descargar"):
        downloader.download()

def check_and_warn_changes(url, format_type):
    if st.session_state.get('validated'):
        if url != st.session_state.get('url') or format_type != st.session_state.get('format_type'):
            st.session_state.validated = False
            st.warning("Se realizaron cambios. Por favor, valide de nuevo.")

def setup_session_state():
    """
    Inicializa y configura las variables de estado de la sesión si no están definidas.
    """
    # if 'download_folder' not in st.session_state:
    #     st.session_state.download_folder = None
    if 'validated' not in st.session_state:
        st.session_state.validated = False
    if 'url' not in st.session_state:
        st.session_state.url = ''
    if 'format_type' not in st.session_state:
        st.session_state.format_type = 'video'