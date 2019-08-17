import yaml


def get_settings():
    """
        Функция для чтения конфигов с yaml
    """
    with open("./settings.yml", 'r') as stream:
        return yaml.safe_load(stream)