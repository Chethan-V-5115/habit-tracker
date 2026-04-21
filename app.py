from flask import Flask, render_template, request, redirect
import json, datetime

app = Flask(__name__)
DATA_FILE = "habits.json"

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def index():
    data = load_data()
    today = datetime.date.today().isoformat()
    habits = data["habits"]
    logs_today = [log for log in data["logs"] if log["date"] == today]
    done_ids = [log["habit_id"] for log in logs_today if log["done"]]
    completion = (len(done_ids) / len(habits)) * 100 if habits else 0
    return render_template("index.html", habits=habits, done_ids=done_ids, completion=completion)

@app.route("/update", methods=["POST"])
def update():
    data = load_data()
    today = datetime.date.today().isoformat()
    habit_id = int(request.form["habit_id"])
    done = request.form.get("done") == "true"

    # Remove old log for today
    data["logs"] = [log for log in data["logs"] if not (log["date"] == today and log["habit_id"] == habit_id)]
    # Add new log
    data["logs"].append({"date": today, "habit_id": habit_id, "done": done})

    # Update streak
    habit = next(h for h in data["habits"] if h["id"] == habit_id)
    if done:
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
        yesterday_log = any(log["date"] == yesterday and log["habit_id"] == habit_id and log["done"] for log in data["logs"])
        habit["streak"] = habit["streak"] + 1 if yesterday_log else 1
    else:
        habit["streak"] = 0

    save_data(data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
