video_url = "https://www.youtube.com/shorts/IMHqGNLLoxo"

def extract_video_id(video_url: str) -> str:
        """Extract video id from a YouTube URL."""
        if "youtube.com/watch?v=" in video_url:
            return video_url.split("v=")[1].split("&")[0]
        if "youtu.be/" in video_url:
            return video_url.split("youtu.be/")[1].split("?")[0]
        if "youtube.com/shorts/" in video_url:
            return video_url.split("shorts/")[1].split("/")[0]
        return video_url

print(extract_video_id(video_url))