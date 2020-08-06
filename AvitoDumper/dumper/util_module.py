import yaml

OUT_FILE = "./out/OUTPUT.txt"


class GetSettings(object):
    """
        Класс для чтения конфигов с yaml
    """

    def __init__(self):
        self.get_settings()

    def get_settings(self):
        with open("./settings.yml", "r") as stream:
            self.config = yaml.safe_load(stream)


class TxtWorker(object):
    """
        Класс для вывода данных в обычный файл txt
    """

    def __init__(self, flag, result):
        self.result = result
        _selector = {
            "get": self.get_txtwork,
            "set": self.set_txtwork,
        }
        _selector[flag]()

    def get_txtwork(self):
        f = open(OUT_FILE, "w")
        f.close()

    def set_txtwork(self):
        f = open(OUT_FILE, "a")
        f.write(self.result)
        f.close()
