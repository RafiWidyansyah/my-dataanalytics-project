import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load Dataset
data = pd.read_csv("data_cleaned.csv")
data["date"] = pd.to_datetime(data["date"])

st.set_page_config(page_title="Bike-Sharing Dashboard",
                   page_icon="bar_chart:",
                   layout="wide")

# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'total_count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'total_count': 'sum'
    }).reset_index()
    return weekday_rent_df

# Create Filter Components
min_date = data['date'].min()
max_date = data['date'].max()

# SIDEBAR

with st.sidebar:
    st.sidebar.header("Filter:")
    start_date, end_date = st.date_input(
        label="Date Filter", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Link filter dengan data
main_data = data[(data["date"] >= str(start_date)) & (data["date"] <= str(end_date))]

# Menyiapkan berbagai dataframe
season_rent_df = create_season_rent_df(main_data)
monthly_rent_df = create_monthly_rent_df(main_data)
weekday_rent_df = create_weekday_rent_df(main_data)

# MAIN PAGE
st.title("Bike-Sharing Dashboard")
st.markdown("##")

col1, col2, col3 = st.columns(3)

with col1:
    total_all_riders = main_data['total_count'].sum()
    st.metric("Total Rides", value=total_all_riders)
with col2:
    total_casual_riders = main_data['casual'].sum()
    st.metric("Total Casual Rides", value=total_casual_riders)
with col3:
    total_registered_riders = main_data['registered'].sum()
    st.metric("Total Registered Rides", value=total_registered_riders)

# Membuat jumlah penyewaan bulanan
st.subheader('Monthly Rentals')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_rent_df.index,
    monthly_rent_df['total_count'],
    marker='o', 
    linewidth=2,
    color='tab:blue'
)

plt.xlabel("Month")
plt.ylabel("Total Rides")
plt.title("Total Bikeshare Rides by Month")

st.pyplot(fig)

# Membuat jumlah penyewaan berdasarkan season
st.subheader('Seasonly Rentals')

fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x='season',
    y='registered',
    data=season_rent_df,
    label='Registered',
    color='tab:blue',
    ax=ax
)

sns.barplot(
    x='season',
    y='casual',
    data=season_rent_df,
    label='Casual',
    color='tab:orange',
    ax=ax
)

plt.xlabel("Seasons")
plt.ylabel("Total Rides")
plt.title("Total Bikeshare Rides by Seasons")

st.pyplot(fig)

# Berdasarkan weekday
st.subheader('Weekday Rentals')

fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
  x='weekday',
  y='total_count',
  data=weekday_rent_df,
  color='tab:red',
  ax=ax
)

plt.xlabel("Weekday")
plt.ylabel("Total Rides")
plt.title("Total Bikeshare Rides by Weekday")

st.pyplot(fig)

st.caption('Copyright (c), created by Rafi Widyansyah')
