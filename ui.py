# ui.py

import tkinter as tk
from tkinter import ttk
import threading
from main import run_bot_with_config

class DiceBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎲 Dice Bot GUI")
        self.running = False

        self.setup_widgets()

    def setup_widgets(self):
        padding = {'padx': 10, 'pady': 5}

        # Strategy Dropdown
        tk.Label(self.root, text="Strategy").grid(row=0, column=0, **padding)
        self.strategy = ttk.Combobox(self.root, values=[
            "martingale", "paroli", "flat", "anti_martingale"
        ])
        self.strategy.set("martingale")
        self.strategy.grid(row=0, column=1, **padding)

        # Base Bet
        tk.Label(self.root, text="Base Bet").grid(row=1, column=0, **padding)
        self.base_bet = tk.Entry(self.root)
        self.base_bet.insert(0, "1.0")
        self.base_bet.grid(row=1, column=1, **padding)

        # Start Balance
        tk.Label(self.root, text="Start Balance").grid(row=2, column=0, **padding)
        self.start_balance = tk.Entry(self.root)
        self.start_balance.insert(0, "100.0")
        self.start_balance.grid(row=2, column=1, **padding)

        # Profit Target
        tk.Label(self.root, text="Profit Target").grid(row=3, column=0, **padding)
        self.profit_target = tk.Entry(self.root)
        self.profit_target.insert(0, "20.0")
        self.profit_target.grid(row=3, column=1, **padding)

        # Start Button
        self.start_button = tk.Button(self.root, text="▶ Start", command=self.start_bot)
        self.start_button.grid(row=4, column=0, **padding)

        # Stop Button
        self.stop_button = tk.Button(self.root, text="⏹ Stop", command=self.stop_bot, state="disabled")
        self.stop_button.grid(row=4, column=1, **padding)

        # Output Display
        self.output = tk.Text(self.root, height=10, width=50)
        self.output.grid(row=5, column=0, columnspan=2, **padding)

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def start_bot(self):
        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        config = {
            "strategy": self.strategy.get(),
            "base_bet": float(self.base_bet.get()),
            "start_balance": float(self.start_balance.get()),
            "profit_target": float(self.profit_target.get())
        }
        threading.Thread(target=self.run_thread, args=(config,), daemon=True).start()

    def run_thread(self, config):
        run_bot_with_config(config, log_func=self.log)
        self.stop_bot()

    def stop_bot(self):
        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.log("🛑 Bot stopped.")

def launch_gui():
    root = tk.Tk()
    app = DiceBotGUI(root)
    root.mainloop()
