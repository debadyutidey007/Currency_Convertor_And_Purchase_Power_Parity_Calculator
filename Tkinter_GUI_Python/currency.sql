-- Currency Converter Pro - MySQL Database Schema
-- Created: July 05, 2025
-- Description: Complete database structure for Currency Converter application with PPP calculations

-- Create database
CREATE DATABASE IF NOT EXISTS CURRENCY_CONVERTER_PRO
CHARACTER SET UTF8MB4
COLLATE UTF8MB4_UNICODE_CI;

USE CURRENCY_CONVERTER_PRO;

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS PPP_HISTORY;

DROP TABLE IF EXISTS CONVERSION_HISTORY;

DROP TABLE IF EXISTS COUNTRIES;

DROP TABLE IF EXISTS CURRENCIES;

-- =============================================
-- CURRENCIES TABLE
-- =============================================
CREATE TABLE CURRENCIES (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    CODE VARCHAR(3) UNIQUE NOT NULL,
    NAME VARCHAR(100) NOT NULL,
    SYMBOL VARCHAR(10),
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX IDX_CODE (CODE),
    INDEX IDX_NAME (NAME)
) ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE=UTF8MB4_UNICODE_CI;

-- =============================================
-- COUNTRIES TABLE
-- =============================================
CREATE TABLE COUNTRIES (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    CODE VARCHAR(3) UNIQUE NOT NULL,
    NAME VARCHAR(100) NOT NULL,
    CURRENCY_CODE VARCHAR(3),
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (CURRENCY_CODE) REFERENCES CURRENCIES(CODE) ON UPDATE CASCADE ON DELETE SET NULL,
    INDEX IDX_CODE (CODE),
    INDEX IDX_NAME (NAME),
    INDEX IDX_CURRENCY_CODE (CURRENCY_CODE)
) ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE=UTF8MB4_UNICODE_CI;

-- =============================================
-- CONVERSION HISTORY TABLE
-- =============================================
CREATE TABLE CONVERSION_HISTORY (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    CONVERSION_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FROM_CURRENCY VARCHAR(3) NOT NULL,
    TO_CURRENCY VARCHAR(3) NOT NULL,
    AMOUNT DECIMAL(15, 4) NOT NULL,
    RESULT DECIMAL(15, 4) NOT NULL,
    EXCHANGE_RATE DECIMAL(12, 6) NOT NULL,
    API_SOURCE VARCHAR(50) DEFAULT 'exchangerate-api',
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (FROM_CURRENCY) REFERENCES CURRENCIES(CODE) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (TO_CURRENCY) REFERENCES CURRENCIES(CODE) ON UPDATE CASCADE ON DELETE CASCADE,
    INDEX IDX_CONVERSION_TIME (CONVERSION_TIME),
    INDEX IDX_FROM_CURRENCY (FROM_CURRENCY),
    INDEX IDX_TO_CURRENCY (TO_CURRENCY),
    INDEX IDX_CURRENCIES_PAIR (FROM_CURRENCY, TO_CURRENCY),
    INDEX IDX_DATE_RANGE (CONVERSION_TIME, FROM_CURRENCY, TO_CURRENCY)
) ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE=UTF8MB4_UNICODE_CI;

-- =============================================
-- PPP HISTORY TABLE
-- =============================================
CREATE TABLE PPP_HISTORY (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    CALCULATION_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FROM_COUNTRY VARCHAR(3) NOT NULL,
    TO_COUNTRY VARCHAR(3) NOT NULL,
    PPP_RATE DECIMAL(10, 4),
    BIG_MAC_INDEX DECIMAL(8, 4),
    COST_OF_LIVING_INDEX DECIMAL(8, 4),
    INCOME_FROM DECIMAL(15, 2),
    INCOME_EQUIVALENT DECIMAL(15, 2),
    EXCHANGE_RATE DECIMAL(12, 6),
    DATA_SOURCE VARCHAR(50) DEFAULT 'worldbank-api',
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (FROM_COUNTRY) REFERENCES COUNTRIES(CODE) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (TO_COUNTRY) REFERENCES COUNTRIES(CODE) ON UPDATE CASCADE ON DELETE CASCADE,
    INDEX IDX_CALCULATION_TIME (CALCULATION_TIME),
    INDEX IDX_FROM_COUNTRY (FROM_COUNTRY),
    INDEX IDX_TO_COUNTRY (TO_COUNTRY),
    INDEX IDX_COUNTRIES_PAIR (FROM_COUNTRY, TO_COUNTRY),
    INDEX IDX_DATE_RANGE (CALCULATION_TIME, FROM_COUNTRY, TO_COUNTRY)
) ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE=UTF8MB4_UNICODE_CI;

