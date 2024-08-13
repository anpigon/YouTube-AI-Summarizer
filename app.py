import os
import time
import logging
from dotenv import load_dotenv
import streamlit as st
from pytubefix import YouTube
from pytubefix.cli import on_progress
import google.generativeai as genai

# Constants
TEMP_VIDEO_FILENAME = "temp_video.mp4"
MODEL_NAME = "gemini-1.5-pro"
SUMMARY_PROMPT = "이 동영상을 요약합니다. 주요 내용을 5개의 bullet point로 정리하고, 그 아래에 상세한 요약을 제공해주세요."
REQUEST_TIMEOUT = 600

# Setup
load_dotenv()
logging.basicConfig(level=logging.DEBUG)
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


def download_youtube_video(url):
    yt = YouTube(url, on_progress_callback=on_progress)
    st.sidebar.info(f"제목: {yt.title}")
    logging.info("유튜브 동영상 다운로드 시작")
    ys = yt.streams.get_lowest_resolution()
    ys.download(filename=TEMP_VIDEO_FILENAME)
    logging.info("유튜브 동영상 다운로드 완료")
    return yt.title


def upload_video_to_genai():
    logging.info("generativeai에 동영상 업로드 시작")
    video_file = genai.upload_file(path=TEMP_VIDEO_FILENAME)
    logging.info("generativeai에 동영상 업로드 완료")
    return video_file


def wait_for_processing(video_file):
    while video_file.state.name == "PROCESSING":
        logging.info("처리 중...")
        time.sleep(10)
        video_file = genai.get_file(video_file.name)
    if video_file.state.name == "FAILED":
        raise ValueError(f"Video processing failed: {video_file.state.name}")
    return video_file


def generate_summary(video_file):
    model = genai.GenerativeModel(model_name=MODEL_NAME)
    logging.info("AI 모델이 동영상을 분석 중...")
    response = model.generate_content(
        [video_file, SUMMARY_PROMPT], request_options={"timeout": REQUEST_TIMEOUT}
    )
    logging.info("AI 모델이 동영상을 분석 완료")
    return response.text


def cleanup(video_file):
    genai.delete_file(video_file.name)
    os.remove(TEMP_VIDEO_FILENAME)
    logging.info("임시 파일 삭제")


def process_video(url):
    try:
        video_title = download_youtube_video(url)
        video_file = upload_video_to_genai()
        video_file = wait_for_processing(video_file)
        summary = generate_summary(video_file)
        cleanup(video_file)
        return summary, video_title
    except Exception as e:
        logging.error(f"Error processing video: {str(e)}")
        raise


def main():
    st.set_page_config(page_title="유튜브 동영상 요약 앱")
    st.title("🎥 유튜브 동영상 요약 앱")
    st.sidebar.title("유튜브 정보")

    url = st.text_input("유튜브 URL을 입력하세요:")

    if st.button("요약하기", key="summarize"):
        if url:
            try:
                with st.spinner("AI 모델이 동영상을 분석 중..."):
                    summary, video_title = process_video(url)
                st.success("요약이 완료되었습니다!")
                st.header(f"📊 '{video_title}' 요약 결과")
                st.markdown(summary)
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")
        else:
            st.warning("URL을 입력해주세요.")


if __name__ == "__main__":
    main()
