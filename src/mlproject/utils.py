import pandas as pd
from src.mlproject.logger import logging
from src.mlproject.exception import CustomException
from dotenv import load_dotenv
import os
import sys
import pymysql 
load_dotenv()

host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
db = os.getenv("db")

def read_data_from_sql():
    try:
        logging.info("start reading from sql")
        mydb = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db
        )
        logging.info("connection is created successfully {mydb}",)
        df = pd.read_sql_query("Select * from data",mydb)
        logging.info("successfully convert sql data to df")
        return df
    except Exception as e:
        raise CustomException(e,sys)