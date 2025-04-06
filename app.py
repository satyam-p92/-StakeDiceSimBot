# app.py

from flask import Flask, render_template, request, redirect, url_for
from threading import Thread
from main import run_bot_with_config

app = Flask(__name__)
bot_thread = None

# Status store (shared between web and thread)
status = {
    "running": False,
    "logs": [],
}

def log_func(msg):
    status["logs"].append(msg)
    if len(status["logs"]) > 100:
        status["logs"].pop(0)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        config = {
            "strategy": request.form["strategy"],
            "base_bet": float(request.form["base_bet"]),
            "start_balance": float(request.form["start_balance"]),
            "profit_target": float(request.form["profit_target"])
        }
        start_bot(config)
        return redirect(url_for("index"))
    return render_template("index.html", status=status)

@app.route("/stop")
def stop():
    status["running"] = False
    return redirect(url_for("index"))

def start_bot(config):
    def bot_runner():
        status["running"] = True
        log_func(f"🚀 Bot started with strategy {config['strategy']}")
        run_bot_with_config(config, log_func=log_func)
        status["running"] = False
        log_func("🛑 Bot stopped.")

    global bot_thread
    if not status["running"]:
        bot_thread = Thread(target=bot_runner, daemon=True)
        bot_thread.start()

if __name__ == "__main__":
    app.run(debug=True)
