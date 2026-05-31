## Hàm thực hiện việc thêm markdown vào trong datanase.

from typing import Optional
from scrapers.anthropic import AnthropicScraper
from database.repository import Repository

def process_anthropic_markdown(limit: Optional[int] = None) -> dict:
    scraper = AnthropicScraper()
    repo = Repository()

    articles = repo.get_anthropic_articles_without_markdown()
    if articles:
        for a in articles:
            mardown = scraper.url_to_markdown(a.url)
            repo.update_anthropic_article_markdown(a.guid, markdown=mardown)
    return "Update all markdowns successfully"

if __name__ == "__main__":
    statement = process_anthropic_markdown()
    print(statement)

