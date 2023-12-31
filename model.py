# -*- coding: utf-8 -*-
"""ready to deploy (pipeline).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1o7X4HUFJr7Lu_6JcrWgKsXToSq6WNsIg
"""

!pip install jcopml

#Import Library
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score

#Import Dataset
from google.colab import drive
drive.mount('/content/drive')
df = pd.read_csv("/content/drive/MyDrive/Dataset TA/LoanData_Bondora.csv")

attr = ['NrOfDependants','Age','Gender','Restructured','UseOfLoan','VerificationType','EmploymentStatus','DebtToIncome','HomeOwnershipType','AppliedAmount','IncomeTotal','Rating_V2']
df = df[attr]
df['NrOfDependants'] = pd.to_numeric(df['NrOfDependants'], errors='coerce')

# Fill 'Restructured' Missing Value with Mode
df['Restructured'] = df['Restructured'].fillna(df['Restructured'].mode()[0])

# Fill 'NrOfDependants' Missing Value with Mode
df['NrOfDependants'] = df['NrOfDependants'].fillna(df['NrOfDependants'].mode()[0])

# Fill 'Gender' Missing Value with Mode
df['Gender'] = df['Gender'].fillna(df['Gender'].mode()[0])

# Fill 'VerificationType' Missing Value with Mode
df['VerificationType'] = df['VerificationType'].fillna(df['VerificationType'].mode()[0])

# Fill 'EmploymentStatus' Missing Value with Mode
df['EmploymentStatus'] = df['EmploymentStatus'].fillna(df['EmploymentStatus'].mode()[0])

# Fill 'DebtToIncome' Missing Value with Mode
df['DebtToIncome'] = df['DebtToIncome'].fillna(df['DebtToIncome'].mode()[0])

# Fill 'HomeOwnershipType' Missing Value with Mode
df['HomeOwnershipType'] = df['HomeOwnershipType'].fillna(df['HomeOwnershipType'].mode()[0])

# Fill 'Rating_V2' Missing Value with Mode
df['Rating_V2'] = df['Rating_V2'].fillna(df['Rating_V2'].mode()[0])

# Change Datatype to Integer
df[['Age','Gender','Restructured','UseOfLoan','VerificationType','EmploymentStatus','HomeOwnershipType','NrOfDependants']] = df[['Age','Gender','Restructured','UseOfLoan','VerificationType','EmploymentStatus','HomeOwnershipType', 'NrOfDependants']].astype('Int64')

df.info()

# Convert dataset to csv
df.to_csv("/content/drive/MyDrive/Dataset TA/dataset.csv", index=False)
df = pd.read_csv("/content/drive/MyDrive/Dataset TA/dataset.csv")

# Splitting dataset to X and y
X = df.drop(columns="Rating_V2")
y = df.Rating_V2

X.info()

from sklearn.model_selection import train_test_split

# Split to 80% training data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.naive_bayes import GaussianNB

# Create pipeline for numerical
numerical_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ])

# Create column transform
transform = ColumnTransformer([
    ('numerical', numerical_pipeline, X.columns)
])

# Create pipeline for algorithm
pipeline = Pipeline([
    ('prep', transform),
    ('algo', GaussianNB()),
])
# Fit Transform X_train and y_train
pipeline.fit(X_train,y_train)

# Prediction
y_pred = pipeline.predict(X_test)

# Evaluation
print(pipeline.score(X_train,y_train), pipeline.score(X_test,y_test))

from jcopml.utils import save_model

save_model(pipeline, "model.pkl")