from typing import Optional
from scrapers.openai import OpenAIScraper
from database.repository import Repository

def process_openai_markdown(limit: Optional[int] = None) -> dict:
    scraper = OpenAIScraper()
    repo = Repository()

    articles = repo.get_openai_articles_without_markdown()
    if articles:
        for a in articles:
            markdown = scraper.url_to_markdown(a.url)
            repo.update_openai_article_markdown(a.guid, markdown=markdown)
    return "Update all OpenAI articles sucessfully"

if __name__ == "__main__":
    print(process_openai_markdown())

