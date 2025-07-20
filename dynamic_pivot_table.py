import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pivot Table Explorer", layout="wide")

st.title("🔍 Interactive Pivot Table Viewer")

# --- Load Data ---
@st.cache_data
def load_default_data():
    return pd.DataFrame({
        'Column1': ['a', 'b', 'c', 'd'] * 5,
        'Column2': ['A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D'],
        'Column3': range(20)
    })

st.sidebar.header("Step 1: Load Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

try:
    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    else:
        st.sidebar.info("Using sample data.")
        df = load_default_data()

    st.subheader("🔢 Raw Data")
    st.dataframe(df, use_container_width=True)

    # --- Choose Pivot Axes ---
    st.sidebar.header("Step 2: Select Pivot Dimensions")

    cols = df.columns.tolist()
    if len(cols) < 2:
        st.warning("Need at least two columns to create a pivot.")
    else:
        row_dim = st.sidebar.selectbox("Row Axis", cols, key="row")
        col_dim = st.sidebar.selectbox("Column Axis", [c for c in cols if c != row_dim], key="col")

        # --- Pivot Table ---
        try:
            pivot_table = pd.pivot_table(df, index=row_dim, columns=col_dim, aggfunc='size', fill_value=0)

            st.subheader("📊 Pivot Table (Counts)")
            st.dataframe(pivot_table, use_container_width=True)

            # --- Cell Selector ---
            st.sidebar.header("Step 3: Explore Pivot Cells")

            row_values = pivot_table.index.tolist()
            col_values = pivot_table.columns.tolist()

            selected_row = st.sidebar.selectbox(f"Select {row_dim}", row_values)
            selected_col = st.sidebar.selectbox(f"Select {col_dim}", col_values)

            filtered_df = df[(df[row_dim] == selected_row) & (df[col_dim] == selected_col)]

            st.markdown(f"### 📄 Rows where `{row_dim}` = **{selected_row}** and `{col_dim}` = **{selected_col}**")
            st.dataframe(filtered_df, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error generating pivot: {e}")

except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    