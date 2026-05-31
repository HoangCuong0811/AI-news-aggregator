from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import AnthropicArticleModel, OpenAIArticleModel, YouTubeVideoModel
from .connection import get_session

class Repository:
    def __init__(self, session: Optional[Session] = None) -> None:
        self.session = session or get_session()

    ### ----------------------------------------------------
    #   Youtube Section
    ### ----------------------------------------------------
    def create_youtube_videos(self, videos: List[dict]) -> int:
        new_videos = []
        for v in videos:
            existing = self.session.query(YouTubeVideoModel).filter_by(video_id=v.video_id).first()
            if not existing:
                new_videos.append(YouTubeVideoModel(
                    video_id=v.video_id,
                    title=v.title,
                    url=v.url,
                    channel_id=v.channel_id or "",
                    published_at=v.published_at,
                    description=v.description or "",
                    transcript=v.transcript or ""
                ))
        if new_videos:
            self.session.add_all(new_videos)
            self.session.commit()
        return len(new_videos)
    
    def get_videos_without_transcript(self, limit: Optional[int] = None) -> List[YouTubeVideoModel]:
        query = self.session.query(YouTubeVideoModel).filter(
            (YouTubeVideoModel.transcript.is_(None)) | (YouTubeVideoModel.transcript == "")
        )
        if limit:
            query = query.limit(limit)
        return query.all()
    
    def update_youtube_transcript(self, video_id: str, transcript: str) -> bool:
        video = self.session.query(YouTubeVideoModel).filter_by(video_id=video_id).first()
        if video:
            video.transcript = transcript
            self.session.commit()
            return True
        return False
    
    ### ----------------------------------------------------
    #   OpenAI section
    ### ----------------------------------------------------
    def create_openai_articles(self, articles: list) -> int:
        new_articles = []
        for a in articles:
            existing = self.session.query(OpenAIArticleModel).filter_by(guid=a.guid).first()
            if not existing:
                new_articles.append(OpenAIArticleModel(
                    guid=a.guid,
                    title=a.title,
                    url=a.url,
                    published_at=a.published_at,
                    description=a.description or "",
                    category=a.category
                ))
        if new_articles:
            self.session.add_all(new_articles)
            self.session.commit()
        return len(new_articles)
    
    def get_openai_articles_without_markdown(self, limit: Optional[int] = None) -> List[OpenAIArticleModel]:
        query = self.session.query(OpenAIArticleModel).filter(OpenAIArticleModel.markdown.is_(None))
        if limit:
            query = query.limit(limit)
        return query.all()
    
    def update_openai_article_markdown(self, guid: str, markdown: str) -> bool:
        article = self.session.query(OpenAIArticleModel).filter_by(guid=guid).first()
        if article:
            article.markdown = markdown
            self.session.commit()
            return True
        return False
    
    ### ----------------------------------------------------
    #   Anthropic section
    ### ----------------------------------------------------
    def create_anthropic_articles(self, articles: list) -> int:
        new_articles = []
        for a in articles:
            existing = self.session.query(AnthropicArticleModel).filter_by(guid=a.guid).first()
            if not existing:
                new_articles.append(AnthropicArticleModel(
                    guid=a.guid,
                    title=a.title,
                    url=a.url,
                    published_at=a.published_at,
                    description=a.description or "",
                    category=a.category,
                    markdown=a.markdown
                ))
        if new_articles:
            self.session.add_all(new_articles)
            self.session.commit()
        return len(new_articles)
    
    def get_anthropic_articles_without_markdown(self, limit: Optional[int] = None) -> List[AnthropicArticleModel]:
        query = self.session.query(AnthropicArticleModel).filter(AnthropicArticleModel.markdown.is_(None))
        if limit:
            query = query.limit(limit)
        return query.all()
    
    def update_anthropic_article_markdown(self, guid: str, markdown: str) -> bool:
        article = self.session.query(AnthropicArticleModel).filter_by(guid=guid).first()
        if article:
            article.markdown = markdown
            self.session.commit()
            return True
        return False
    
if __name__ == "__main__":
    repo = Repository()
    videos = repo.get_videos_without_transcript()
    print(videos)