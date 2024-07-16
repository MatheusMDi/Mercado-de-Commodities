# Painel de Cotações

## Visão Geral

O **Painel de Cotações** é um projeto desenvolvido para centralizar e exibir cotações de diversas moedas e commodities em tempo real, proporcionando ao time de engenharia uma ferramenta eficiente para tomar decisões mais assertivas. Este painel pode ser exibido em uma TV ou monitor, mostrando os valores das cotações e gráficos de tendência ao longo do tempo.

## Objetivo do Projeto

O principal objetivo deste projeto é resolver a necessidade do time de engenharia de ter todas as cotações centralizadas em um único lugar, permitindo uma visão clara e consolidada das informações financeiras necessárias para suas operações. Isso é crucial para tomar decisões rápidas e informadas no mercado financeiro.

## Público-Alvo

Este projeto é destinado a todos os profissionais que utilizam informações financeiras de moedas e commodities para tomar decisões estratégicas, incluindo equipes de engenharia, analistas financeiros, traders e gestores de fundos.

## Funcionalidades

- **Centralização das Cotações**: Exibição de cotações atualizadas de diversas moedas e commodities.
- **Gráficos de Tendência**: Visualização de gráficos que mostram a variação dos valores ao longo do tempo.
- **Interface Responsiva**: Interface amigável e responsiva, adaptável para exibição em TVs, monitores e outros dispositivos.
- **Filtro de Data**: Possibilidade de filtrar as cotações por data específica.

## Tecnologias Utilizadas

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Banco de Dados**: SQL Server
- **Bibliotecas e Ferramentas**: ApexCharts (para gráficos), pyodbc (para conexão com SQL Server), requests, lxml, pandas, yfinance

## Estrutura do Projeto

- **app.py**: Arquivo principal que contém a aplicação Flask.
- **templates/**: Diretório que contém os arquivos HTML.
- **static/**: Diretório que contém os arquivos CSS e JavaScript.
- **data/**: Diretório que contém scripts Python para extração e manipulação de dados.

## Scripts na Pasta `data`

### Código 1: Extração de Dados de Commodities

Este script realiza a extração de dados históricos de diversas commodities a partir do site Investing. As informações extraídas são inseridas em tabelas correspondentes no banco de dados SQL Server.

```python
import requests
from lxml import html
import pandas as pd
import pyodbc

# URLs e símbolos para extração de dados
urls = [
    ("steel_rebar", "https://br.investing.com/commodities/steel-rebar-historical-data"),
    ...
]

def extract_data(url):
    ...
    
def insert_df_to_sql(df_final, table_name, cursor):
    ...

def truncate_table(table_name, cursor):
    ...

def create_dataframe(name, data):
    ...

def main():
    ...
    
if __name__ == "__main__":
    main()
```

### Código 2: Obtenção de Cotações de Moedas

Este script utiliza a biblioteca yfinance para obter cotações de moedas específicas, processa os dados e insere ou atualiza as informações no banco de dados.

```python
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import pyodbc

# Funções
def get_cotacao(ticker, dt_inicial, dt_final):
    ...

def upsert_df_to_sql(df, table_name, cursor):
    ...

def prepare_dataframes(tickers, symbols, dt_inicial, dt_final):
    ...

def main():
    ...
    
if __name__ == "__main__":
    main()
```

## Configuração e Instalação

### Pré-requisitos

- Python 3.x
- SQL Server
- Ambiente virtual (opcional, mas recomendado)

### Passos para Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/MatheusMDi/Mercado-de-Commodities.git
   cd painel-de-cotacoes
   ```

2. Crie e ative um ambiente virtual (opcional):
   ```bash
   python -m venv venv
   source venv/bin/activate # Linux/Mac
   .\venv\Scripts\activate # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure a conexão com o banco de dados no arquivo `config.py`.

5. Execute a aplicação:
   ```bash
   python app.py
   ```

## Criação do Banco de Dados

### Script de Criação das Tabelas

data\create.sql

## Uso

Após a instalação e configuração, acesse a aplicação via navegador em `http://localhost:5000`. Utilize o painel para visualizar as cotações em tempo real e os gráficos de tendência.

## Contribuição

Se desejar contribuir para este projeto, por favor, siga os passos abaixo:

1. Faça um fork deste repositório.
2. Crie uma branch para suas modificações (`git checkout -b minha-modificacao`).
3. Commit suas alterações (`git commit -m 'Adiciona minha modificação'`).
4. Envie para a branch (`git push origin minha-modificacao`).
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Sinta-se à vontade para ajustar qualquer parte do README de acordo com suas necessidades!