from src.mlproject.logger import logging
from src.mlproject.exception import CustomException
import os
import sys
from src.mlproject.components.data_ingestion import DataIngestion,DataIngestionConfig





if __name__ == "__main__":
    logging.info("starting excution")
    try:
        Data_Ingestion = DataIngestion()
        Data_Ingestion.initaite_data_ingestion()

    except Exception as e:
        raise CustomException(e,sys)