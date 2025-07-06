from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = "data.json"

# Load data
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route('/')
def home():
    return '''
        <h2>Enter Room</h2>
        <form action="/go" method="post">
            <input name="room_id" placeholder="Enter room name">
            <button type="submit">Enter</button>
        </form>
    '''

@app.route('/go', methods=['POST'])
def go():
    room_id = request.form['room_id']
    return redirect(url_for('room', room_id=room_id))

@app.route('/room/<room_id>', methods=['GET', 'POST'])
def room(room_id):
    data = load_data()
    if room_id not in data:
        data[room_id] = []

    if request.method == 'POST':
        msg = request.form['message'].strip()
        if msg:
            data[room_id].append(msg)
            save_data(data)

    return render_template("room.html", room_id=room_id, messages=data[room_id])

if __name__ == "__main__":
    app.run(debug=True)
