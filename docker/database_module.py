import pymysql.cursors
import yaml

class DatabaseLogicClass():
    def __init__(self, SQLString, method):

        with open("./yaml/DBlist.yaml", 'r') as stream:
            self.DBLogin = yaml.load(stream)
        self.SQLString = SQLString
        self.result = ""
        _selector = {
            1: self.MySQLWriter,
            2: self.MySQLFetchOne,
            3: self.MySQLFetchAll,
        }

        _selector[method]()

    def MySQLWriter(self):
        """
        Запись данных в БД
        """
        DBLogin = self.DBLogin
        connection = pymysql.connect(host=DBLogin[0], port=DBLogin[1], user=DBLogin[2], password=DBLogin[3],
                                     db=DBLogin[4], cursorclass=pymysql.cursors.DictCursor, autocommit=False)
        try:
            cursor = connection.cursor()
            cursor.execute(self.SQLString)
        except pymysql.err.IntegrityError:
            print("Такой номер уже есть, скипаем")
        except:
            connection.rollback()
            connection.close()
            raise
        else:
            connection.commit()
            connection.close()

    def MySQLFetchOne(self):
        """
        Получение одного элемента БД
        """
        DBLogin = self.DBLogin
        connection = pymysql.connect(host=DBLogin[0], port=DBLogin[1], user=DBLogin[2], password=DBLogin[3],
                                     db=DBLogin[4], cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                cursor.execute(self.SQLString)
                result = cursor.fetchone()
        finally:
            connection.close()
        self.result = result

    def MySQLFetchAll(self):
        """
        Получение более одного элемента в БД
        """
        DBLogin = self.DBLogin
        connection = pymysql.connect(host=DBLogin[0], port=DBLogin[1], user=DBLogin[2], password=DBLogin[3],
                                     db=DBLogin[4], cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                cursor.execute(self.SQLString)
                result = cursor.fetchall()
        finally:
            connection.close()
        self.result = result