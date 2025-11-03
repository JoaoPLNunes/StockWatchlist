from flask import Flask, request, url_for, flash, redirect,render_template
from utils import load_watchlist, save_watchlist, fetch_stock_data
app = Flask(__name__, template_folder='templates')
app.secret_key = 'wlccarjjua14'

@app.route('/', methods = ['GET', 'POST'])
def index():
    tickers = load_watchlist()
    if request.method == 'POST':
        ticker = request.form.get('ticker').upper().strip()
        if not ticker:
            flash("Insere ticker", 'error')
        else:
            data = fetch_stock_data(ticker)
            if data:
                if ticker not in tickers:
                    tickers.append(ticker)
                    save_watchlist(tickers)
                    flash(f'{ticker} adicionado', 'success')
                else:
                    flash(f'{ticker} já está na lista.', 'info')
            else:
                    flash(f'Problema no {ticker} .', 'error')
            return redirect(url_for('index'))
    else:
        stocks_data = []
        for ticker in tickers:
            data = fetch_stock_data(ticker)
            if data:
                stocks_data.append(data)
        return render_template('index.html', stocks = stocks_data)





@app.route('/remove/<ticker>')
def remove(ticker):
    tickers = load_watchlist()
    if ticker in tickers:
        tickers.remove(ticker)
        save_watchlist(tickers)
        flash(f'{ticker} removido', 'success')
    else:
        flash(f'{ticker} não está na lista', 'error')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug = True)