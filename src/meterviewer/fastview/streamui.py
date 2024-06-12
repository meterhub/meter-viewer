import streamlit as st
import pandas as pd
import numpy as np
from meterviewer.config import get_root_path


def our_app():
    st.title("Quick Viewer of Meterdata")
    root_path = get_root_path()
    path = st.text_input("Enter the path of the data", value="generated_merged")
    num = st.text_input("Enter the number of data")
    x_name = st.text_input("Enter the value of x_name", value="x_test.npy")
    y_name = st.text_input("Enter the value of y_name", value="y_test.npy")

    try:
        data_load_state = st.text("reading data...")
        num = int(num)
        data_load_state.text("Done!")
    except ValueError:
        data_load_state.text("Please enter a number")
        return

    folder_path = root_path / path
    x_path = folder_path / x_name
    y_path = folder_path / y_name

    x = np.load(x_path)
    y = np.load(y_path)

    st.image(x[num], caption=f"Meterdata {num}")
    st.text(f"Meterdata {num} is {y[num]}")


def example():
    st.title("Uber pickups in NYC")
    DATE_COLUMN = "date/time"
    DATA_URL = (
        "https://s3-us-west-2.amazonaws.com/"
        "streamlit-demo-data/uber-raw-data-sep14.csv.gz"
    )

    @st.cache_data
    def load_data(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis="columns", inplace=True)
        data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
        return data

    data_load_state = st.text("Loading data...")
    data = load_data(10000)
    data_load_state.text("Done! (using st.cache_data)")

    if st.checkbox("Show raw data"):
        st.subheader("Raw data")
        st.write(data)

    st.subheader("Number of pickups by hour")
    hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
    st.bar_chart(hist_values)

    # Some number in the range 0-23
    hour_to_filter = st.slider("hour", 0, 23, 17)
    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

    st.subheader("Map of all pickups at %s:00" % hour_to_filter)
    st.map(filtered_data)


our_app()
