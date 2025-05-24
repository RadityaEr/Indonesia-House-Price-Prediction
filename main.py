import streamlit as st
import house_utility_pred  # Import first file
import price_prediction  # Import second file

st.set_page_config(page_title="House Price Models", layout="wide", page_icon=":house:")
st.title("Raditya Erlang Arkananta - ML Portfolio")
st.header("Predictive Models for Housing Market")

# Create only 2 tabs
tabs = st.tabs(["🏠 Predict House Price", "📉 Buying House Prediction"])

with tabs[0]:
    st.subheader("🏠 Predict House Price")
    st.markdown("This section will demonstrate a regression model that predicts house prices based on various features such as location, size, and amenities.")
    # Call the content from price_prediction.py
    price_prediction.main() 

with tabs[1]:
    st.subheader("📉 Buying House Prediction")
    st.markdown("This section will present a classification model to predict whether a user is likely to buy a house based on demographic and behavioral data.")
    # Call the content from house_utility_pred.py
    house_utility_pred.main()  # Assuming 'main()' is the function that runs the model
