# Twitter Trending Topics Scraper

This project is a web application that scrapes the top 5 trending topics from Twitter using Selenium and stores the results in a MongoDB database. The application also uses ProxyMesh to rotate IP addresses for each request.

## Features

- Scrapes top 5 trending topics from Twitter
- Uses ProxyMesh for IP rotation
- Stores results in MongoDB
- Provides a web interface to trigger the scraper and display results

## Prerequisites

- Python 3.x
- MongoDB
- ChromeDriver
- ProxyMesh account

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/twitter-trending-scraper.git
    cd twitter-trending-scraper
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a .env file in the  directory with the following content:
    ```properties
    TWITTER_USERNAME=your_twitter_username
    TWITTER_PASSWORD=your_twitter_password
    MONGO_URI=mongodb://localhost:27017/twitter_db
    DB_NAME=twitter_db
    PROXYMESH_HOST=us-ca.proxymesh.com
    PROXYMESH_USERNAME=your_proxymesh_username
    PROXYMESH_PASSWORD=your_proxymesh_password
    PROXYMESH_PORT=31280
    ```

5. Run the Flask application:
    ```bash
    python app.py
    ```

6. Open your web browser and navigate to `http://127.0.0.1:5000/` to access the web interface.

## Usage

- Enter your Twitter username and password in the web interface and click the "Run Script" button to trigger the scraper.
- The top 5 trending topics will be displayed along with the IP address used for the request and a JSON extract of the record from MongoDB.

## Project Structure

```plaintext
twitter-trending-scraper/
├── controller/
│   ├── .env
│   ├── MongodbCrud.py
│   ├── proxymesh.py
│   └── Twitter.py
├── templates/
│   └── index.html
├── app.py
├── requirements.txt
├── LICENSE
└── README.md