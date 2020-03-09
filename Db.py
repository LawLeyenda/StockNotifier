import sqlite3


class Db:

    def __init__(self, database):
        self.conn = sqlite3.connect(database)

    def sql_insert_stock(self, entities):
        c = self.conn.cursor()
        c.execute(
            '''INSERT INTO Stock(stock_name,company_name,price,yesterday_close,pe_ratio,week52high,week52low) VALUES(?,?,?,?,?,?,?)''',
            entities)
        self.conn.commit()

    def sql_insert_stock_news(self, entities):
        c = self.conn.cursor()
        c.execute(
            '''INSERT INTO StockNews(stock_name,Stock_new_id,Article,url,datetime) VALUES(?,?,?,?,?)''',
            entities)
        self.conn.commit()

    def sql_insert_analysts(self, entities):
        c = self.conn.cursor()
        c.execute(
            '''INSERT INTO Analysts(last_updated,analysts_id,priceTargetHigh,priceTargetLow,numberOfAnalysts,stock_name) VALUES(?,?,?,?,?,?)''',
            entities)
        self.conn.commit()

    def sql_insert_user_notified(self, entities):
        c = self.conn.cursor()
        c.execute(
            '''INSERT INTO UserNotified(last_updated, UserNotified_id, notified_percent, notified_time, notified_price, stock_name) VALUES(?,?,?,?,?,?)''',
            entities)
        self.conn.commit()

    def sql_update(self, entities):
        c = self.conn.cursor()
        c.execute(
            '''UPDATE Stock SET stock_name = ? ,company_name = ?,price = ?,yesterday_close = ?, pe_ratio = ?, week52high = ?, week52low = ? WHERE stock_name = ?''',
            entities)
        self.conn.commit()

    def sql_fetch_one(self, *args):  #VULNERABLE TO SQL INJECTION! JUST USING FOR CONVENIENCE
        c = self.conn.cursor()
        statement = """SELECT %s FROM %s """ % args
        # c.execute("""SELECT * FROM Stock WHERE stock_name=?""", (stock_name,))
        c.execute(statement)
        rows = c.fetchone()
        return rows

    def sql_fetch_many(self, *args):  #VULNERABLE TO SQL INJECTION! JUST USING FOR CONVENIENCE
        c = self.conn.cursor()
        statement = """SELECT %s FROM %s """ % args
        # c.execute("""SELECT * FROM Stock WHERE stock_name=?""", (stock_name,))
        c.execute(statement)
        rows = c.fetchall()
        return rows #returns multidimensional list

    # attributes = ("BABA")
    # # sql_update(conn, entities )
    # # sql_insert(conn, entities1)
    # sql_fetch(conn, "AAPL")

    # conn.close()
