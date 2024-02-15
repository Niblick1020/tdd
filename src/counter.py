from flask import Flask, jsonify
import status

app = Flask(__name__)

COUNTERS = {}



@app.route('/counters/<name>', methods=['POST'])
def create_or_reject_counter(name):
    """Create a new counter if it does not exist. If it exists, reject with a
    conflict error."""
    if name in COUNTERS:
        # Counter exists, return a conflict response
        return jsonify({"Message": f"Counter {name} already exists"}), status.HTTP_409_CONFLICT
    else:
        # Create and return a new counter
        COUNTERS[name] = 1
        return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED


@app.route('/counters/<name>', methods=['PUT'])
def update_counter(name):
    """Increment an existing counter by 1. If it doesn't exist, return a not
    found error."""
    if name not in COUNTERS:
        # Counter does not exist, return a not found response
        return jsonify({"Message": f"Counter {name} does not exist"}), status.HTTP_404_NOT_FOUND
    else:
        # Update and return the counter
        COUNTERS[name] += 1
        return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK


@app.route('/counters/<name>', methods=['GET'])
def read_counter(name):
    """Return the current value of an existing counter. If it doesn't exist,
    return a not found error."""
    if name not in COUNTERS:
        # Counter does not exist, return a not found response
        return jsonify({"Message": f"Counter {name} does not exist"}), status.HTTP_404_NOT_FOUND
    else:
        # Return the counter
        return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK


@app.route('/counters/<name>', methods=['DELETE'])
def delete_counter(name):
    """Delete an existing counter. If it doesn't exist, return a not found error."""
    if name in COUNTERS:
        del COUNTERS[name]
        return '', status.HTTP_204_NO_CONTENT
    else:
        return jsonify({"Message": f"Counter {name} does not exist"}), status.HTTP_404_NOT_FOUND