import streamlit as st
from pytubefix import YouTube
from pathlib import Path

# Título do app
st.title("📥 Downloader de Vídeos do YouTube")

# Caixa de texto para colar o link do vídeo
url = st.text_input("Cole o link do vídeo do YouTube aqui:")

# Criar pasta para salvar os vídeos
destino = Path("downloads")
destino.mkdir(exist_ok=True)

# Se o usuário digitou um link
if url:
    try:
        yt = YouTube(url)

        st.write(f"**Título:** {yt.title}")
        st.write(f"**Duração:** {yt.length} segundos")

        # Escolher o tipo de download
        opcao = st.radio(
            "Escolha o que deseja baixar:",
            ("Vídeo (qualidade máxima)", "Vídeo (escolher qualidade)", "Áudio (MP3)")
        )

        # Se o usuário escolher vídeo em qualidade máxima
        if opcao == "Vídeo (qualidade máxima)":
            if st.button("Baixar em Alta Resolução"):
                stream = yt.streams.get_highest_resolution()
                caminho = stream.download(output_path=destino)
                st.success(f"✅ Download concluído! Arquivo salvo em: {caminho}")
                st.video(caminho)

        # Se o usuário quiser escolher qualidade
        elif opcao == "Vídeo (escolher qualidade)":
            streams = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc()
            qualidades = [stream.resolution for stream in streams]

            qualidade = st.selectbox("Escolha a resolução:", qualidades)

            if st.button("Baixar na Qualidade Escolhida"):
                stream = yt.streams.filter(res=qualidade, file_extension="mp4", progressive=True).first()
                caminho = stream.download(output_path=destino)
                st.success(f"✅ Download concluído! Arquivo salvo em: {caminho}")
                st.video(caminho)

        # Se o usuário quiser só o áudio
        elif opcao == "Áudio (MP3)":
            if st.button("Baixar Áudio (MP3)"):
                stream = yt.streams.filter(only_audio=True).first()
                caminho = stream.download(output_path=destino)
                novo_caminho = Path(caminho).with_suffix(".mp3")  # troca extensão para .mp3
                Path(caminho).rename(novo_caminho)
                st.success(f"✅ Download concluído! Arquivo salvo em: {novo_caminho}")
                st.audio(str(novo_caminho))

    except Exception as e:
        st.error(f"❌ Erro: {e}")
