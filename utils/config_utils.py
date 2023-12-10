import os
import configparser


def get_db_config():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(current_directory, '..', 'config', 'config.cfg')

    config = configparser.ConfigParser()
    config.read(config_path)

    db_config = {
        'host': config.get('DATABASE', 'DB_HOST'),
        'database': config.get('DATABASE', 'DB_NAME'),
        'user': config.get('DATABASE', 'DB_USER'),
        'password': config.get('DATABASE', 'DB_PASSWORD')
    }

    return db_config
