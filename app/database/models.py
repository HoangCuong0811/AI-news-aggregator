from sqlalchemy import Column, DateTime, Integer, String, Text, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AnthropicArticleModel(Base):
    __tablename__ = "anthropic_articles"

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    url = Column(String(1000), nullable=False)
    guid = Column(String(500), nullable=False, unique=True, index=True)
    published_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    category = Column(String(255), nullable=True)


class OpenAIArticleModel(Base):
    __tablename__ = "openai_articles"

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    url = Column(String(1000), nullable=False)
    guid = Column(String(500), nullable=False, unique=True, index=True)
    published_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    category = Column(String(255), nullable=True)


class YouTubeVideoModel(Base):
    __tablename__ = "youtube_videos"

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    url = Column(String(1000), nullable=False)
    channel_id = Column(String, nullable=False)
    video_id = Column(String(128), nullable=False, unique=True, index=True)
    published_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    description = Column(Text, nullable=False)
    transcript = Column(Text, nullable=True)
