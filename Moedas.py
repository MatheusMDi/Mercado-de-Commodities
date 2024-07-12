import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import pyodbc


def get_cotacao(ticker, dt_inicial, dt_final):
    data = yf.download(ticker, start=dt_inicial, end=dt_final)
    df = data[['Close']].reset_index()
    return df

def insert_df_to_sql(df_final, table_name, cursor):
    sql_insert = f"""
                 INSERT INTO {table_name}
                 ({', '.join(['[' + col.replace('\n', '').replace(' ', '_').replace('/', '') + ']' for col in df_final.columns])})
                 VALUES ({', '.join(['?' for _ in range(len(df_final.columns))])})
                 """
    values = [tuple(str(value) for value in row) for _, row in df_final.iterrows()]
    cursor.executemany(sql_insert, values)
    print(f"{len(values)} linhas foram inseridas na tabela {table_name}.")

def truncate_table(table_name, cursor):
    sql_truncate = f"TRUNCATE TABLE {table_name}"
    cursor.execute(sql_truncate)
    print(f"Tabela {table_name} foi truncada.")

dias_atras = 30

dt_final = datetime.now().strftime('%Y-%m-%d')
dt_inicial = (datetime.now() - timedelta(days=dias_atras)).strftime('%Y-%m-%d')


print('Euro:')
eur_brl_df = get_cotacao('EURBRL=X', dt_inicial, dt_final)
print('Dolár:')
usd_brl_df = get_cotacao('BRL=X', dt_inicial, dt_final)
print('Won sul-coreano:')
krw_usd_df = get_cotacao('KRW=X', dt_inicial, dt_final)
print('ringgit malaio:')
myr_usd_df = get_cotacao('MYR=X', dt_inicial, dt_final)
print('DIRR3:')
diir3_df = get_cotacao('DIRR3.SA', dt_inicial, dt_final)

usd_brl_df.rename(columns={'Close': 'Valor'}, inplace=True)
eur_brl_df.rename(columns={'Close': 'Valor'}, inplace=True)
krw_usd_df.rename(columns={'Close': 'Valor'}, inplace=True)
myr_usd_df.rename(columns={'Close': 'Valor'}, inplace=True)
diir3_df.rename(columns={'Close': 'Valor'}, inplace=True)

usd_brl_df.rename(columns={'Date': 'Data'}, inplace=True)
eur_brl_df.rename(columns={'Date': 'Data'}, inplace=True)
krw_usd_df.rename(columns={'Date': 'Data'}, inplace=True)
myr_usd_df.rename(columns={'Date': 'Data'}, inplace=True)
diir3_df.rename(columns={'Date': 'Data'}, inplace=True)

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

truncate_table('CotacaoDolar', cursor)
insert_df_to_sql(usd_brl_df, 'CotacaoDolar', cursor)
print('Inseriu USD')

truncate_table('CotacaoEuro', cursor)
insert_df_to_sql(eur_brl_df, 'CotacaoEuro', cursor)
print('Inseriu EUR')

truncate_table('CotacaoWon', cursor)
insert_df_to_sql(krw_usd_df, 'CotacaoWon', cursor)
print('Inseriu KRW')

truncate_table('CotacaoRinggit', cursor)
insert_df_to_sql(myr_usd_df, 'CotacaoRinggit', cursor)
print('Inseriu MYR')


conn.commit()
conn.close()
print('Fechou conexão')
