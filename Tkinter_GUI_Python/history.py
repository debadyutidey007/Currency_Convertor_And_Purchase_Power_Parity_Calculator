import sqlite3
from datetime import datetime

# Database setup
def initialize_database():
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    
    # Create PPP history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ppp_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_country TEXT,
            to_country TEXT,
            ppp_rate REAL,
            calculation_time TEXT
        )
    ''')
    
    # Create Currency Converter history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversion_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_currency TEXT,
            to_currency TEXT,
            amount REAL,
            conversion_rate REAL,
            conversion_time TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# PPP Calculator functions
def calculate_ppp(from_country, to_country):
    # Dummy PPP rate calculation (replace with real logic/API call)
    ppp_rate = 1.25  # Example rate
    log_ppp_calculation(from_country, to_country, ppp_rate)
    return ppp_rate

def log_ppp_calculation(from_country, to_country, ppp_rate):
    try:
        conn = sqlite3.connect('history.db')
        cursor = conn.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "INSERT INTO ppp_history (from_country, to_country, ppp_rate, calculation_time) VALUES (?, ?, ?, ?)",
            (from_country, to_country, ppp_rate, timestamp)
        )
        conn.commit()
        print(f"Logged PPP: {from_country} to {to_country}, Rate: {ppp_rate}")
    except Exception as e:
        print(f"Error logging PPP calculation: {e}")
    finally:
        conn.close()

def get_ppp_history():
    try:
        conn = sqlite3.connect('history.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ppp_history ORDER BY calculation_time DESC")
        history = cursor.fetchall()
        return history
    except Exception as e:
        print(f"Error fetching PPP history: {e}")
        return []
    finally:
        conn.close()

# Currency Converter functions
def convert_currency(from_currency, to_currency, amount):
    # Dummy conversion rate (replace with real logic/API call)
    conversion_rate = 0.85  # Example rate
    converted_amount = amount * conversion_rate
    log_conversion(from_currency, to_currency, amount, conversion_rate)
    return converted_amount

def log_conversion(from_currency, to_currency, amount, conversion_rate):
    try:
        conn = sqlite3.connect('history.db')
        cursor = conn.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "INSERT INTO conversion_history (from_currency, to_currency, amount, conversion_rate, conversion_time) VALUES (?, ?, ?, ?, ?)",
            (from_currency, to_currency, amount, conversion_rate, timestamp)
        )
        conn.commit()
        print(f"Logged Conversion: {amount} {from_currency} to {to_currency}, Rate: {conversion_rate}")
    except Exception as e:
        print(f"Error logging conversion: {e}")
    finally:
        conn.close()

def get_conversion_history():
    try:
        conn = sqlite3.connect('history.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM conversion_history ORDER BY conversion_time DESC")
        history = cursor.fetchall()
        return history
    except Exception as e:
        print(f"Error fetching conversion history: {e}")
        return []
    finally:
        conn.close()

# Main application logic
def main():
    initialize_database()
    
    # Test PPP Calculator
    print("\nTesting PPP Calculator:")
    ppp_rate = calculate_ppp("USA", "Canada")
    print(f"PPP Rate: {ppp_rate}")
    
    # Test Currency Converter
    print("\nTesting Currency Converter:")
    converted_amount = convert_currency("USD", "EUR", 100)
    print(f"Converted Amount: {converted_amount}")
    
    # Display PPP History
    print("\nPPP History:")
    ppp_history = get_ppp_history()
    for entry in ppp_history:
        print(f"ID: {entry[0]}, From: {entry[1]}, To: {entry[2]}, Rate: {entry[3]}, Time: {entry[4]}")
    
    # Display Conversion History
    print("\nConversion History:")
    conversion_history = get_conversion_history()
    for entry in conversion_history:
        print(f"ID: {entry[0]}, From: {entry[1]}, To: {entry[2]}, Amount: {entry[3]}, Rate: {entry[4]}, Time: {entry[5]}")

if __name__ == "__main__":
    main()