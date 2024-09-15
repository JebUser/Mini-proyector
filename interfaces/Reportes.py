import streamlit as st
from connection import connect
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


dia, semana, mes, año = st.tabs(["1D", "1W", "1M", "1Y"])

#Fetch daily data
def fetch_yearly_revenue():
    query = """
    SELECT v.NroVenta, v.Fecha, c.Nombre, SUM(p.precio * pv.Cantidad) AS total_venta
    FROM venta v
    JOIN Cliente c ON v.ID_Cliente = c.Cedula
    JOIN prod_venta pv ON v.NroVenta = pv.NroVenta
    JOIN productos p ON pv.ID_Producto = p.id
    WHERE v.Fecha >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
    GROUP BY v.NroVenta, v.Fecha, c.Nombre;
    """
    return connect.query(query)

# Fetch monthly data
def fetch_monthly_revenue():
    query = """
    SELECT v.NroVenta, v.Fecha, c.Nombre, SUM(p.precio * pv.Cantidad) AS total_venta
    FROM venta v
    JOIN Cliente c ON v.ID_Cliente = c.Cedula
    JOIN prod_venta pv ON v.NroVenta = pv.NroVenta
    JOIN productos p ON pv.ID_Producto = p.id
    WHERE v.Fecha >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
    GROUP BY v.NroVenta, v.Fecha, c.Nombre;
    """
    return connect.query(query)

#Fetch weekly data
def fetch_weekly_revenue():
    query = """
    SELECT v.NroVenta, v.Fecha, c.Nombre, SUM(p.precio * pv.Cantidad) AS total_venta
    FROM venta v
    JOIN Cliente c ON v.ID_Cliente = c.Cedula
    JOIN prod_venta pv ON v.NroVenta = pv.NroVenta
    JOIN productos p ON pv.ID_Producto = p.id
    WHERE v.Fecha >= DATE_SUB(CURDATE(), INTERVAL 1 WEEK)
    GROUP BY v.NroVenta, v.Fecha, c.Nombre;
    """
    return connect.query(query)

#Fetch daily data
def fetch_daily_revenue():
    query = """
    SELECT v.NroVenta, v.Fecha, c.Nombre, SUM(p.precio * pv.Cantidad) AS total_venta
    FROM venta v
    JOIN Cliente c ON v.ID_Cliente = c.Cedula
    JOIN prod_venta pv ON v.NroVenta = pv.NroVenta
    JOIN productos p ON pv.ID_Producto = p.id
    WHERE v.Fecha = CURDATE()
    GROUP BY v.NroVenta, v.Fecha, c.Nombre;
    """
    return connect.query(query)

with dia:
    st.header("Reporte diario")
    # Fetch data for the last day
    df = fetch_daily_revenue()

    # Calculate total revenue for the week
    total_revenue = df['total_venta'].sum()

     # Display key metrics
    col1, col2 = st.columns(2)
    col1.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
    col2.metric(label="Total Sales", value=f"{df.shape[0]} sales")

with semana:
    st.header("Reporte semanal")
    # Fetch data for the last week
    df = fetch_weekly_revenue()

    # Verifica si el DataFrame no está vacío
    
    # Convert 'Fecha' to datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'])

    # Calculate total revenue for the week
    total_revenue = df['total_venta'].sum()

    # Display key metrics
    col1, col2 = st.columns(2)
    col1.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
    col2.metric(label="Total Sales", value=f"{df.shape[0]} sales")

    if not df.empty:
        # Display the data as a table
        st.subheader("Weekly Sales")
        st.dataframe(df[['Fecha', 'Nombre', 'total_venta']])

        # Prepare data for the line chart (aggregate sales by date)
        daily_sales = df.groupby(df['Fecha'].dt.date)['total_venta'].sum().reset_index()

        # Create a line chart for daily sales using matplotlib
        st.subheader("Daily Revenue (Last Week)")
        fig, ax = plt.subplots(figsize=(10, 5))

        # Plotting the data
        ax.plot(daily_sales['Fecha'], daily_sales['total_venta'], marker='o', linestyle='-', color='b')

        # Add labels and title
        ax.set_title("Total Revenue per Day (Last Week)", fontsize=16)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Revenue ($)", fontsize=12)

        # Format x-axis for dates (display days)
        ax.set_xticks(daily_sales['Fecha'])
        ax.set_xticklabels(daily_sales['Fecha'].apply(lambda x: x.strftime('%d')), rotation=45)
        # Show grid
        ax.grid(True)

        # Display the plot
        st.pyplot(fig)

with mes:
    st.header("Reporte mensual")

    df = fetch_monthly_revenue()

    # Convert 'Fecha' to datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'])

    # Calculate total revenue for the month
    total_revenue = df['total_venta'].sum()

    # Display key metrics
    col1, col2 = st.columns(2)
    col1.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
    col2.metric(label="Total Sales", value=f"{df.shape[0]} sales")

    if not df.empty:
        # Display the data as a table
        st.subheader("Daily Sales")
        st.dataframe(df[['Fecha', 'Nombre', 'total_venta']])

        # Prepare data for the line chart (aggregate sales by date)
        daily_sales = df.groupby(df['Fecha'].dt.date)['total_venta'].sum().reset_index()

        # Create a line chart for daily sales using matplotlib
        st.subheader("Daily Revenue")
        fig, ax = plt.subplots(figsize=(10, 5))

        # Plotting the data
        ax.plot(daily_sales['Fecha'], daily_sales['total_venta'], marker='o', linestyle='-', color='b')

        # Add labels and title
        ax.set_title("Total Revenue per Day", fontsize=16)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Revenue ($)", fontsize=12)

        # Format x-axis for dates (display days)
        ax.set_xticks(daily_sales['Fecha'])
        ax.set_xticklabels(daily_sales['Fecha'].apply(lambda x: x.strftime('%d')), rotation=45)

        # Show grid
        ax.grid(True)

        # Display the plot
        st.pyplot(fig)
        
with año:
    st.header("Reporte anual")
    # Fetch yearly data
    df = fetch_yearly_revenue()

    # Convert 'Fecha' to datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'])

    # Calculate total revenue for the year
    total_revenue = df['total_venta'].sum()

    # Display key metrics
    col1, col2 = st.columns(2)
    col1.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
    col2.metric(label="Total Sales", value=f"{df.shape[0]} sales")

    if not df.empty:
        # Display the data as a table
        st.subheader("Daily Sales")
        st.dataframe(df[['Fecha', 'Nombre', 'total_venta']])

        # Prepare data for the line chart (aggregate sales by month)
        monthly_sales = df.groupby(df['Fecha'].dt.to_period('M').dt.to_timestamp())['total_venta'].sum().reset_index()

        # Create a line chart for monthly sales using matplotlib
        st.subheader("Monthly Revenue")
        fig, ax = plt.subplots(figsize=(12, 6))

        # Plotting the data
        ax.plot(monthly_sales['Fecha'], monthly_sales['total_venta'], marker='o', linestyle='-', color='b')

        # Add labels and title
        ax.set_title("Total Revenue per Month (Last Year)", fontsize=16)
        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("Revenue ($)", fontsize=12)

        # Format x-axis for dates (display months)
        ax.set_xticks(monthly_sales['Fecha'])
        ax.set_xticklabels(monthly_sales['Fecha'].dt.strftime('%b-%Y'), rotation=45)

        # Show grid
        ax.grid(True)

        # Display the plot
        st.pyplot(fig)