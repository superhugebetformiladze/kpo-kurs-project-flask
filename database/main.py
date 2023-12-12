from database_utils import create_database, database_exists
from tables_utils import drop_all_tables, create_tables
from generate_data import insert_services_data

import sys
import os
current_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(root_directory)

from utils.config_utils import get_db_config


if __name__ == "__main__":
    db_config = get_db_config()
    
    create_database(db_config)
    drop_all_tables()
    create_tables()
    insert_services_data(1)



