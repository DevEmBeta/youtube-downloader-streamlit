import streamlit as st
import yt_dlp
from pathlib import Path

st.title("📥 Downloader de Vídeos do YouTube")

url = st.text_input("Cole o link do vídeo do YouTube aqui:")

# Pasta para salvar
destino = Path("downloads")
destino.mkdir(exist_ok=True)

if url:
    try:
        # Mostrar opções
        opcao = st.radio(
            "Escolha o que deseja baixar:",
            ("Vídeo (qualidade máxima)", "Áudio (MP3)")
        )

        if st.button("Baixar"):
            if opcao == "Vídeo (qualidade máxima)":
                ydl_opts = {
                    "outtmpl": str(destino / "%(title)s.%(ext)s"),
                    "format": "bestvideo+bestaudio/best",
                }
            else:  # Áudio
                ydl_opts = {
                    "outtmpl": str(destino / "%(title)s.%(ext)s"),
                    "format": "bestaudio/best",
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }],
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                arquivo = ydl.prepare_filename(info)

                if opcao == "Áudio (MP3)":
                    arquivo = arquivo.rsplit(".", 1)[0] + ".mp3"
                    st.success(f"✅ Áudio salvo em: {arquivo}")
                    st.audio(arquivo)
                else:
                    st.success(f"✅ Vídeo salvo em: {arquivo}")
                    st.video(arquivo)

    except Exception as e:
        st.error(f"❌ Erro: {e}")
