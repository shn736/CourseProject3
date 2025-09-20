from src.dbmanager import DBManager
from src.user_interface import user_interface

if __name__ == "__main__":
    db_manager = DBManager("courseproject3", "postgres", "191979")
    user_interface(db_manager)
    db_manager.close()
