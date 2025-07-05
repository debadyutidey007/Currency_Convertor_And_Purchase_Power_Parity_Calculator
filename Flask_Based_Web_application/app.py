from flask import Flask, render_template, request, jsonify, send_file
import logging
import datetime
import json
import os
from database import DatabaseManager
from currency_api import CurrencyAPI
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import base64

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)

# Initialize database and API
db_manager = DatabaseManager()
currency_api = CurrencyAPI()

@app.route('/')
def index():
    """Main page with currency converter and PPP calculator."""
    try:
        # Get all currencies for dropdown
        currencies = db_manager.get_all_currencies()
        countries = db_manager.get_all_countries()
        
        return render_template('index.html', 
                             currencies=currencies, 
                             countries=countries)
    except Exception as e:
        logging.error(f"Error loading main page: {e}")
        return render_template('index.html', 
                             currencies=[], 
                             countries=[],
                             error="Failed to load currency data")

@app.route('/api/convert', methods=['POST'])
def convert_currency():
    """Convert currency using real-time exchange rates."""
    try:
        data = request.json
        from_currency = data.get('from_currency')
        to_currency = data.get('to_currency')
        amount = float(data.get('amount', 0))
        
        if not all([from_currency, to_currency, amount]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Get exchange rate
        exchange_rate = currency_api.get_exchange_rate(from_currency, to_currency)
        if exchange_rate is None:
            return jsonify({'error': 'Failed to get exchange rate'}), 500
        
        # Calculate result
        result = amount * exchange_rate
        
        # Save to database
        db_manager.save_conversion_history(
            from_currency, to_currency, amount, result, exchange_rate
        )
        
        return jsonify({
            'success': True,
            'result': round(result, 4),
            'exchange_rate': exchange_rate,
            'from_currency': from_currency,
            'to_currency': to_currency,
            'amount': amount,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Currency conversion error: {e}")
        return jsonify({'error': 'Conversion failed'}), 500

@app.route('/api/ppp', methods=['POST'])
def calculate_ppp():
    """Calculate Purchasing Power Parity between countries."""
    try:
        data = request.json
        from_country = data.get('from_country')
        to_country = data.get('to_country')
        income = float(data.get('income', 0))
        
        if not all([from_country, to_country, income]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Get PPP data
        ppp_data = currency_api.get_ppp_data(from_country, to_country)
        if not ppp_data:
            return jsonify({'error': 'Failed to get PPP data'}), 500
        
        # Calculate equivalent income
        ppp_rate = ppp_data.get('ppp_rate', 1.0)
        equivalent_income = income * ppp_rate
        
        # Save to database
        db_manager.save_ppp_history(
            from_country, to_country, ppp_rate,
            ppp_data.get('big_mac_index', 0),
            ppp_data.get('cost_of_living_index', 0),
            income, equivalent_income
        )
        
        return jsonify({
            'success': True,
            'ppp_rate': ppp_rate,
            'equivalent_income': round(equivalent_income, 2),
            'big_mac_index': ppp_data.get('big_mac_index', 0),
            'cost_of_living_index': ppp_data.get('cost_of_living_index', 0),
            'from_country': from_country,
            'to_country': to_country,
            'income': income,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"PPP calculation error: {e}")
        return jsonify({'error': 'PPP calculation failed'}), 500

@app.route('/api/history')
def get_history():
    """Get conversion and PPP history."""
    try:
        history_type = request.args.get('type', 'conversion')
        limit = int(request.args.get('limit', 20))
        
        if history_type == 'conversion':
            history = db_manager.get_conversion_history(limit)
        else:
            history = db_manager.get_ppp_history(limit)
        
        return jsonify({
            'success': True,
            'history': history
        })
        
    except Exception as e:
        logging.error(f"History retrieval error: {e}")
        return jsonify({'error': 'Failed to retrieve history'}), 500

@app.route('/api/chart')
def get_chart_data():
    """Generate chart data for visualization."""
    try:
        chart_type = request.args.get('type', 'conversion_trends')
        
        if chart_type == 'conversion_trends':
            data = db_manager.get_conversion_trends()
        else:
            data = db_manager.get_ppp_trends()
        
        # Create chart
        plt.figure(figsize=(10, 6))
        
        if chart_type == 'conversion_trends':
            df = pd.DataFrame(data)
            if not df.empty:
                df['date'] = pd.to_datetime(df['conversion_time'])
                daily_counts = df.groupby(df['date'].dt.date).size()
                
                plt.plot(daily_counts.index, daily_counts.values, marker='o')
                plt.title('Daily Conversion Activity')
                plt.xlabel('Date')
                plt.ylabel('Number of Conversions')
                plt.xticks(rotation=45)
        else:
            df = pd.DataFrame(data)
            if not df.empty:
                df['date'] = pd.to_datetime(df['calculation_time'])
                daily_counts = df.groupby(df['date'].dt.date).size()
                
                plt.plot(daily_counts.index, daily_counts.values, marker='s')
                plt.title('Daily PPP Calculation Activity')
                plt.xlabel('Date')
                plt.ylabel('Number of Calculations')
                plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        # Convert to base64 string
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.read()).decode()
        plt.close()
        
        return jsonify({
            'success': True,
            'chart': f'data:image/png;base64,{img_str}'
        })
        
    except Exception as e:
        logging.error(f"Chart generation error: {e}")
        return jsonify({'error': 'Failed to generate chart'}), 500

@app.route('/api/export')
def export_data():
    """Export conversion history to CSV."""
    try:
        export_type = request.args.get('type', 'conversion')
        
        if export_type == 'conversion':
            data = db_manager.get_conversion_history(1000)
            df = pd.DataFrame(data)
            filename = f'conversion_history_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        else:
            data = db_manager.get_ppp_history(1000)
            df = pd.DataFrame(data)
            filename = f'ppp_history_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        # Create CSV in memory
        output = BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        logging.error(f"Export error: {e}")
        return jsonify({'error': 'Export failed'}), 500

@app.route('/api/delete-history', methods=['POST'])
def delete_history():
    """Delete conversion or PPP history."""
    try:
        data = request.get_json()
        history_type = data.get('type')
        
        if history_type == 'conversion':
            success = db_manager.delete_conversion_history()
            if success:
                return jsonify({'message': 'Conversion history deleted successfully'}), 200
            else:
                return jsonify({'error': 'Failed to delete conversion history'}), 500
        
        elif history_type == 'ppp':
            success = db_manager.delete_ppp_history()
            if success:
                return jsonify({'message': 'PPP history deleted successfully'}), 200
            else:
                return jsonify({'error': 'Failed to delete PPP history'}), 500
        
        else:
            return jsonify({'error': 'Invalid history type'}), 400
            
    except Exception as e:
        logging.error(f"Delete history error: {e}")
        return jsonify({'error': 'Failed to delete history'}), 500

@app.route('/api/currencies')
def get_currencies():
    """Get all available currencies."""
    try:
        currencies = db_manager.get_all_currencies()
        return jsonify({
            'success': True,
            'currencies': currencies
        })
    except Exception as e:
        logging.error(f"Currencies retrieval error: {e}")
        return jsonify({'error': 'Failed to retrieve currencies'}), 500

@app.route('/api/countries')
def get_countries():
    """Get all available countries."""
    try:
        countries = db_manager.get_all_countries()
        return jsonify({
            'success': True,
            'countries': countries
        })
    except Exception as e:
        logging.error(f"Countries retrieval error: {e}")
        return jsonify({'error': 'Failed to retrieve countries'}), 500

if __name__ == '__main__':
    # Initialize database on startup
    db_manager.initialize_database()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)