import streamlit as st
import pandas as pd

st.set_page_config(page_title="💰 Split Expenses", layout="centered")
st.title("💰 Fair Expense Splitter")
st.subheader("Easily split dinner/trip expenses with your friends")

# --- Basic Inputs ---
total_amount = st.number_input("Enter total bill amount (₹):", min_value=0.0, step=10.0)
num_people = st.number_input("Number of friends (including you):", min_value=1, step=1)

st.markdown("---")

# --- Equal split (simple mode) ---
if st.button("💡 Calculate Equal Split"):
    if num_people > 0:
        per_head = total_amount / num_people
        st.success(f"Each person should pay: **₹{per_head:.2f}**")
    else:
        st.error("Number of people must be at least 1.")

st.markdown("---")

# --- Detailed contributions (advanced mode) ---
st.subheader("Optional: Add individual contributions")

with st.form("contributions_form"):
    names = []
    contributions = []

    for i in range(int(num_people)):
        col1, col2 = st.columns([2, 1])
        with col1:
            name = st.text_input(f"Name of Person {i+1}", key=f"name_{i}")
        with col2:
            contrib = st.number_input(f"Paid by {i+1}", min_value=0.0, step=10.0, key=f"contrib_{i}")

        names.append(name if name else f"Person {i+1}")
        contributions.append(contrib)

    submitted = st.form_submit_button("📊 Calculate Settlement")

if submitted:
    # Convert to DataFrame
    df = pd.DataFrame({"Name": names, "Paid": contributions})
    total_paid = df["Paid"].sum()
    per_head = total_paid / num_people if num_people else 0
    df["Balance"] = df["Paid"] - per_head

    st.write("### Summary of Contributions")
    st.table(df)

    st.info(f"💡 Each person should ideally pay **₹{per_head:.2f}**")
    st.success(f"✅ Total Paid = ₹{total_paid:.2f}, Expected Total = ₹{total_amount:.2f}")

    st.write("### Who owes whom?")
    givers = df[df["Balance"] < 0].copy()
    takers = df[df["Balance"] > 0].copy()

    givers["Balance"] = givers["Balance"].abs()

    transactions = []
    for _, giver in givers.iterrows():
        for _, taker in takers.iterrows():
            if giver["Balance"] > 0 and taker["Balance"] > 0:
                amt = min(giver["Balance"], taker["Balance"])
                transactions.append(f"👉 {giver['Name']} should pay ₹{amt:.2f} to {taker['Name']}")
                giver["Balance"] -= amt
                taker["Balance"] -= amt

    if transactions:
        for t in transactions:
            st.write(t)
    else:
        st.success("Everyone has paid their fair share already 🎉")
