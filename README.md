# TikTok Scraping Challenge

## Overview

This project is designed for scraping TikTok data based on specified keywords and date ranges. The script utilizes Selenium for web scraping and Pandas for data manipulation.

## Prerequisites

- Python 3.x
- ChromeDriver (for Selenium, make sure it matches your Chrome version)
- Virtual environment (recommended)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/JANBOUBI-ABDERRAHIM/Challenge_Scraping.git
   cd Challenge_Scraping
   ```

2. Create a virtual environment:

    ```bash
    python -m venv challenge_tiktok
    source challenge_tiktok/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script with the following command:

  ```bash
  python scrap.py --keywords maroc morocco --start_date 2023-11-12 --end_date 2023-12-12 --waiting_time 3
  ```

## File Structure

- [`scrap.py`](scrap.py): Main script for TikTok scraping.
- [`helper.py`](helper.py): Helper functions for date transformation, filtering, and result saving.

## Results

The scraped data will be saved in a CSV file named [`RESULTS.csv`](RESULTS.csv).
