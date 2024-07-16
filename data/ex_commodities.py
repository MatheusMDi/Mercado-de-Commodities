import requests
from lxml import html
import pandas as pd
import pyodbc

# URLs e símbolos para extração de dados
urls = [
    ("steel_rebar", "https://br.investing.com/commodities/steel-rebar-historical-data"),
    ("steel_scrap", "https://br.investing.com/commodities/steel-scrap-historical-data"),
    ("aluminum", "https://br.investing.com/commodities/aluminum-historical-data"),
    ("iron_ore", "https://br.investing.com/commodities/iron-ore-62-cfr-futures-historical-data"),
    ("copper", "https://br.investing.com/commodities/copper-historical-data"),
    ("soybean_oil", "https://br.investing.com/commodities/us-soybean-oil-historical-data"),
    ("natural_gas", "https://br.investing.com/commodities/natural-gas-historical-data"),
    ("brent_oil", "https://br.investing.com/commodities/brent-oil-historical-data"),
    ("pp_futures", "https://br.investing.com/commodities/pp-futures-historical-data"),
    ("pvc_futures", "https://br.investing.com/commodities/pvc-com-futures-historical-data"),
    ("lldpe_futures", "https://br.investing.com/commodities/lldpe-futures-historical-data")
]

def extract_data(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)

    xpath = '/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[3]/table'
    table = tree.xpath(xpath)

    if not table:
        raise Exception(f"Tabela não encontrada para {url}!")

    data = []
    for row in table[0].xpath('.//tr')[1:]: 
        cols = row.xpath('.//td')
        if len(cols) >= 6:  # Verifica se há colunas suficientes
            data.append([
                cols[0].text_content().strip(),  # Data
                cols[1].text_content().strip(),  # Último (preço)
                cols[2].text_content().strip(),  # Abertura
                cols[3].text_content().strip(),  # Máxima
                cols[4].text_content().strip(),  # Mínima
                #cols[5].text_content().strip(),  # Volume
                cols[6].text_content().strip()   # Variação
            ])

    return data

def insert_df_to_sql(df_final, table_name, cursor):
    sql_insert = f"""
        INSERT INTO {table_name}
        ([Data], [price], [Simbolo], [Abertura], [Máxima], [Mínima], [Var])
        VALUES ({', '.join(['?' for _ in range(len(df_final.columns))])})
    """
    values = [tuple(row) for row in df_final.values]
    cursor.executemany(sql_insert, values)
    print(f"{len(values)} linhas foram inseridas na tabela {table_name}.")

def truncate_table(table_name, cursor):
    sql_truncate = f"TRUNCATE TABLE {table_name}"
    cursor.execute(sql_truncate)
    print(f"Tabela {table_name} foi truncada.")

def create_dataframe(name, data):
    df = pd.DataFrame(data, columns=['Data', 'Último', 'Abertura', 'Máxima', 'Mínima',  'Var%'])
    df['Simbolo'] = name.replace('_', ' ').title()  # Adiciona o símbolo
    df = df.rename(columns={'Último': 'price'})  # Renomeia 'Último' para 'price'
    return df[['Data', 'price', 'Simbolo', 'Abertura', 'Máxima', 'Mínima',  'Var%']]  # Ordena as colunas

def main():
    # Extração de dados e criação de DataFrames
    dataframes = {}
    for name, url in urls:
        data = extract_data(url)
        dataframes[name] = create_dataframe(name, data)

    # Conexão com o banco de dados
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

    # Alteração de tipos de colunas
    alter_queries = [
        f"ALTER TABLE Cotacao{name.title().replace('_', '')} ALTER COLUMN [price] VARCHAR(50)" for name in dataframes.keys()
    ]
    for query in alter_queries:
        try:
            cursor.execute(query)
        except Exception as e:
            print(f"Erro ao executar a query: {query}\n{e}")

    # Inserção de dados no banco de dados
    for name, df in dataframes.items():
        table_name = f'Cotacao{name.title().replace("_", "")}'
        truncate_table(table_name, cursor)
        insert_df_to_sql(df, table_name, cursor)
        print(f'Inseriu {df["Simbolo"].iloc[0]}')

    # Atualização e conversão do formato do preço
    update_queries = [
        f"UPDATE {table_name} SET [price] = REPLACE(REPLACE([price], '.', ''), ',', '.') WHERE [price] IS NOT NULL"
        for table_name in [f'Cotacao{name.title().replace("_", "")}' for name in dataframes.keys()]
    ]
    
    for query in update_queries:
        try:
            cursor.execute(query)
        except Exception as e:
            print(f"Erro ao executar a query: {query}\n{e}")

    convert_queries = [
        f"UPDATE {table_name} SET [price] = TRY_CAST([price] AS DECIMAL(10, 2))"
        for table_name in [f'Cotacao{name.title().replace("_", "")}' for name in dataframes.keys()]
    ]
    
    for query in convert_queries:
        try:
            cursor.execute(query)
        except Exception as e:
            print(f"Erro ao executar a query: {query}\n{e}")

    # Alteração das colunas para o tipo DECIMAL
    alter_queries = [
        f"ALTER TABLE Cotacao{name.title().replace('_', '')} ALTER COLUMN [price] DECIMAL(10, 2)"
        for name in dataframes.keys()
    ]
    
    for query in alter_queries:
        try:
            cursor.execute(query)
        except Exception as e:
            print(f"Erro ao executar a query: {query}\n{e}")

    conn.commit()
    conn.close()
    print('Fechou conexão')

if __name__ == "__main__":
    main()
