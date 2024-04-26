import pandas as pd
from telegram import Bot, Update, ParseMode
from telegram.ext import Updater, CommandHandler

# Increase the connection pool size
from telegram.utils.request import Request

request = Request(con_pool_size=8)

# Read the data from the CSV file
data = pd.read_csv('disease_precaution.csv')


# Start command handler
def start(update: Update, context):
    update.message.reply_text(
        "Welcome to the Disease Precautions Bot! Use /precautions <disease> command to get precautions for a specific disease.")


# Precautions command handler
def precautions(update: Update, context):
    try:
        # Get the disease name from the user's message
        disease = update.message.text.split("/precautions ", 1)[1].lower()

        # Filter the data for the given disease
        precautions_1 = data[data['Disease'].str.lower() == disease]['Precaution_1']
        precautions_2 = data[data['Disease'].str.lower() == disease]['Precaution_2']
        precautions_3 = data[data['Disease'].str.lower() == disease]['Precaution_3']
        precautions_4 = data[data['Disease'].str.lower() == disease]['Precaution_4']

        # Convert float values to strings
        precautions_1 = precautions_1.astype(str).tolist()
        precautions_2 = precautions_2.astype(str).tolist()
        precautions_3 = precautions_3.astype(str).tolist()
        precautions_4 = precautions_4.astype(str).tolist()

        # Combine the precautions from all columns
        all_precautions = precautions_1 + precautions_2 + precautions_3 + precautions_4

        if all_precautions:
            # Convert the precautions list to a formatted string
            precautions_text = "\n".join(all_precautions)
            response = f"Precautions for {disease}:\n{precautions_text}"
        else:
            response = f"No precautions found for {disease}"

        # Send the response back to the user
        update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
    except IndexError:
        # Handle the case when the command is not followed by a disease name
        update.message.reply_text("Please specify a disease name. Example: /precautions flu")
    except Exception as e:
        # Handle other exceptions
        update.message.reply_text("An error occurred. Please try again later.")
        print(f"Error: {e}")


# Error handler
def error_handler(update: Update, context):
    # Log the error message
    print(f"Update {update} caused error {context.error}")

    # Reply to the user with an error message
    update.message.reply_text("An error occurred. Please try again later.")


# Main function
def main():
    # Initialize the bot
    bot = Bot(token="6226543223:AAHuVdQXFs4m-nKPxBVEKUNZ4ovkN3DRMaI", request=request)

    # Initialize the updater and dispatcher
    updater = Updater(bot=bot, use_context=True)
    dispatcher = updater.dispatcher

    # Add the command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("precautions", precautions))

    # Add the error handler
    dispatcher.add_error_handler(error_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
