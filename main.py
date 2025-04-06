# main.py

import time
from config import *
import strategy
from simulator import roll_dice
from logger import init_logger, log_bet
from telegram_alerts import send_telegram_message


def run_bot():
    config = {
        "strategy": STRATEGY,
        "base_bet": BASE_BET, # type: ignore
        "start_balance": START_BALANCE,
        "profit_target": PROFIT_TARGET
    }
    run_bot_with_config(config)

def run_bot_with_config(custom_config: dict, log_func=print):
    balance = custom_config["start_balance"]
    base_bet = custom_config["base_bet"]
    strategy_name = custom_config["strategy"]
    profit_target = custom_config["profit_target"]

    current_bet = base_bet
    profit = 0.0
    total_bets = 0
    win_streak = 0
    loss_streak = 0
    max_loss_streak = 0

    log_file = init_logger()
    log_func(f"🎮 Starting Dice Bot [{strategy_name.upper()} Strategy]")

    while total_bets < MAX_BETS and profit < profit_target and profit > -STOP_LOSS:
        result = "LOSS"
        win = roll_dice(WIN_CHANCE)
        total_bets += 1

        if win:
            balance += current_bet
            profit += current_bet
            win_streak += 1
            loss_streak = 0
            result = "WIN"
        else:
            balance -= current_bet
            profit -= current_bet
            win_streak = 0
            loss_streak += 1
            max_loss_streak = max(max_loss_streak, loss_streak)

        log_bet(log_file, total_bets, current_bet, result, balance, profit)
        log_func(f"#{total_bets}: {result} | Bet: ${current_bet:.2f} | Profit: ${profit:.2f} | Balance: ${balance:.2f}")

        # Strategy selector
        if strategy_name == "martingale":
            current_bet = strategy.martingale(current_bet, win, base_bet, MULTIPLIER)
        elif strategy_name == "paroli":
            current_bet, win_streak = strategy.paroli(current_bet, win, base_bet, MULTIPLIER, win_streak)
        elif strategy_name == "flat":
            current_bet = strategy.flat(current_bet, win, base_bet)
        elif strategy_name == "anti_martingale":
            current_bet = strategy.anti_martingale(current_bet, win, base_bet, MULTIPLIER)
        else:
            log_func(f"❌ Unknown strategy: {strategy_name}")
            break

        if current_bet > balance:
            log_func("⚠️ Bet exceeds balance! Stopping.")
            break

        time.sleep(DELAY)

    log_func("🛑 Session Ended")
    log_func(f"🎯 Total Bets: {total_bets}")
    log_func(f"💰 Final Balance: ${balance:.2f}")
    log_func(f"📈 Profit: ${profit:.2f}")
    log_func(f"🔻 Max Loss Streak: {max_loss_streak}")

if __name__ == "__main__":
    run_bot()
