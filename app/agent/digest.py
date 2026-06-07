from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types
import time

load_dotenv()

class DigestOutput(BaseModel):
    title: str
    summary: str

SYSTEM_PROMPT = """
    You are an expert AI news analyst specializing in summarizing technical articles, research papers, and video content about artificial intelligence.

    Your role is to create concise, informative digests that help readers quickly understand the key points and significance of AI-related content.

    Guidelines:
    - Create a compelling title (5-10 words) that captures the essence of the content
    - Write a 2-3 sentence summary that highlights the main points and why they matter
    - Focus on actionable insights and implications
    - Use clear, accessible language while maintaining technical accuracy
    - Avoid marketing fluff - focus on substance
"""

class DigestAgent():
    def __init__(self):
        self.client = genai.Client()
        self.model = "gemini-2.0-flash-lite"
        self.system_prompt = SYSTEM_PROMPT

    def generate_digest(self, title: str, content: str, article_type: str) -> Optional[DigestOutput]:
        try:
            user_prompt = f"""Create a digest for this {article_type}:
                            Title: {title}

                            Content:
                            {content[:8000]}

                            Provide a title and 2-3 sentence summary.
                        """

            response = self.client.models.generate_content(
                model=self.model,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    temperature=0.7,
                    response_mime_type="application/json",
                    response_schema=DigestOutput,
                )
            )

            # Lấy data đã được SDK tự động parse ra Pydantic Object,
            # fall back về việc dùng model_validate_json nếu method không hỗ trợ .parsed
            return response.parsed or DigestOutput.model_validate_json(response.text)
        except Exception as e:
            if "503" in str(e):
                print(f"⏳ Model overloaded (503): {str(e)}")
                time.sleep(3)
                return None
            else:
                # Log lỗi chi tiết và raise lên để process_digest.py catch
                print(f"❌ API Error trong generate_digest: {type(e).__name__}: {str(e)}")
                raise
            
    