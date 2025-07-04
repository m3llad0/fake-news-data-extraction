from flask import jsonify, request, Blueprint
from app.tools import GoogleSheetsManager, NewsScraper
import logging

routes = Blueprint('routes', __name__)  

@routes.route('/', methods=['GET'])     
def scrape_news():
    try:
        news_scraper = NewsScraper()
        sheets_manager = GoogleSheetsManager("https://docs.google.com/spreadsheets/d/1qH9feKFgkSOjSu5fmTA2dnfgWcqvYcBLD1XL5tN2bFI/")
        rows = sheets_manager.get_rows("Raw")

        logging.info(f"Retrieved {len(rows)} rows from the worksheet.")

        if not rows:
            return jsonify({"error": "No rows found in the worksheet"}), 404
        
        for row_num, row in enumerate(rows, start=2):
            if row.get("url") and row.get("scrapped", "").lower() != "yes":
                logging.info(f"Scraping news from URL: {row['url']}")
                article_data = news_scraper.parse_article(url=row["url"])

                if not article_data:
                    logging.warning(f"No article data found for URL: {row['url']}")
                    continue

                sheets_manager.append_row("Scrapped data", [
                    article_data["title"],
                    article_data["text"],
                    ", ".join(article_data["authors"]),
                    str(article_data["publish_date"]) if article_data["publish_date"] else "",
                    row["url"],
                    str(article_data["metadata"]),
                    row["category"].lower(),
                ])

                sheets_manager.update_row("Raw", row_num, 3, "yes")
                logging.info(f"Successfully scraped and saved article from URL: {row['url']}")

        return jsonify({"message": "News articles scraped and saved successfully!"}), 200

    except Exception as e:
        logging.error(f"An error occurred while scraping news: {e}")
        return jsonify({"error": str(e)}), 500
