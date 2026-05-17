from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from typing import Optional
import json

def get_transcripts(video_id: str) -> Optional[str]:
    try:
        # 1. Bắt buộc khởi tạo đối tượng API trước
        ytt_api = YouTubeTranscriptApi()
        
        # 2. Gọi hàm fetch từ đối tượng vừa tạo
        fetched_transcript = ytt_api.fetch(video_id)
        return " ".join([snipet.text for snipet in fetched_transcript])
        
    except (TranscriptsDisabled, NoTranscriptFound):
        print(f"Video {video_id} không có phụ đề hoặc đã bị tắt.")
        return None
    except Exception as e:
        # In ra màn hình nguyên nhân lỗi thực sự thay vì trả về None trong im lặng
        print(f"Đã xảy ra lỗi: {type(e).__name__} - {e}")
        return None

if __name__ == "__main__":
    transcript = get_transcripts("XvKiTfd6Xvo")
    print(transcript)