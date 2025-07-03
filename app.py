from src.mlproject.logger import logging
from src.mlproject.exception import CustomException
import os
import sys
from src.mlproject.components.data_ingestion import DataIngestion,DataIngestionConfig
from src.mlproject.components.data_transformation import DataTransformation
from src.mlproject.components.model_tranier import ModelTrainer





if __name__ == "__main__":
    logging.info("starting excution")
    try:
        Data_Ingestion = DataIngestion()
        train_path,test_path = Data_Ingestion.initaite_data_ingestion()
        data_transformation = DataTransformation()
        train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_path,test_path)
        model_trainer=ModelTrainer()
        model_trainer.initiate_model_trainer(train_arr,test_arr)

    except Exception as e:
        raise CustomException(e,sys)