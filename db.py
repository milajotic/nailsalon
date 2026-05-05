import os
import mariadb
from dotenv import load_dotenv
 
load_dotenv()  #Load .env file
 
def get_connection():
    return mariadb.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )