import os
import configparser

def get_db_config():
    # config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.cfg')
    config_path = 'D:\учебный\кпо\курсовая\kpo-kurs-flask\kpo-kurs-project-flask\config\config.cfg'
    config = configparser.ConfigParser()
    config.read(config_path)

    db_config = {
        'host': config.get('DATABASE', 'DB_HOST'),
        'database': config.get('DATABASE', 'DB_NAME'),
        'user': config.get('DATABASE', 'DB_USER'),
        'password': config.get('DATABASE', 'DB_PASSWORD')
    }

    return db_config
