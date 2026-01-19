import streamlit as st
import pandas as pd
from openai import OpenAI
import io
import re

st.set_page_config(page_title="Dataset Column Mapper", page_icon="📊", layout="wide")

st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

source_file = st.sidebar.file_uploader("Upload Source Dataset", type=["csv"])
target_file = st.sidebar.file_uploader("Upload Target Dataset", type=["csv"])

client = OpenAI(api_key=api_key) if api_key else None

def get_column_mapping(source_cols, target_cols):
    prompt = f"""
    I have two datasets with the following columns.

    Source dataset columns: {source_cols}
    Target dataset columns: {target_cols}

    Please provide a mapping between the two, matching similar meaning columns.
    Return the output as a markdown table with three columns:
    Source Column | Target Column | Notes
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content

def clean_markdown_table(md_text: str) -> pd.DataFrame:
    table_lines = [line for line in md_text.split("\n") if "|" in line]

    table_lines = [
        line for line in table_lines
        if not re.match(r'^\s*\|?\s*-+\s*\|', line)
    ]

    table_lines = [
        line for line in table_lines
        if not "this table" in line.lower()
    ]

    table_str = "\n".join(table_lines)
    return pd.read_csv(io.StringIO(table_str.replace("|", ",")))

def generate_mapping_insights(mapping_df):
    mappings_list = mapping_df[["Source Column", "Target Column"]].values.tolist()

    prompt = "Provide a brief explanation (one short sentence each) of why the following column pairs were mapped:\n\n"
    for source, target in mappings_list:
        prompt += f"- {source} → {target}\n"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content

st.title("Dataset Column Mapper")
st.markdown("Easily map columns between two datasets using the power of OpenAI.")

if source_file and target_file and client:
    col1, col2 = st.columns(2)

    source_df = pd.read_csv(source_file)
    target_df = pd.read_csv(target_file)

    with col1:
        with st.expander("Source Dataset Preview", expanded=False):
            st.dataframe(source_df.head())

    with col2:
        with st.expander("Target Dataset Preview", expanded=False):
            st.dataframe(target_df.head())

    source_cols = list(source_df.columns)
    target_cols = list(target_df.columns)

    st.markdown("---")
    st.subheader("Generated Column Mapping")

    mapping_md = get_column_mapping(source_cols, target_cols)

    try:
        mapping_df = clean_markdown_table(mapping_md)
        st.dataframe(mapping_df, use_container_width=True)

        csv_buffer = io.StringIO()
        mapping_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Download Mapping as CSV",
            data=csv_buffer.getvalue(),
            file_name="column_mapping.csv",
            mime="text/csv",
        )

        st.markdown("---")
        st.subheader("AI Insights")
        insights = generate_mapping_insights(mapping_df)
        st.markdown(insights)

    except Exception:
        st.markdown(mapping_md)

elif not client:
    st.warning("Please enter your OpenAI API key in the sidebar to continue.")
else:
    st.info("Upload both source and target CSV files from the sidebar to begin.")