-- =============================================
-- INSERT INITIAL CURRENCY DATA
-- =============================================
INSERT INTO CURRENCIES (
    CODE,
    NAME,
    SYMBOL
) VALUES
 -- Major currencies
(
    'USD',
    'US Dollar',
    '$'
),
(
    'EUR',
    'Euro',
    '€'
),
(
    'GBP',
    'British Pound Sterling',
    '£'
),
(
    'JPY',
    'Japanese Yen',
    '¥'
),
(
    'CHF',
    'Swiss Franc',
    'CHF'
),
(
    'CAD',
    'Canadian Dollar',
    '$'
),
(
    'AUD',
    'Australian Dollar',
    '$'
),
(
    'NZD',
    'New Zealand Dollar',
    '$'
),
 
-- Asian currencies
(
    'CNY',
    'Chinese Yuan',
    '¥'
),
(
    'INR',
    'Indian Rupee',
    '₹'
),
(
    'KRW',
    'South Korean Won',
    '₩'
),
(
    'SGD',
    'Singapore Dollar',
    '$'
),
(
    'HKD',
    'Hong Kong Dollar',
    '$'
),
(
    'MYR',
    'Malaysian Ringgit',
    'RM'
),
(
    'THB',
    'Thai Baht',
    '฿'
),
(
    'PHP',
    'Philippine Peso',
    '₱'
),
(
    'IDR',
    'Indonesian Rupiah',
    'Rp'
),
(
    'VND',
    'Vietnamese Dong',
    '₫'
),
 
-- European currencies
(
    'SEK',
    'Swedish Krona',
    'kr'
),
(
    'NOK',
    'Norwegian Krone',
    'kr'
),
(
    'DKK',
    'Danish Krone',
    'kr'
),
(
    'PLN',
    'Polish Zloty',
    'zł'
),
(
    'CZK',
    'Czech Koruna',
    'Kč'
),
(
    'HUF',
    'Hungarian Forint',
    'Ft'
),
(
    'RON',
    'Romanian Leu',
    'lei'
),
(
    'BGN',
    'Bulgarian Lev',
    'лв'
),
(
    'HRK',
    'Croatian Kuna',
    'kn'
),
(
    'RUB',
    'Russian Ruble',
    '₽'
),
(
    'UAH',
    'Ukrainian Hryvnia',
    '₴'
),
(
    'TRY',
    'Turkish Lira',
    '₺'
),
 
-- Middle Eastern currencies
(
    'AED',
    'UAE Dirham',
    'د.إ'
),
(
    'SAR',
    'Saudi Riyal',
    '﷼'
),
(
    'QAR',
    'Qatari Rial',
    '﷼'
),
(
    'KWD',
    'Kuwaiti Dinar',
    'KD'
),
(
    'BHD',
    'Bahraini Dinar',
    '.د.ب'
),
(
    'OMR',
    'Omani Rial',
    '﷼'
),
(
    'JOD',
    'Jordanian Dinar',
    'JD'
),
(
    'ILS',
    'Israeli New Sheqel',
    '₪'
),
 
