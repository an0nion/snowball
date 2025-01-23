import streamlit as st
import pickle
import numpy as np
import pandas as pd
import sklearn.preprocessing
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
# LabelEncoder coverts categorical data into numerical labels (numbers)
le = LabelEncoder()

st.logo("snow.svg")

df = pd.read_csv('credit.zip')
df.dropna(inplace = True)
df = df.drop(["log.annual.inc", "not.fully.paid"], axis=1)


# Load the .pkl model
@st.cache_resource  # Cache the model to avoid reloading on every app interaction
def load_model():
    with open("new_fico.pk1", "rb") as file:
        model = pickle.load(file)
    return model

model = load_model()

# Streamlit app title and description
st.title("Find your credit score with :primaryColor[snowball]")
st.caption("Want to know what your American credit score would be? Feel free to\
         fiddle around with this model!")
st.write("This machine learning model is trained off 10 key features regarding\
         one line of credit. As such, feel free to consider a single line of credit\
         while making this!")
st.caption("The FICO score, introduced in 1989 by the Fair Isaac Corporation, is\
          a widely used credit scoring system designed to assess \
         creditworthiness objectively. It ranges from 300 to 850, calculated \
         using factors like payment history, credit utilisation, and credit age\
         , amongst others. Its statistical distribution is typically right-skewed\
         , with the majority of scores clustering in the 670–739 range, \
         considered fair to good credit. High scores (740+) are less common, \
         representing excellent credit, while scores below 580, indicating poor \
         credit, are relatively rare.")


# Input fields for user data
# Adjust the inputs based on the model's features

def user_input_features():
    creditpolicy = 1
    genpurpose = st.selectbox(
    "What is the purpose of this loan?",
    ("Educational", "Credit Card", "Major Purchase", "Debt Consolidation", "Small Business", "Other")
    )
    if genpurpose == "Educational":
        purpose = "educational"
    elif genpurpose == "Credit Card":
        purpose = "credit_card"
    elif genpurpose == "Debt Consolidation":
        purpose = "debt_consolidation"
    elif genpurpose == "Major Purchase":
        purpose = "major_purchase"
    elif genpurpose == "Small Business":
        purpose = "small_business"
    else:
        purpose = "all_other"

    purpose = le.fit_transform(df["purpose"].astype(str))[0]

    int_rate = float(st.slider("Interest Rate (%)", 6, 22, 8)) / 100


    installment = st.slider("Whats the monthly installment of this loan?", 16, 940, 300)

    dti = st.slider("What is the debt to income ratio of this credit line?", 0, 30, 10)

    dayswcred = st.slider("How many days of credit history does this credit line have?", 180, 17600, 500)

    revol_bal = st.slider("What is the balance remaining in your loan?", 0, 1210000, 300000)

    revol_util = st.slider("What is your line utilisation rate as a percentage? (How much have you\
                            spend in comparison to your credit limit?)", 0, 119, 50)
    
    inq6ms = st.slider("How many creditor inquiries have you had in the last 6 months?", 0, 33, 4)

    delinq2 = st.slider("How many times have you been 30+ days overdue on a payment in the last 2 years?", 0, 13, 3)

    pub_rec = st.slider("How many derogatory public records do you have? (Bankruptcy filings, tax liens)", 0, 5, 0)

    return np.array([creditpolicy, purpose, int_rate, installment, dti, dayswcred, revol_bal, revol_util, inq6ms, delinq2, pub_rec])

# Get user inputs
input_features = user_input_features()

# Reshape input for the model
input_features = input_features.reshape(1, -1)  # Ensure input is 2D for sklearn models

# Make a prediction
if st.button("Predict"):
    prediction = model.predict(input_features)
    st.write("_Prediction Results!_")
    st.success(f"Your predicted credit score would be: {round(prediction[0])}")

