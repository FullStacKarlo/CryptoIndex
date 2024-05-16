from flask import Flask, render_template
from pycoingecko import CoinGeckoAPI

# Crea una instancia de Flask
app = Flask(__name__, static_folder='static')

# Crea una instancia de CoinGeckoAPI
cg = CoinGeckoAPI()

# Variables globales para almacenar los datos de la API
top_cryptos = []
prices_usd = {}
prices_eur = {}

# Función para actualizar los datos de la API
def update_data():
    global top_cryptos, prices_usd, prices_eur
    # Obtén la lista de las 20 criptomonedas más populares solo si está vacía
    if not top_cryptos:
        top_cryptos = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=20, page=1)
    
    # Extrae los identificadores de las criptomonedas
    crypto_ids = [crypto['id'] for crypto in top_cryptos]

    # Obtén los precios de las criptomonedas en USD y EUR solo si no están disponibles
    if not prices_usd:
        prices_usd = cg.get_price(ids=crypto_ids, vs_currencies='usd')
    if not prices_eur:
        prices_eur = cg.get_price(ids=crypto_ids, vs_currencies='eur')

# Ruta para la página principal
@app.route('/')
def index():
    update_data()  # Actualiza los datos antes de renderizar la plantilla
    # Renderiza la plantilla HTML y pasa los datos a la plantilla
    return render_template('index.html', top_cryptos=top_cryptos, prices_usd=prices_usd, prices_eur=prices_eur)

if __name__ == '__main__':
    app.run(debug=True)