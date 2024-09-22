import streamlit as st
from connection import connect
import pandas as pd
import matplotlib.pyplot as plt
from controller.ControladorPDF import ControladorPdf
from dateutil.relativedelta import relativedelta
import os
from constants import IVA

dia, semana, mes, año = st.tabs(["1D", "1W", "1M", "1Y"])

#Fetch daily data
def fetch_yearly_revenue():
    query = """
    SELECT v.NroVenta, v.Fecha, c.Nombre, SUM(p.precio * pv.Cantidad) AS total_venta, SUM(pv.Cantidad) AS units_sold
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

def fetch_yearly_products():
    query="""
    SELECT p.nombre, SUM(pv.Cantidad) AS amount_sold
    FROM prod_venta pv
    JOIN productos p ON pv.ID_Producto = p.id
    JOIN venta v ON pv.NroVenta = v.NroVenta
    WHERE v.Fecha >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
    GROUP BY p.id;
    """
    return connect.query(query)

# Creates the line diagram of the year.
def create_yearly_figure(df):
    # Prepare data for the line chart (aggregate sales by month)
    monthly_sales = df.groupby(df['Fecha'].dt.to_period('M').dt.to_timestamp())['total_venta'].sum().reset_index()

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

    return fig

def create_yearly_circle(amount_sold):
    most_sold = amount_sold.nlargest(5, 'amount_sold') # Los 5 productos más vendidos.
    labels = most_sold['nombre'] # Categorías
    values = most_sold['amount_sold'] # Valores
    total_sold = sum(values)
    sizes = [(value / total_sold * 100) for value in values] # Convertir a porcentajes.

    # Crear el gráfico circular.
    fig,ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    
    # Establecer forma circular.
    ax.axis('equal')

    # Título del gráfico.
    ax.set_title("Five Most Sold Products", fontsize=18)

    return fig
with dia:
    st.header("Reporte diario")
    # Fetch data for the last day
    df = fetch_daily_revenue()

    # Calculate total revenue for the week
    total_revenue = df['total_venta'].sum()
    taxes = total_revenue*IVA
    total_revenue -= taxes # Aplicar el IVA

     # Display key metrics
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
    col2.metric(label="Total Taxes", value=f"${taxes:,.2f}")
    col3.metric(label="Total Sales", value=f"{df.shape[0]} sales")

with semana:
    st.header("Reporte semanal")
    # Fetch data for the last week
    df = fetch_weekly_revenue()

    # Verifica si el DataFrame no está vacío
    
    # Convert 'Fecha' to datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'])

    # Calculate total revenue for the week
    total_revenue = df['total_venta'].sum()
    taxes = total_revenue*IVA
    total_revenue -= taxes # Aplicar el IVA.

    # Display key metrics
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
    col2.metric(label="Total Taxes", value=f"${taxes:,.2f}")
    col3.metric(label="Total Sales", value=f"{df.shape[0]} sales")

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
    taxes = total_revenue*IVA
    total_revenue -= taxes # Aplicar el IVA

    # Display key metrics
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
    col2.metric(label="Total Taxes", value=f"${taxes:,.2f}")
    col3.metric(label="Total Sales", value=f"{df.shape[0]} sales")

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
    taxes = total_revenue*IVA
    total_revenue -= taxes # Aplicar el IVA

    # Display key metrics
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
    col2.metric(label="Total Taxes", value=f"${taxes:,.2f}")
    col3.metric(label="Total Sales", value=f"{df.shape[0]} sales")

    if not df.empty:
        # Display the data as a table
        st.subheader("Daily Sales")
        st.dataframe(df[['Fecha', 'Nombre', 'total_venta']])

        # Create a line chart for monthly sales using matplotlib
        st.subheader("Monthly Revenue")
        fig = create_yearly_figure(df)

        # Display the plot
        st.pyplot(fig)

st.header("Descargar Reporte Anual")
if st.button("Generar PDF"):
    sales = fetch_yearly_revenue()
    sales['Fecha'] = pd.to_datetime(sales['Fecha']) # Convertir el formato a datetime.
    total_revenue = sales['total_venta'].sum()
    taxes = total_revenue * IVA # Lo que se tiene que pagar de impuestos.
    total_revenue -= taxes # Lo que se paga de impuestos, se debe descontar de la ganancia total.
    sales_this_month = sales[sales['Fecha'].dt.month == pd.Timestamp.now().month] # Ventas en el mes actual.
    prev_time = pd.Timestamp.now()-relativedelta(months=1) # Al día actual se le resta 1 mes.
    sales_last_month = sales[sales['Fecha'].dt.month == prev_time.month] # Ventas en el mes pasado.
    this_month = sales_this_month['units_sold'].sum() # Cantidad de productos vendidos en el mes actual.
    last_month = sales_last_month['units_sold'].sum() # Cantidad de productos vendidos el mes pasado.
    per_trans = sales['units_sold'].mean() # Promedio de cantidad de productos vendidos por venta.
    diagram_fig = create_yearly_figure(sales)
    diagram_path = 'images' # CAMBIALO SI LO NECESITAS.
    # La idea es crear la carpeta si todavia no se ha creado.
    if not os.path.exists(diagram_path):
            try:
                os.makedirs(diagram_path)
            except OSError as e:
                st.write("No se pudo crear el directorio")
    diagram_fig.savefig(f'{diagram_path}/diagram.png')
    amount_sold = fetch_yearly_products() # Cantidad vendida de cada producto.
    circle_fig = create_yearly_circle(amount_sold)
    circle_fig.savefig(f'{diagram_path}/circle.png')
    pdf = ControladorPdf()
    pdf.generar_reporte(total_revenue, int(last_month), int(this_month), per_trans, taxes, f'{diagram_path}/diagram.png', f'{diagram_path}/circle.png')
    pdf_out = pdf.output(dest='S').encode('latin1')
    st.success("¡PDF generado con éxito!")
    st.download_button(
        label="Descargar PDF",
        data = pdf_out,
        file_name="sales report.pdf",
        mime="application/pdf"
    )