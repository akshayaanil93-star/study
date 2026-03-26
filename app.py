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
    
    # Clean Datetimes
    df_payment['payment_date'] = pd.to_datetime(df_payment['payment_date'])
    df_rental['rental_date'] = pd.to_datetime(df_rental['rental_date'])
    df_rental['return_date'] = pd.to_datetime(df_rental['return_date'])
    
    # Feature Engineering
    df_payment['payment_year_month'] = df_payment['payment_date'].dt.to_period('M').astype(str)
    df_rental['rental_duration_days'] = (df_rental['return_date'] - df_rental['rental_date']).dt.days
    
    # Merges
    df_master = pd.merge(df_payment, df_rental[['rental_id', 'rental_date', 'return_date', 'inventory_id', 'rental_duration_days']], on='rental_id', how='left')
    df_master = pd.merge(df_master, df_customer[['customer_id', 'first_name', 'last_name']], on='customer_id', how='left')
    df_master = pd.merge(df_master, df_inventory[['inventory_id', 'film_id']], on='inventory_id', how='left')
    df_master = pd.merge(df_master, df_film[['film_id', 'title', 'rating']], on='film_id', how='left')
    
    return df_payment, df_rental, df_master

df_payment, df_rental, df_master = load_and_prepare_data()

# --- DASHBOARD HEADER ---
st.title("🎬 Sakila DVD Rental Dashboard")
st.markdown("Interactive dashboard analyzing Sakila database revenue, rentals, and customer behaviors.")

# --- KPIs ---
total_revenue = df_payment['amount'].sum()
total_rentals = len(df_rental)
avg_payment = df_payment['amount'].mean()
unreturned_count = df_rental['return_date'].isna().sum()

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
    monthly_revenue = df_payment.groupby('payment_year_month')['amount'].sum().reset_index()
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    sns.barplot(data=monthly_revenue, x='payment_year_month', y='amount', color='steelblue', ax=ax1)
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Revenue ($)")
    plt.xticks(rotation=45)
    st.pyplot(fig1)

with colB:
    st.subheader("⭐ Rentals by Movie Rating")
    rating_counts = df_master['rating'].value_counts().reset_index()
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
    top_customers = df_master.groupby(['first_name', 'last_name'])['amount'].sum().sort_values(ascending=False).head(5).reset_index()
    top_customers['Customer'] = top_customers['first_name'] + " " + top_customers['last_name']
    st.dataframe(top_customers[['Customer', 'amount']].rename(columns={'amount': 'Total Revenue ($)'}), hide_index=True)

with colY:
    st.subheader("🔍 Recent Transactions")
    recent = df_master.sort_values(by='payment_date', ascending=False).head(10)
    st.dataframe(recent[['payment_date', 'first_name', 'last_name', 'amount', 'title']].rename(
        columns={'payment_date': 'Date', 'first_name': 'First Name', 'last_name': 'Last Name', 'amount': 'Amount', 'title': 'Movie Title'}
    ), hide_index=True)
