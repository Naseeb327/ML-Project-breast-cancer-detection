from src.mlproject.logger import logging
from src.mlproject.exception import CustomException
import os
import sys
from src.mlproject.components.data_ingestion import DataIngestion,DataIngestionConfig
from src.mlproject.components.data_transformation import DataTransformation





if __name__ == "__main__":
    logging.info("starting excution")
    try:
        Data_Ingestion = DataIngestion()
        train_path,test_path = Data_Ingestion.initaite_data_ingestion()
        data_transformation = DataTransformation()
        data_transformation.initiate_data_transformation(train_path,test_path)

    except Exception as e:
        raise CustomException(e,sys)