import snscrape.modules.twitter as sntwitter
import logging

class SocialMediaScraper:
    """
    Scrapes tweets from a list of tweet URLs (pre-labeled) using snscrape.
    """

    def __init__(self):
        pass

    def extract_tweet_id(self, url: str) -> str:
        """
        Extracts the tweet ID from a standard tweet URL.
        """
        try:
            return url.split("/")[-1]
        except Exception as e:
            logging.error(f"Error extracting tweet ID from {url}: {e}")
            return None

    def scrape_tweet(self, tweet_id: str) -> dict:
        """
        Uses snscrape to fetch a tweet's text and metadata.
        """
        try:
            tweet = next(sntwitter.TwitterTweetScraper(tweet_id).get_items())
            return {
                "text": tweet.content,
                "username": tweet.user.username,
                "date": str(tweet.date),
                "url": tweet.url
            }
        except Exception as e:
            logging.error(f"Error scraping tweet ID {tweet_id}: {e}")
            return None
