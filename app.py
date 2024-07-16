from flask import Flask, jsonify, render_template
import pyodbc

app = Flask(__name__)

server = 'localhost'
database = 'db_dados_mercado'

connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    'Trusted_Connection=yes;'
)

def get_stock_data():
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    stock_data = []

    tables = [
        'CotacaoDolar', 'CotacaoEuro', 'CotacaoWon', 'CotacaoRinggit',
        'CotacaoDirecional', 'CotacaoSteelRebar', 'CotacaoSteelScrap',
        'CotacaoAluminum', 'CotacaoIronOre', 'CotacaoCopper',
        'CotacaoSoybeanOil', 'CotacaoNaturalGas', 'CotacaoBrentOil',
        'CotacaoPPFutures', 'CotacaoPVCFutures', 'CotacaoLLDPEFutures'
    ]
    
    for table in tables:
        cursor.execute(f"""
            SELECT TOP 1 simbolo, price, Data FROM {table}
            ORDER BY Data DESC
        """)
        latest = cursor.fetchone()
        if latest:
            cursor.execute(f"""
                SELECT TOP 1 price FROM {table}
                WHERE Data < ?
                ORDER BY Data DESC
            """, latest.Data)
            previous = cursor.fetchone()

            if previous and latest.price is not None and previous.price is not None:
                change = float(latest.price) - float(previous.price)
                stock_data.append({
                    'symbol': latest.simbolo,
                    'price': float(latest.price),
                    'change': change
                })
            else:
                print(f"No valid previous price found for table {table}")
        else:
            print(f"No data found for table {table}")

    conn.close()
    return stock_data


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stock-data')
def stock_data():
    data = get_stock_data()
    return jsonify(data)

@app.route('/api/history/cotacaodolar')
def currency_history():
    return fetch_history('CotacaoDolar')

@app.route('/api/history/cotacaoeuro')
def euro_history():
    return fetch_history('CotacaoEuro')

@app.route('/api/history/cotacaoWon')
def won_history():
    return fetch_history('CotacaoWon')

@app.route('/api/history/cotacaoringgit')
def cotacao_ringgit():
    return fetch_history('CotacaoRinggit')

@app.route('/api/history/cotacaodir3')
def cotacao_dir3():
    return fetch_history('CotacaoDirecional')

@app.route('/api/history/CotacaoSteelRebar')
def steel_rebar_history():
    return fetch_history('CotacaoSteelRebar')

@app.route('/api/history/CotacaoSteelScrap')
def steel_scrap_history():
    return fetch_history('CotacaoSteelScrap')

@app.route('/api/history/CotacaoAluminum')
def aluminum_history():
    return fetch_history('CotacaoAluminum')

@app.route('/api/history/CotacaoIronOre')
def iron_ore_history():
    return fetch_history('CotacaoIronOre')

@app.route('/api/history/CotacaoCopper')
def copper_history():
    return fetch_history('CotacaoCopper')

@app.route('/api/history/CotacaoSoybeanOil')
def soybean_oil_history():
    return fetch_history('CotacaoSoybeanOil')

@app.route('/api/history/CotacaoNaturalGas')
def natural_gas_history():
    return fetch_history('CotacaoNaturalGas')

@app.route('/api/history/CotacaoBrentOil')
def brent_oil_history():
    return fetch_history('CotacaoBrentOil')

@app.route('/api/history/CotacaoPPFutures')
def pp_futures_history():
    return fetch_history('CotacaoPPFutures')

@app.route('/api/history/CotacaoPVCFutures')
def pvc_futures_history():
    return fetch_history('CotacaoPVCFutures')

@app.route('/api/history/CotacaoLLDPEFutures')
def lldpe_futures_history():
    return fetch_history('CotacaoLLDPEFutures')

def fetch_history(table_name):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    cursor.execute(f"""
        SELECT Data, price FROM {table_name}
        ORDER BY Data ASC
    """)
    
    history = cursor.fetchall()
    conn.close()
    
    return jsonify([{'Data': row[0].strftime('%Y-%m-%d'), 'price': row[1]} for row in history])
