import os
import sys
from src.mlproject.logger import logging
from src.mlproject.exception import CustomException
from src.mlproject.utils import read_data_from_sql
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
import pandas as pd
@dataclass
class DataIngestionConfig:
    raw_data_path = os.path.join("Artifacts","raw_data.csv")
    train_data_path = os.path.join("Artifacts","train_data.csv")
    test_data_path = os.path.join("Artifacts","test_data.csv")

class DataIngestion:
    def __init__(self):
        self.IngestionConfig_path = DataIngestionConfig()

    def initaite_data_ingestion(self):
        try:
            logging.info("starting data initaite func")

            # df = read_data_from_sql() if want read data from database

            df = pd.read_csv(os.path.join("Artifacts","raw_data.csv"))
            logging.info(" data reading from sql is completed")
            os.makedirs(os.path.dirname(self.IngestionConfig_path.raw_data_path),exist_ok=True)
            
            df.to_csv(self.IngestionConfig_path.raw_data_path,header=True,index=False)

            train_data,test_data = train_test_split(df,test_size=0.2,random_state=42)

            train_data.to_csv(self.IngestionConfig_path.train_data_path, index=False, header=True)
            test_data.to_csv(self.IngestionConfig_path.test_data_path, index=False, header=True)


            logging.info("completing data ingestion part")
            return(
                self.IngestionConfig_path.train_data_path,
                self.IngestionConfig_path.test_data_path
            )


        except Exception as e:
            raise CustomException(e,sys)