import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
import re
from datetime import datetime


plt.style.use('seaborn-v0_8')
sns.set_palette("tab10")

# ----------------------------
# PART 1: LOAD & EXPLORE DATA
# ----------------------------
def load_and_explore_data(file_path):
    try:
        df = pd.read_csv(file_path, low_memory=False)
        print(" ## Metadata loaded successfully.")
    except Exception as e:
        print(f" ** Failed to load data: {e}")
        return None

    print("\n" + "="*60)
    print("PART 1: DATASET OVERVIEW (CORD-19 metadata.csv)")
    print("="*60)
    print(f"Total records: {df.shape[0]:,}")
    print(f"Columns: {list(df.columns)}")

    missing = df.isnull().sum()
    missing_nonzero = missing[missing > 0]
    if not missing_nonzero.empty:
        print("\nTop missing columns:")
        print(missing_nonzero.sort_values(ascending=False).head())
    else:
        print("\nNo missing values.")

    # Show sample of publish_time formats
    sample_times = df['publish_time'].dropna().head(10).tolist()
    print(f"\nSample 'publish_time' formats: {sample_times}")

    return df

# ----------------------------
# PART 2: CLEAN & PREPARE DATA
# ----------------------------
def parse_publish_time(time_str):
    """Robustly parse CORD-19 publish_time into year."""
    if pd.isna(time_str):
        return np.nan
    time_str = str(time_str).strip()
    # Try common formats: YYYY, YYYY-MM, YYYY-MM-DD
    for fmt in ["%Y", "%Y-%m", "%Y-%m-%d"]:
        try:
            return datetime.strptime(time_str, fmt).year
        except ValueError:
            continue
    # Handle formats like "2020 Mar" or "Mar 2020"
    try:
        # Extract 4-digit year
        year_match = re.search(r'\b(19|20)\d{2}\b', time_str)
        if year_match:
            return int(year_match.group(0))
    except:
        pass
    return np.nan

def clean_data(df):
    print("\n" + "="*60)
    print("PART 2: CLEANING CORD-19 METADATA")
    print("="*60)
    
    df_clean = df.copy()
    
    # Keep only records with title and abstract (core content)
    before = len(df_clean)
    df_clean = df_clean[df_clean['title'].notna() & df_clean['abstract'].notna()]
    after = len(df_clean)
    print(f"Kept {after:,} records with both title and abstract ({before - after:,} removed).")

    # Parse publish_time to year
    print("Parsing 'publish_time' to extract publication year...")
    df_clean['publish_year'] = df_clean['publish_time'].apply(parse_publish_time)
    
    # Keep only years 2020–2023 (COVID era)
    df_clean = df_clean[
        (df_clean['publish_year'] >= 2020) & 
        (df_clean['publish_year'] <= 2023)
    ]
    print(f"Filtered to {len(df_clean):,} papers published in 2020–2023.")

    # Clean journal names (remove whitespace, handle NaN)
    df_clean['journal'] = df_clean['journal'].fillna("Unknown").str.strip()
    df_clean['journal'] = df_clean['journal'].replace("", "Unknown")

    print(" ## Cleaning complete.")
    return df_clean

