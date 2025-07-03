import sys
import os
import pandas as pd
import numpy as np
from src.mlproject.logger import logging
from src.mlproject.exception import CustomException
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from dataclasses import dataclass
from src.mlproject.utils import save_object

@dataclass
class DataTransformationConfig:
    transformation_obj_path = os.path.join("Artifacts",'preprocesser.pkl')

class DataTransformation():
    def __init__(self):
        self.transformation_obj_config = DataTransformationConfig()


    def get_data_transformation_obj(self):
        """This function is responsible for creating preprocessing obj"""
        try:
            logging.info("start creating preprocesser obj")
            pipeline = Pipeline([
                ("imputer",SimpleImputer(strategy='median')),
                ('scaler', StandardScaler()),
                ('pca', PCA(n_components=0.95))
            ])
            logging.info("Numerical-only transformation pipeline created.")

            return pipeline
        except Exception as e:
            raise CustomException(e,sys)
        


    def initiate_data_transformation(self,train_path,test_path):
        try:
            logging.info("data initiate transformation is started")
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            preprocessing_obj = self.get_data_transformation_obj()
            target_column = ["diagnosis"]
            drop_coloumn = ["diagnosis","id"]

            train_input_feature = train_df.drop(drop_coloumn,axis=1)
            train_target_feature = train_df[target_column]

            test_input_feature = test_df.drop(drop_coloumn,axis=1)
            test_target_feature = test_df[target_column]

            train_input_feature_arr = preprocessing_obj.fit_transform(train_input_feature)
            test_input_feature_arr = preprocessing_obj.transform(test_input_feature)

            train_arr = np.c_[train_input_feature_arr,np.array(train_target_feature)]
            test_arr = np.c_[test_input_feature_arr,np.array(test_target_feature)]

            logging.info("data transformation is completed")

            save_object(
                file_path=self.transformation_obj_config.transformation_obj_path,
                obj=preprocessing_obj
            )
            
            return(
                train_arr,
                test_arr,
                self.transformation_obj_config.transformation_obj_path
            )
        

        except Exception as e:
            raise CustomException(e,sys)