import streamlit as st
import yt_dlp as ytdlp
import requests

# Ruta a FFmpeg
ffmpeg_path = r"C:\ffmpeg\bin"

# Crea una sesión de requests para manejar las cookies de YouTube
session = requests.Session()

def save_cookies_to_netscape_format(cookies, filename):
    with open(filename, 'w') as f:
        f.write("# Netscape HTTP Cookie File\n")
        f.write("# This is a generated file! Do not edit.\n")
        for cookie in cookies:
            # Línea en formato Netscape
            f.write(f"{cookie.domain}\t{'TRUE' if cookie.domain.startswith('.') else 'FALSE'}\t{cookie.path}\t{'TRUE' if cookie.secure else 'FALSE'}\t{cookie.expires}\t{cookie.name}\t{cookie.value}\n")

def fetch_cookies(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        save_cookies_to_netscape_format(session.cookies, 'cookies.txt')
    else:
        st.error(f'Error al acceder a la URL: {response.status_code}')

class YouTubeDownloader:
    def __init__(self, url, format_type):
        self.url = url
        self.format_type = format_type
        self.progress_bar = st.progress(0)
        
        # Fetch cookies and save them to a file
        fetch_cookies(self.url)
        
        self.ytdlp = ytdlp.YoutubeDL({
            'format': 'bestaudio/best' if format_type == 'audio' else 'best',
            'progress_hooks': [self._progress_hook],
            'cookiefile': 'cookies.txt',  # Especifica la ruta a tus cookies aquí
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',  # Simula un navegador
            'ffmpeg_location': ffmpeg_path,  # Ruta a FFmpeg
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
    if 'validated' not in st.session_state:
        st.session_state.validated = False
    if 'url' not in st.session_state:
        st.session_state.url = ''
    if 'format_type' not in st.session_state:
        st.session_state.format_type = 'video'