# ----------------------------
# PART 3: ANALYSIS & VISUALIZATION
# ----------------------------
def analyze_and_visualize(df):
    print("\n" + "="*60)
    print("PART 3: ANALYSIS & VISUALIZATION")
    print("="*60)
    
    os.makedirs('plots', exist_ok=True)
    plots = []

    # Sample for faster plotting (max 20k points)
    df_sample = df.sample(n=min(20000, len(df)), random_state=42)

    # 1. Publications over time
    plt.figure(figsize=(10, 5))
    year_counts = df['publish_year'].value_counts().sort_index()
    sns.barplot(x=year_counts.index, y=year_counts.values, color='steelblue')
    plt.title('Research Publications per Year (2020–2023)')
    plt.xlabel('Year')
    plt.ylabel('Number of Papers')
    plt.tight_layout()
    path = 'plots/publications_by_year.png'
    plt.savefig(path)
    plots.append(path)
    plt.close()
    print(" ## Saved: Publications by year")

    # 2. Top 15 Journals
    top_journals = df['journal'].value_counts().head(15)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_journals.values, y=top_journals.index, orient='h')
    plt.title('Top 15 Journals Publishing COVID-19 Research')
    plt.xlabel('Number of Papers')
    plt.tight_layout()
    path = 'plots/top_journals.png'
    plt.savefig(path)
    plots.append(path)
    plt.close()
    print(" ## Saved: Top journals")

    # 3. Source distribution (e.g., CZI, PMC, bioRxiv, etc.)
    source_counts = df['source_x'].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=source_counts.values, y=source_counts.index, orient='h')
    plt.title('Top 10 Data Sources (by Paper Count)')
    plt.xlabel('Number of Papers')
    plt.tight_layout()
    path = 'plots/top_sources_bar.png'
    plt.savefig(path)
    plots.append(path)
    plt.close()

    # 4. Abstract length distribution (as proxy for content)
    df_sample['abstract_len'] = df_sample['abstract'].str.len()
    plt.figure(figsize=(10, 5))
    sns.histplot(df_sample['abstract_len'], bins=50, kde=False)
    plt.title('Distribution of Abstract Lengths (Characters)')
    plt.xlabel('Abstract Length')
    plt.ylabel('Frequency')
    plt.tight_layout()
    path = 'plots/abstract_length.png'
    plt.savefig(path)
    plots.append(path)
    plt.close()
    print(" ## Saved: Abstract length")

    return plots

# ----------------------------
# PART 4: STREAMLIT APP
# ----------------------------
def run_streamlit_app(df, plot_paths):
    st.set_page_config(page_title="CORD-19 Research Dashboard", layout="wide")
    st.title("CORD-19 Research Trends (2020–2023)")
    st.markdown("Analysis of the [CORD-19 metadata](https://www.kaggle.com/datasets/allen-institute-for-ai/CORD-19-research-challenge) dataset")

    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Overview", "Visualizations", "Data Sample"])

    if page == "Overview":
        st.subheader("Dataset Summary")
        st.write(f"**Total papers analyzed**: {len(df):,}")
        st.write(f"**Time range**: 2020 – 2023")
        st.write(f"**Top journal**: {df['journal'].value_counts().index[0]}")
        st.write(f"**Main sources**: {', '.join(df['source_x'].unique()[:4])}")

    elif page == "Visualizations":
        st.subheader("Key Insights")
        for plot in plot_paths:
            st.image(plot, use_column_width=True)

    elif page == "Data Sample":
        st.subheader("Sample Records")
        st.dataframe(df[['publish_year', 'journal', 'title', 'abstract']].sample(10).reset_index(drop=True))

# ----------------------------
# PART 5: MAIN EXECUTION
# ----------------------------
if __name__ == "__main__":
    DATA_FILE = "metadata.csv"  # Make sure this file is in the same directory

    if 'streamlit' in str(os.environ.get('SERVER_SOFTWARE', '')):
        # Streamlit mode
        df_raw = load_and_explore_data(DATA_FILE)
        if df_raw is not None:
            df_clean = clean_data(df_raw)
            plots = analyze_and_visualize(df_clean)
            run_streamlit_app(df_clean, plots)
    else:
        # Script mode
        print(" Starting CORD-19 metadata analysis...\n")
        df_raw = load_and_explore_data(DATA_FILE)
        if df_raw is None:
            exit()
        df_clean = clean_data(df_raw)
        plots = analyze_and_visualize(df_clean)
        print(f"\n ## Analysis complete! Plots saved in 'plots/' folder.")
        print(f"\n --> To launch dashboard: streamlit run {os.path.basename(__file__)}")