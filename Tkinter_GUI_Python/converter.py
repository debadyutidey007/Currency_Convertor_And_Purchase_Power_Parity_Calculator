import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests
import logging
import datetime
import tkinter.messagebox as messagebox
from typing import Optional, Dict
import mysql.connector
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ---------------------------
# MySQL Database Functions
# ---------------------------
def get_db_connection():
    """Get MySQL database connection."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="DEBADYUTIDEY7700",  # Update with your MySQL password
            database="currency_converter",
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        return conn
    except mysql.connector.Error as e:
        logging.error(f"Database connection error: {e}")
        return None

def initialize_database():
    """Initialize database and tables if they don't exist."""
    try:
        # First connect without specifying database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="DEBADYUTIDEY7700",  # Update with your MySQL password
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS currency_converter CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute("USE currency_converter")
        
        # Create currencies table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS currencies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                code VARCHAR(3) UNIQUE NOT NULL,
                name VARCHAR(100),
                symbol VARCHAR(10),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create countries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS countries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                code VARCHAR(3) UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL,
                currency_code VARCHAR(3),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (currency_code) REFERENCES currencies(code)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create conversion_history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversion_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                conversion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                from_currency VARCHAR(3) NOT NULL,
                to_currency VARCHAR(3) NOT NULL,
                amount DECIMAL(15, 4) NOT NULL,
                result DECIMAL(15, 4) NOT NULL,
                exchange_rate DECIMAL(12, 6) NOT NULL,
                FOREIGN KEY (from_currency) REFERENCES currencies(code),
                FOREIGN KEY (to_currency) REFERENCES currencies(code)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create ppp_history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ppp_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                calculation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                from_country VARCHAR(3) NOT NULL,
                to_country VARCHAR(3) NOT NULL,
                ppp_rate DECIMAL(10, 4),
                big_mac_index DECIMAL(8, 4),
                cost_of_living_index DECIMAL(8, 4),
                income_from DECIMAL(15, 2),
                income_equivalent DECIMAL(15, 2),
                FOREIGN KEY (from_country) REFERENCES countries(code),
                FOREIGN KEY (to_country) REFERENCES countries(code)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Insert comprehensive currency data
        cursor.execute("SELECT COUNT(*) FROM currencies")
        if cursor.fetchone()[0] == 0:
            currencies = [
                ("AED", "UAE Dirham", "د.إ"), ("AFN", "Afghan Afghani", "؋"), ("ALL", "Albanian Lek", "L"),
                ("AMD", "Armenian Dram", "֏"), ("ANG", "Netherlands Antillean Guilder", "ƒ"), ("AOA", "Angolan Kwanza", "Kz"),
                ("ARS", "Argentine Peso", "$"), ("AUD", "Australian Dollar", "$"), ("AWG", "Aruban Florin", "ƒ"),
                ("AZN", "Azerbaijani Manat", "₼"), ("BAM", "Bosnia and Herzegovina Convertible Mark", "KM"), ("BBD", "Barbadian Dollar", "$"),
                ("BDT", "Bangladeshi Taka", "৳"), ("BGN", "Bulgarian Lev", "лв"), ("BHD", "Bahraini Dinar", ".د.ب"),
                ("BIF", "Burundian Franc", "FBu"), ("BMD", "Bermudian Dollar", "$"), ("BND", "Brunei Dollar", "$"),
                ("BOB", "Bolivian Boliviano", "$b"), ("BRL", "Brazilian Real", "R$"), ("BSD", "Bahamian Dollar", "$"),
                ("BTN", "Bhutanese Ngultrum", "Nu."), ("BWP", "Botswana Pula", "P"), ("BYN", "Belarusian Ruble", "Br"),
                ("BZD", "Belize Dollar", "BZ$"), ("CAD", "Canadian Dollar", "$"), ("CDF", "Congolese Franc", "FC"),
                ("CHF", "Swiss Franc", "CHF"), ("CLP", "Chilean Peso", "$"), ("CNY", "Chinese Yuan", "¥"),
                ("COP", "Colombian Peso", "$"), ("CRC", "Costa Rican Colon", "₡"), ("CUP", "Cuban Peso", "₱"),
                ("CVE", "Cape Verdean Escudo", "$"), ("CZK", "Czech Koruna", "Kč"), ("DJF", "Djiboutian Franc", "Fdj"),
                ("DKK", "Danish Krone", "kr"), ("DOP", "Dominican Peso", "RD$"), ("DZD", "Algerian Dinar", "دج"),
                ("EGP", "Egyptian Pound", "£"), ("ERN", "Eritrean Nakfa", "Nfk"), ("ETB", "Ethiopian Birr", "Br"),
                ("EUR", "Euro", "€"), ("FJD", "Fijian Dollar", "$"), ("FKP", "Falkland Islands Pound", "£"),
                ("GBP", "British Pound Sterling", "£"), ("GEL", "Georgian Lari", "₾"), ("GHS", "Ghanaian Cedi", "¢"),
                ("GIP", "Gibraltar Pound", "£"), ("GMD", "Gambian Dalasi", "D"), ("GNF", "Guinean Franc", "FG"),
                ("GTQ", "Guatemalan Quetzal", "Q"), ("GYD", "Guyanaese Dollar", "$"), ("HKD", "Hong Kong Dollar", "$"),
                ("HNL", "Honduran Lempira", "L"), ("HRK", "Croatian Kuna", "kn"), ("HTG", "Haitian Gourde", "G"),
                ("HUF", "Hungarian Forint", "Ft"), ("IDR", "Indonesian Rupiah", "Rp"), ("ILS", "Israeli New Sheqel", "₪"),
                ("INR", "Indian Rupee", "₹"), ("IQD", "Iraqi Dinar", "ع.د"), ("IRR", "Iranian Rial", "﷼"),
                ("ISK", "Icelandic Krona", "kr"), ("JMD", "Jamaican Dollar", "J$"), ("JOD", "Jordanian Dinar", "JD"),
                ("JPY", "Japanese Yen", "¥"), ("KES", "Kenyan Shilling", "KSh"), ("KGS", "Kyrgystani Som", "лв"),
                ("KHR", "Cambodian Riel", "៛"), ("KMF", "Comorian Franc", "CF"), ("KPW", "North Korean Won", "₩"),
                ("KRW", "South Korean Won", "₩"), ("KWD", "Kuwaiti Dinar", "KD"), ("KYD", "Cayman Islands Dollar", "$"),
                ("KZT", "Kazakhstani Tenge", "₸"), ("LAK", "Laotian Kip", "₭"), ("LBP", "Lebanese Pound", "£"),
                ("LKR", "Sri Lankan Rupee", "₨"), ("LRD", "Liberian Dollar", "$"), ("LSL", "Lesotho Loti", "M"),
                ("LYD", "Libyan Dinar", "LD"), ("MAD", "Moroccan Dirham", "MAD"), ("MDL", "Moldovan Leu", "L"),
                ("MGA", "Malagasy Ariary", "Ar"), ("MKD", "Macedonian Denar", "ден"), ("MMK", "Myanma Kyat", "K"),
                ("MNT", "Mongolian Tugrik", "₮"), ("MOP", "Macanese Pataca", "MOP$"), ("MRU", "Mauritanian Ouguiya", "UM"),
                ("MUR", "Mauritian Rupee", "₨"), ("MVR", "Maldivian Rufiyaa", "Rf"), ("MWK", "Malawian Kwacha", "MK"),
                ("MXN", "Mexican Peso", "$"), ("MYR", "Malaysian Ringgit", "RM"), ("MZN", "Mozambican Metical", "MT"),
                ("NAD", "Namibian Dollar", "$"), ("NGN", "Nigerian Naira", "₦"), ("NIO", "Nicaraguan Cordoba", "C$"),
                ("NOK", "Norwegian Krone", "kr"), ("NPR", "Nepalese Rupee", "₨"), ("NZD", "New Zealand Dollar", "$"),
                ("OMR", "Omani Rial", "﷼"), ("PAB", "Panamanian Balboa", "B/."), ("PEN", "Peruvian Nuevo Sol", "S/."),
                ("PGK", "Papua New Guinean Kina", "K"), ("PHP", "Philippine Peso", "₱"), ("PKR", "Pakistani Rupee", "₨"),
                ("PLN", "Polish Zloty", "zł"), ("PYG", "Paraguayan Guarani", "Gs"), ("QAR", "Qatari Rial", "﷼"),
                ("RON", "Romanian Leu", "lei"), ("RSD", "Serbian Dinar", "Дин."), ("RUB", "Russian Ruble", "₽"),
                ("RWF", "Rwandan Franc", "R₣"), ("SAR", "Saudi Riyal", "﷼"), ("SBD", "Solomon Islands Dollar", "$"),
                ("SCR", "Seychellois Rupee", "₨"), ("SDG", "Sudanese Pound", "ج.س."), ("SEK", "Swedish Krona", "kr"),
                ("SGD", "Singapore Dollar", "$"), ("SLL", "Sierra Leonean Leone", "Le"), ("SOS", "Somali Shilling", "S"),
                ("SRD", "Surinamese Dollar", "$"), ("SSP", "South Sudanese Pound", "£"), ("STN", "Sao Tome and Principe Dobra", "Db"),
                ("SVC", "Salvadoran Colon", "$"), ("SYP", "Syrian Pound", "£"), ("SZL", "Swazi Lilangeni", "E"),
                ("THB", "Thai Baht", "฿"), ("TJS", "Tajikistani Somoni", "SM"), ("TMT", "Turkmenistani Manat", "T"),
                ("TND", "Tunisian Dinar", "د.ت"), ("TOP", "Tongan Pa'anga", "T$"), ("TRY", "Turkish Lira", "₺"),
                ("TTD", "Trinidad and Tobago Dollar", "TT$"), ("TWD", "New Taiwan Dollar", "NT$"), ("TZS", "Tanzanian Shilling", "TSh"),
                ("UAH", "Ukrainian Hryvnia", "₴"), ("UGX", "Ugandan Shilling", "USh"), ("USD", "US Dollar", "$"),
                ("UYU", "Uruguayan Peso", "$U"), ("UZS", "Uzbekistan Som", "лв"), ("VES", "Venezuelan Bolívar", "Bs"),
                ("VND", "Vietnamese Dong", "₫"), ("VUV", "Vanuatu Vatu", "VT"), ("WST", "Samoan Tala", "WS$"),
                ("XAF", "CFA Franc BEAC", "FCFA"), ("XCD", "East Caribbean Dollar", "$"), ("XOF", "CFA Franc BCEAO", "CFA"),
                ("XPF", "CFP Franc", "₣"), ("YER", "Yemeni Rial", "﷼"), ("ZAR", "South African Rand", "R"),
                ("ZMW", "Zambian Kwacha", "ZK"), ("ZWL", "Zimbabwean Dollar", "Z$")
            ]
            
            for code, name, symbol in currencies:
                cursor.execute("INSERT INTO currencies (code, name, symbol) VALUES (%s, %s, %s)", (code, name, symbol))
        
        # Insert comprehensive country data
        cursor.execute("SELECT COUNT(*) FROM countries")
        if cursor.fetchone()[0] == 0:
            countries = [
                ("US", "United States", "USD"), ("GB", "United Kingdom", "GBP"), ("DE", "Germany", "EUR"),
                ("FR", "France", "EUR"), ("IT", "Italy", "EUR"), ("ES", "Spain", "EUR"), ("JP", "Japan", "JPY"),
                ("CN", "China", "CNY"), ("IN", "India", "INR"), ("BR", "Brazil", "BRL"), ("CA", "Canada", "CAD"),
                ("AU", "Australia", "AUD"), ("RU", "Russia", "RUB"), ("KR", "South Korea", "KRW"),
                ("MX", "Mexico", "MXN"), ("ID", "Indonesia", "IDR"), ("SA", "Saudi Arabia", "SAR"),
                ("TR", "Turkey", "TRY"), ("CH", "Switzerland", "CHF"), ("NL", "Netherlands", "EUR"),
                ("BE", "Belgium", "EUR"), ("SE", "Sweden", "SEK"), ("NO", "Norway", "NOK"), ("DK", "Denmark", "DKK"),
                ("FI", "Finland", "EUR"), ("PL", "Poland", "PLN"), ("CZ", "Czech Republic", "CZK"),
                ("HU", "Hungary", "HUF"), ("IL", "Israel", "ILS"), ("ZA", "South Africa", "ZAR"),
                ("AE", "United Arab Emirates", "AED"), ("SG", "Singapore", "SGD"), ("HK", "Hong Kong", "HKD"),
                ("MY", "Malaysia", "MYR"), ("TH", "Thailand", "THB"), ("PH", "Philippines", "PHP"),
                ("VN", "Vietnam", "VND"), ("EG", "Egypt", "EGP"), ("NG", "Nigeria", "NGN"),
                ("AR", "Argentina", "ARS"), ("CL", "Chile", "CLP"), ("CO", "Colombia", "COP"),
                ("PE", "Peru", "PEN"), ("UA", "Ukraine", "UAH"), ("RO", "Romania", "RON"),
                ("BG", "Bulgaria", "BGN"), ("HR", "Croatia", "HRK"), ("SI", "Slovenia", "EUR"),
                ("LT", "Lithuania", "EUR"), ("LV", "Latvia", "EUR"), ("EE", "Estonia", "EUR"),
                ("SK", "Slovakia", "EUR"), ("MT", "Malta", "EUR"), ("CY", "Cyprus", "EUR"),
                ("LU", "Luxembourg", "EUR"), ("IE", "Ireland", "EUR"), ("AT", "Austria", "EUR"),
                ("PT", "Portugal", "EUR"), ("GR", "Greece", "EUR"), ("IS", "Iceland", "ISK"),
                ("LI", "Liechtenstein", "CHF"), ("MC", "Monaco", "EUR"), ("SM", "San Marino", "EUR")
            ]
            
            for code, name, currency in countries:
                cursor.execute("INSERT INTO countries (code, name, currency_code) VALUES (%s, %s, %s)", (code, name, currency))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logging.error(f"Database initialization error: {e}")
        return False