-- African currencies
(
    'ZAR',
    'South African Rand',
    'R'
),
(
    'EGP',
    'Egyptian Pound',
    '£'
),
(
    'NGN',
    'Nigerian Naira',
    '₦'
),
(
    'MAD',
    'Moroccan Dirham',
    'MAD'
),
(
    'KES',
    'Kenyan Shilling',
    'KSh'
),
(
    'TZS',
    'Tanzanian Shilling',
    'TSh'
),
(
    'UGX',
    'Ugandan Shilling',
    'USh'
),
(
    'ZMW',
    'Zambian Kwacha',
    'ZK'
),
 
-- Latin American currencies
(
    'BRL',
    'Brazilian Real',
    'R$'
),
(
    'MXN',
    'Mexican Peso',
    '$'
),
(
    'ARS',
    'Argentine Peso',
    '$'
),
(
    'CLP',
    'Chilean Peso',
    '$'
),
(
    'COP',
    'Colombian Peso',
    '$'
),
(
    'PEN',
    'Peruvian Nuevo Sol',
    'S/.'
),
(
    'UYU',
    'Uruguayan Peso',
    '$U'
),
(
    'PYG',
    'Paraguayan Guarani',
    'Gs'
),
(
    'BOB',
    'Bolivian Boliviano',
    '$b'
),
(
    'VES',
    'Venezuelan Bolívar',
    'Bs'
),
 
-- Other currencies
(
    'IRR',
    'Iranian Rial',
    '﷼'
),
(
    'PKR',
    'Pakistani Rupee',
    '₨'
),
(
    'BDT',
    'Bangladeshi Taka',
    '৳'
),
(
    'LKR',
    'Sri Lankan Rupee',
    '₨'
),
(
    'NPR',
    'Nepalese Rupee',
    '₨'
),
(
    'AFN',
    'Afghan Afghani',
    '؋'
),
(
    'KZT',
    'Kazakhstani Tenge',
    '₸'
),
(
    'UZS',
    'Uzbekistan Som',
    'лв'
),
(
    'KGS',
    'Kyrgystani Som',
    'лв'
),
(
    'TJS',
    'Tajikistani Somoni',
    'SM'
),
(
    'TMT',
    'Turkmenistani Manat',
    'T'
),
(
    'MNT',
    'Mongolian Tugrik',
    '₮'
);

-- =============================================
-- INSERT INITIAL COUNTRY DATA
-- =============================================
INSERT INTO COUNTRIES (
    CODE,
    NAME,
    CURRENCY_CODE
) VALUES
 -- North America
(
    'US',
    'United States',
    'USD'
),
(
    'CA',
    'Canada',
    'CAD'
),
(
    'MX',
    'Mexico',
    'MXN'
),
 
-- Europe
(
    'GB',
    'United Kingdom',
    'GBP'
),
(
    'DE',
    'Germany',
    'EUR'
),
(
    'FR',
    'France',
    'EUR'
),
(
    'IT',
    'Italy',
    'EUR'
),
(
    'ES',
    'Spain',
    'EUR'
),
(
    'NL',
    'Netherlands',
    'EUR'
),
(
    'BE',
    'Belgium',
    'EUR'
),
(
    'AT',
    'Austria',
    'EUR'
),
(
    'PT',
    'Portugal',
    'EUR'
),
(
    'IE',
    'Ireland',
    'EUR'
),
(
    'GR',
    'Greece',
    'EUR'
),
(
    'FI',
    'Finland',
    'EUR'
),
(
    'LU',
    'Luxembourg',
    'EUR'
),
(
    'MT',
    'Malta',
    'EUR'
),
(
    'CY',
    'Cyprus',
    'EUR'
),
(
    'EE',
    'Estonia',
    'EUR'
),
(
    'LV',
    'Latvia',
    'EUR'
),
(
    'LT',
    'Lithuania',
    'EUR'
),
(
    'SI',
    'Slovenia',
    'EUR'
),
(
    'SK',
    'Slovakia',
    'EUR'
),
(
    'CH',
    'Switzerland',
    'CHF'
),
(
    'NO',
    'Norway',
    'NOK'
),
(
    'SE',
    'Sweden',
    'SEK'
),
(
    'DK',
    'Denmark',
    'DKK'
),
(
    'IS',
    'Iceland',
    'ISK'
),
(
    'PL',
    'Poland',
    'PLN'
),
(
    'CZ',
    'Czech Republic',
    'CZK'
),
(
    'HU',
    'Hungary',
    'HUF'
),
(
    'RO',
    'Romania',
    'RON'
),
(
    'BG',
    'Bulgaria',
    'BGN'
),
(
    'HR',
    'Croatia',
    'HRK'
),
(
    'RS',
    'Serbia',
    'RSD'
),
(
    'RU',
    'Russia',
    'RUB'
),
(
    'UA',
    'Ukraine',
    'UAH'
),
(
    'TR',
    'Turkey',
    'TRY'
),
 
