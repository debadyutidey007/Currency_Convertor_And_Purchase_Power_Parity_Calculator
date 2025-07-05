import mysql.connector
from mysql.connector import Error
import logging
import os
from typing import List, Dict, Optional
import datetime

class DatabaseManager:
    def __init__(self):
        # MySQL Workbench credentials - Update these with your actual credentials
        self.host = os.getenv('MYSQL_HOST', 'localhost')
        self.user = os.getenv('MYSQL_USER', 'root')
        self.password = os.getenv('MYSQL_PASSWORD', 'DEBADYUTIDEY7700')  # Set your MySQL root password here
        self.database = os.getenv('MYSQL_DATABASE', 'currency_converter')
        self.port = int(os.getenv('MYSQL_PORT', '3306'))
        
    def get_db_connection(self):
        """Get MySQL database connection."""
        try:
            # First try to connect without specifying database to create it if needed
            if not self._database_exists():
                self._create_database()
            
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='DEBADYUTIDEY7700',
                database='currency_converter',
                port=3306,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci',
                autocommit=True
            )
            return conn
        except Error as e:
            logging.error(f"MySQL connection error: {e}")
            logging.error(f"Connection details: host={self.host}, user={self.user}, database={self.database}, port={self.port}")
            logging.error("Please check your MySQL credentials in database.py or set environment variables:")
            logging.error("MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_PORT")
            return None
    
    def _database_exists(self):
        """Check if database exists."""
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='DEBADYUTIDEY7700',
                port=3306
            )
            cursor = conn.cursor()
            cursor.execute(f"SHOW DATABASES LIKE '{self.database}'")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result is not None
        except Error:
            return False
    
    def _create_database(self):
        """Create database if it doesn't exist."""
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            cursor.close()
            conn.close()
            logging.info(f"Database '{self.database}' created successfully")
        except Error as e:
            logging.error(f"Error creating database: {e}")

    def initialize_database(self):
        """Initialize database and tables if they don't exist."""
        try:
            conn = self.get_db_connection()
            if not conn:
                raise Exception("Could not connect to database")
                
            cursor = conn.cursor()
            
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
                    FOREIGN KEY (currency_code) REFERENCES currencies(code) ON UPDATE CASCADE ON DELETE SET NULL
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
                    FOREIGN KEY (from_currency) REFERENCES currencies(code) ON UPDATE CASCADE ON DELETE CASCADE,
                    FOREIGN KEY (to_currency) REFERENCES currencies(code) ON UPDATE CASCADE ON DELETE CASCADE
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
                    FOREIGN KEY (from_country) REFERENCES countries(code) ON UPDATE CASCADE ON DELETE CASCADE,
                    FOREIGN KEY (to_country) REFERENCES countries(code) ON UPDATE CASCADE ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            self._insert_initial_data(cursor)
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logging.info("Database initialized successfully")
            
        except Error as e:
            logging.error(f"Database initialization error: {e}")
            raise

    def _insert_initial_data(self, cursor):
        """Insert initial currency and country data."""
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
                ("BTN", "Bhutanese Ngultrum", "Nu."), ("BWP", "Botswanan Pula", "P"), ("BYN", "Belarusian Ruble", "Br"),
                ("BZD", "Belize Dollar", "$"), ("CAD", "Canadian Dollar", "$"), ("CDF", "Congolese Franc", "FC"),
                ("CHF", "Swiss Franc", "CHF"), ("CLP", "Chilean Peso", "$"), ("CNY", "Chinese Yuan", "¥"),
                ("COP", "Colombian Peso", "$"), ("CRC", "Costa Rican Colón", "₡"), ("CUC", "Cuban Convertible Peso", "$"),
                ("CUP", "Cuban Peso", "₱"), ("CVE", "Cape Verdean Escudo", "$"), ("CZK", "Czech Koruna", "Kč"),
                ("DJF", "Djiboutian Franc", "Fdj"), ("DKK", "Danish Krone", "kr"), ("DOP", "Dominican Peso", "$"),
                ("DZD", "Algerian Dinar", "دج"), ("EGP", "Egyptian Pound", "£"), ("ERN", "Eritrean Nakfa", "Nfk"),
                ("ETB", "Ethiopian Birr", "Br"), ("EUR", "Euro", "€"), ("FJD", "Fijian Dollar", "$"),
                ("FKP", "Falkland Islands Pound", "£"), ("GBP", "British Pound Sterling", "£"), ("GEL", "Georgian Lari", "₾"),
                ("GHS", "Ghanaian Cedi", "¢"), ("GIP", "Gibraltar Pound", "£"), ("GMD", "Gambian Dalasi", "D"),
                ("GNF", "Guinean Franc", "FG"), ("GTQ", "Guatemalan Quetzal", "Q"), ("GYD", "Guyanaese Dollar", "$"),
                ("HKD", "Hong Kong Dollar", "$"), ("HNL", "Honduran Lempira", "L"), ("HRK", "Croatian Kuna", "kn"),
                ("HTG", "Haitian Gourde", "G"), ("HUF", "Hungarian Forint", "Ft"), ("IDR", "Indonesian Rupiah", "Rp"),
                ("ILS", "Israeli New Sheqel", "₪"), ("IMP", "Manx Pound", "£"), ("INR", "Indian Rupee", "₹"),
                ("IQD", "Iraqi Dinar", "ع.د"), ("IRR", "Iranian Rial", "﷼"), ("ISK", "Icelandic Króna", "kr"),
                ("JEP", "Jersey Pound", "£"), ("JMD", "Jamaican Dollar", "$"), ("JOD", "Jordanian Dinar", "JD"),
                ("JPY", "Japanese Yen", "¥"), ("KES", "Kenyan Shilling", "KSh"), ("KGS", "Kyrgystani Som", "лв"),
                ("KHR", "Cambodian Riel", "៛"), ("KMF", "Comorian Franc", "CF"), ("KPW", "North Korean Won", "₩"),
                ("KRW", "South Korean Won", "₩"), ("KWD", "Kuwaiti Dinar", "KD"), ("KYD", "Cayman Islands Dollar", "$"),
                ("KZT", "Kazakhstani Tenge", "₸"), ("LAK", "Laotian Kip", "₭"), ("LBP", "Lebanese Pound", "£"),
                ("LKR", "Sri Lankan Rupee", "₨"), ("LRD", "Liberian Dollar", "$"), ("LSL", "Lesotho Loti", "M"),
                ("LTL", "Lithuanian Litas", "Lt"), ("LVL", "Latvian Lats", "Ls"), ("LYD", "Libyan Dinar", "LD"),
                ("MAD", "Moroccan Dirham", "MAD"), ("MDL", "Moldovan Leu", "lei"), ("MGA", "Malagasy Ariary", "Ar"),
                ("MKD", "Macedonian Denar", "ден"), ("MMK", "Myanma Kyat", "K"), ("MNT", "Mongolian Tugrik", "₮"),
                ("MOP", "Macanese Pataca", "MOP$"), ("MRO", "Mauritanian Ouguiya", "UM"), ("MUR", "Mauritian Rupee", "₨"),
                ("MVR", "Maldivian Rufiyaa", "Rf"), ("MWK", "Malawian Kwacha", "MK"), ("MXN", "Mexican Peso", "$"),
                ("MYR", "Malaysian Ringgit", "RM"), ("MZN", "Mozambican Metical", "MT"), ("NAD", "Namibian Dollar", "$"),
                ("NGN", "Nigerian Naira", "₦"), ("NIO", "Nicaraguan Córdoba", "C$"), ("NOK", "Norwegian Krone", "kr"),
                ("NPR", "Nepalese Rupee", "₨"), ("NZD", "New Zealand Dollar", "$"), ("OMR", "Omani Rial", "﷼"),
                ("PAB", "Panamanian Balboa", "B/."), ("PEN", "Peruvian Nuevo Sol", "S/."), ("PGK", "Papua New Guinean Kina", "K"),
                ("PHP", "Philippine Peso", "₱"), ("PKR", "Pakistani Rupee", "₨"), ("PLN", "Polish Zloty", "zł"),
                ("PYG", "Paraguayan Guarani", "Gs"), ("QAR", "Qatari Rial", "﷼"), ("RON", "Romanian Leu", "lei"),
                ("RSD", "Serbian Dinar", "Дин."), ("RUB", "Russian Ruble", "₽"), ("RWF", "Rwandan Franc", "R₣"),
                ("SAR", "Saudi Riyal", "﷼"), ("SBD", "Solomon Islands Dollar", "$"), ("SCR", "Seychellois Rupee", "₨"),
                ("SDG", "Sudanese Pound", "ج.س."), ("SEK", "Swedish Krona", "kr"), ("SGD", "Singapore Dollar", "$"),
                ("SHP", "Saint Helena Pound", "£"), ("SLE", "Sierra Leonean Leone", "Le"), ("SLL", "Sierra Leonean Leone", "Le"),
                ("SOS", "Somali Shilling", "S"), ("SRD", "Surinamese Dollar", "$"), ("STD", "São Tomé and Príncipe Dobra", "Db"),
                ("SVC", "Salvadoran Colón", "$"), ("SYP", "Syrian Pound", "£"), ("SZL", "Swazi Lilangeni", "E"),
                ("THB", "Thai Baht", "฿"), ("TJS", "Tajikistani Somoni", "SM"), ("TMT", "Turkmenistani Manat", "T"),
                ("TND", "Tunisian Dinar", "د.ت"), ("TOP", "Tongan Paʻanga", "T$"), ("TRY", "Turkish Lira", "₺"),
                ("TTD", "Trinidad and Tobago Dollar", "TT$"), ("TVD", "Tuvaluan Dollar", "$"), ("TWD", "New Taiwan Dollar", "NT$"),
                ("TZS", "Tanzanian Shilling", "TSh"), ("UAH", "Ukrainian Hryvnia", "₴"), ("UGX", "Ugandan Shilling", "USh"),
                ("USD", "US Dollar", "$"), ("UYU", "Uruguayan Peso", "$U"), ("UZS", "Uzbekistan Som", "лв"),
                ("VED", "Venezuelan Bolívar", "Bs"), ("VES", "Venezuelan Bolívar", "Bs"), ("VND", "Vietnamese Dong", "₫"),
                ("VUV", "Vanuatu Vatu", "VT"), ("WST", "Samoan Tala", "WS$"), ("XAF", "CFA Franc BEAC", "FCFA"),
                ("XAG", "Silver Ounce", "XAG"), ("XAU", "Gold Ounce", "XAU"), ("XCD", "East Caribbean Dollar", "$"),
                ("XDR", "Special Drawing Rights", "XDR"), ("XOF", "CFA Franc BCEAO", "CFA"), ("XPD", "Palladium Ounce", "XPD"),
                ("XPF", "CFP Franc", "₣"), ("XPT", "Platinum Ounce", "XPT"), ("YER", "Yemeni Rial", "﷼"),
                ("ZAR", "South African Rand", "R"), ("ZMK", "Zambian Kwacha", "ZK"), ("ZMW", "Zambian Kwacha", "ZK"),
                ("ZWL", "Zimbabwean Dollar", "$")
            ]
            
            cursor.executemany(
                "INSERT INTO currencies (code, name, symbol) VALUES (%s, %s, %s)",
                currencies
            )
            
        # Insert comprehensive country data
        cursor.execute("SELECT COUNT(*) FROM countries")
        if cursor.fetchone()[0] == 0:
            countries = [
                ("AD", "Andorra", "EUR"), ("AE", "United Arab Emirates", "AED"), ("AF", "Afghanistan", "AFN"),
                ("AG", "Antigua and Barbuda", "XCD"), ("AI", "Anguilla", "XCD"), ("AL", "Albania", "ALL"),
                ("AM", "Armenia", "AMD"), ("AO", "Angola", "AOA"), ("AQ", "Antarctica", None),
                ("AR", "Argentina", "ARS"), ("AS", "American Samoa", "USD"), ("AT", "Austria", "EUR"),
                ("AU", "Australia", "AUD"), ("AW", "Aruba", "AWG"), ("AX", "Åland Islands", "EUR"),
                ("AZ", "Azerbaijan", "AZN"), ("BA", "Bosnia and Herzegovina", "BAM"), ("BB", "Barbados", "BBD"),
                ("BD", "Bangladesh", "BDT"), ("BE", "Belgium", "EUR"), ("BF", "Burkina Faso", "XOF"),
                ("BG", "Bulgaria", "BGN"), ("BH", "Bahrain", "BHD"), ("BI", "Burundi", "BIF"),
                ("BJ", "Benin", "XOF"), ("BL", "Saint Barthélemy", "EUR"), ("BM", "Bermuda", "BMD"),
                ("BN", "Brunei", "BND"), ("BO", "Bolivia", "BOB"), ("BQ", "Bonaire, Sint Eustatius and Saba", "USD"),
                ("BR", "Brazil", "BRL"), ("BS", "Bahamas", "BSD"), ("BT", "Bhutan", "BTN"),
                ("BV", "Bouvet Island", "NOK"), ("BW", "Botswana", "BWP"), ("BY", "Belarus", "BYN"),
                ("BZ", "Belize", "BZD"), ("CA", "Canada", "CAD"), ("CC", "Cocos (Keeling) Islands", "AUD"),
                ("CD", "Congo, Democratic Republic of the", "CDF"), ("CF", "Central African Republic", "XAF"),
                ("CG", "Congo", "XAF"), ("CH", "Switzerland", "CHF"), ("CI", "Côte d'Ivoire", "XOF"),
                ("CK", "Cook Islands", "NZD"), ("CL", "Chile", "CLP"), ("CM", "Cameroon", "XAF"),
                ("CN", "China", "CNY"), ("CO", "Colombia", "COP"), ("CR", "Costa Rica", "CRC"),
                ("CU", "Cuba", "CUP"), ("CV", "Cape Verde", "CVE"), ("CW", "Curaçao", "ANG"),
                ("CX", "Christmas Island", "AUD"), ("CY", "Cyprus", "EUR"), ("CZ", "Czech Republic", "CZK"),
                ("DE", "Germany", "EUR"), ("DJ", "Djibouti", "DJF"), ("DK", "Denmark", "DKK"),
                ("DM", "Dominica", "XCD"), ("DO", "Dominican Republic", "DOP"), ("DZ", "Algeria", "DZD"),
                ("EC", "Ecuador", "USD"), ("EE", "Estonia", "EUR"), ("EG", "Egypt", "EGP"),
                ("EH", "Western Sahara", "MAD"), ("ER", "Eritrea", "ERN"), ("ES", "Spain", "EUR"),
                ("ET", "Ethiopia", "ETB"), ("FI", "Finland", "EUR"), ("FJ", "Fiji", "FJD"),
                ("FK", "Falkland Islands (Malvinas)", "FKP"), ("FM", "Micronesia", "USD"),
                ("FO", "Faroe Islands", "DKK"), ("FR", "France", "EUR"), ("GA", "Gabon", "XAF"),
                ("GB", "United Kingdom", "GBP"), ("GD", "Grenada", "XCD"), ("GE", "Georgia", "GEL"),
                ("GF", "French Guiana", "EUR"), ("GG", "Guernsey", "GBP"), ("GH", "Ghana", "GHS"),
                ("GI", "Gibraltar", "GIP"), ("GL", "Greenland", "DKK"), ("GM", "Gambia", "GMD"),
                ("GN", "Guinea", "GNF"), ("GP", "Guadeloupe", "EUR"), ("GQ", "Equatorial Guinea", "XAF"),
                ("GR", "Greece", "EUR"), ("GS", "South Georgia and the South Sandwich Islands", "GBP"),
                ("GT", "Guatemala", "GTQ"), ("GU", "Guam", "USD"), ("GW", "Guinea-Bissau", "XOF"),
                ("GY", "Guyana", "GYD"), ("HK", "Hong Kong", "HKD"), ("HM", "Heard Island and McDonald Islands", "AUD"),
                ("HN", "Honduras", "HNL"), ("HR", "Croatia", "HRK"), ("HT", "Haiti", "HTG"),
                ("HU", "Hungary", "HUF"), ("ID", "Indonesia", "IDR"), ("IE", "Ireland", "EUR"),
                ("IL", "Israel", "ILS"), ("IM", "Isle of Man", "GBP"), ("IN", "India", "INR"),
                ("IO", "British Indian Ocean Territory", "USD"), ("IQ", "Iraq", "IQD"), ("IR", "Iran", "IRR"),
                ("IS", "Iceland", "ISK"), ("IT", "Italy", "EUR"), ("JE", "Jersey", "GBP"),
                ("JM", "Jamaica", "JMD"), ("JO", "Jordan", "JOD"), ("JP", "Japan", "JPY"),
                ("KE", "Kenya", "KES"), ("KG", "Kyrgyzstan", "KGS"), ("KH", "Cambodia", "KHR"),
                ("KI", "Kiribati", "AUD"), ("KM", "Comoros", "KMF"), ("KN", "Saint Kitts and Nevis", "XCD"),
                ("KP", "Korea, Democratic People's Republic of", "KPW"), ("KR", "Korea, Republic of", "KRW"),
                ("KW", "Kuwait", "KWD"), ("KY", "Cayman Islands", "KYD"), ("KZ", "Kazakhstan", "KZT"),
                ("LA", "Lao People's Democratic Republic", "LAK"), ("LB", "Lebanon", "LBP"),
                ("LC", "Saint Lucia", "XCD"), ("LI", "Liechtenstein", "CHF"), ("LK", "Sri Lanka", "LKR"),
                ("LR", "Liberia", "LRD"), ("LS", "Lesotho", "LSL"), ("LT", "Lithuania", "EUR"),
                ("LU", "Luxembourg", "EUR"), ("LV", "Latvia", "EUR"), ("LY", "Libya", "LYD"),
                ("MA", "Morocco", "MAD"), ("MC", "Monaco", "EUR"), ("MD", "Moldova", "MDL"),
                ("ME", "Montenegro", "EUR"), ("MF", "Saint Martin (French part)", "EUR"),
                ("MG", "Madagascar", "MGA"), ("MH", "Marshall Islands", "USD"), ("MK", "Macedonia", "MKD"),
                ("ML", "Mali", "XOF"), ("MM", "Myanmar", "MMK"), ("MN", "Mongolia", "MNT"),
                ("MO", "Macao", "MOP"), ("MP", "Northern Mariana Islands", "USD"), ("MQ", "Martinique", "EUR"),
                ("MR", "Mauritania", "MRO"), ("MS", "Montserrat", "XCD"), ("MT", "Malta", "EUR"),
                ("MU", "Mauritius", "MUR"), ("MV", "Maldives", "MVR"), ("MW", "Malawi", "MWK"),
                ("MX", "Mexico", "MXN"), ("MY", "Malaysia", "MYR"), ("MZ", "Mozambique", "MZN"),
                ("NA", "Namibia", "NAD"), ("NC", "New Caledonia", "XPF"), ("NE", "Niger", "XOF"),
                ("NF", "Norfolk Island", "AUD"), ("NG", "Nigeria", "NGN"), ("NI", "Nicaragua", "NIO"),
                ("NL", "Netherlands", "EUR"), ("NO", "Norway", "NOK"), ("NP", "Nepal", "NPR"),
                ("NR", "Nauru", "AUD"), ("NU", "Niue", "NZD"), ("NZ", "New Zealand", "NZD"),
                ("OM", "Oman", "OMR"), ("PA", "Panama", "PAB"), ("PE", "Peru", "PEN"),
                ("PF", "French Polynesia", "XPF"), ("PG", "Papua New Guinea", "PGK"), ("PH", "Philippines", "PHP"),
                ("PK", "Pakistan", "PKR"), ("PL", "Poland", "PLN"), ("PM", "Saint Pierre and Miquelon", "EUR"),
                ("PN", "Pitcairn", "NZD"), ("PR", "Puerto Rico", "USD"), ("PS", "Palestine", "ILS"),
                ("PT", "Portugal", "EUR"), ("PW", "Palau", "USD"), ("PY", "Paraguay", "PYG"),
                ("QA", "Qatar", "QAR"), ("RE", "Réunion", "EUR"), ("RO", "Romania", "RON"),
                ("RS", "Serbia", "RSD"), ("RU", "Russia", "RUB"), ("RW", "Rwanda", "RWF"),
                ("SA", "Saudi Arabia", "SAR"), ("SB", "Solomon Islands", "SBD"), ("SC", "Seychelles", "SCR"),
                ("SD", "Sudan", "SDG"), ("SE", "Sweden", "SEK"), ("SG", "Singapore", "SGD"),
                ("SH", "Saint Helena", "SHP"), ("SI", "Slovenia", "EUR"), ("SJ", "Svalbard and Jan Mayen", "NOK"),
                ("SK", "Slovakia", "EUR"), ("SL", "Sierra Leone", "SLE"), ("SM", "San Marino", "EUR"),
                ("SN", "Senegal", "XOF"), ("SO", "Somalia", "SOS"), ("SR", "Suriname", "SRD"),
                ("SS", "South Sudan", "SSP"), ("ST", "Sao Tome and Principe", "STD"), ("SV", "El Salvador", "USD"),
                ("SX", "Sint Maarten", "ANG"), ("SY", "Syrian Arab Republic", "SYP"), ("SZ", "Swaziland", "SZL"),
                ("TC", "Turks and Caicos Islands", "USD"), ("TD", "Chad", "XAF"), ("TF", "French Southern Territories", "EUR"),
                ("TG", "Togo", "XOF"), ("TH", "Thailand", "THB"), ("TJ", "Tajikistan", "TJS"),
                ("TK", "Tokelau", "NZD"), ("TL", "Timor-Leste", "USD"), ("TM", "Turkmenistan", "TMT"),
                ("TN", "Tunisia", "TND"), ("TO", "Tonga", "TOP"), ("TR", "Turkey", "TRY"),
                ("TT", "Trinidad and Tobago", "TTD"), ("TV", "Tuvalu", "AUD"), ("TW", "Taiwan", "TWD"),
                ("TZ", "Tanzania", "TZS"), ("UA", "Ukraine", "UAH"), ("UG", "Uganda", "UGX"),
                ("UM", "United States Minor Outlying Islands", "USD"), ("US", "United States", "USD"),
                ("UY", "Uruguay", "UYU"), ("UZ", "Uzbekistan", "UZS"), ("VA", "Vatican City", "EUR"),
                ("VC", "Saint Vincent and the Grenadines", "XCD"), ("VE", "Venezuela", "VES"),
                ("VG", "Virgin Islands, British", "USD"), ("VI", "Virgin Islands, U.S.", "USD"),
                ("VN", "Vietnam", "VND"), ("VU", "Vanuatu", "VUV"), ("WF", "Wallis and Futuna", "XPF"),
                ("WS", "Samoa", "WST"), ("YE", "Yemen", "YER"), ("YT", "Mayotte", "EUR"),
                ("ZA", "South Africa", "ZAR"), ("ZM", "Zambia", "ZMW"), ("ZW", "Zimbabwe", "ZWL")
            ]
            
            cursor.executemany(
                "INSERT INTO countries (code, name, currency_code) VALUES (%s, %s, %s)",
                countries
            )

    def get_all_currencies(self) -> List[Dict]:
        """Get all available currencies."""
        conn = self.get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT code, name, symbol FROM currencies ORDER BY code")
            currencies = cursor.fetchall()
            return currencies
        except Error as e:
            logging.error(f"Error fetching currencies: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            conn.close()

    def get_all_countries(self) -> List[Dict]:
        """Get all available countries."""
        conn = self.get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT code, name, currency_code FROM countries ORDER BY name")
            countries = cursor.fetchall()
            return countries
        except Error as e:
            logging.error(f"Error fetching countries: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            conn.close()

    def save_conversion_history(self, from_currency: str, to_currency: str, amount: float, result: float, exchange_rate: float):
        """Save conversion to history."""
        conn = self.get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO conversion_history (from_currency, to_currency, amount, result, exchange_rate) VALUES (%s, %s, %s, %s, %s)",
                (from_currency, to_currency, amount, result, exchange_rate)
            )
            conn.commit()
        except Error as e:
            logging.error(f"Error saving conversion history: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()

    def save_ppp_history(self, from_country: str, to_country: str, ppp_rate: float, big_mac_index: float, cost_of_living_index: float, income_from: float, income_equivalent: float):
        """Save PPP calculation to history."""
        conn = self.get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO ppp_history (from_country, to_country, ppp_rate, big_mac_index, cost_of_living_index, income_from, income_equivalent) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (from_country, to_country, ppp_rate, big_mac_index, cost_of_living_index, income_from, income_equivalent)
            )
            conn.commit()
        except Error as e:
            logging.error(f"Error saving PPP history: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()

    def get_conversion_history(self, limit: int = 20) -> List[Dict]:
        """Get conversion history."""
        conn = self.get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT ch.*, 
                       c1.name as from_currency_name, 
                       c2.name as to_currency_name
                FROM conversion_history ch
                LEFT JOIN currencies c1 ON ch.from_currency = c1.code
                LEFT JOIN currencies c2 ON ch.to_currency = c2.code
                ORDER BY ch.conversion_time DESC
                LIMIT %s
            """, (limit,))
            history = cursor.fetchall()
            return history
        except Error as e:
            logging.error(f"Error fetching conversion history: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            conn.close()

    def get_ppp_history(self, limit: int = 20) -> List[Dict]:
        """Get PPP calculation history."""
        conn = self.get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT ph.*, 
                       c1.name as from_country_name, 
                       c2.name as to_country_name
                FROM ppp_history ph
                LEFT JOIN countries c1 ON ph.from_country = c1.code
                LEFT JOIN countries c2 ON ph.to_country = c2.code
                ORDER BY ph.calculation_time DESC
                LIMIT %s
            """, (limit,))
            history = cursor.fetchall()
            return history
        except Error as e:
            logging.error(f"Error fetching PPP history: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            conn.close()

    def get_conversion_trends(self) -> List[Dict]:
        """Get conversion trends for charts."""
        conn = self.get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT DATE(conversion_time) as date, COUNT(*) as count
                FROM conversion_history
                WHERE conversion_time >= DATE_SUB(NOW(), INTERVAL 30 DAY)
                GROUP BY DATE(conversion_time)
                ORDER BY date DESC
            """)
            trends = cursor.fetchall()
            return trends
        except Error as e:
            logging.error(f"Error fetching conversion trends: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            conn.close()

    def get_ppp_trends(self) -> List[Dict]:
        """Get PPP calculation trends for charts."""
        conn = self.get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT DATE(calculation_time) as date, COUNT(*) as count
                FROM ppp_history
                WHERE calculation_time >= DATE_SUB(NOW(), INTERVAL 30 DAY)
                GROUP BY DATE(calculation_time)
                ORDER BY date DESC
            """)
            trends = cursor.fetchall()
            return trends
        except Error as e:
            logging.error(f"Error fetching PPP trends: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            conn.close()

    def delete_conversion_history(self) -> bool:
        """Delete all conversion history."""
        conn = self.get_db_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM conversion_history")
            conn.commit()
            return True
        except Error as e:
            logging.error(f"Error deleting conversion history: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            conn.close()

    def delete_ppp_history(self) -> bool:
        """Delete all PPP history."""
        conn = self.get_db_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ppp_history")
            conn.commit()
            return True
        except Error as e:
            logging.error(f"Error deleting PPP history: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            conn.close()