def get_report_data():
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    query = """
    SELECT * from (
SELECT 
        Simbolo,
        price,
        Abertura,
        Máxima,
        Mínima,
        REPLACE(REPLACE(REPLACE(Var, '%', ''), '{', ''), '+', '') AS Var
    FROM 
        CotacaoDolar
    WHERE 
        data = (SELECT MAX(data) FROM CotacaoDolar)

    UNION ALL

    SELECT 
        Simbolo,
        price,
        Abertura,
        Máxima,
        Mínima,
        REPLACE(REPLACE(REPLACE(Var, '%', ''), '{', ''), '+', '') AS Var
    FROM 
        CotacaoEuro
    WHERE 
        data = (SELECT MAX(data) FROM CotacaoEuro)

    UNION ALL

    SELECT 
        Simbolo,
        price,
        Abertura,
        Máxima,
        Mínima,
        REPLACE(REPLACE(REPLACE(Var, '%', ''), '{', ''), '+', '') AS Var
    FROM 
        CotacaoWon
    WHERE 
        data = (SELECT MAX(data) FROM CotacaoWon)

    UNION ALL

    SELECT 
        Simbolo,
        price,
        Abertura,
        Máxima,
        Mínima,
        REPLACE(REPLACE(REPLACE(Var, '%', ''), '{', ''), '+', '') AS Var
    FROM 
        CotacaoRinggit
    WHERE 
        data = (SELECT MAX(data) FROM CotacaoRinggit)

    UNION ALL

    SELECT 
        Simbolo,
        price,
        Abertura,
        Máxima,
        Mínima,
        REPLACE(REPLACE(REPLACE(Var, '%', ''), '{', ''), '+', '') AS Var
    FROM 
        CotacaoDirecional
    WHERE 
        data = (SELECT MAX(data) FROM CotacaoDirecional)

    UNION ALL

SELECT 
    Simbolo,
    price,
    REPLACE(REPLACE(Abertura, '.', ''), ',', '.') AS Abertura,
    REPLACE(REPLACE(Máxima, '.', ''), ',', '.') AS Máxima,
    REPLACE(REPLACE(Mínima, '.', ''), ',', '.') AS Mínima,
    REPLACE(REPLACE(REPLACE(Var, '%', ''), '-', ''), '+', '') AS Var
FROM 
    CotacaoSteelRebar
WHERE 
    data = (SELECT MAX(data) FROM CotacaoSteelRebar)

UNION ALL

SELECT 
    Simbolo,
    price,
    REPLACE(REPLACE(Abertura, '.', ''), ',', '.') AS Abertura,
    REPLACE(REPLACE(Máxima, '.', ''), ',', '.') AS Máxima,
    REPLACE(REPLACE(Mínima, '.', ''), ',', '.') AS Mínima,
    REPLACE(REPLACE(REPLACE(Var, '%', ''), '-', ''), '+', '') AS Var
FROM 
    CotacaoSteelScrap
WHERE 
    data = (SELECT MAX(data) FROM CotacaoSteelScrap)

UNION ALL

SELECT 
    Simbolo,
	price,
    REPLACE(REPLACE(Abertura, '.', ''), ',', '.') AS Abertura,
    REPLACE(REPLACE(Máxima, '.', ''), ',', '.') AS Máxima,
    REPLACE(REPLACE(Mínima, '.', ''), ',', '.') AS Mínima,
    REPLACE(REPLACE(REPLACE(Var, '%', ''), '-', ''), '+', '') AS Var
FROM 
    CotacaoAluminum
WHERE 
    data = (SELECT MAX(data) FROM CotacaoAluminum)

UNION ALL

SELECT top 1
    Simbolo,
    price,
    REPLACE(REPLACE(Abertura, '.', ''), ',', '.') AS Abertura,
    REPLACE(REPLACE(Máxima, '.', ''), ',', '.') AS Máxima,
    REPLACE(REPLACE(Mínima, '.', ''), ',', '.') AS Mínima,
    REPLACE(REPLACE(REPLACE(Var, '%', ''), '-', ''), '+', '') AS Var
FROM 
    CotacaoIronOre
WHERE 
    data = (SELECT MAX(data) FROM CotacaoIronOre)

UNION ALL

SELECT 
    Simbolo,
    price,
    REPLACE(REPLACE(Abertura, '.', ''), ',', '.') AS Abertura,
    REPLACE(REPLACE(Máxima, '.', ''), ',', '.') AS Máxima,
    REPLACE(REPLACE(Mínima, '.', ''), ',', '.') AS Mínima,
    REPLACE(REPLACE(REPLACE(Var, '%', ''), '-', ''), '+', '') AS Var
FROM 
    CotacaoCopper
WHERE 
    data = (SELECT MAX(data) FROM CotacaoCopper)

UNION ALL

SELECT 
    Simbolo,
	price,
    REPLACE(REPLACE(Abertura, '.', ''), ',', '.') AS Abertura,
    REPLACE(REPLACE(Máxima, '.', ''), ',', '.') AS Máxima,
    REPLACE(REPLACE(Mínima, '.', ''), ',', '.') AS Mínima,
    REPLACE(REPLACE(REPLACE(Var, '%', ''), '-', ''), '+', '') AS Var
FROM 
    CotacaoSoybeanOil
WHERE 
    data = (SELECT MAX(data) FROM CotacaoSoybeanOil)

UNION ALL

SELECT 
    Simbolo,
    price,
    REPLACE(REPLACE(Abertura, '.', ''), ',', '.') AS Abertura,
    REPLACE(REPLACE(Máxima, '.', ''), ',', '.') AS Máxima,
    REPLACE(REPLACE(Mínima, '.', ''), ',', '.') AS Mínima,
    REPLACE(REPLACE(REPLACE(Var, '%', ''), '-', ''), '+', '') AS Var
FROM 
    CotacaoNaturalGas
WHERE 
    data = (SELECT MAX(data) FROM CotacaoNaturalGas)

UNION ALL

SELECT 
    Simbolo,
    price,
    REPLACE(REPLACE(Abertura, '.', ''), ',', '.') AS Abertura,
    REPLACE(REPLACE(Máxima, '.', ''), ',', '.') AS Máxima,
    REPLACE(REPLACE(Mínima, '.', ''), ',', '.') AS Mínima,
    REPLACE(REPLACE(REPLACE(Var, '%', ''), '-', ''), '+', '') AS Var
FROM 
    CotacaoBrentOil
WHERE 
    data = (SELECT MAX(data) FROM CotacaoBrentOil)

UNION ALL

SELECT 
    Simbolo,
	price,
    REPLACE(REPLACE(Abertura, '.', ''), ',', '.') AS Abertura,
    REPLACE(REPLACE(Máxima, '.', ''), ',', '.') AS Máxima,
    REPLACE(REPLACE(Mínima, '.', ''), ',', '.') AS Mínima,
    REPLACE(REPLACE(REPLACE(Var, '%', ''), '-', ''), '+', '') AS Var
FROM 
    CotacaoPPFutures
WHERE 
    data = (SELECT MAX(data) FROM CotacaoPPFutures)

UNION ALL

SELECT 
    Simbolo,
    price,
    REPLACE(REPLACE(Abertura, '.', ''), ',', '.') AS Abertura,
    REPLACE(REPLACE(Máxima, '.', ''), ',', '.') AS Máxima,
    REPLACE(REPLACE(Mínima, '.', ''), ',', '.') AS Mínima,
    REPLACE(REPLACE(REPLACE(Var, '%', ''), '-', ''), '+', '') AS Var
FROM 
    CotacaoPVCFutures
WHERE 
    data = (SELECT MAX(data) FROM CotacaoPVCFutures)

UNION ALL

SELECT 
    Simbolo,
    price,
    REPLACE(REPLACE(Abertura, '.', ''), ',', '.') AS Abertura,
    REPLACE(REPLACE(Máxima, '.', ''), ',', '.') AS Máxima,
    REPLACE(REPLACE(Mínima, '.', ''), ',', '.') AS Mínima,
    REPLACE(REPLACE(REPLACE(Var, '%', ''), '-', ''), '+', '') AS Var
FROM 
    CotacaoLLDPEFutures
WHERE 
    data = (SELECT MAX(data) FROM CotacaoLLDPEFutures)) data;
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    
    return result

@app.route('/report')
def report():
    report_data = get_report_data()
    return render_template('report.html', report_data=report_data)


if __name__ == '__main__':
    app.run(debug=True)
