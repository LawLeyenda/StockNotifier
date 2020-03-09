import sqlite3

conn = sqlite3.connect('stock.db')

c = conn.cursor()

sql_create_stocks_table = """CREATE TABLE IF NOT EXISTS Stock(
                                stock_name text PRIMARY KEY,
                                company_name text,
                                price real,
                                yesterday_close real,
                                pe_ratio real,
                                week52high real,
                                week52low real);"""
sql_create_stocks_news_table = """CREATE TABLE IF NOT EXISTS StockNews(
                                    stock_name text,
                                    Stock_new_id text PRIMARY KEY,
                                    Article text,
                                    url text,
                                    datetime text,
                                    FOREIGN KEY (stock_name) REFERENCES Stock (stock_name));"""
sql_create_analysts_table = """CREATE TABLE IF NOT EXISTS Analysts(
                                    last_updated text,
                                    analysts_id text PRIMARY KEY,
                                    priceTargetHigh real,
                                    priceTargetLow real,
                                    numberOfAnalysts real,
                                    stock_name text,
                                    FOREIGN KEY (stock_name) REFERENCES Stock (stock_name));"""
sql_create_user_notified_table = """CREATE TABLE IF NOT EXISTS UserNotified(
                                    last_updated text,
                                    UserNotified_id text PRIMARY KEY,
                                    notified_percent real,
                                    notified_time real,
                                    notified_price real,
                                    stock_name text,
                                    FOREIGN KEY (stock_name) REFERENCES Stock (stock_name));"""

# c.execute(sql_create_stocks_table)
# c.execute(sql_create_analysts_table)
# c.execute(sql_create_stocks_news_table)
# c.execute(sql_create_user_notified_table)

conn.commit()
conn.close()
