# Handbag Scanner

A minimalist, local AI tool designed to identify handbag models from user-uploaded images.
It leverages OpenAI's CLIP model for visual feature extraction and a PostgreSQL database with `pgvector` for high-speed cosine similarity search.

## Tech Stack

- **Backend:** Python
- **AI Model:** Hugging Face `transformers` (CLIP: `openai/clip-vit-base-patch32`)
- **Database:** PostgreSQL with `pgvector` (Docker)
- **Web Interface:** Streamlit
- **Data Extraction:** Selenium, Cloudscraper, BeautifulSoup4

## Project Structure

```text
.
├── data/
│   ├── dataset_bag.csv       # Scraped metadata
│   ├── dataset_vectorise.pkl # Pre-computed CLIP embeddings
│   └── images/               # Local image storage
├── src/
│   ├── scraper.py            # Data ingestion and image downloading
│   ├── vectorizer.py         # CLIP feature extraction pipeline
│   ├── database.py           # PostgreSQL vector table initialization
│   ├── model.py               # AI model loading configuration (silenced Hub)
│   ├── similarity.py         # Core search logic & distance computation
│   └── app.py                # Streamlit web interface
├── .env                      # Database credentials
└── requirements.txt
```

## Installation

### 1. Set up the Python environment

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### 2. Database setup

Make sure Docker is running and your PostgreSQL container (with `pgvector`, port 5432) is active.

Create a `.env` file in the root directory:

```env
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
```

## Usage

### 1. Build the database (pipeline)

If starting from scratch, run the ingestion and database pipeline sequentially from the `src/` directory:

```bash
cd src/
python3 scraper.py      # Scrape images and metadata
python3 vectorizer.py   # Generate 512-dimensional CLIP vectors
python3 database.py     # Create the table and inject data into PostgreSQL
```

### 2. Launch the web application

```bash
cd src/
streamlit run app.py
```

The application will automatically open in your default web browser.

### 3. CLI mode (terminal)

You can also bypass the UI and test a specific image directly from the terminal:

```bash
cd src/
python3 similarity.py /path/to/your/test_image.jpg
```