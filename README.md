# macOS Price Tracker 

An automated Python app that monitors different set turl prices and sends native macOS notifications when target prices are met. 

## Technical 
- **Data Persistence:** Utilizes **SQLite** for lightweight, local storage of product URLs and price history.
- **Automation:** Designed to run as a background process using `nohup` or Mac `launchd`.
- **System Integration:** Leverages **AppleScript (osascript)** via Python's `subprocess` module for native OS notifications.
- **Robustness:** Implemented custom headers and error handling to manage connection timeouts and anti-scraping measures.

## Tech Stack 
- **Language:** Python 3
- **Libraries:** BeautifulSoup4, Requests, Python-dotenv
- **Database:** SQLite3
- **OS:** macOS (Integration via AppleScript)

## Setup 
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
4. Run `python3 add_product.py` to add your first target.
5. Launch the tracker: `python3 scraper.py`.
