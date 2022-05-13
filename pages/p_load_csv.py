import tsf_util as tu
from streamlit_multipage import MultiPage


# @st.cache(suppress_st_warning=True)
def p_load_csv(st, **state):
    st.title("Load the demand data")

    f = st.file_uploader("Load here your demand data as a .csv", type=[".csv"])
    if f != None:
        df = tu.load_csv(f)
        st.write(df.head())
    else:
        route = "./DataCoSupplyChainDataset.csv"
        df = tu.load_csv(route)

    st.subheader(
        "Write the header of the following columns as written in your .csv file"
    )

    c1, c2, c3, c4 = st.columns(4)
    _, sc2, _ = st.columns(3)

    product_c = c1.text_input(label="Product Identifier Column Name")
    count_c = c2.text_input(label="Amount Bought Per Order Column Name")
    location_c = c3.text_input(label="Location Identifier Column Name")
    date_c = c4.text_input(label="Date Column Name")

    if (
        f != None
        and product_c != None
        and count_c != None
        and location_c != None
        and date_c != None
    ):
        if sc2.button("Check and save data"):
            f1, f2, f3, f4 = False, False, False, False
            if product_c in df.columns:
                c1.success("Product column found!")
                f1 = True
            else:
                c1.error("Please check the product column name spelling")
            if count_c in df.columns:
                c2.success("Sales count column found!")
                f2 = True
            else:
                c2.error("Please check the sales count column name spelling")
            if location_c in df.columns:
                c3.success("Location column found!")
                f3 = True
            else:
                c3.error("Please check the location column name spelling")
            if date_c in df.columns:
                c4.success("Date column found!")
                f4 = True
            else:
                c4.error("Please check the date column name spelling")
            if f1 and f2 and f3 and f4:
                MultiPage.save(
                    {
                        "df": df,
                        "product column": product_c,
                        "count column": count_c,
                        "location column": location_c,
                        "date column": date_c,
                    }
                )
    elif f is None:
        MultiPage.save(
            {
                "df": df,
                "product column": "Product Card Id",
                "count column": "Order Item Quantity",
                "location column": "Order Region",
                "date column": "shipping date (DateOrders)",
            }
        )
