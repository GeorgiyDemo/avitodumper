import pymysql.cursors
import yaml

class mysql_writer():
    def __init__(self, sql_string, method):
        with open("./yaml/DBlist.yaml", 'r') as stream:
            self.DBLogin = yaml.load(stream)
        self.sql_string = sql_string
        self.result = ""
        _selector = {
            1: self.mysql_writer,
            2: self.mysql_fetchone,
            3: self.mysql_fetchall,
        }
        _selector[method]()

    def mysql_writer(self):
        """
        Запись данных в БД
        """
        DBLogin = self.DBLogin
        connection = pymysql.connect(host=DBLogin[0], port=DBLogin[1], user=DBLogin[2], password=DBLogin[3],
                                     db=DBLogin[4], cursorclass=pymysql.cursors.DictCursor, autocommit=False)
        try:
            cursor = connection.cursor()
            cursor.execute(self.sql_string)
        except pymysql.err.IntegrityError:
            pass
        except:
            connection.rollback()
            connection.close()
            raise
        else:
            connection.commit()
            connection.close()

    def mysql_fetchone(self):
        """
        Получение одного элемента БД
        """
        DBLogin = self.DBLogin
        connection = pymysql.connect(host=DBLogin[0], port=DBLogin[1], user=DBLogin[2], password=DBLogin[3],
                                     db=DBLogin[4], cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                cursor.execute(self.sql_string)
                result = cursor.fetchone()
        finally:
            connection.close()
        self.result = result

    def mysql_fetchall(self):
        """
        Получение более одного элемента в БД
        """
        DBLogin = self.DBLogin
        connection = pymysql.connect(host=DBLogin[0], port=DBLogin[1], user=DBLogin[2], password=DBLogin[3],
                                     db=DBLogin[4], cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                cursor.execute(self.sql_string)
                result = cursor.fetchall()
        finally:
            connection.close()
        self.result = result