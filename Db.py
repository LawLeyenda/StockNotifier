import sqlite3
import datetime
import re


class Db:

    def __init__(self, database):
        self.conn = sqlite3.connect(database, check_same_thread=False) # shares connection among multiple threads

    def sql_insert_stock(self, entities):
        c = self.conn.cursor()
        c.execute(
            '''INSERT INTO Stock(stock_name,company_name,price,yesterday_close,pe_ratio,week52high,week52low) VALUES(?,?,?,?,?,?,?)''',
            entities)
        self.conn.commit()

    def sql_user_notified(self, entities):
        c = self.conn.cursor()
        c.execute(
            '''INSERT INTO Stock(last_updated,stock,price,yesterday_close,pe_ratio,week52high,week52low) VALUES(?,?,?,?,?,?,?)''',
            entities)
        self.conn.commit()

    def sql_delete_stock(self, stock):
        c = self.conn.cursor()
        c.execute(
            '''DELETE from Stock WHERE stock_name = %s''' % stock)
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
            '''INSERT INTO UserNotified(last_updated, UserNotified_id, notified_percent, notified_time, notified_price, stock_name, is_user_notified) VALUES(?,?,?,?,?,?,?)''',
            entities)
        self.conn.commit()

    def sql_insert_stock_news(self, entities): #interns news article if it doesnt already exist
        c = self.conn.cursor()
        c.execute(
            '''INSERT or IGNORE INTO StockNews(stock_name, article_used, Article, url, datetime, summary) VALUES(?,?,?,?,?,?) ''',
            entities)
        self.conn.commit()

    def sql_update(self, entities):
        c = self.conn.cursor()
        c.execute(
            '''UPDATE Stock SET stock_name = ? ,company_name = ?,price = ?,yesterday_close = ?, pe_ratio = ?, week52high = ?, week52low = ? WHERE stock_name = ?''',
            entities)
        self.conn.commit()

    def sql_update_open(self, *args): #VULNERABLE TO SQL INJECTION! JUST USING FOR CONVENIENCE
        #open to write whatever i want
        c = self.conn.cursor()
        c.execute(
            '''UPDATE %s SET %s''' % args)
        self.conn.commit()

    def sql_fetch_one(self, *args):  #VULNERABLE TO SQL INJECTION! JUST USING FOR CONVENIENCE
        c = self.conn.cursor()
        statement = """SELECT %s FROM %s """ % args
        # c.execute("""SELECT * FROM Stock WHERE stock_name=?""", (stock_name,))
        c.execute(statement)
        rows = c.fetchone()
        if rows is None:
            return None
        return rows[0] #they return tuples

    def sql_fetch_many(self, *args):  #VULNERABLE TO SQL INJECTION! JUST USING FOR CONVENIENCE
        c = self.conn.cursor()
        statement = """SELECT %s FROM %s """ % args
        # c.execute("""SELECT * FROM Stock WHERE stock_name=?""", (stock_name,))
        c.execute(statement)
        rows = c.fetchall()
        return rows #returns multidimensional list

    def stock_list(self):  # stock list of db
        list = self.sql_fetch_many("stock_name", "stock")
        str_list = str(list).strip("\n")
        my_list = re.findall(r"\('(.*?)',\)", str_list)
        return my_list

    def close_now(self):
        self.conn.close()

    # attributes = ("BABA")
    # # sql_update(conn, entities )
    # # sql_insert(conn, entities1)
    # sql_fetch(conn, "AAPL")

