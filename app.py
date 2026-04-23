import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0a0a0f;
    color: #e8e8f0;
}
.main { background-color: #0a0a0f; }
h1,h2,h3 { font-family: 'IBM Plex Mono', monospace; }

.kpi-card {
    background: linear-gradient(145deg, #12121f, #1a1a2e);
    border: 1px solid #2a2a4a;
    border-left: 4px solid #6c63ff;
    border-radius: 12px;
    padding: 20px 22px;
    margin-bottom: 10px;
    transition: all 0.3s;
}
.kpi-card:hover { border-left-color: #00d4aa; box-shadow: 0 4px 20px #6c63ff22; }
.kpi-value { font-family: 'IBM Plex Mono', monospace; font-size: 1.8rem; font-weight: 600; color: #6c63ff; }
.kpi-label { font-size: 0.75rem; color: #888; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 4px; }
.kpi-delta { font-size: 0.8rem; color: #00d4aa; margin-top: 4px; }

.section-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1rem;
    color: #6c63ff;
    border-bottom: 1px solid #2a2a4a;
    padding-bottom: 8px;
    margin: 20px 0 16px 0;
}

div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0a0f, #12121f);
    border-right: 1px solid #2a2a4a;
}

.stButton > button {
    background: linear-gradient(135deg, #6c63ff, #00d4aa);
    color: white;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
}

.highlight { color: #6c63ff; font-weight: 600; }
.positive { color: #00d4aa; }
.negative { color: #ff6b6b; }
</style>
""", unsafe_allow_html=True)

# ── Dark Chart Style ──────────────────────────────────────────────────────────
def set_dark_style():
    plt.rcParams.update({
        "figure.facecolor": "#12121f",
        "axes.facecolor": "#1a1a2e",
        "axes.edgecolor": "#2a2a4a",
        "axes.labelcolor": "#888",
        "xtick.color": "#888",
        "ytick.color": "#888",
        "text.color": "#e8e8f0",
        "grid.color": "#2a2a4a",
        "grid.linestyle": "--",
        "grid.alpha": 0.5,
        "font.family": "monospace",
        "legend.facecolor": "#12121f",
        "legend.edgecolor": "#2a2a4a",
    })

PALETTE = ["#6c63ff", "#00d4aa", "#ff6b6b", "#ffd700", "#ff9f43", "#4dd9ff", "#fd79a8", "#a8ff78"]

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    if not os.path.exists('sales_data.csv'):
        from data_generator import generate_sales_data
        df = generate_sales_data()
    else:
        df = pd.read_csv('sales_data.csv', parse_dates=['order_date'])
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['month'] = df['order_date'].dt.to_period('M')
    df['month_str'] = df['order_date'].dt.strftime('%b %Y')
    df['year'] = df['order_date'].dt.year
    df['quarter'] = df['order_date'].dt.quarter
    return df

df_full = load_data()

# ── Sidebar Filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Sales Dashboard")
    st.markdown("---")

    page = st.radio("Navigate", [
        "🏠 Overview", "📈 Revenue Analysis",
        "🗺️ Regional Performance", "👥 Sales Rep Analysis",
        "📦 Product Insights", "📋 KPI Report"
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("### 🔍 Filters")

    years = sorted(df_full['year'].unique())
    selected_years = st.multiselect("Year", years, default=years)

    regions = sorted(df_full['region'].unique())
    selected_regions = st.multiselect("Region", regions, default=regions)

    segments = sorted(df_full['segment'].unique())
    selected_segments = st.multiselect("Segment", segments, default=segments)

    categories = sorted(df_full['category'].unique())
    selected_categories = st.multiselect("Category", categories, default=categories)

    st.markdown("---")
    total_records = len(df_full)
    st.markdown(f"**Total Records:** {total_records:,}")

# ── Filter Data ───────────────────────────────────────────────────────────────
df = df_full[
    df_full['year'].isin(selected_years) &
    df_full['region'].isin(selected_regions) &
    df_full['segment'].isin(selected_segments) &
    df_full['category'].isin(selected_categories)
].copy()

# ── YoY Calculation ───────────────────────────────────────────────────────────
def yoy_growth(df, col):
    try:
        y1 = df[df['year'] == 2023][col].sum()
        y2 = df[df['year'] == 2024][col].sum()
        return round(((y2 - y1) / y1) * 100, 1) if y1 > 0 else 0
    except:
        return 0

# ════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":
    st.markdown("# 📊 Sales Performance Dashboard")
    st.markdown(f"*Filtered: {len(df):,} records | {', '.join(map(str, selected_years))}*")
    st.markdown("---")

    total_revenue = df['revenue'].sum()
    total_profit = df['profit'].sum()
    avg_margin = df['profit_margin'].mean()
    total_orders = len(df)
    yoy_rev = yoy_growth(df, 'revenue')
    yoy_prof = yoy_growth(df, 'profit')

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Total Revenue</div>
            <div class="kpi-value">₹{total_revenue/1e7:.2f}Cr</div>
            <div class="kpi-delta">▲ {yoy_rev}% YoY Growth</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Total Profit</div>
            <div class="kpi-value">₹{total_profit/1e7:.2f}Cr</div>
            <div class="kpi-delta">▲ {yoy_prof}% YoY Growth</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Avg Profit Margin</div>
            <div class="kpi-value">{avg_margin:.1f}%</div>
            <div class="kpi-delta">Across all segments</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Total Orders</div>
            <div class="kpi-value">{total_orders:,}</div>
            <div class="kpi-delta">Avg ₹{total_revenue/total_orders:,.0f} / order</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<div class="section-title">Monthly Revenue Trend</div>', unsafe_allow_html=True)
        monthly = df.groupby('month_str').agg(revenue=('revenue','sum')).reset_index()
        monthly['sort_key'] = pd.to_datetime(monthly['month_str'], format='%b %Y')
        monthly = monthly.sort_values('sort_key')
        set_dark_style()
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.fill_between(range(len(monthly)), monthly['revenue']/1e5, alpha=0.3, color='#6c63ff')
        ax.plot(range(len(monthly)), monthly['revenue']/1e5, color='#6c63ff', linewidth=2.5, marker='o', markersize=4)
        ax.set_xticks(range(len(monthly)))
        ax.set_xticklabels(monthly['month_str'], rotation=45, ha='right', fontsize=6)
        ax.set_ylabel('Revenue (₹ Lakhs)')
        ax.set_title('Monthly Revenue', color='#6c63ff', fontsize=11)
        ax.grid(axis='y')
        fig.patch.set_facecolor('#12121f')
        st.pyplot(fig); plt.close()

    with col_r:
        st.markdown('<div class="section-title">Revenue by Category</div>', unsafe_allow_html=True)
        cat_rev = df.groupby('category')['revenue'].sum().sort_values(ascending=True)
        set_dark_style()
        fig2, ax2 = plt.subplots(figsize=(7, 4))
        bars = ax2.barh(cat_rev.index, cat_rev.values/1e5, color=PALETTE[:len(cat_rev)], edgecolor='#0a0a0f', height=0.6)
        ax2.set_xlabel('Revenue (₹ Lakhs)')
        ax2.set_title('Category-wise Revenue', color='#6c63ff', fontsize=11)
        for bar, val in zip(bars, cat_rev.values):
            ax2.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                     f'₹{val/1e5:.0f}L', va='center', fontsize=7, color='#e8e8f0')
        fig2.patch.set_facecolor('#12121f')
        st.pyplot(fig2); plt.close()

    # Segment pie + Top products
    col3a, col3b = st.columns(2)
    with col3a:
        st.markdown('<div class="section-title">Revenue by Segment</div>', unsafe_allow_html=True)
        seg = df.groupby('segment')['revenue'].sum()
        set_dark_style()
        fig3, ax3 = plt.subplots(figsize=(5, 4))
        wedges, texts, autotexts = ax3.pie(seg.values, labels=seg.index, colors=PALETTE,
            autopct='%1.1f%%', startangle=90,
            wedgeprops=dict(width=0.6, edgecolor='#0a0a0f', linewidth=2))
        for at in autotexts: at.set_fontsize(8); at.set_color('#fff')
        ax3.set_title('Segment Split', color='#6c63ff', fontsize=11)
        fig3.patch.set_facecolor('#12121f')
        st.pyplot(fig3); plt.close()

    with col3b:
        st.markdown('<div class="section-title">Top 10 Products by Revenue</div>', unsafe_allow_html=True)
        top_prod = df.groupby('product')['revenue'].sum().nlargest(10).reset_index()
        top_prod['revenue'] = top_prod['revenue'].apply(lambda x: f'₹{x/1e5:.1f}L')
        top_prod.columns = ['Product', 'Revenue']
        st.dataframe(top_prod, use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE: REVENUE ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
elif page == "📈 Revenue Analysis":
    st.markdown("# 📈 Revenue Analysis")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">YoY Revenue Comparison</div>', unsafe_allow_html=True)
        yoy = df.groupby(['year', df['order_date'].dt.month])['revenue'].sum().reset_index()
        yoy.columns = ['year', 'month', 'revenue']
        set_dark_style()
        fig, ax = plt.subplots(figsize=(7, 4))
        for i, yr in enumerate(yoy['year'].unique()):
            data = yoy[yoy['year'] == yr]
            ax.plot(data['month'], data['revenue']/1e5, marker='o', label=str(yr),
                    color=PALETTE[i], linewidth=2.5, markersize=5)
        ax.set_xlabel('Month')
        ax.set_ylabel('Revenue (₹ Lakhs)')
        ax.set_title('Year-over-Year Revenue', color='#6c63ff', fontsize=11)
        ax.legend()
        ax.grid(axis='y')
        fig.patch.set_facecolor('#12121f')
        st.pyplot(fig); plt.close()

    with col2:
        st.markdown('<div class="section-title">Quarterly Revenue & Profit</div>', unsafe_allow_html=True)
        qtr = df.groupby(['year', 'quarter']).agg(revenue=('revenue','sum'), profit=('profit','sum')).reset_index()
        qtr['label'] = qtr['year'].astype(str) + ' Q' + qtr['quarter'].astype(str)
        set_dark_style()
        fig2, ax2 = plt.subplots(figsize=(7, 4))
        x = range(len(qtr))
        w = 0.4
        ax2.bar([i - w/2 for i in x], qtr['revenue']/1e5, width=w, label='Revenue', color='#6c63ff', alpha=0.85)
        ax2.bar([i + w/2 for i in x], qtr['profit']/1e5, width=w, label='Profit', color='#00d4aa', alpha=0.85)
        ax2.set_xticks(list(x))
        ax2.set_xticklabels(qtr['label'], rotation=45, ha='right', fontsize=7)
        ax2.set_ylabel('₹ Lakhs')
        ax2.set_title('Quarterly Performance', color='#6c63ff', fontsize=11)
        ax2.legend()
        ax2.grid(axis='y')
        fig2.patch.set_facecolor('#12121f')
        st.pyplot(fig2); plt.close()

    # Profit Margin by Category
    st.markdown('<div class="section-title">Profit Margin by Category & Segment</div>', unsafe_allow_html=True)
    pivot = df.pivot_table(values='profit_margin', index='category', columns='segment', aggfunc='mean')
    set_dark_style()
    fig3, ax3 = plt.subplots(figsize=(12, 4))
    sns.heatmap(pivot, ax=ax3, cmap='RdYlGn', annot=True, fmt='.1f',
                linewidths=0.5, linecolor='#0a0a0f',
                annot_kws={'size': 9}, cbar_kws={'shrink': 0.8})
    ax3.set_title('Avg Profit Margin % (Category × Segment)', color='#6c63ff', fontsize=11)
    ax3.set_xlabel(''); ax3.set_ylabel('')
    fig3.patch.set_facecolor('#12121f')
    st.pyplot(fig3); plt.close()

    # Discount vs Profit scatter
    st.markdown('<div class="section-title">Discount Impact on Profit Margin</div>', unsafe_allow_html=True)
    set_dark_style()
    fig4, ax4 = plt.subplots(figsize=(12, 4))
    for i, cat in enumerate(df['category'].unique()):
        sub = df[df['category'] == cat]
        ax4.scatter(sub['discount'], sub['profit_margin'], alpha=0.4,
                    color=PALETTE[i % len(PALETTE)], label=cat, s=15)
    ax4.set_xlabel('Discount Rate')
    ax4.set_ylabel('Profit Margin %')
    ax4.set_title('Discount vs Profit Margin', color='#6c63ff', fontsize=11)
    ax4.legend(fontsize=7)
    ax4.grid()
    fig4.patch.set_facecolor('#12121f')
    st.pyplot(fig4); plt.close()

# ════════════════════════════════════════════════════════════════════════════
# PAGE: REGIONAL PERFORMANCE
# ════════════════════════════════════════════════════════════════════════════
elif page == "🗺️ Regional Performance":
    st.markdown("# 🗺️ Regional Performance")
    st.markdown("---")

    reg = df.groupby('region').agg(
        revenue=('revenue','sum'),
        profit=('profit','sum'),
        orders=('order_id','count'),
        margin=('profit_margin','mean')
    ).reset_index().sort_values('revenue', ascending=False)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Revenue by Region</div>', unsafe_allow_html=True)
        set_dark_style()
        fig, ax = plt.subplots(figsize=(6, 4))
        colors = PALETTE[:len(reg)]
        bars = ax.bar(reg['region'], reg['revenue']/1e5, color=colors, edgecolor='#0a0a0f', width=0.6)
        for bar, val in zip(bars, reg['revenue']):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'₹{val/1e5:.0f}L', ha='center', fontsize=8, color='#e8e8f0')
        ax.set_ylabel('Revenue (₹ Lakhs)')
        ax.set_title('Region-wise Revenue', color='#6c63ff', fontsize=11)
        ax.grid(axis='y')
        fig.patch.set_facecolor('#12121f')
        st.pyplot(fig); plt.close()

    with col2:
        st.markdown('<div class="section-title">Profit Margin by Region</div>', unsafe_allow_html=True)
        set_dark_style()
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        bars2 = ax2.bar(reg['region'], reg['margin'], color='#00d4aa', edgecolor='#0a0a0f', width=0.6, alpha=0.85)
        for bar, val in zip(bars2, reg['margin']):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                     f'{val:.1f}%', ha='center', fontsize=8, color='#e8e8f0')
        ax2.set_ylabel('Avg Profit Margin %')
        ax2.set_title('Region-wise Profit Margin', color='#6c63ff', fontsize=11)
        ax2.grid(axis='y')
        fig2.patch.set_facecolor('#12121f')
        st.pyplot(fig2); plt.close()

    st.markdown('<div class="section-title">Regional Summary Table</div>', unsafe_allow_html=True)
    reg_display = reg.copy()
    reg_display['revenue'] = reg_display['revenue'].apply(lambda x: f'₹{x/1e5:.1f}L')
    reg_display['profit'] = reg_display['profit'].apply(lambda x: f'₹{x/1e5:.1f}L')
    reg_display['margin'] = reg_display['margin'].apply(lambda x: f'{x:.1f}%')
    reg_display.columns = ['Region', 'Revenue', 'Profit', 'Orders', 'Margin']
    st.dataframe(reg_display, use_container_width=True, hide_index=True)

    # Region + Category heatmap
    st.markdown('<div class="section-title">Region × Category Revenue Heatmap</div>', unsafe_allow_html=True)
    hmap = df.pivot_table(values='revenue', index='region', columns='category', aggfunc='sum')/1e5
    set_dark_style()
    fig3, ax3 = plt.subplots(figsize=(12, 4))
    sns.heatmap(hmap, ax=ax3, cmap='Blues', annot=True, fmt='.0f',
                linewidths=0.5, linecolor='#0a0a0f', annot_kws={'size': 9})
    ax3.set_title('Revenue (₹ Lakhs) — Region × Category', color='#6c63ff', fontsize=11)
    ax3.set_xlabel(''); ax3.set_ylabel('')
    fig3.patch.set_facecolor('#12121f')
    st.pyplot(fig3); plt.close()

# ════════════════════════════════════════════════════════════════════════════
# PAGE: SALES REP ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
elif page == "👥 Sales Rep Analysis":
    st.markdown("# 👥 Sales Rep Performance")
    st.markdown("---")

    rep = df.groupby('sales_rep').agg(
        revenue=('revenue','sum'),
        profit=('profit','sum'),
        orders=('order_id','count'),
        margin=('profit_margin','mean')
    ).reset_index().sort_values('revenue', ascending=False)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Top Sales Reps by Revenue</div>', unsafe_allow_html=True)
        set_dark_style()
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.barh(rep['sales_rep'], rep['revenue']/1e5, color=PALETTE[:len(rep)], edgecolor='#0a0a0f', height=0.6)
        ax.set_xlabel('Revenue (₹ Lakhs)')
        ax.set_title('Sales Rep Revenue', color='#6c63ff', fontsize=11)
        ax.grid(axis='x')
        fig.patch.set_facecolor('#12121f')
        st.pyplot(fig); plt.close()

    with col2:
        st.markdown('<div class="section-title">Profit vs Orders</div>', unsafe_allow_html=True)
        set_dark_style()
        fig2, ax2 = plt.subplots(figsize=(6, 5))
        scatter = ax2.scatter(rep['orders'], rep['profit']/1e5, s=rep['margin']*20,
                              c=PALETTE[:len(rep)], alpha=0.85, edgecolors='#fff', linewidth=0.5)
        for _, row in rep.iterrows():
            ax2.annotate(row['sales_rep'].split()[0], (row['orders'], row['profit']/1e5),
                        fontsize=7, color='#e8e8f0', xytext=(5, 5), textcoords='offset points')
        ax2.set_xlabel('Number of Orders')
        ax2.set_ylabel('Profit (₹ Lakhs)')
        ax2.set_title('Orders vs Profit (bubble = margin)', color='#6c63ff', fontsize=11)
        ax2.grid()
        fig2.patch.set_facecolor('#12121f')
        st.pyplot(fig2); plt.close()

    st.markdown('<div class="section-title">Leaderboard</div>', unsafe_allow_html=True)
    rep_display = rep.copy()
    rep_display['Rank'] = range(1, len(rep_display)+1)
    rep_display['revenue'] = rep_display['revenue'].apply(lambda x: f'₹{x/1e5:.1f}L')
    rep_display['profit'] = rep_display['profit'].apply(lambda x: f'₹{x/1e5:.1f}L')
    rep_display['margin'] = rep_display['margin'].apply(lambda x: f'{x:.1f}%')
    rep_display = rep_display[['Rank','sales_rep','revenue','profit','orders','margin']]
    rep_display.columns = ['Rank','Sales Rep','Revenue','Profit','Orders','Margin']
    st.dataframe(rep_display, use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE: PRODUCT INSIGHTS
# ════════════════════════════════════════════════════════════════════════════
elif page == "📦 Product Insights":
    st.markdown("# 📦 Product Insights")
    st.markdown("---")

    prod = df.groupby(['category', 'product']).agg(
        revenue=('revenue','sum'),
        profit=('profit','sum'),
        qty=('quantity','sum'),
        margin=('profit_margin','mean')
    ).reset_index()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Top 10 Products by Revenue</div>', unsafe_allow_html=True)
        top10 = prod.nlargest(10, 'revenue')
        set_dark_style()
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.barh(top10['product'], top10['revenue']/1e5, color='#6c63ff', edgecolor='#0a0a0f', height=0.6)
        ax.set_xlabel('Revenue (₹ Lakhs)')
        ax.set_title('Top 10 Products', color='#6c63ff', fontsize=11)
        ax.grid(axis='x')
        fig.patch.set_facecolor('#12121f')
        st.pyplot(fig); plt.close()

    with col2:
        st.markdown('<div class="section-title">Category Profit Margin Distribution</div>', unsafe_allow_html=True)
        set_dark_style()
        fig2, ax2 = plt.subplots(figsize=(6, 5))
        data_box = [df[df['category']==c]['profit_margin'].values for c in df['category'].unique()]
        bp = ax2.boxplot(data_box, labels=df['category'].unique(), patch_artist=True,
                         medianprops=dict(color='#fff', linewidth=2))
        for patch, color in zip(bp['boxes'], PALETTE):
            patch.set_facecolor(color); patch.set_alpha(0.7)
        ax2.set_ylabel('Profit Margin %')
        ax2.set_title('Margin Distribution', color='#6c63ff', fontsize=11)
        plt.xticks(rotation=20, fontsize=7)
        ax2.grid(axis='y')
        fig2.patch.set_facecolor('#12121f')
        st.pyplot(fig2); plt.close()

    st.markdown('<div class="section-title">All Products Summary</div>', unsafe_allow_html=True)
    prod_display = prod.sort_values('revenue', ascending=False).copy()
    prod_display['revenue'] = prod_display['revenue'].apply(lambda x: f'₹{x/1e5:.1f}L')
    prod_display['profit'] = prod_display['profit'].apply(lambda x: f'₹{x/1e5:.1f}L')
    prod_display['margin'] = prod_display['margin'].apply(lambda x: f'{x:.1f}%')
    prod_display.columns = ['Category','Product','Revenue','Profit','Qty Sold','Margin']
    st.dataframe(prod_display, use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE: KPI REPORT
# ════════════════════════════════════════════════════════════════════════════
elif page == "📋 KPI Report":
    st.markdown("# 📋 KPI Report")
    st.markdown("---")

    total_revenue = df['revenue'].sum()
    total_profit = df['profit'].sum()
    avg_margin = df['profit_margin'].mean()
    total_orders = len(df)
    yoy_rev = yoy_growth(df, 'revenue')
    yoy_prof = yoy_growth(df, 'profit')
    top_region = df.groupby('region')['revenue'].sum().idxmax()
    top_rep = df.groupby('sales_rep')['revenue'].sum().idxmax()
    top_cat = df.groupby('category')['revenue'].sum().idxmax()

    col1, col2, col3 = st.columns(3)
    kpis = [
        ("Total Revenue", f"₹{total_revenue/1e7:.2f} Cr", f"▲ {yoy_rev}% YoY"),
        ("Total Profit", f"₹{total_profit/1e7:.2f} Cr", f"▲ {yoy_prof}% YoY"),
        ("Avg Profit Margin", f"{avg_margin:.1f}%", "Across all categories"),
        ("Total Orders", f"{total_orders:,}", f"Avg ₹{total_revenue/total_orders:,.0f}/order"),
        ("Top Region", top_region, "By Revenue"),
        ("Top Sales Rep", top_rep, "By Revenue"),
        ("Top Category", top_cat, "By Revenue"),
        ("Avg Order Value", f"₹{total_revenue/total_orders:,.0f}", "Per transaction"),
        ("Revenue per Rep", f"₹{total_revenue/8/1e5:.1f}L", "Avg per sales rep"),
    ]

    for i, (label, value, delta) in enumerate(kpis):
        col = [col1, col2, col3][i % 3]
        with col:
            st.markdown(f"""<div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value" style="font-size:1.4rem">{value}</div>
                <div class="kpi-delta">{delta}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)
    st.markdown(f"""
    - **Total Revenue** of ₹{total_revenue/1e7:.2f} Crore achieved with **{yoy_rev}% YoY growth**
    - **Profit Margin** maintained at **{avg_margin:.1f}%** average across all segments
    - **{top_region}** region leads in revenue contribution
    - **{top_cat}** is the highest revenue-generating category
    - **{top_rep}** is the top performing sales representative
    - **{total_orders:,}** total orders processed with average order value of ₹{total_revenue/total_orders:,.0f}
    """)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Full Dataset", csv, "sales_data.csv", "text/csv")
