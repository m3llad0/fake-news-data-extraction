from newspaper import Article
import logging

class NewsScraper:
    """
    A class to scrape news articles using the newspaper3k library.
    """
    def __init__(self):
        self.article = None

    def parse_article(self, url: str) -> dict:
        """Parses the article to extract its content."""
        if not url:
            raise ValueError("URL cannot be empty.")

        try:
            self.article = Article(url, language="es")
            self.article.download()
            self.article.parse()
        except Exception as e:
            logging.error(f"Failed to process article at {url}: {e}")
            return None

        # validate
        if not self.article.text or len(self.article.text) < 100:
            logging.warning(f"Article at {url} appears empty or too short.")
            return None

        return {
            "title": self.article.title,
            "text": self.article.text,
            "authors": self.article.authors,
            "publish_date": str(self.article.publish_date) if self.article.publish_date else None,
            "metadata": self.article.meta_data,
        }
