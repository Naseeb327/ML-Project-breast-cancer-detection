import pandas as pd
import pymysql
import os
import sys
from dotenv import load_dotenv
import pickle
from src.mlproject.logger import logging
from src.mlproject.exception import CustomException
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
load_dotenv()

host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
db = os.getenv("db")

def read_data_from_sql():
    try:
        logging.info("Connecting to SQL using pymysql...")
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db
        )
        logging.info("Connection successful.")

        # Step 1: Load data
        df = pd.read_sql("SELECT * FROM data", con=conn)
        logging.info(f"Raw shape: {df.shape}")
        logging.info(f"First few rows:\n{df.head(3)}")

        # Step 2: Use first row as header
        new_header = df.iloc[0].tolist()
        df = df[1:]
        df.columns = new_header
        logging.info(f"Columns renamed to: {df.columns.tolist()}")

        # Step 3: Remove any row that still contains string header values
        df = df[df["id"].str.lower() != "id"]

        # Step 4: Convert all types safely
        df["id"] = pd.to_numeric(df["id"], errors="raise").astype("int64")
        df["diagnosis"] = pd.to_numeric(df["diagnosis"], errors="raise").astype("int64")
        df[df.columns[2:]] = df[df.columns[2:]].astype("float64")

        logging.info("Final cleaned shape: %s", df.shape)
        return df

    except Exception as e:
        logging.error("❌ Error during SQL data cleanup", exc_info=True)
        raise CustomException(e, sys)


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    


def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)