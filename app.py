from flask import Flask, jsonify, render_template
import subprocess
import json
from datetime import datetime
import sys
import io
from Twitter import run_script_and_show_results
from viewTrendingTopics import fetch_latest_entry_from_db

app = Flask(__name__)

# Route to serve the index.html page
@app.route('/')
def index():
    return render_template('index.html')

# Route to trigger the Selenium script and return the results
@app.route('/run-script')
def run_script():
    print("Running /run-script route...")  # Log when the route is called

    # Run the script and capture the result (which is already a dictionary)
    run_script_and_show_results()

    # Fetch the latest entry from the database
    latest_entry = fetch_latest_entry_from_db()
    print(f"Latest entry: {latest_entry}")
   
    return jsonify(latest_entry)




if __name__ == '__main__':
    app.run(debug=True)
