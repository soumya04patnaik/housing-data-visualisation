# app.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Streamlit Page Setup ---
st.set_page_config(page_title="🏡 Housing Data BI Dashboard", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("HousingData.csv")
    return df.dropna()

df = load_data()

# --- Sidebar Navigation ---
st.sidebar.title("🏡 BI Dashboard Navigation")
page = st.sidebar.radio("Go to", [
    "📊 Overview",
    "📈 Trend Analysis",
    "💠 Correlation & Comparison",
    "📉 Price Drivers",
    "💡 Business Insights"
])

# --- Common Filters ---
st.sidebar.markdown("### 🔍 Filters")
price_min, price_max = int(df["MEDV"].min()), int(df["MEDV"].max())
price_range = st.sidebar.slider("Select Price Range ($1000s):", price_min, price_max, (price_min, price_max))

room_filter = st.sidebar.slider("Filter by Rooms (RM):", float(df["RM"].min()), float(df["RM"].max()),
                                (float(df["RM"].min()), float(df["RM"].max())))

df_filtered = df[(df["MEDV"] >= price_range[0]) & (df["MEDV"] <= price_range[1])]
df_filtered = df_filtered[(df_filtered["RM"] >= room_filter[0]) & (df_filtered["RM"] <= room_filter[1])]

# =====================================================
# 📊 PAGE 1: OVERVIEW
# =====================================================
if page == "📊 Overview":
    st.title("📊 Dataset Overview and KPIs")

    col1, col2, col3 = st.columns(3)
    col1.metric("🏠 Average Price", f"${df_filtered['MEDV'].mean():.2f}K")
    col2.metric("🛏️ Avg Rooms", f"{df_filtered['RM'].mean():.2f}")
    col3.metric("🎓 Avg PTRATIO", f"{df_filtered['PTRATIO'].mean():.2f}")

    st.markdown("---")
    st.subheader("🏙️ Price Distribution")
    fig, ax = plt.subplots(figsize=(8,5))
    sns.histplot(df_filtered["MEDV"], kde=True, color="#0078AA")
    plt.title("Distribution of House Prices")
    plt.xlabel("Median Value ($1000s)")
    st.pyplot(fig)

    st.markdown("---")
    st.subheader("🏡 Relationship Between Rooms and Price")
    fig, ax = plt.subplots(figsize=(8,5))
    sns.scatterplot(x=df_filtered["RM"], y=df_filtered["MEDV"], color="#00C853", alpha=0.7)
    plt.title("More Rooms = Higher Prices")
    st.pyplot(fig)

# =====================================================
# 📈 PAGE 2: TREND ANALYSIS
# =====================================================
elif page == "📈 Trend Analysis":
    st.title("📈 Trend & Distribution Analysis")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🔸 TAX vs PRICE")
        fig, ax = plt.subplots(figsize=(6,4))
        sns.scatterplot(x=df_filtered["TAX"], y=df_filtered["MEDV"], color="#F57F17", alpha=0.6)
        plt.title("Effect of Property Tax on House Value")
        st.pyplot(fig)

    with c2:
        st.markdown("#### 🔸 PTRATIO vs PRICE")
        fig, ax = plt.subplots(figsize=(6,4))
        sns.lineplot(x=df_filtered["PTRATIO"], y=df_filtered["MEDV"], color="#8E44AD")
        plt.title("Education Quality vs Housing Price")
        st.pyplot(fig)

    st.markdown("---")
    st.subheader("📦 Outlier Detection (Boxplots)")
    colA, colB = st.columns(2)
    with colA:
        fig, ax = plt.subplots(figsize=(6,4))
        sns.boxplot(y=df_filtered["MEDV"], color="#00BFA6")
        plt.title("Price Outliers")
        st.pyplot(fig)
    with colB:
        fig, ax = plt.subplots(figsize=(6,4))
        sns.boxplot(y=df_filtered["RM"], color="#E91E63")
        plt.title("Room Count Outliers")
        st.pyplot(fig)

# =====================================================
# 💠 PAGE 3: CORRELATION & COMPARISON
# =====================================================
elif page == "💠 Correlation & Comparison":
    st.title("💠 Correlation and Feature Relationships")

    st.markdown("#### 🔥 Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(df_filtered.corr(), cmap="YlGnBu", annot=True, fmt=".2f")
    st.pyplot(fig)

    st.markdown("---")
    st.markdown("#### 🔸 Pairplot (Top 4 Features)")
    top_features = ["RM", "LSTAT", "PTRATIO", "MEDV"]
    fig = sns.pairplot(df_filtered[top_features], diag_kind='kde', corner=True)
    st.pyplot(fig)

# =====================================================
# 📉 PAGE 4: PRICE DRIVERS
# =====================================================
elif page == "📉 Price Drivers":
    st.title("📉 Key Drivers of Housing Prices")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🧭 LSTAT (Lower Status %) vs PRICE")
        fig, ax = plt.subplots(figsize=(6,4))
        sns.regplot(x=df_filtered["LSTAT"], y=df_filtered["MEDV"], color="#2E86C1", line_kws={"color": "red"})
        plt.title("Socioeconomic Impact on Price")
        st.pyplot(fig)

    with col2:
        st.markdown("#### 🚨 Crime Rate (CRIM) vs PRICE")
        fig, ax = plt.subplots(figsize=(6,4))
        sns.regplot(x=df_filtered["CRIM"], y=df_filtered["MEDV"], color="#E74C3C", line_kws={"color": "black"})
        plt.title("Crime Rate vs Housing Value")
        st.pyplot(fig)

    st.markdown("---")
    st.subheader("📊 Feature Importance Visualization (Correlation with MEDV)")
    corr_values = df_filtered.corr()["MEDV"].sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8,5))
    sns.barplot(x=corr_values.values, y=corr_values.index, palette="viridis")
    plt.title("Feature Impact on Price")
    st.pyplot(fig)

# =====================================================
# 💡 PAGE 5: BUSINESS INSIGHTS
# =====================================================
elif page == "💡 Business Insights":
    st.title("💡 Strategic Business Insights")

    st.markdown("""
    ### 🧭 Summary of Findings
    - **More rooms → higher price:** A positive correlation between average rooms and price shows that larger homes command a premium.  
    - **Crime rate reduces price:** High-CRIM areas consistently show lower property values, critical for urban policy decisions.  
    - **Education matters:** Neighborhoods with a lower **pupil-teacher ratio (PTRATIO)** see higher prices — families prefer educational quality.  
    - **Wealth factor:** Higher **LSTAT** (lower-status percentage) corresponds to lower prices, highlighting socioeconomic influence.  
    - **Taxes impact affordability:** TAX correlates moderately with price — indicating that tax policy may indirectly affect housing demand.  

    ---
    ### 💼 Business Application
    - **For Real Estate Developers:** Identify ideal zones for premium projects (low crime, low PTRATIO, high RM).  
    - **For City Planners:** Improve affordability by targeting education and crime parameters.  
    - **For Investors:** Use this dashboard to locate undervalued but promising areas.
    """)

    st.markdown("📍 *Developed by Soumyashree Patnaik — Business Intelligence Dashboard Project*")
