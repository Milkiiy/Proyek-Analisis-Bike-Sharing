import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def load_data():
    sns.set(style='dark')

    # Season Labels for find Sumarize

    bike_all = pd.read_csv("/workspaces/Proyek-Analisis-Bike-Sharing/dashboard/bike_all.csv")
    season_labels = {
        1: 'Spring',
        2: 'Summer',
        3: 'Fall',
        4: 'Winter'
    }
    bike_all['season_labels'] = bike_all['season_x'].map(season_labels)
    bike_all.groupby('season_labels')['cnt_x'].sum().reset_index().sort_values('cnt_x')

    # Weather Labels for Find Sumarize

    weather_labels = {
        1: 'Clear, Few clouds, Partly cloudy, Partly cloudy',
        2: 'Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist',
        3: 'Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds',
        4: 'Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog'
    }
    bike_all['weather_labels'] = bike_all['weathersit_x'].map(weather_labels)
    bike_all.groupby('weather_labels')['cnt_x'].sum().reset_index().sort_values('cnt_x')

    # ===========================================

    datetime_columns = ["dteday"]
    for column in datetime_columns:
        bike_all[column] = pd.to_datetime(bike_all[column])

    min_date = bike_all["dteday"].min()
    max_date = bike_all["dteday"].max()

    return bike_all, min_date, max_date


def setup_sidebar(min_date, max_date):
    with st.sidebar:
        st.subheader('Bike Sharing')
        st.subheader('Rizky Andika Apriansyah m117b4ky3925')
        st.image("https://cdn.pixabay.com/photo/2012/04/28/19/26/bicycles-44154_960_720.png")
        
        selected_dates = st.date_input(
            label='Rentang Waktu Rental', min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )

    # Checking the date already inputed or no
        if len(selected_dates) != 2:
            raise ValueError("Masukkan rentang waktu yang lengkap. Mohon pilih kedua tanggal.")
        
        start_date, end_date = selected_dates
    return start_date, end_date

def filter_data(bike_sharing_df, start_date, end_date):
    main_df = bike_sharing_df[(bike_sharing_df["dteday"] >= str(start_date)) & 
                      (bike_sharing_df["dteday"] <= str(end_date))]
    return main_df

def show_header():
    st.header('Dashboard Analisis Data Bike Sharing')
    st.subheader('Daily Total User')

def show_user_metrics(main_df):
    total_user = main_df.cnt_x.sum()
    st.metric("Total user : ", value=total_user)

def show_graphic_1(main_df):
    st.subheader("Total Penyewaan Sepeda berdasarkan Musim")
    # Group the data by season labels and sum the total counts
    season_counts = main_df.groupby('season_labels')['cnt_x'].sum().reset_index()

    # Plotting
    plt.figure(figsize=(12, 6))

    # Create a bar plot for total counts by season with hue set to season_labels
    sns.barplot(x='season_labels', y='cnt_x', data=season_counts, hue='season_labels', palette='coolwarm', dodge=False)

    # Adding labels and title
    plt.title('Distribusi Total Penyewaan Sepeda berdasarkan Musim')
    plt.xlabel('Musim')
    plt.ylabel('Jumlah Penyewaan')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    st.pyplot(plt)

def show_graphic_2(main_df):
    st.subheader("Pengaruh Cuaca terhadap penyewaan sepeda")
    weather_counts = main_df.groupby('weather_labels')['cnt_x'].sum()

    plt.figure(figsize=(8,8))
    plt.pie(weather_counts, labels=weather_counts.index, autopct='%1.1f%%', colors=sns.color_palette('coolwarm', len(weather_counts)))
    plt.title('Distribusi Penyewaan Sepeda berdasarkan Cuaca')
    st.pyplot(plt)














def main():
    bike_sharing_df, min_date, max_date = load_data()
    start_date, end_date = setup_sidebar(min_date, max_date)
    main_df = filter_data(bike_sharing_df, start_date, end_date)
    show_header()
    show_user_metrics(main_df)
    show_graphic_1(main_df)
    show_graphic_2(main_df)


if __name__ == '__main__':
    main()