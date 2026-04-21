from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = "habits.json"

def load_habits():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f)

def save_habits(habits):
    with open(DATA_FILE, "w") as f:
        json.dump(habits, f)

@app.route("/", methods=["GET", "POST"])
def index():
    habits = load_habits()
    if request.method == "POST":
        new_habit = request.form.get("habit")
        if new_habit:  # avoid empty entries
            habits.append({"name": new_habit, "done": False})
            save_habits(habits)
        return redirect("/")
    return render_template("index.html", habits=habits)

@app.route("/complete/<int:habit_id>", methods=["POST"])
def complete(habit_id):
    habits = load_habits()
    if 0 <= habit_id < len(habits):
        habits[habit_id]["done"] = True
        save_habits(habits)
    return redirect("/")

@app.route("/delete/<int:habit_id>", methods=["POST"])
def delete(habit_id):
    habits = load_habits()
    if 0 <= habit_id < len(habits):
        habits.pop(habit_id)
        save_habits(habits)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