def get_currency_codes():
    """Get comprehensive list of currency codes from database."""
    try:
        conn = get_db_connection()
        if not conn:
            return get_fallback_currencies()
            
        cursor = conn.cursor()
        cursor.execute("SELECT code FROM currencies ORDER BY code")
        codes = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return codes if codes else get_fallback_currencies()
    except Exception as e:
        logging.error(f"Error fetching currency codes: {e}")
        return get_fallback_currencies()

def get_fallback_currencies():
    """Fallback currency list if database is unavailable."""
    return [
        "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN",
        "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BRL",
        "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHF", "CLP", "CNY",
        "COP", "CRC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP",
        "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GHS", "GIP", "GMD",
        "GNF", "GTQ", "GYD", "HKD", "HNL", "HRK", "HTG", "HUF", "IDR", "ILS",
        "INR", "IQD", "IRR", "ISK", "JMD", "JOD", "JPY", "KES", "KGS", "KHR",
        "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD",
        "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRU",
        "MUR", "MVR", "MWK", "MXN", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK",
        "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG",
        "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK",
        "SGD", "SLL", "SOS", "SRD", "SSP", "STN", "SVC", "SYP", "SZL", "THB",
        "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX",
        "USD", "UYU", "UZS", "VES", "VND", "VUV", "WST", "XAF", "XCD", "XOF",
        "XPF", "YER", "ZAR", "ZMW", "ZWL"
    ]