-- Asia Pacific
(
    'JP',
    'Japan',
    'JPY'
),
(
    'CN',
    'China',
    'CNY'
),
(
    'IN',
    'India',
    'INR'
),
(
    'KR',
    'South Korea',
    'KRW'
),
(
    'SG',
    'Singapore',
    'SGD'
),
(
    'HK',
    'Hong Kong',
    'HKD'
),
(
    'TW',
    'Taiwan',
    'TWD'
),
(
    'MY',
    'Malaysia',
    'MYR'
),
(
    'TH',
    'Thailand',
    'THB'
),
(
    'PH',
    'Philippines',
    'PHP'
),
(
    'ID',
    'Indonesia',
    'IDR'
),
(
    'VN',
    'Vietnam',
    'VND'
),
(
    'AU',
    'Australia',
    'AUD'
),
(
    'NZ',
    'New Zealand',
    'NZD'
),
 
-- Middle East
(
    'AE',
    'United Arab Emirates',
    'AED'
),
(
    'SA',
    'Saudi Arabia',
    'SAR'
),
(
    'QA',
    'Qatar',
    'QAR'
),
(
    'KW',
    'Kuwait',
    'KWD'
),
(
    'BH',
    'Bahrain',
    'BHD'
),
(
    'OM',
    'Oman',
    'OMR'
),
(
    'JO',
    'Jordan',
    'JOD'
),
(
    'IL',
    'Israel',
    'ILS'
),
(
    'IR',
    'Iran',
    'IRR'
),
 
-- Africa
(
    'ZA',
    'South Africa',
    'ZAR'
),
(
    'EG',
    'Egypt',
    'EGP'
),
(
    'NG',
    'Nigeria',
    'NGN'
),
(
    'MA',
    'Morocco',
    'MAD'
),
(
    'KE',
    'Kenya',
    'KES'
),
(
    'TZ',
    'Tanzania',
    'TZS'
),
(
    'UG',
    'Uganda',
    'UGX'
),
(
    'ZM',
    'Zambia',
    'ZMW'
),
 
-- Latin America
(
    'BR',
    'Brazil',
    'BRL'
),
(
    'AR',
    'Argentina',
    'ARS'
),
(
    'CL',
    'Chile',
    'CLP'
),
(
    'CO',
    'Colombia',
    'COP'
),
(
    'PE',
    'Peru',
    'PEN'
),
(
    'UY',
    'Uruguay',
    'UYU'
),
(
    'PY',
    'Paraguay',
    'PYG'
),
(
    'BO',
    'Bolivia',
    'BOB'
),
(
    'VE',
    'Venezuela',
    'VES'
);

-- =============================================
-- CREATE VIEWS FOR ANALYTICS
-- =============================================

