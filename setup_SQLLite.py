import sqlite3


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

conn = sqlite3.connect('stock.db')

conn.commit()  # saves all the changes made


def sql_insert(conn, entities):
    c = conn.cursor()

    c.execute(
        '''INSERT INTO Stock(stock_name,company_name,price,yesterday_close,pe_ratio,week52high,week52low) VALUES(?,?,?,?,?,?,?)''',
        entities)

    conn.commit()


entities = ("BABA", None, 1234, None, None, None, None, "BABA")
entities1 = ("MMM", None, 1234, None, None, None, None)


def sql_update(conn, entities):
    c = conn.cursor()
    c.execute(
        '''UPDATE Stock SET stock_name = ? ,company_name = ?,price = ?,yesterday_close = ?, pe_ratio = ?, week52high = ?, week52low = ? WHERE stock_name = ?''',
        entities)

    conn.commit()


def sql_fetch(conn, *args): #
    c = conn.cursor()
    statement="""SELECT %s FROM %s""" % (table ,args)
    #c.execute("""SELECT * FROM Stock WHERE stock_name=?""", (stock_name,))

    rows = c.fetchone()
    return rows


attributes = ("BABA")
# sql_update(conn, entities )
# sql_insert(conn, entities1)
sql_fetch(conn, "AAPL")

# conn.close()
