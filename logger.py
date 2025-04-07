# logger.py

import csv
import os
from datetime import datetime

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

def init_logger():
    filename = f"logs/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Bet #", "Bet Amount", "Result", "Balance", "Profit"])
    return filename

def log_bet(filename, bet_number, bet_amount, result, balance, profit):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([bet_number, f"{bet_amount:.2f}", result, f"{balance:.2f}", f"{profit:.2f}"])
