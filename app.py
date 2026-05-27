import streamlit as st
import requests
import pandas as pd


server_location = st.secrets["server_url"]

st.title("💰 Expense Tracker Application")


opt = st.sidebar.selectbox(
    "Select Operation",
    [
        "Add Expense",
        "View Expenses",
        "Update Expense",
        "Delete Expense",
        "Search Expense",
        "Sort Expenses",
        "Filter Expenses",
        "Analyze Spending"
    ]
)


# =========================
# ADD EXPENSE
# =========================

if opt == "Add Expense":

    st.header("➕ Add Expense")

    with st.form("add_expense"):

        title = st.text_input("Expense Title")

        amount = st.number_input(
            "Amount",
            min_value=0.0
        )

        category = st.selectbox(
            "Category",
            [
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Entertainment",
                "Other"
            ]
        )

        date = st.date_input("Expense Date")

        btn = st.form_submit_button("Add Expense")

        if btn:

            new_data = {
                "title": title,
                "amount": amount,
                "category": category,
                "date": str(date)
            }

            try:

                response = requests.post(
                    f"{server_location}/expenses",
                    json=new_data
                )

                data = response.json()

                if response.status_code == 200:
                    st.success(
                        data.get(
                            "message",
                            "Expense Added Successfully"
                        )
                    )

                else:
                    st.error(data)

            except Exception as e:
                st.error(f"Error: {e}")


# =========================
# VIEW EXPENSES
# =========================

elif opt == "View Expenses":

    st.header("📋 View Expenses")

    try:

        response = requests.get(
            f"{server_location}/expenses"
        )

        data = response.json()

        if response.status_code == 200:

            df = pd.DataFrame(data)

            st.dataframe(df)

        else:
            st.error(data)

    except Exception as e:
        st.error(f"Error: {e}")


# =========================
# UPDATE EXPENSE
# =========================

elif opt == "Update Expense":

    st.header("✏️ Update Expense")

    expense_id = st.number_input(
        "Expense ID",
        min_value=1
    )

    title = st.text_input("New Title")

    amount = st.number_input(
        "New Amount",
        min_value=0.0
    )

    category = st.selectbox(
        "New Category",
        [
            "Food",
            "Travel",
            "Shopping",
            "Bills",
            "Entertainment",
            "Other"
        ]
    )

    btn = st.button("Update Expense")

    if btn:

        updated_data = {
            "title": title,
            "amount": amount,
            "category": category
        }

        try:

            response = requests.put(
                f"{server_location}/expenses/{expense_id}",
                json=updated_data
            )

            data = response.json()

            if response.status_code == 200:
                st.success(
                    data.get(
                        "message",
                        "Expense Updated Successfully"
                    )
                )

            else:
                st.error(data)

        except Exception as e:
            st.error(f"Error: {e}")


# =========================
# DELETE EXPENSE
# =========================

elif opt == "Delete Expense":

    st.header("🗑️ Delete Expense")

    expense_id = st.number_input(
        "Expense ID",
        min_value=1
    )

    btn = st.button("Delete Expense")

    if btn:

        try:

            response = requests.delete(
                f"{server_location}/expenses/{expense_id}"
            )

            data = response.json()

            if response.status_code == 200:
                st.warning(
                    data.get(
                        "message",
                        "Expense Deleted Successfully"
                    )
                )

            else:
                st.error(data)

        except Exception as e:
            st.error(f"Error: {e}")


# =========================
# SEARCH EXPENSE
# =========================

elif opt == "Search Expense":

    st.header("🔍 Search Expense")

    keyword = st.text_input(
        "Enter title/category"
    )

    btn = st.button("Search")

    if btn:

        try:

            response = requests.get(
                f"{server_location}/expenses/search/{keyword}"
            )

            data = response.json()

            if response.status_code == 200:

                df = pd.DataFrame(data)

                st.dataframe(df)

            else:
                st.error(data)

        except Exception as e:
            st.error(f"Error: {e}")


# =========================
# SORT EXPENSES
# =========================

elif opt == "Sort Expenses":

    st.header("📊 Sort Expenses")

    sort_by = st.selectbox(
        "Sort By",
        [
            "amount",
            "date",
            "category"
        ]
    )

    try:

        response = requests.get(
            f"{server_location}/expenses/sort/{sort_by}"
        )

        data = response.json()

        if response.status_code == 200:

            df = pd.DataFrame(data)

            st.dataframe(df)

        else:
            st.error(data)

    except Exception as e:
        st.error(f"Error: {e}")


# =========================
# FILTER EXPENSES
# =========================

elif opt == "Filter Expenses":

    st.header("🎯 Filter Expenses")

    category = st.selectbox(
        "Select Category",
        [
            "Food",
            "Travel",
            "Shopping",
            "Bills",
            "Entertainment",
            "Other"
        ]
    )

    btn = st.button("Filter")

    if btn:

        try:

            response = requests.get(
                f"{server_location}/expenses/filter/{category}"
            )

            data = response.json()

            if response.status_code == 200:

                df = pd.DataFrame(data)

                st.dataframe(df)

            else:
                st.error(data)

        except Exception as e:
            st.error(f"Error: {e}")


# =========================
# ANALYZE SPENDING
# =========================

elif opt == "Analyze Spending":

    st.header("📈 Spending Analysis")

    try:

        response = requests.get(
            f"{server_location}/expenses/analysis"
        )

        data = response.json()

        if response.status_code == 200:

            st.subheader("Total Spending")

            st.write(
                data["total_spending"]
            )

            st.subheader(
                "Category Wise Spending"
            )

            category_df = pd.DataFrame(
                data["category_wise"]
            )

            st.bar_chart(
                category_df.set_index(
                    "category"
                )
            )

        else:
            st.error(data)

    except Exception as e:
        st.error(f"Error: {e}")