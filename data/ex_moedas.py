import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import pyodbc

# Funções
def get_cotacao(ticker, dt_inicial, dt_final):
    data = yf.download(ticker, start=dt_inicial, end=dt_final)
    data = data[['Open', 'High', 'Low', 'Close']].rename(columns={'Close': 'price'}).reset_index()
    data['Data'] = data['Date']
    del data['Date']
    data.dropna(subset=['Data'], inplace=True)
    return data

def upsert_df_to_sql(df, table_name, cursor):
    for _, row in df.iterrows():
        # Verifica se os valores são válidos
        if pd.isnull(row['price']) or pd.isnull(row['Abertura']) or pd.isnull(row['Máxima']) or pd.isnull(row['Mínima']) or pd.isnull(row['Var']):
            continue  # Pula linhas com valores inválidos

        sql_upsert = f"""
            MERGE INTO {table_name} AS target
            USING (SELECT ? AS Data, ? AS price, ? AS Simbolo, ? AS Abertura, ? AS Máxima, ? AS Mínima, ? AS Var) AS source
            ON target.Data = source.Data AND target.Simbolo = source.Simbolo
            WHEN MATCHED THEN
                UPDATE SET
                    target.price = source.price,
                    target.Abertura = source.Abertura,
                    target.Máxima = source.Máxima,
                    target.Mínima = source.Mínima,
                    target.Var = source.Var
            WHEN NOT MATCHED THEN
                INSERT (Data, price, Simbolo, Abertura, Máxima, Mínima, Var)
                VALUES (source.Data, source.price, source.Simbolo, source.Abertura, source.Máxima, source.Mínima, source.Var);
        """
        cursor.execute(sql_upsert, 
                       row['Data'], 
                       row['price'], 
                       row['Simbolo'], 
                       row['Abertura'], 
                       row['Máxima'], 
                       row['Mínima'], 
                       row['Var'])
    print(f"{len(df)} linhas foram inseridas/atualizadas na tabela {table_name}.")

def prepare_dataframes(tickers, symbols, dt_inicial, dt_final):
    dfs = []
    for ticker, symbol in zip(tickers, symbols):
        df = get_cotacao(ticker, dt_inicial, dt_final)
        df['Simbolo'] = symbol
        df['Var'] = (df['price'] - df['price'].shift(1)) / df['price'].shift(1) * 100
        
        # Renomear colunas
        df.rename(columns={
            'Open': 'Abertura',
            'High': 'Máxima',
            'Low': 'Mínima'
        }, inplace=True)

        df['price'] = df['price'].round(2)
        df['Abertura'] = df['Abertura'].round(2)
        df['Máxima'] = df['Máxima'].round(2)
        df['Mínima'] = df['Mínima'].round(2)
        df['Var'] = df['Var'].round(2)

        dfs.append(df)
    return dfs

def main():
    dias_atras = 10
    dt_final = datetime.now().strftime('%Y-%m-%d')
    dt_inicial = (datetime.now() - timedelta(days=dias_atras)).strftime('%Y-%m-%d')

    tickers = ['EURBRL=X', 'BRL=X', 'KRW=X', 'MYR=X', 'DIRR3.SA']
    symbols = ['Euro', 'Dólar', 'Won', 'Ringgit', 'DIRR3']

    print('Buscando cotações...')
    dataframes = prepare_dataframes(tickers, symbols, dt_inicial, dt_final)

    server = 'localhost'
    database = 'db_dados_mercado'
    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={server};'
        f'DATABASE={database};'
        'Trusted_Connection=yes;'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    for df, table_name in zip(dataframes, ['CotacaoEuro', 'CotacaoDolar', 'CotacaoWon', 'CotacaoRinggit', 'CotacaoDirecional']):
        upsert_df_to_sql(df, table_name, cursor)
        print(f'Inseriu/atualizou {df["Simbolo"].iloc[0]}')

    conn.commit()
    conn.close()
    print('Fechou conexão')

if __name__ == "__main__":
    main()