-- View for currency conversion analytics
CREATE VIEW CONVERSION_ANALYTICS AS
    SELECT
        DATE(CONVERSION_TIME) AS CONVERSION_DATE,
        FROM_CURRENCY,
        TO_CURRENCY,
        COUNT(*)              AS CONVERSION_COUNT,
        AVG(AMOUNT)           AS AVG_AMOUNT,
        AVG(EXCHANGE_RATE)    AS AVG_EXCHANGE_RATE,
        MIN(EXCHANGE_RATE)    AS MIN_RATE,
        MAX(EXCHANGE_RATE)    AS MAX_RATE
    FROM
        CONVERSION_HISTORY
    GROUP BY
        DATE(CONVERSION_TIME),
        FROM_CURRENCY,
        TO_CURRENCY
    ORDER BY
        CONVERSION_DATE DESC;

-- View for PPP analytics
CREATE VIEW PPP_ANALYTICS AS
    SELECT
        DATE(CALCULATION_TIME)    AS CALCULATION_DATE,
        FROM_COUNTRY,
        TO_COUNTRY,
        COUNT(*)                  AS CALCULATION_COUNT,
        AVG(PPP_RATE)             AS AVG_PPP_RATE,
        AVG(BIG_MAC_INDEX)        AS AVG_BIG_MAC_INDEX,
        AVG(COST_OF_LIVING_INDEX) AS AVG_COST_OF_LIVING,
        AVG(INCOME_FROM)          AS AVG_INCOME_FROM,
        AVG(INCOME_EQUIVALENT)    AS AVG_INCOME_EQUIVALENT
    FROM
        PPP_HISTORY
    GROUP BY
        DATE(CALCULATION_TIME),
        FROM_COUNTRY,
        TO_COUNTRY
    ORDER BY
        CALCULATION_DATE DESC;

-- View for popular currency pairs
CREATE VIEW POPULAR_CURRENCY_PAIRS AS
    SELECT
        FROM_CURRENCY,
        TO_CURRENCY,
        COUNT(*)             AS USAGE_COUNT,
        AVG(EXCHANGE_RATE)   AS AVG_RATE,
        MAX(CONVERSION_TIME) AS LAST_USED
    FROM
        CONVERSION_HISTORY
    GROUP BY
        FROM_CURRENCY,
        TO_CURRENCY
    ORDER BY
        USAGE_COUNT DESC;

-- View for popular country pairs (PPP)
CREATE VIEW POPULAR_COUNTRY_PAIRS AS
    SELECT
        FROM_COUNTRY,
        TO_COUNTRY,
        COUNT(*)              AS USAGE_COUNT,
        AVG(PPP_RATE)         AS AVG_PPP_RATE,
        MAX(CALCULATION_TIME) AS LAST_USED
    FROM
        PPP_HISTORY
    GROUP BY
        FROM_COUNTRY,
        TO_COUNTRY
    ORDER BY
        USAGE_COUNT DESC;

-- =============================================
-- CREATE STORED PROCEDURES
-- =============================================

DELIMITER

/

/

-- Procedure to clean old data (older than 1 year)
CREATE PROCEDURE CleanOldData()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    DELETE FROM conversion_history 
    WHERE conversion_time < DATE_SUB(NOW(), INTERVAL 1 YEAR);
    
    DELETE FROM ppp_history 
    WHERE calculation_time < DATE_SUB(NOW(), INTERVAL 1 YEAR);
    
    COMMIT;
END //

-- Procedure to get conversion statistics
CREATE PROCEDURE GetConversionStats(
    IN start_date DATE,
    IN end_date DATE
)
BEGIN
    SELECT 
        COUNT(*) as total_conversions,
        COUNT(DISTINCT from_currency) as unique_from_currencies,
        COUNT(DISTINCT to_currency) as unique_to_currencies,
        COUNT(DISTINCT CONCAT(from_currency, '-', to_currency)) as unique_pairs,
        AVG(amount) as avg_conversion_amount,
        SUM(amount) as total_amount_converted
    FROM conversion_history
    WHERE conversion_time BETWEEN start_date AND end_date;
END //