def get_country_codes():
    """Get list of country codes and names from database."""
    try:
        conn = get_db_connection()
        if not conn:
            return get_fallback_countries()
            
        cursor = conn.cursor()
        cursor.execute("SELECT code, name FROM countries ORDER BY name")
        countries = [(row[0], row[1]) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return countries if countries else get_fallback_countries()
    except Exception as e:
        logging.error(f"Error fetching country codes: {e}")
        return get_fallback_countries()

def get_fallback_countries():
    """Fallback country list if database is unavailable."""
    return [
        ("US", "United States"), ("GB", "United Kingdom"), ("DE", "Germany"),
        ("FR", "France"), ("IT", "Italy"), ("ES", "Spain"), ("JP", "Japan"),
        ("CN", "China"), ("IN", "India"), ("BR", "Brazil"), ("CA", "Canada"),
        ("AU", "Australia"), ("RU", "Russia"), ("KR", "South Korea"),
        ("MX", "Mexico"), ("ID", "Indonesia"), ("SA", "Saudi Arabia"),
        ("TR", "Turkey"), ("CH", "Switzerland"), ("NL", "Netherlands")
    ]

def log_conversion_to_db(conversion_time, from_currency, to_currency, amount, result, exchange_rate):
    """Insert conversion record into database."""
    try:
        conn = get_db_connection()
        if not conn:
            return
            
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO conversion_history 
            (conversion_time, from_currency, to_currency, amount, result, exchange_rate)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (conversion_time, from_currency, to_currency, amount, result, exchange_rate))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error logging conversion: {e}")

def log_ppp_calculation_to_db(calculation_time, from_country, to_country, ppp_rate, big_mac_index, cost_of_living_index):
    """Insert PPP calculation record into database."""
    try:
        conn = get_db_connection()
        if not conn:
            return
            
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ppp_history 
            (calculation_time, from_country, to_country, ppp_rate, big_mac_index, cost_of_living_index)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (calculation_time, from_country, to_country, ppp_rate, big_mac_index, cost_of_living_index))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error logging PPP calculation: {e}")

def get_conversion_history():
    """Retrieve conversion history from database."""
    try:
        conn = get_db_connection()
        if not conn:
            return []
            
        cursor = conn.cursor()
        cursor.execute("""
            SELECT conversion_time, from_currency, to_currency, amount, result
            FROM conversion_history
            ORDER BY conversion_time DESC
            LIMIT 100
        """)
        history = cursor.fetchall()
        cursor.close()
        conn.close()
        
        formatted_history = []
        for row in history:
            formatted_history.append((
                row[0].strftime("%Y-%m-%d %H:%M:%S") if row[0] else "",
                row[1] or "",
                row[2] or "",
                f"{float(row[3]):.2f}" if row[3] else "0.00",
                f"{float(row[4]):.2f}" if row[4] else "0.00"
            ))
        return formatted_history
    except Exception as e:
        logging.error(f"Error fetching conversion history: {e}")
        return []

