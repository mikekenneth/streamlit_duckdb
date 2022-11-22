import duckdb
import streamlit as st
from generate_data import generate_dataset_orders, load_file


def execute_query(query: str, return_type: str = "df"):
    with duckdb.connect("duck.db", read_only=True) as con:
        if return_type == "df":
            return con.execute(query).df()
        else:
            return con.execute(query)


if __name__ == "__main__":
    st.title("Streamlit + duckdb")

    button = st.button(label="Generate or Refresh Data")
    if button:
        generate_dataset_orders(num_rows=100)
        load_file()

    data = execute_query("select * from orders")
    st.write("## Sample")
    st.write(data.head(5))

    st.write("## Visualization (Line Charts)")
    option = st.selectbox("Select a dimension", ["product_name", "customer_name", "status"], key="option")
    if option:
        st.write(f"### Line Chart: Counts x {option}")
        st.line_chart(data.pivot_table(index="datetime", columns=option, values="id", aggfunc="count", fill_value=0))

        st.write(f"### Line Chart: Amount x {option}")
        st.line_chart(data.pivot_table(index="datetime", columns=option, values="amount", aggfunc="sum", fill_value=0))

        st.write(f"### Line Chart: Quantity x {option}")
        st.line_chart(
            data.pivot_table(index="datetime", columns=option, values="quantity", aggfunc="sum", fill_value=0)
        )

    st.write("## Visualization (Bar Charts)")
    option2 = st.selectbox("Select a dimension", ["product_name", "customer_name", "status"], key="option2")
    if option2:
        st.write(f"### Bar Chart: {option2} x Quantity")
        st.bar_chart(data, x=option2, y="quantity")

        st.write(f"### Bar Chart: {option2} x Amount")
        st.bar_chart(data, x=option2, y="amount")

        st.write(f"### Bar Chart: {option2} x Count")
        st.bar_chart(data[option2].value_counts())