-- Procedure to get PPP statistics
CREATE PROCEDURE GetPPPStats(
    IN start_date DATE,
    IN end_date DATE
)
BEGIN
    SELECT 
        COUNT(*) as total_calculations,
        COUNT(DISTINCT from_country) as unique_from_countries,
        COUNT(DISTINCT to_country) as unique_to_countries,
        COUNT(DISTINCT CONCAT(from_country, '-', to_country)) as unique_pairs,
        AVG(income_from) as avg_income_from,
        AVG(income_equivalent) as avg_income_equivalent,
        AVG(ppp_rate) as avg_ppp_rate
    FROM ppp_history
    WHERE calculation_time BETWEEN start_date AND end_date;
END //

DELIMITER ;

-- =============================================
-- CREATE TRIGGERS FOR AUDIT
-- =============================================

-- Trigger to update currency updated_at timestamp
DELIMITER //
CREATE TRIGGER currency_update_timestamp 
    BEFORE UPDATE ON currencies
    FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END //
DELIMITER ;

-- Trigger to update country updated_at timestamp
DELIMITER //
CREATE TRIGGER country_update_timestamp 
    BEFORE UPDATE ON countries
    FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END //
DELIMITER ;

-- =============================================
-- GRANT PERMISSIONS (adjust as needed)
-- =============================================

-- Create application user (replace with actual credentials)
-- CREATE USER 'currency_app'@'localhost' IDENTIFIED BY 'secure_password_here';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON currency_converter_pro.* TO 'currency_app'@'localhost';
-- GRANT EXECUTE ON PROCEDURE currency_converter_pro.CleanOldData TO 'currency_app'@'localhost';
-- GRANT EXECUTE ON PROCEDURE currency_converter_pro.GetConversionStats TO 'currency_app'@'localhost';
-- GRANT EXECUTE ON PROCEDURE currency_converter_pro.GetPPPStats TO 'currency_app'@'localhost';
-- FLUSH PRIVILEGES;

-- =============================================
-- OPTIMIZATION SETTINGS
-- =============================================

-- Optimize table settings for better performance
ALTER TABLE conversion_history 
    PARTITION BY RANGE (YEAR(conversion_time)) (
        PARTITION p2023 VALUES LESS THAN (2024),
        PARTITION p2024 VALUES LESS THAN (2025),
        PARTITION p2025 VALUES LESS THAN (2026),
        PARTITION p_future VALUES LESS THAN MAXVALUE
    );

ALTER TABLE ppp_history 
    PARTITION BY RANGE (YEAR(calculation_time)) (
        PARTITION p2023 VALUES LESS THAN (2024),
        PARTITION p2024 VALUES LESS THAN (2025),
        PARTITION p2025 VALUES LESS THAN (2026),
        PARTITION p_future VALUES LESS THAN MAXVALUE
    );

-- =============================================
-- SAMPLE QUERIES FOR TESTING
-- =============================================

/*
-- Test currency conversion insertion
INSERT INTO conversion_history (from_currency, to_currency, amount, result, exchange_rate, api_source)
VALUES ('USD', 'EUR', 100.00, 85.20, 0.8520, 'exchangerate-api');

-- Test PPP calculation insertion
INSERT INTO ppp_history (from_country, to_country, ppp_rate, big_mac_index, cost_of_living_index, income_from, income_equivalent, exchange_rate, data_source)
VALUES ('US', 'GB', 0.65, -12.5, 84.2, 5000.00, 4200.00, 0.73, 'worldbank-api');

-- Get conversion trends for last 30 days
SELECT DATE(conversion_time) as date, COUNT(*) as conversions
FROM conversion_history 
WHERE conversion_time >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY DATE(conversion_time)
ORDER BY date DESC;

-- Get most popular currency pairs
SELECT from_currency, to_currency, COUNT(*) as usage_count
FROM conversion_history
GROUP BY from_currency, to_currency
ORDER BY usage_count DESC
LIMIT 10;

-- Get PPP calculation trends
SELECT DATE(calculation_time) as date, COUNT(*) as calculations
FROM ppp_history 
WHERE calculation_time >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY DATE(calculation_time)
ORDER BY date DESC;
*/

-- End of currency_converter_mysql.sql