def get_ppp_history():
    """Retrieve PPP calculation history from database."""
    try:
        conn = get_db_connection()
        if not conn:
            return []
            
        cursor = conn.cursor()
        cursor.execute("""
            SELECT calculation_time, from_country, to_country, ppp_rate, big_mac_index, cost_of_living_index
            FROM ppp_history
            ORDER BY calculation_time DESC
            LIMIT 100
        """)
        history = cursor.fetchall()
        cursor.close()
        conn.close()
        
        formatted_history = []
        for row in history:
            formatted_history.append((
                row[0].strftime("%Y-%m-%d %H:%M:%S") if row[0] else "",
                row[1] or "",
                row[2] or "",
                f"{float(row[3]):.4f}" if row[3] else "0.0000",
                f"{float(row[4]):.4f}" if row[4] else "0.0000",
                f"{float(row[5]):.4f}" if row[5] else "0.0000"
            ))
        return formatted_history
    except Exception as e:
        logging.error(f"Error fetching PPP history: {e}")
        return []

def clear_conversion_history():
    """Clear all conversion history records."""
    try:
        conn = get_db_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()
        cursor.execute("DELETE FROM conversion_history")
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        logging.error(f"Error clearing conversion history: {e}")
        return False

def clear_ppp_history():
    """Clear all PPP history records."""
    try:
        conn = get_db_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ppp_history")
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        logging.error(f"Error clearing PPP history: {e}")
        return False

# ---------------------------
# Exchange Rate API Functions
# ---------------------------
def get_exchange_rate(from_currency, to_currency):
    """Get real-time exchange rate using multiple API sources."""
    try:
        # Try ExchangeRate-API (free tier)
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if to_currency in data['rates']:
                return data['rates'][to_currency]
    except Exception as e:
        logging.warning(f"ExchangeRate-API failed: {e}")
    
    try:
        # Try Fixer.io as backup (requires API key but has free tier)
        # For demo purposes, using mock data
        # In production, replace with actual API key
        rates = {
            'USD': {'EUR': 0.85, 'GBP': 0.73, 'JPY': 110.0, 'INR': 83.12, 'CAD': 1.25, 'AUD': 1.35},
            'EUR': {'USD': 1.18, 'GBP': 0.86, 'JPY': 129.0, 'INR': 98.0, 'CAD': 1.47, 'AUD': 1.59},
            'GBP': {'USD': 1.37, 'EUR': 1.16, 'JPY': 150.0, 'INR': 114.0, 'CAD': 1.71, 'AUD': 1.85},
            'JPY': {'USD': 0.0091, 'EUR': 0.0077, 'GBP': 0.0067, 'INR': 0.76, 'CAD': 0.011, 'AUD': 0.012},
            'INR': {'USD': 0.012, 'EUR': 0.010, 'GBP': 0.0088, 'JPY': 1.32, 'CAD': 0.015, 'AUD': 0.016}
        }
        
        if from_currency in rates and to_currency in rates[from_currency]:
            return rates[from_currency][to_currency]
        elif to_currency in rates and from_currency in rates[to_currency]:
            return 1.0 / rates[to_currency][from_currency]
    except Exception as e:
        logging.warning(f"Backup rate lookup failed: {e}")
    
    # Fallback to 1.0 if all APIs fail
    return 1.0

# ---------------------------
# PPP Calculation Functions
# ---------------------------
def get_ppp_data(country_code: str) -> Optional[Dict]:
    """Get comprehensive PPP data for a country."""
    ppp_data = {
        "US": {"ppp_rate": 1.0, "big_mac_price": 5.81, "cost_of_living": 100.0},
        "GB": {"ppp_rate": 0.72, "big_mac_price": 4.19, "cost_of_living": 85.2},
        "DE": {"ppp_rate": 0.79, "big_mac_price": 4.95, "cost_of_living": 73.8},
        "FR": {"ppp_rate": 0.81, "big_mac_price": 5.21, "cost_of_living": 78.9},
        "IT": {"ppp_rate": 0.75, "big_mac_price": 5.15, "cost_of_living": 72.4},
        "ES": {"ppp_rate": 0.70, "big_mac_price": 4.75, "cost_of_living": 65.8},
        "JP": {"ppp_rate": 102.74, "big_mac_price": 390.0, "cost_of_living": 83.4},
        "CN": {"ppp_rate": 3.51, "big_mac_price": 24.40, "cost_of_living": 42.1},
        "IN": {"ppp_rate": 22.27, "big_mac_price": 190.0, "cost_of_living": 25.1},
        "BR": {"ppp_rate": 2.32, "big_mac_price": 17.65, "cost_of_living": 33.7},
        "CA": {"ppp_rate": 1.24, "big_mac_price": 6.77, "cost_of_living": 73.2},
        "AU": {"ppp_rate": 1.52, "big_mac_price": 6.75, "cost_of_living": 75.8},
        "RU": {"ppp_rate": 25.1, "big_mac_price": 135.0, "cost_of_living": 28.5},
        "KR": {"ppp_rate": 870.0, "big_mac_price": 4200.0, "cost_of_living": 78.1},
        "MX": {"ppp_rate": 9.8, "big_mac_price": 54.0, "cost_of_living": 35.6},
        "ID": {"ppp_rate": 6800.0, "big_mac_price": 31000.0, "cost_of_living": 32.8},
        "SA": {"ppp_rate": 1.8, "big_mac_price": 14.0, "cost_of_living": 45.7},
        "TR": {"ppp_rate": 3.2, "big_mac_price": 15.5, "cost_of_living": 38.9},
        "CH": {"ppp_rate": 1.2, "big_mac_price": 6.5, "cost_of_living": 122.4},
        "NL": {"ppp_rate": 0.84, "big_mac_price": 4.95, "cost_of_living": 79.2}
    }
    return ppp_data.get(country_code)

def calculate_ppp_comparison(from_country: str, to_country: str) -> Dict:
    """Calculate comprehensive PPP comparison between countries."""
    try:
        from_data = get_ppp_data(from_country)
        to_data = get_ppp_data(to_country)
        
        if not from_data or not to_data:
            return {"error": "PPP data not available for selected countries"}
        
        ppp_ratio = to_data["ppp_rate"] / from_data["ppp_rate"]
        big_mac_ratio = to_data["big_mac_price"] / from_data["big_mac_price"]
        cost_of_living_ratio = to_data["cost_of_living"] / from_data["cost_of_living"]
        
        return {
            "ppp_ratio": ppp_ratio,
            "big_mac_ratio": big_mac_ratio,
            "cost_of_living_ratio": cost_of_living_ratio,
            "from_data": from_data,
            "to_data": to_data
        }
    except Exception as e:
        logging.error(f"Error calculating PPP comparison: {e}")
        return {"error": str(e)}

