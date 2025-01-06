from flask import Flask, jsonify, render_template, request
from controller.Twitter import run_script_and_show_results
from controller.MongodbCrud import fetch_latest_entry_from_db

app = Flask(__name__)

# Route to serve the index.html page
@app.route('/')
def index():
    return render_template('index.html')

# Route to trigger the Selenium script and return the results
@app.route('/run-script', methods=['POST'])
def run_script():
    print("Running /run-script route...")  # Log when the route is called

    # Get username and password from the request
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Run the script and capture the result (which is already a dictionary)
    run_script_and_show_results(username, password)

    # Fetch the latest entry from the database
    latest_entry = fetch_latest_entry_from_db()


    return jsonify(latest_entry)

if __name__ == '__main__':
    app.run(debug=True)