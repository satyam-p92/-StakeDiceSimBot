def run_strategy_simulation(strategy_name, base_bet, balance, target, max_rounds, payout):
    profit_progression = []
    profit = 0
    current_bet = base_bet
    initial_balance = balance

    for round_num in range(max_rounds):
        if balance < current_bet:
            break

        win = payout > 2.0  # Simulated outcome
        if win:
            profit += current_bet * (payout - 1)
            balance += current_bet * (payout - 1)
            current_bet = base_bet
        else:
            profit -= current_bet
            balance -= current_bet
            if strategy_name == "martingale":
                current_bet *= 2
            elif strategy_name == "d_alembert":
                current_bet += base_bet
            elif strategy_name == "fixed":
                current_bet = base_bet

        profit_progression.append(profit)

        if profit >= target:
            break

    summary = (
        f"📊 Strategy: {strategy_name}\n"
        f"💰 Starting Balance: {initial_balance}\n"
        f"🎯 Target Profit: {target}\n"
        f"🏁 Final Balance: {balance}\n"
        f"📈 Final Profit: {profit}\n"
        f"🔁 Rounds Played: {len(profit_progression)}"
    )

    return {"summary": summary}, profit_progression
