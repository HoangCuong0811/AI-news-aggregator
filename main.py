from app.runner import run_scrapers

def main():
    print("Run scraper for Youtube videos, Anthropic and OpenAI articles successfully")
    result = run_scrapers()

    print(f"\nScraping result")
    print(f"Youtube videos: {len(result.get("youtube", []))}")
    print(f"OpenAI Articles: {len(result.get("openai", []))}")
    print(f"Anthropic videos: {len(result.get("anthropic", []))}")
    return result


if __name__ == "__main__":
    main()