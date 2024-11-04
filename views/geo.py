import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Load the dataset using Pandas
@st.cache_data
def load_data():
    data_path = r'data\\geography.csv'  # Update with your actual file path
    df = pd.read_csv(data_path)
    return df

# Preprocess data function
def preprocess_data(df):
    df = df.dropna(subset=['lon', 'lat', 'SALE_PRICE'])  # Drop rows with NaN in critical columns
    return df

# Predict population density using a machine learning model
def predict_population_density(X):
    # Create a sample dataset for training
    data = pd.DataFrame({
        'lon': np.random.rand(100) * 100,
        'lat': np.random.rand(100) * 100,
        'year': np.random.randint(2000, 2021, size=100),
        'population_density': np.random.rand(100) * 1000
    })
    
    X_train, X_test, y_train, y_test = train_test_split(data[['lon', 'lat', 'year']], data['population_density'], test_size=0.2, random_state=42)
    
    # Build the model
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    
    # Predict for the provided input
    prediction = model.predict(X)
    return prediction

# Streamlit app
def app():
    st.title("Geospatial Data Visualization and Analysis with AI")
    
    df = load_data()
    
    st.write(f"Total rows in dataset: {len(df)}")
    
    df = preprocess_data(df)
    
    year = st.slider("Select Year:", 2000, 2030, 2020)
    
    st.subheader(f"Geospatial Data for the Year {year}")
    filtered_df = df[df['YEAR_BUILT'] == year]  
    if not filtered_df.empty:
        layer = pdk.Layer(
            "ScatterplotLayer",
            filtered_df[['lon', 'lat']],
            get_position=["lon", "lat"],
            get_radius=10000,
            get_color=[255, 0, 0],
            pickable=True,
        )

        view_state = pdk.ViewState(
            latitude=filtered_df['lat'].mean(),
            longitude=filtered_df['lon'].mean(),
            zoom=10,
            pitch=50,
        )

        deck = pdk.Deck(layers=[layer], initial_view_state=view_state)
        st.pydeck_chart(deck)
    else:
        st.write("No data available for the selected year.")

    st.subheader("Population Density Prediction")
    lon = st.number_input("Enter Longitude:", value=0.0)
    lat = st.number_input("Enter Latitude:", value=0.0)
    
    if st.button("Predict Population Density"):
        prediction = predict_population_density(pd.DataFrame({'lon': [lon], 'lat': [lat], 'year': [year]}))
        st.write(f"Predicted Population Density: {prediction[0]}")

    st.sidebar.header("Filters")
    min_price, max_price = st.sidebar.slider("Select Sale Price Range:", 0, 10000000, (0, 1000000))
    filtered_data = df[(df['SALE_PRICE'] >= min_price) & (df['SALE_PRICE'] <= max_price)]
    
    st.write(f"Filtered Data based on Sale Price Range: {min_price} - {max_price}")
    st.write(filtered_data.head())
