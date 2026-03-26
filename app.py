import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Sakila DVD Rental Dashboard", layout="wide")
sns.set_theme(style="whitegrid")

# Cache data loading so it doesn't run on every interaction
@st.cache_data
def load_and_prepare_data():
    # Load required CSVs
    df_payment = pd.read_csv('payment.csv')
    df_rental = pd.read_csv('rental.csv')
    df_customer = pd.read_csv('customer.csv')
    df_inventory = pd.read_csv('inventory.csv')
    df_film = pd.read_csv('film.csv')
    df_category = pd.read_csv('category.csv')
    df_film_category = pd.read_csv('film_category.csv')
    df_address = pd.read_csv('address.csv')
    df_city = pd.read_csv('city.csv')
    df_country = pd.read_csv('country.csv')
    
    # Clean Datetimes
    df_payment['payment_date'] = pd.to_datetime(df_payment['payment_date'])
    df_rental['rental_date'] = pd.to_datetime(df_rental['rental_date'])
    df_rental['return_date'] = pd.to_datetime(df_rental['return_date'])
    
    # Feature Engineering
    df_payment['payment_year_month'] = df_payment['payment_date'].dt.to_period('M').astype(str)
    df_payment['payment_year'] = df_payment['payment_date'].dt.year
    df_rental['rental_duration_days'] = (df_rental['return_date'] - df_rental['rental_date']).dt.days
    
    # Merges
    df_master = pd.merge(df_payment, df_rental[['rental_id', 'rental_date', 'return_date', 'inventory_id', 'rental_duration_days']], on='rental_id', how='left')
    df_master = pd.merge(df_master, df_customer[['customer_id', 'first_name', 'last_name', 'address_id']], on='customer_id', how='left')
    df_master = pd.merge(df_master, df_inventory[['inventory_id', 'film_id']], on='inventory_id', how='left')
    df_master = pd.merge(df_master, df_film[['film_id', 'title', 'rating']], on='film_id', how='left')
    df_master = pd.merge(df_master, df_film_category[['film_id', 'category_id']], on='film_id', how='left')
    df_master = pd.merge(df_master, df_category[['category_id', 'name']], on='category_id', how='left').rename(columns={'name': 'category'})
    df_master = pd.merge(df_master, df_address[['address_id', 'city_id']], on='address_id', how='left')
    df_master = pd.merge(df_master, df_city[['city_id', 'country_id']], on='city_id', how='left')
    df_master = pd.merge(df_master, df_country[['country_id', 'country']], on='country_id', how='left').rename(columns={'country': 'region'})
    
    return df_payment, df_rental, df_master

df_payment, df_rental, df_master = load_and_prepare_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Results")

years = ['All'] + sorted(df_master['payment_year'].dropna().unique().tolist())
selected_year = st.sidebar.selectbox("Select Year", years)

categories = ['All'] + sorted(df_master['category'].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", categories)

regions = ['All'] + sorted(df_master['region'].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Select Region", regions)

filtered_master = df_master.copy()
if selected_year != 'All':
    filtered_master = filtered_master[filtered_master['payment_year'] == selected_year]
if selected_category != 'All':
    filtered_master = filtered_master[filtered_master['category'] == selected_category]
if selected_region != 'All':
    filtered_master = filtered_master[filtered_master['region'] == selected_region]

# Filter base dataframes based on the master's filtered IDs
filtered_payment = df_payment[df_payment['payment_id'].isin(filtered_master['payment_id'])]
filtered_rental = df_rental[df_rental['rental_id'].isin(filtered_master['rental_id'])]

# --- DASHBOARD HEADER ---
st.title("🎬 Sakila DVD Rental Dashboard")
st.markdown("Interactive dashboard analyzing Sakila database revenue, rentals, and customer behaviors.")

# --- KPIs ---
total_revenue = filtered_payment['amount'].sum()
total_rentals = len(filtered_rental)
avg_payment = filtered_payment['amount'].mean() if not filtered_payment.empty else 0.0
unreturned_count = filtered_rental['return_date'].isna().sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Rentals", f"{total_rentals:,}")
col3.metric("Avg. Payment", f"${avg_payment:,.2f}")
col4.metric("Active Rentals (Unreturned)", f"{unreturned_count:,}")

st.divider()

# --- MAIN CHARTS ---
colA, colB = st.columns(2)

with colA:
    st.subheader("📈 Monthly Revenue Trend")
    monthly_revenue = filtered_payment.groupby('payment_year_month')['amount'].sum().reset_index()
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    sns.barplot(data=monthly_revenue, x='payment_year_month', y='amount', color='steelblue', ax=ax1)
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Revenue ($)")
    plt.xticks(rotation=45)
    st.pyplot(fig1)

with colB:
    st.subheader("⭐ Rentals by Movie Rating")
    rating_counts = filtered_master['rating'].value_counts().reset_index()
    rating_counts.columns = ['rating', 'rental_count']
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.barplot(data=rating_counts, x='rating', y='rental_count', palette='viridis', ax=ax2)
    ax2.set_xlabel("Film Rating")
    ax2.set_ylabel("Rental Count")
    st.pyplot(fig2)

st.divider()

# --- TOP CUSTOMERS ---
colX, colY = st.columns([1, 2])
with colX:
    st.subheader("🏆 Top 5 Customers by Revenue")
    top_customers = filtered_master.groupby(['first_name', 'last_name'])['amount'].sum().sort_values(ascending=False).head(5).reset_index()
    top_customers['Customer'] = top_customers['first_name'] + " " + top_customers['last_name']
    st.dataframe(top_customers[['Customer', 'amount']].rename(columns={'amount': 'Total Revenue ($)'}), hide_index=True)

with colY:
    st.subheader("🔍 Recent Transactions")
    recent = filtered_master.sort_values(by='payment_date', ascending=False).head(10)
    st.dataframe(recent[['payment_date', 'first_name', 'last_name', 'amount', 'title']].rename(
        columns={'payment_date': 'Date', 'first_name': 'First Name', 'last_name': 'Last Name', 'amount': 'Amount', 'title': 'Movie Title'}
    ), hide_index=True)
