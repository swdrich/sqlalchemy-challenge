# 1. import Flask
from flask import Flask, jsonify

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# 3. Define what to do when a user hits the index route
@app.route("/")
def index():
    return "Welcome to the 'Index' page!"


# 4. Define what to do when a user hits the /stations route
@app.route("/api/v1.0/stations")
def stations():
    return "Welcome to the 'Stations' page!"

# 5. Define what to do when a user hits the /tobs route
@app.route("/api/v1.0/tobs")
def stations():
    return "Welcome to the 'Temperature Observations' page!"

# 6. Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def stations():
    return "Welcome to the 'Precipitation' page!"



if __name__ == "__main__":
    app.run(debug=True)