from database_utils import create_database, database_exists
from tables_utils import drop_all_tables, create_tables
from generate_data import insert_services_data
from config_utils import get_db_config


if __name__ == "__main__":
    db_config = get_db_config()
    
    create_database(db_config)
    drop_all_tables(db_config)
    create_tables(db_config)
    insert_services_data(db_config, 10)



