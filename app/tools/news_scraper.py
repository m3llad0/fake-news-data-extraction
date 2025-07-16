from newspaper import Article
import logging

class NewsScraper:
    """
    A class to scrape news articles using the newspaper3k library.
    """
    def __init__(self):
        """
        Initialize a NewsScraper instance with no loaded article.
        """
        self.article = None

    def parse_article(self, url: str) -> dict:
        """
        Downloads and parses a news article from the given URL in Spanish, returning its main content and metadata.
        
        Parameters:
            url (str): The URL of the news article to parse.
        
        Returns:
            dict or None: A dictionary with the article's title, text, authors, publish date (as a string or None), and metadata if parsing is successful and the article is sufficiently long; otherwise, None.
        
        Raises:
            ValueError: If the provided URL is empty.
        """
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
