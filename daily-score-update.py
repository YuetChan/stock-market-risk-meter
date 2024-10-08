import pandas as pd
import sqlite3
from datetime import datetime


# Load settings from CSV or Excel file (e.g., 'risk_model_settings.csv')
def load_settings(file_path):
    settings_df = pd.read_csv(file_path)  # Or use pd.read_excel() if it's an Excel file
    allowed_stocks = settings_df['stock'].tolist()  # Get the list of allowed stocks
    return allowed_stocks


# Initialize the database (if necessary)
def init_scores():
    conn = sqlite3.connect('/smrm-backend/stocks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_scores (
            id INTEGER PRIMARY KEY,
            stock TEXT,
            score REAL,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Input stock score for the day (loops through each stock in the settings)
def input_daily_score(allowed_stocks):
    conn = sqlite3.connect('/smrm-backend/stocks.db')
    cursor = conn.cursor()

    # Prompt user to enter a specific date or press Enter for today's date
    date_input = input("Enter the date for the score entry (YYYY-MM-DD) or press Enter for today: ")
    
    if date_input:
        try:
            # Try to parse the input date
            date = datetime.strptime(date_input, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return
        
    else:
        # Default to today's date if no input
        date = datetime.now().strftime("%Y-%m-%d")

    # Delete existing data for the given date to avoid duplicates
    cursor.execute('DELETE FROM stock_scores WHERE date = ?', (date,))

    # Loop through each allowed stock and prompt the user to enter the score
    for stock in allowed_stocks:
        while True:
            try:
                score = float(input(f"Enter the score for {stock} (1 to 7): "))
                if score < 1 or score > 7:
                    raise ValueError("Score must be between 1 and 5.")
                break  # Break out of the loop if the score is valid
            except ValueError as e:
                print(e)
        
        # Insert the score for the stock into the database
        cursor.execute('INSERT INTO stock_scores (stock, score, date) VALUES (?, ?, ?)', (stock, score, date))
    

    conn.commit()

    print(f"All scores for {date} have been recorded.")
    
    conn.close()


# Main console program for entering daily scores
def score_console():
    settings_file_path = 'stock-risk-model-settings.csv'  # Path to the settings file
    allowed_stocks = load_settings(settings_file_path)  # Load allowed stocks from the settings file

    init_scores()  # Ensure the database and table are initialized
    
    input_daily_score(allowed_stocks)


if __name__ == "__main__":
    score_console()
