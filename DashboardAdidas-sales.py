import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Adidas US Sales Dashboard", page_icon=":bar_chart:", layout="wide")
st.title("Adidas US Data Sales")
st.subheader("Kelompok 8 Perancangan Aplikasi Data Sains")
# ---- READ EXCEL ----


df = pd.read_excel(
    io="adidas_us_sales_new.xlsx",
    engine="openpyxl",
    sheet_name="Sheet1",
    skiprows=0,
    usecols="B:R",
    nrows=9649,
)

st.dataframe(df)

#------SIDEBAR-----
st.sidebar.header("Please Filter Here:")
region = st.sidebar.multiselect(
    "Select the Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

product = st.sidebar.multiselect(
    "Select the Product",
    options=df["Product"].unique(),
    default=df["Product"].unique()
)

retailer = st.sidebar.multiselect(
    "Select the Retailer",
    options=df["Retailer"].unique(),
    default=df["Retailer"].unique()
)

df_selection = df.query(
    "Region == @region & Product ==@product & Retailer == @retailer"
)


# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

#TOP KPI'S
total_sales = int(df_selection["Total Sales"].sum())
average_PpU = round(df_selection["Price per Unit"].mean(), 1)
margin_rating = "📈" * int(round(average_PpU, 0))
average_sale_by_transaction = round(df_selection["Total Sales"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Margin Rating:")
    st.subheader(f"{average_PpU} {margin_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

# SALES BY PRODUCT [BAR CHART]
sales_by_product = (
    df_selection.groupby(by=["Product"]).sum()[["Total Sales"]].sort_values(by="Total Sales")
)

fig_product_sales = px.bar(
    sales_by_product,
    x="Total Sales",
    y=sales_by_product.index,
    orientation="h",
    title="<b>Sales by Product</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


# SALES BY REGION [BAR CHART]
sales_by_hour = df_selection.groupby(by=["Region"]).sum()[["Total Sales"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total Sales",
    title="<b>Sales by Region</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

# --- PLOT PIE CHART

# SALES BY RETAILER & UNITS sOLD [PIE CHART]
fig = px.pie(data_frame=df,
            title='Total Units Sold of Retailer',
            names='Retailer',
            values='Units Sold')


st.plotly_chart(fig)


st.title("Anggota")
st.subheader("Osa Nastiyar Maulani - 13052100055")
st.subheader("Nurwulan Handayani - 1305210102")
st.subheader("Egi Dhea Nagita - 1305213009")
            

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