# ---------------------------
# GUI Components
# ---------------------------
class AutocompleteCombobox(ttk.Combobox):
    """Enhanced combobox with autocompletion and debounce."""
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self._completion_list = list(self['values'])
        self._after_id = None
        self.bind('<KeyRelease>', self._handle_keyrelease)
    
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)
        self['values'] = self._completion_list

    def _handle_keyrelease(self, event):
        if event.keysym in ("Up", "Down", "Left", "Right", "Return", "Escape"):
            return
        if self._after_id:
            self.after_cancel(self._after_id)
        self._after_id = self.after(300, self._perform_filter)

    def _perform_filter(self):
        current_text = self.get()
        if not current_text:
            self['values'] = self._completion_list
        else:
            filtered = [item for item in self._completion_list if current_text.lower() in item.lower()]
            self['values'] = filtered if filtered else self._completion_list
        self._after_id = None
        if current_text and self['values']:
            self.event_generate('<Down>')

class CreateToolTip:
    """Professional tooltip implementation."""
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(500, self.showtip)

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def showtip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = ttk.Label(tw, text=self.text, justify=LEFT, background="#ffffe0",
                         relief=SOLID, borderwidth=1, font=("Segoe UI", 10))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

# ---------------------------
# Main Application Class
# ---------------------------
class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Currency Converter & PPP Calculator")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        # Initialize database
        initialize_database()
        
        # Configure styling
        self.configure_styles()
        
        # Load data
        self.currency_codes = get_currency_codes()
        self.country_data = get_country_codes()
        self.country_codes = [f"{code} - {name}" for code, name in self.country_data]
        
        # Create interface
        self.create_main_interface()
        
        # Load initial history
        self.load_conversion_history()
        self.load_ppp_history()

    def configure_styles(self):
        """Configure professional styling."""
        style = ttk.Style()
        
        try:
            style.configure("TFrame", background="#f8fafc")
            style.configure("TNotebook", background="#f8fafc", borderwidth=0)
            style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=(15, 8))
            
            style.configure("MainHeader.TLabel", 
                           font=("Segoe UI", 20, "bold"),
                           foreground="#2563eb",
                           background="#f8fafc")
            
            style.configure("SectionHeader.TLabel", 
                           font=("Segoe UI", 14, "bold"),
                           foreground="#1e293b",
                           background="#ffffff")
            
            style.configure("TLabel", 
                           font=("Segoe UI", 10),
                           background="#ffffff",
                           foreground="#1e293b")
            
            style.configure("Field.TLabel", 
                           font=("Segoe UI", 10, "bold"),
                           background="#ffffff",
                           foreground="#1e293b")
            
            style.configure("TEntry", font=("Segoe UI", 10))
            style.configure("TCombobox", font=("Segoe UI", 10))
            style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"))
            style.configure("Secondary.TButton", font=("Segoe UI", 10))
            
            style.configure("TLabelframe", background="#ffffff")
            style.configure("TLabelframe.Label", 
                           font=("Segoe UI", 11, "bold"),
                           background="#ffffff",
                           foreground="#1e293b")
            
            style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
            style.configure("Treeview", font=("Segoe UI", 9), rowheight=28)
            
        except Exception as e:
            logging.warning(f"Styling configuration failed: {e}")

    def create_main_interface(self):
        """Create the main tabbed interface."""
        # Main header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=X, padx=20, pady=10)
        
        main_header = ttk.Label(header_frame, 
                               text="Professional Currency Converter & PPP Calculator",
                               style="MainHeader.TLabel")
        main_header.pack()
        
        # Create notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=YES, padx=20, pady=10)
        
        # Create tabs
        self.converter_tab = ttk.Frame(self.notebook)
        self.ppp_tab = ttk.Frame(self.notebook)
        self.history_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.converter_tab, text="Currency Converter")
        self.notebook.add(self.ppp_tab, text="Purchase Power Parity")
        self.notebook.add(self.history_tab, text="History")
        
        # Create tab content
        self.create_converter_tab()
        self.create_ppp_tab()
        self.create_history_tab()
        self.create_menu()
        self.create_status_bar()

    def create_converter_tab(self):
        """Create currency converter interface."""
        main_card = ttk.LabelFrame(self.converter_tab, text="Currency Conversion", padding=20)
        main_card.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Input section
        input_frame = ttk.Frame(main_card)
        input_frame.pack(fill=X, pady=(0, 20))
        
        # Amount input
        amount_frame = ttk.Frame(input_frame)
        amount_frame.pack(fill=X, pady=5)
        ttk.Label(amount_frame, text="Amount:", style="Field.TLabel").pack(side=LEFT, padx=(0, 10))
        self.amount_entry = ttk.Entry(amount_frame, font=("Segoe UI", 12), width=20)
        self.amount_entry.pack(side=LEFT)
        CreateToolTip(self.amount_entry, "Enter the amount you want to convert")
        
        # Currency selection
        currency_frame = ttk.Frame(input_frame)
        currency_frame.pack(fill=X, pady=10)
        
        # From currency
        from_frame = ttk.Frame(currency_frame)
        from_frame.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
        ttk.Label(from_frame, text="From Currency:", style="Field.TLabel").pack(anchor=W)
        self.from_currency = tk.StringVar(value="USD")
        self.from_combo = AutocompleteCombobox(from_frame, font=("Segoe UI", 11), textvariable=self.from_currency)
        self.from_combo.set_completion_list(self.currency_codes)
        self.from_combo.pack(fill=X, pady=5)
        CreateToolTip(self.from_combo, "Select the source currency")
        
        # To currency
        to_frame = ttk.Frame(currency_frame)
        to_frame.pack(side=RIGHT, fill=X, expand=True, padx=(10, 0))
        ttk.Label(to_frame, text="To Currency:", style="Field.TLabel").pack(anchor=W)
        self.to_currency = tk.StringVar(value="EUR")
        self.to_combo = AutocompleteCombobox(to_frame, font=("Segoe UI", 11), textvariable=self.to_currency)
        self.to_combo.set_completion_list(self.currency_codes)
        self.to_combo.pack(fill=X, pady=5)
        CreateToolTip(self.to_combo, "Select the target currency")
        
        # Result section
        result_frame = ttk.Frame(input_frame)
        result_frame.pack(fill=X, pady=10)
        ttk.Label(result_frame, text="Converted Amount:", style="Field.TLabel").pack(side=LEFT, padx=(0, 10))
        self.result_var = tk.StringVar()
        self.result_entry = ttk.Entry(result_frame, textvariable=self.result_var, 
                                     font=("Segoe UI", 12), width=20, state="readonly")
        self.result_entry.pack(side=LEFT)
        
        # Exchange rate info
        self.exchange_rate_var = tk.StringVar()
        self.exchange_rate_label = ttk.Label(input_frame, textvariable=self.exchange_rate_var, 
                                           foreground="#64748b")
        self.exchange_rate_label.pack(pady=5)
        
        # Button frame
        button_frame = ttk.Frame(main_card)
        button_frame.pack(pady=10)
        
        swap_btn = ttk.Button(button_frame, text="Swap", command=self.swap_currencies, style="Secondary.TButton")
        swap_btn.grid(row=0, column=0, padx=5)
        CreateToolTip(swap_btn, "Swap from and to currencies")
        
        convert_btn = ttk.Button(button_frame, text="Convert", command=self.convert_currency, style="Primary.TButton")
        convert_btn.grid(row=0, column=1, padx=5)
        CreateToolTip(convert_btn, "Convert currency with live exchange rates")
        
        clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_fields, style="Secondary.TButton")
        clear_btn.grid(row=0, column=2, padx=5)
        CreateToolTip(clear_btn, "Clear all fields")

    def create_ppp_tab(self):
        """Create PPP calculator interface."""
        main_card = ttk.LabelFrame(self.ppp_tab, text="Purchase Power Parity Calculator", padding=20)
        main_card.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Input section
        input_frame = ttk.Frame(main_card)
        input_frame.pack(fill=X, pady=(0, 20))
        
        # Country selection
        country_frame = ttk.Frame(input_frame)
        country_frame.pack(fill=X, pady=10)
        
        # From country
        from_frame = ttk.Frame(country_frame)
        from_frame.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
        ttk.Label(from_frame, text="From Country:", style="Field.TLabel").pack(anchor=W)
        self.from_country = tk.StringVar(value="US - United States")
        self.from_country_combo = AutocompleteCombobox(from_frame, font=("Segoe UI", 11), textvariable=self.from_country)
        self.from_country_combo.set_completion_list(self.country_codes)
        self.from_country_combo.pack(fill=X, pady=5)
        CreateToolTip(self.from_country_combo, "Select the source country")
        
        # To country
        to_frame = ttk.Frame(country_frame)
        to_frame.pack(side=RIGHT, fill=X, expand=True, padx=(10, 0))
        ttk.Label(to_frame, text="To Country:", style="Field.TLabel").pack(anchor=W)
        self.to_country = tk.StringVar(value="GB - United Kingdom")
        self.to_country_combo = AutocompleteCombobox(to_frame, font=("Segoe UI", 11), textvariable=self.to_country)
        self.to_country_combo.set_completion_list(self.country_codes)
        self.to_country_combo.pack(fill=X, pady=5)
        CreateToolTip(self.to_country_combo, "Select the target country")
        
        # Income input
        income_frame = ttk.Frame(input_frame)
        income_frame.pack(fill=X, pady=10)
        ttk.Label(income_frame, text="Annual Income (optional):", style="Field.TLabel").pack(side=LEFT, padx=(0, 10))
        self.income_entry = ttk.Entry(income_frame, font=("Segoe UI", 11), width=20)
        self.income_entry.pack(side=LEFT)
        CreateToolTip(self.income_entry, "Enter annual income for equivalent salary calculation")
        
        # Results section
        results_frame = ttk.LabelFrame(main_card, text="PPP Analysis Results", padding=15)
        results_frame.pack(fill=BOTH, expand=True, pady=10)
        
        self.ppp_results_text = tk.Text(results_frame, height=12, wrap=tk.WORD, 
                                       font=("Segoe UI", 10), state=tk.DISABLED)
        self.ppp_results_text.pack(fill=BOTH, expand=True)
        
        # Button frame
        button_frame = ttk.Frame(main_card)
        button_frame.pack(pady=10)
        
        swap_btn = ttk.Button(button_frame, text="Swap", command=self.swap_countries, style="Secondary.TButton")
        swap_btn.grid(row=0, column=0, padx=5)
        CreateToolTip(swap_btn, "Swap from and to countries")
        
        calculate_btn = ttk.Button(button_frame, text="Calculate", command=self.calculate_ppp, style="Primary.TButton")
        calculate_btn.grid(row=0, column=1, padx=5)
        CreateToolTip(calculate_btn, "Calculate PPP comparison with income analysis")
        
        clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_ppp_fields, style="Secondary.TButton")
        clear_btn.grid(row=0, column=2, padx=5)
        CreateToolTip(clear_btn, "Clear all fields")

    def create_history_tab(self):
        """Create history tab with separate sections."""
        main_frame = ttk.Frame(self.history_tab)
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Currency Conversion History
        conv_history_frame = ttk.LabelFrame(main_frame, text="Currency Conversion History", padding=15)
        conv_history_frame.pack(fill=BOTH, expand=True, pady=(0, 10))
        
        conv_columns = ("Time", "From", "To", "Amount", "Result")
        self.conv_history_tree = ttk.Treeview(conv_history_frame, columns=conv_columns, show="headings", height=8)
        
        for col in conv_columns:
            self.conv_history_tree.heading(col, text=col)
            self.conv_history_tree.column(col, width=120, anchor=CENTER)
        
        conv_scrollbar = ttk.Scrollbar(conv_history_frame, orient=VERTICAL, command=self.conv_history_tree.yview)
        self.conv_history_tree.configure(yscrollcommand=conv_scrollbar.set)
        
        self.conv_history_tree.pack(side=LEFT, fill=BOTH, expand=True)
        conv_scrollbar.pack(side=RIGHT, fill=Y)
        
        conv_button_frame = ttk.Frame(conv_history_frame)
        conv_button_frame.pack(fill=X, pady=10)
        
        refresh_conv_btn = ttk.Button(conv_button_frame, text="Refresh", 
                                     command=self.load_conversion_history, style="Secondary.TButton")
        refresh_conv_btn.pack(side=LEFT, padx=5)
        
        forget_conv_btn = ttk.Button(conv_button_frame, text="Forget History", 
                                    command=self.forget_conversion_history, style="Secondary.TButton")
        forget_conv_btn.pack(side=RIGHT, padx=5)
        CreateToolTip(forget_conv_btn, "Clear all currency conversion history")
        
        # PPP History
        ppp_history_frame = ttk.LabelFrame(main_frame, text="Purchase Power Parity History", padding=15)
        ppp_history_frame.pack(fill=BOTH, expand=True, pady=(10, 0))
        
        ppp_columns = ("Time", "From Country", "To Country", "PPP Rate", "Big Mac", "Cost of Living")
        self.ppp_history_tree = ttk.Treeview(ppp_history_frame, columns=ppp_columns, show="headings", height=8)
        
        for col in ppp_columns:
            self.ppp_history_tree.heading(col, text=col)
            self.ppp_history_tree.column(col, width=120, anchor=CENTER)
        
        ppp_scrollbar = ttk.Scrollbar(ppp_history_frame, orient=VERTICAL, command=self.ppp_history_tree.yview)
        self.ppp_history_tree.configure(yscrollcommand=ppp_scrollbar.set)
        
        self.ppp_history_tree.pack(side=LEFT, fill=BOTH, expand=True)
        ppp_scrollbar.pack(side=RIGHT, fill=Y)
        
        ppp_button_frame = ttk.Frame(ppp_history_frame)
        ppp_button_frame.pack(fill=X, pady=10)
        
        refresh_ppp_btn = ttk.Button(ppp_button_frame, text="Refresh", 
                                    command=self.load_ppp_history, style="Secondary.TButton")
        refresh_ppp_btn.pack(side=LEFT, padx=5)
        
        forget_ppp_btn = ttk.Button(ppp_button_frame, text="Forget History", 
                                   command=self.forget_ppp_history, style="Secondary.TButton")
        forget_ppp_btn.pack(side=RIGHT, padx=5)
        CreateToolTip(forget_ppp_btn, "Clear all PPP calculation history")

    def create_menu(self):
        """Create application menu."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Refresh Data", command=self.refresh_all_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_status_bar(self):
        """Create professional status bar."""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side=BOTTOM, fill=X, padx=2, pady=2)
        
        self.status_bar = ttk.Label(status_frame, 
                                   text="Ready - Professional Currency Converter & PPP Calculator", 
                                   font=("Segoe UI", 9),
                                   anchor=W)
        self.status_bar.pack(side=LEFT, fill=X, expand=True)
        
        self.timestamp_var = tk.StringVar()
        timestamp_label = ttk.Label(status_frame,
                                   textvariable=self.timestamp_var,
                                   font=("Segoe UI", 8))
        timestamp_label.pack(side=RIGHT, padx=(0, 10))
        
        self.update_timestamp()
    
    def update_timestamp(self):
        """Update timestamp in status bar."""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.timestamp_var.set(current_time)
        self.root.after(1000, self.update_timestamp)

    def show_about(self):
        """Show about dialog."""
        about_text = """
            Professional Currency Converter & PPP Calculator

            Features:
            • Real-time currency conversion with live exchange rates
            • Comprehensive Purchase Power Parity analysis
            • Income comparison across countries
            • Complete history tracking with separate sections
            • MySQL database integration
            • Professional modern interface

            Version 3.0
            Built with Python, ttkbootstrap, and MySQL
            """
        messagebox.showinfo("About", about_text)

    def extract_country_code(self, country_display: str) -> str:
        """Extract country code from display format."""
        return country_display.split(' - ')[0] if ' - ' in country_display else country_display

    def convert_currency(self):
        """Convert currency with real exchange rates."""
        try:
            self.status_bar.config(text="Converting currency...")
            self.root.update()
            
            amount_text = self.amount_entry.get().strip()
            if not amount_text:
                messagebox.showerror("Input Error", "Please enter an amount.")
                return
            
            amount = float(amount_text)
            from_curr = self.from_currency.get().strip()
            to_curr = self.to_currency.get().strip()
            
            if not from_curr or not to_curr:
                messagebox.showerror("Input Error", "Please select both currencies.")
                return
            
            if from_curr == to_curr:
                result = amount
                rate = 1.0
            else:
                rate = get_exchange_rate(from_curr, to_curr)
                result = amount * rate
            
            self.result_var.set(f"{result:.4f}")
            self.exchange_rate_var.set(f"Exchange Rate: 1 {from_curr} = {rate:.6f} {to_curr}")
            
            # Log to database
            log_conversion_to_db(
                datetime.datetime.now(),
                from_curr,
                to_curr,
                amount,
                result,
                rate
            )
            
            self.status_bar.config(text=f"Conversion completed: {amount} {from_curr} = {result:.4f} {to_curr}")
            
            # Refresh history to show new entry
            self.load_conversion_history()
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid numeric amount.")
            self.status_bar.config(text="Invalid input")
        except Exception as e:
            logging.error(f"Conversion error: {e}")
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")
            self.status_bar.config(text="Conversion failed")

    def calculate_ppp(self):
        """Calculate PPP with comprehensive analysis."""
        try:
            self.status_bar.config(text="Calculating PPP...")
            self.root.update()

            from_country_code = self.extract_country_code(self.from_country.get())
            to_country_code = self.extract_country_code(self.to_country.get())

            if not from_country_code or not to_country_code:
                messagebox.showerror("Input Error", "Please select both countries.")
                return

            ppp_data = calculate_ppp_comparison(from_country_code, to_country_code)
            
            if "error" in ppp_data:
                messagebox.showerror("Error", ppp_data["error"])
                return

            # Format comprehensive results
            results = []
            results.append("🌍 PURCHASE POWER PARITY ANALYSIS")
            results.append("=" * 60)
            results.append(f"From: {self.from_country.get()}")
            results.append(f"To: {self.to_country.get()}")
            results.append("")
            
            results.append("📊 PPP INDICATORS:")
            results.append(f"• PPP Exchange Rate Ratio: {ppp_data['ppp_ratio']:.4f}")
            results.append(f"• Big Mac Index Ratio: {ppp_data['big_mac_ratio']:.4f}")
            results.append(f"• Cost of Living Ratio: {ppp_data['cost_of_living_ratio']:.4f}")
            results.append("")
            
            # Income comparison
            income_text = self.income_entry.get().strip()
            if income_text:
                try:
                    income = float(income_text)
                    equivalent_income = income * ppp_data['cost_of_living_ratio']
                    purchasing_power_change = ((equivalent_income/income - 1) * 100)
                    
                    results.append("💰 INCOME COMPARISON:")
                    results.append(f"• Current Annual Income: ${income:,.2f}")
                    results.append(f"• Equivalent Income Needed: ${equivalent_income:,.2f}")
                    results.append(f"• Purchasing Power Change: {purchasing_power_change:+.1f}%")
                    
                    if purchasing_power_change > 0:
                        results.append("• Analysis: You would need MORE income to maintain same lifestyle")
                    else:
                        results.append("• Analysis: You would need LESS income to maintain same lifestyle")
                    results.append("")
                except ValueError:
                    pass
            
            results.append("🏪 DETAILED BREAKDOWN:")
            results.append(f"• {from_country_code} Big Mac Price: ${ppp_data['from_data']['big_mac_price']:.2f}")
            results.append(f"• {to_country_code} Big Mac Price: ${ppp_data['to_data']['big_mac_price']:.2f}")
            results.append(f"• {from_country_code} Cost of Living Index: {ppp_data['from_data']['cost_of_living']:.1f}")
            results.append(f"• {to_country_code} Cost of Living Index: {ppp_data['to_data']['cost_of_living']:.1f}")
            results.append("")
            
            results.append("💡 INTERPRETATION:")
            if ppp_data['cost_of_living_ratio'] > 1.1:
                results.append("• The destination country is significantly more expensive")
            elif ppp_data['cost_of_living_ratio'] < 0.9:
                results.append("• The destination country is significantly less expensive")
            else:
                results.append("• Both countries have similar cost of living")
            
            # Display results
            self.ppp_results_text.config(state=tk.NORMAL)
            self.ppp_results_text.delete(1.0, tk.END)
            self.ppp_results_text.insert(tk.END, "\n".join(results))
            self.ppp_results_text.config(state=tk.DISABLED)
            
            # Log to database
            log_ppp_calculation_to_db(
                datetime.datetime.now(),
                from_country_code,
                to_country_code,
                ppp_data['ppp_ratio'],
                ppp_data['big_mac_ratio'],
                ppp_data['cost_of_living_ratio']
            )
            
            self.status_bar.config(text=f"PPP analysis completed for {from_country_code} to {to_country_code}")
            
            # Refresh history to show new entry
            self.load_ppp_history()
            
        except Exception as e:
            logging.error(f"PPP calculation error: {e}")
            messagebox.showerror("Error", f"PPP calculation failed: {str(e)}")
            self.status_bar.config(text="PPP calculation failed")

    def clear_fields(self):
        """Clear currency converter fields."""
        self.amount_entry.delete(0, tk.END)
        self.from_currency.set("USD")
        self.to_currency.set("EUR")
        self.result_var.set("")
        self.exchange_rate_var.set("")
        self.status_bar.config(text="Currency converter fields cleared")

    def clear_ppp_fields(self):
        """Clear PPP calculator fields."""
        self.from_country.set("US - United States")
        self.to_country.set("GB - United Kingdom")
        self.income_entry.delete(0, tk.END)
        self.ppp_results_text.config(state=tk.NORMAL)
        self.ppp_results_text.delete(1.0, tk.END)
        self.ppp_results_text.config(state=tk.DISABLED)
        self.status_bar.config(text="PPP calculator fields cleared")

    def swap_currencies(self):
        """Swap from and to currencies."""
        from_val = self.from_currency.get()
        to_val = self.to_currency.get()
        self.from_currency.set(to_val)
        self.to_currency.set(from_val)
        self.status_bar.config(text="Currencies swapped")

    def swap_countries(self):
        """Swap from and to countries."""
        from_val = self.from_country.get()
        to_val = self.to_country.get()
        self.from_country.set(to_val)
        self.to_country.set(from_val)
        self.status_bar.config(text="Countries swapped")

    def load_conversion_history(self):
        """Load conversion history from database."""
        try:
            history = get_conversion_history()
            
            # Clear existing items
            for item in self.conv_history_tree.get_children():
                self.conv_history_tree.delete(item)
            
            # Insert new data
            for record in history:
                self.conv_history_tree.insert("", "end", values=record)
                
        except Exception as e:
            logging.error(f"Error loading conversion history: {e}")

    def load_ppp_history(self):
        """Load PPP calculation history from database."""
        try:
            history = get_ppp_history()
            
            # Clear existing items
            for item in self.ppp_history_tree.get_children():
                self.ppp_history_tree.delete(item)
            
            # Insert new data
            for record in history:
                self.ppp_history_tree.insert("", "end", values=record)
                
        except Exception as e:
            logging.error(f"Error loading PPP history: {e}")

    def forget_conversion_history(self):
        """Clear all conversion history."""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all conversion history?"):
            if clear_conversion_history():
                self.load_conversion_history()
                self.status_bar.config(text="Conversion history cleared")
                messagebox.showinfo("Success", "Conversion history has been cleared.")
            else:
                messagebox.showerror("Error", "Failed to clear conversion history.")

    def forget_ppp_history(self):
        """Clear all PPP history."""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all PPP history?"):
            if clear_ppp_history():
                self.load_ppp_history()
                self.status_bar.config(text="PPP history cleared")
                messagebox.showinfo("Success", "PPP history has been cleared.")
            else:
                messagebox.showerror("Error", "Failed to clear PPP history.")

    def refresh_all_data(self):
        """Refresh all data including history."""
        self.load_conversion_history()
        self.load_ppp_history()
        self.status_bar.config(text="All data refreshed")

def main():
    """Main function to run the application."""
    root = ttk.Window(themename="flatly")
    app = CurrencyConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()