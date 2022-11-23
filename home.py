import duckdb
import streamlit as st
from generate_data import generate_dataset_orders, load_file


db = "duck.db"
destination_table_name = "orders"
filename = "orders.csv"


def execute_query(query: str, db: str, return_type: str = "df"):
    with duckdb.connect(db, read_only=True) as con:
        if return_type == "df":
            return con.execute(query).df()
        elif return_type == "arrow":
            return con.execute(query).arrow()
        elif return_type == "list":
            return con.execute(query).fetchall()


@st.experimental_memo  # An optimization wrapper to memoize the result of the function
def export_df(df):
    return df.to_csv(index=False).encode("utf-8")


if __name__ == "__main__":
    st.title("Streamlit + duckdb")
    try:
        button = st.button(label="Generate or Refresh Data")
        if button:
            generate_dataset_orders(filename=filename, num_rows=1000)
            load_file(db=db, infile_path=filename, table_name=destination_table_name)

        data = execute_query(f"select * from {destination_table_name}", db=db, return_type="df")

        st.write("## Sample")
        st.dataframe(data.head(10), height=300)

        st.write("## Visualization")
        option = st.selectbox("Select a dimension", ["product_name", "customer_name", "status"], key="option")
        if option:
            st.write(f"### Bar Chart: {option} x Quantity")
            st.bar_chart(data, x=option, y="quantity")

            st.write(f"### Bar Chart: {option} x Amount")
            st.bar_chart(data, x=option, y="amount")

            st.write(f"### Bar Chart: {option} x Count")
            st.bar_chart(data[option].value_counts())

        st.write("## Filters (by Products Name)")
        products_list = [
            row[0]
            for row in execute_query(
                f"select distinct(product_name) from {destination_table_name}", db=db, return_type="list"
            )
        ]
        product_filter = st.selectbox(label="Select a Product", options=products_list, key="product_filter")
        if product_filter != "--":
            result = execute_query(
                f"select * from {destination_table_name} where product_name = '{product_filter}'",
                db=db,
                return_type="df",
            )
            st.dataframe(result, height=400)

            # To download the data we have just selected
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
