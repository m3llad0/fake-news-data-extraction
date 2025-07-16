from flask import jsonify, request, Blueprint
from app.tools import GoogleSheetsManager, NewsScraper, SocialMediaScraper
import logging
from app.config import Config

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET'])
def scrape_news():
    try:
        news_scraper = NewsScraper()
        social_media_scraper = SocialMediaScraper()
        sheets_manager = GoogleSheetsManager(Config.SHEET_LINK)
        rows = sheets_manager.get_rows("Raw")
        logging.info(f"Retrieved {len(rows)} rows from the worksheet.")

        if not rows:
            return jsonify({"error": "No rows found in the worksheet"}), 404

        for row_num, row in enumerate(rows, start=2):
            url = row.get("url")
            if url and row.get("scrapped", "").lower() != "yes":
                content_type = row.get("type", "").lower()
                category = row.get("category", "unknown").lower()

                if content_type == "news article":
                    logging.info(f"Scraping news article from URL: {url}")
                    try:
                        article_data = news_scraper.parse_article(url=url)
                        if not article_data:
                            logging.warning(f"No article data found for URL: {url}")
                            continue
                    except Exception as e:
                        logging.error(f"Error parsing article at {url}: {e}")
                        continue

                    sheets_manager.append_row("Scrapped news", [
                        article_data["title"],
                        article_data["text"],
                        ", ".join(article_data["authors"]),
                        str(article_data["publish_date"]) if article_data["publish_date"] else "",
                        url,
                        str(article_data["metadata"]),
                        category,
                    ])
                    sheets_manager.update_row("Raw", row_num, 3, "yes")
                    logging.info(f"Successfully scraped and saved article from URL: {url}")

                elif content_type == "tweet":
                    tweet_id = social_media_scraper.extract_tweet_id(url)
                    if not tweet_id:
                        logging.warning(f"Invalid tweet URL: {url}")
                        continue

                    try:
                        tweet_data = social_media_scraper.scrape_tweet(tweet_id)
                        if not tweet_data:
                            logging.warning(f"No tweet data found for ID: {tweet_id}")
                            continue
                    except Exception as e:
                        logging.error(f"Error scraping tweet ID {tweet_id}: {e}")
                        continue

                    sheets_manager.append_row("Scrapped tweets", [
                        tweet_data["text"],
                        tweet_data["username"],
                        tweet_data["date"],
                        tweet_data["url"],
                        category,
                    ])
                    sheets_manager.update_row("Raw", row_num, 3, "yes")
                    logging.info(f"Successfully scraped and saved tweet from ID: {tweet_id}")

        return jsonify({"message": "Articles and social posts scraped and saved successfully!"}), 200

    except Exception as e:
        logging.error(f"An error occurred while scraping: {e}")
        return jsonify({"error": str(e)}), 500


@routes.route('/dataset', methods=['GET'])
def get_dataset():
    try:
        SHEETS = ["Scrapped news", "Scrapped tweets"]

        sheets_manager = GoogleSheetsManager(Config.SHEET_LINK)

        dataset = {}

        for sheet in SHEETS:
            rows = sheets_manager.get_rows(sheet)
            if not rows:
                logging.warning(f"No data found in sheet: {sheet}")
                continue

            dataset[sheet] = rows

        if not dataset:
            logging.warning("No data found in any of the sheets.")
            return jsonify({"error": "No data found in the dataset"}), 404
        
        return jsonify(dataset), 200
    except Exception as e:
        logging.error(f"An error occurred while retrieving the dataset: {e}")
        return jsonify({"error": str(e)}), 500


@routes.route('/health', methods=['GET'])
def health_check():
    try:
        Config.validate()
        return jsonify({"status": "ok"}), 200
    except ValueError as ve:
        logging.error(f"Configuration error: {ve}")
        return jsonify({"error": str(ve)}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500