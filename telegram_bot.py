import logging
import matplotlib.pyplot as plt
from io import BytesIO
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from dice_strategies import run_strategy_simulation

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TOKEN = "7457248307:AAGKosnNTyN6zl7--LeNt0JHuRnev1rkBJM"

user_config = {}
user_steps = {}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎲 Welcome to Dice Strategy Simulator Bot!\n\n"
        "Use /configure to set up a simulation or /simulate to run with your last config."
    )

# Step-by-step configuration
async def configure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_config[user_id] = {}
    user_steps[user_id] = "strategy"
    await update.message.reply_text("Choose a strategy: martingale / d_alembert / fixed")

# Handle user replies
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.lower()

    if user_id not in user_steps:
        await update.message.reply_text("Use /configure to start configuration.")
        return

    step = user_steps[user_id]
    config = user_config[user_id]

    try:
        if step == "strategy":
            if text not in ["martingale", "d_alembert", "fixed"]:
                await update.message.reply_text("Invalid. Choose: martingale / d_alembert / fixed")
                return
            config["strategy"] = text
            user_steps[user_id] = "base_bet"
            await update.message.reply_text("Enter base bet amount:")
        elif step == "base_bet":
            config["base_bet"] = float(text)
            user_steps[user_id] = "balance"
            await update.message.reply_text("Enter starting balance:")
        elif step == "balance":
            config["balance"] = float(text)
            user_steps[user_id] = "target"
            await update.message.reply_text("Enter profit target:")
        elif step == "target":
            config["target"] = float(text)
            user_steps[user_id] = "max_rounds"
            await update.message.reply_text("Enter max number of rounds:")
        elif step == "max_rounds":
            config["max_rounds"] = int(text)
            user_steps[user_id] = "payout"
            await update.message.reply_text("Enter payout (e.g., 2.0):")
        elif step == "payout":
            config["payout"] = float(text)
            del user_steps[user_id]  # Finished
            await update.message.reply_text("✅ Configuration complete! Type /simulate to run.")
    except ValueError:
        await update.message.reply_text("Please enter a valid number.")

# Simulate
async def simulate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_config:
        await update.message.reply_text("Please configure first using /configure.")
        return

    config = user_config[user_id]
    logging.info(f"Running simulation with config: {config}")
    await update.message.reply_text("Running simulation with your config... ⏳")

    try:
        result, profit_progression = run_strategy_simulation(
            config["strategy"],
            config["base_bet"],
            config["balance"],
            config["target"],
            config["max_rounds"],
            config["payout"]
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=result["summary"]
        )

        if profit_progression:
            fig, ax = plt.subplots()
            ax.plot(profit_progression, label='Profit over Time', color='blue')
            ax.set_title("📈 Profit Progression")
            ax.set_xlabel("Rounds")
            ax.set_ylabel("Profit")
            ax.grid(True)
            ax.legend()

            buffer = BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            plt.close()
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=buffer)

    except Exception as e:
        logging.error(f"Simulation error: {e}")
        await update.message.reply_text("⚠️ Error during simulation. Please check your inputs.")

# Start bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("configure", configure))
    app.add_handler(CommandHandler("simulate", simulate))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("✅ Telegram bot is running...")
    app.run_polling()
