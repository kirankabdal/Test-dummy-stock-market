from flask import Flask, render_template, request, redirect, url_for, jsonify
import random

app = Flask(__name__)

# Dummy stock data
stocks = {
    "AAPL": {"name": "Apple Inc.", "price": 150.0},
    "GOOGL": {"name": "Alphabet Inc.", "price": 2800.0},
    "AMZN": {"name": "Amazon.com Inc.", "price": 3400.0},
    "TSLA": {"name": "Tesla Inc.", "price": 800.0},
    "MSFT": {"name": "Microsoft Corporation", "price": 300.0},
}

# Dummy user portfolio (stock symbol and quantity)
portfolio = {
    "AAPL": 0,
    "GOOGL": 0,
    "AMZN": 0,
    "TSLA": 0,
    "MSFT": 0,
}

# Simulating stock price changes
def update_stock_prices():
    for symbol in stocks:
        price_change = random.uniform(-10, 10)
        stocks[symbol]["price"] += price_change
        if stocks[symbol]["price"] < 0:
            stocks[symbol]["price"] = 0.1  # Prevent negative prices

@app.route('/')
def index():
    update_stock_prices()  # Update stock prices
    return render_template('index.html', stocks=stocks, portfolio=portfolio)

@app.route('/buy/<symbol>', methods=['POST'])
def buy_stock(symbol):
    if symbol in stocks:
        quantity = int(request.form['quantity'])
        if quantity > 0:
            portfolio[symbol] += quantity
    return redirect(url_for('index'))

@app.route('/sell/<symbol>', methods=['POST'])
def sell_stock(symbol):
    if symbol in stocks:
        quantity = int(request.form['quantity'])
        if quantity > 0 and portfolio[symbol] >= quantity:
            portfolio[symbol] -= quantity
    return redirect(url_for('index'))

@app.route('/api/stocks')
def api_stocks():
    return jsonify(stocks)

if __name__ == "__main__":
    app.run(debug=True)