import streamlit as st
from pytubefix import YouTube
from pytubefix.cli import on_progress
import google.generativeai as genai
import time
import os

# Gemini API 키 설정
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


def process_video(url):
    with st.spinner("동영상 처리 중..."):
        yt = YouTube(url, on_progress_callback=on_progress)
        st.sidebar.info(f"제목: {yt.title}")

        video_file_name = "video.mp4"
        ys = yt.streams.get_lowest_resolution()
        ys.download(filename=video_file_name)

        st.sidebar.info("유튜브 동영상 다운로드 완료")

        video_file = genai.upload_file(path=video_file_name)
        st.sidebar.info(f"generativeai에 동영상 업로드 완료")

        while video_file.state.name == "PROCESSING":
            st.sidebar.info("처리 중...")
            time.sleep(10)
            video_file = genai.get_file(video_file.name)

        if video_file.state.name == "FAILED":
            raise ValueError(video_file.state.name)

        prompt = "이 동영상을 요약합니다. 주요 내용을 5개의 bullet point로 정리하고, 그 아래에 상세한 요약을 제공해주세요."
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")

        st.sidebar.info("AI 모델이 동영상을 분석 중...")
        response = model.generate_content(
            [video_file, prompt], request_options={"timeout": 600}
        )

        genai.delete_file(video_file.name)
        st.sidebar.info("임시 파일 삭제 완료")

        os.remove(video_file_name)
        st.sidebar.info("임시 비디오 파일 삭제 완료")

    return response.text


st.set_page_config(page_title="유튜브 동영상 요약 앱", layout="wide")

st.title("🎥 유튜브 동영상 요약 앱")

url = st.text_input("유튜브 URL을 입력하세요:")

if st.button("요약하기", key="summarize"):
    if url:
        try:
            summary = process_video(url)

            st.success("요약이 완료되었습니다!")

            # 요약 결과 표시
            st.header("📊 요약 결과")

            # 주요 내용 (bullet points)
            st.subheader("주요 내용")
            bullet_points = summary.split("\n\n")[0].split("\n")[1:]
            for point in bullet_points:
                st.markdown(f"- {point.strip()}")

            # 상세 요약
            st.subheader("상세 요약")
            detailed_summary = "\n\n".join(summary.split("\n\n")[1:])
            st.markdown(detailed_summary)

        except Exception as e:
            st.error(f"오류 발생: {str(e)}")
    else:
        st.warning("URL을 입력해주세요.")

# 사이드바에 로그 정보 표시
st.sidebar.title("처리 로그")
