# iris_explorer.py
import streamlit as st
import pandas as pd
import altair as alt
from sklearn import datasets
from io import StringIO

# --- Page config
st.set_page_config(page_title="Iris Data Explorer", layout="centered")

# --- Title + short description
st.title("🌼 Iris Data Explorer — Beginner Friendly")
st.markdown(
    """
    Explore the Iris dataset (or upload your own CSV).  
    Learn widgets, data filtering, plotting, and exporting in Streamlit — step by step.
    """
)

# --- Load default dataset (Iris) into a pandas DataFrame
@st.cache_data
def load_iris() -> pd.DataFrame:
    iris = datasets.load_iris(as_frame=True)
    df = iris.frame.copy()  # DataFrame with features and target
    # Add a human-friendly species column
    df["species"] = df["target"].apply(lambda i: iris.target_names[i])
    return df

df = load_iris()

# --- Option: allow user to upload their own CSV to replace the dataset
st.sidebar.header("Data input")
uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV (optional) — columns should include numeric features and an optional 'species' column",
    type=["csv"],
)

if uploaded_file is not None:
    # read uploaded CSV
    try:
        uploaded_text = StringIO(uploaded_file.getvalue().decode("utf-8"))
        user_df = pd.read_csv(uploaded_text)
        st.sidebar.success("CSV loaded — using your data")
        df = user_df
    except Exception as e:
        st.sidebar.error(f"Could not read the CSV: {e}")

# --- Show raw data (collapsible)
if st.checkbox("Show raw data"):
    st.write(df)

# --- Basic summary stats
st.subheader("Summary statistics")
st.write(df.describe(include="all"))

# --- Filtering UI
st.subheader("Filter the data")

# Species filter (if column exists)
if "species" in df.columns:
    species_options = ["All"] + sorted(df["species"].astype(str).unique().tolist())
    chosen_species = st.selectbox("Choose species", species_options)
    if chosen_species != "All":
        df = df[df["species"].astype(str) == chosen_species]

# Numeric sliders for any numeric columns
numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
if numeric_cols:
    st.markdown("**Filter numeric ranges**")
    range_filters = {}
    for col in numeric_cols:
        col_min = float(df[col].min())
        col_max = float(df[col].max())
        step = (col_max - col_min) / 100 if (col_max - col_min) != 0 else 0.1
        low, high = st.slider(
            label=f"{col}",
            min_value=col_min,
            max_value=col_max,
            value=(col_min, col_max),
            step=step,
        )
        range_filters[col] = (low, high)
        # apply filter
        df = df[(df[col] >= low) & (df[col] <= high)]

# --- Show filtered row count
st.write(f"Filtered rows: {len(df)}")

# --- Plotting area
st.subheader("Plots")

# Scatter plot: choose x and y among numeric columns
if len(numeric_cols) >= 2:
    col1 = st.selectbox("X axis", numeric_cols, index=0)
    col2 = st.selectbox("Y axis", numeric_cols, index=1)
    color_by = st.selectbox(
        "Color by (optional)",
        options=["None"] + (["species"] if "species" in df.columns else []),
    )

    base = alt.Chart(df).mark_circle(size=70).encode(
        x=alt.X(col1, scale=alt.Scale(zero=False)),
        y=alt.Y(col2, scale=alt.Scale(zero=False)),
        tooltip=numeric_cols + (["species"] if "species" in df.columns else []),
    )

    if color_by != "None":
        chart = base.encode(color=color_by)
    else:
        chart = base

    st.altair_chart(chart.interactive(), use_container_width=True)
else:
    st.info("Need at least two numeric columns to draw a scatter plot.")

# Histogram for a selected numeric column
if numeric_cols:
    st.markdown("---")
    hist_col = st.selectbox("Choose column for histogram", numeric_cols, index=0)
    hist = alt.Chart(df).mark_bar().encode(
        alt.X(hist_col, bin=alt.Bin(maxbins=30)),
        y="count()",
        tooltip=[hist_col, "count()"],
    )
    st.altair_chart(hist, use_container_width=True)

# --- Download the filtered data
st.subheader("Download filtered data")
csv = df.to_csv(index=False)
st.download_button(label="📥 Download CSV", data=csv, file_name="filtered_data.csv", mime="text/csv")

# --- Small help section for learners
st.markdown(
    """
    ---
    **Tip for learners:**  
    - Try uploading your own CSV with similar numeric columns.  
    - Use the sliders to see how filtering updates the table and plots instantly.
    - Explore Altair docs later to make more advanced charts.
    """
)
