import duckdb
import streamlit as st
from generate_data import generate_dataset_orders, load_file


def execute_query(query: str, return_type: str = "df"):
    with duckdb.connect("duck.db", read_only=True) as con:
        if return_type == "df":
            return con.execute(query).df()
        elif return_type == "arrow":
            return con.execute(query).arrow()
        elif return_type == "list":
            return con.execute(query).fetchall()


@st.experimental_memo  # An optimization wrapper to memoize the result of the function
def export_df(df):
    return df.to_csv(index=False).encode("utf-8")


st.title("Streamlit + duckdb")
try:
    button = st.button(label="Generate or Refresh Data")
    if button:
        generate_dataset_orders(num_rows=1000)
        load_file()

    data = execute_query("select * from orders", return_type="df")

    st.write("## Sample")
    st.dataframe(data.head(10), height=300)

    st.write("## Visualization")
    option2 = st.selectbox("Select a dimension", ["product_name", "customer_name", "status"], key="option2")
    if option2:
        st.write(f"### Bar Chart: {option2} x Quantity")
        st.bar_chart(data, x=option2, y="quantity")

        st.write(f"### Bar Chart: {option2} x Amount")
        st.bar_chart(data, x=option2, y="amount")

        st.write(f"### Bar Chart: {option2} x Count")
        st.bar_chart(data[option2].value_counts())

    # To Filter based on "products" we need to extract the list
    st.write("## Filters (by Products Name)")
    products = [row[0] for row in execute_query("select distinct(product_name) from orders", return_type="list")]
    products.append("--")
    product_filter = st.selectbox("Select a Product", products, key="product_filter", index=len(products) - 1)
    if product_filter != "--":
        result = execute_query(f"select * from orders where product_name = '{product_filter}'", return_type="df")
        st.dataframe(result, height=400)

        # To donwload the data we just selected
        st.write("### Download Data")
        st.download_button(
            label="Press to Download",
            data=export_df(result),
            file_name=f"orders - product='{product_filter}'.csv",
            mime="text/csv",
            key="download-csv",
        )
except duckdb.CatalogException:  # Catch exception when the database file don't exist yet
    st.text("Please Clik on the above button to generate data.")
