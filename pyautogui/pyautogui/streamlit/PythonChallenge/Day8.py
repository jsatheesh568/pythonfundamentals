import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="💱 Currency Converter Pro",
    page_icon="💰",
    layout="wide"
)

# Custom CSS for attractive styling
st.markdown("""
<style>
    .currency-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .rate-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 5px 0;
        box-shadow: 0 4px 15px 0 rgba(31, 38, 135, 0.2);
    }
    
    .conversion-result {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 30px;
        border-radius: 25px;
        color: white;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin: 20px 0;
        box-shadow: 0 10px 40px 0 rgba(31, 38, 135, 0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .flag {
        font-size: 2em;
        margin: 0 10px;
    }
    
    .trending-up { color: #00ff88; }
    .trending-down { color: #ff4757; }
    
    .stSelectbox > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
    }

    /* responsive tweaks */
    @media (max-width: 600px) {
        .flag { font-size: 1.6em; }
        .conversion-result { font-size: 18px; padding: 18px; }
    }
</style>
""", unsafe_allow_html=True)

# Exchange rates (static rates - in real app, you'd fetch from API)
EXCHANGE_RATES = {
    'INR': {'rate': 1.0, 'flag': '🇮🇳', 'name': 'Indian Rupee', 'symbol': '₹'},
    'USD': {'rate': 0.012, 'flag': '🇺🇸', 'name': 'US Dollar', 'symbol': '$'},
    'EUR': {'rate': 0.011, 'flag': '🇪🇺', 'name': 'Euro', 'symbol': '€'},
    'GBP': {'rate': 0.0095, 'flag': '🇬🇧', 'name': 'British Pound', 'symbol': '£'},
    'JPY': {'rate': 1.79, 'flag': '🇯🇵', 'name': 'Japanese Yen', 'symbol': '¥'},
    'CAD': {'rate': 0.016, 'flag': '🇨🇦', 'name': 'Canadian Dollar', 'symbol': 'C$'},
    'AUD': {'rate': 0.018, 'flag': '🇦🇺', 'name': 'Australian Dollar', 'symbol': 'A$'},
    'CHF': {'rate': 0.011, 'flag': '🇨🇭', 'name': 'Swiss Franc', 'symbol': 'CHF'},
    'CNY': {'rate': 0.087, 'flag': '🇨🇳', 'name': 'Chinese Yuan', 'symbol': '¥'},
    'SGD': {'rate': 0.016, 'flag': '🇸🇬', 'name': 'Singapore Dollar', 'symbol': 'S$'},
    'AED': {'rate': 0.044, 'flag': '🇦🇪', 'name': 'UAE Dirham', 'symbol': 'AED'},
    'KRW': {'rate': 15.8, 'flag': '🇰🇷', 'name': 'South Korean Won', 'symbol': '₩'},
}

# Initialize session state
if 'conversion_history' not in st.session_state:
    st.session_state.conversion_history = []
if 'favorite_pairs' not in st.session_state:
    st.session_state.favorite_pairs = []

def convert_currency(amount, from_currency, to_currency):
    """Convert currency using static rates"""
    # Convert to INR first (base currency)
    inr_amount = amount / EXCHANGE_RATES[from_currency]['rate']
    # Then convert to target currency
    converted_amount = inr_amount * EXCHANGE_RATES[to_currency]['rate']
    return converted_amount

def add_to_history(amount, from_cur, to_cur, result):
    """Add conversion to history"""
    history_entry = {
        'timestamp': datetime.now(),
        'amount': amount,
        'from_currency': from_cur,
        'to_currency': to_cur,
        'result': result,
        'rate': result / amount if amount != 0 else 0
    }
    st.session_state.conversion_history.insert(0, history_entry)
    # Keep only last 50 conversions
    if len(st.session_state.conversion_history) > 50:
        st.session_state.conversion_history = st.session_state.conversion_history[:50]

def create_rate_comparison_chart():
    """Create a comparison chart of all currencies against INR"""
    currencies = list(EXCHANGE_RATES.keys())
    rates = [EXCHANGE_RATES[curr]['rate'] for curr in currencies]
    flags = [EXCHANGE_RATES[curr]['flag'] for curr in currencies]
    
    # Create custom labels with flags
    labels = [f"{flag} {curr}" for flag, curr in zip(flags, currencies)]
    
    fig = px.bar(
        x=rates,
        y=labels,
        orientation='h',
        title='💹 Exchange Rates (1 INR = X Currency)',
        labels={'x': 'Exchange Rate', 'y': 'Currency'},
        color=rates,
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        height=500,
        showlegend=False,
        title_font_size=20,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_currency_strength_radar():
    """Create a radar chart showing currency strength"""
    currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD']
    
    # Simulate strength metrics (in real app, use economic indicators)
    strength_metrics = {
        'Economic Stability': [85, 80, 75, 70, 72, 68],
        'Inflation Rate': [88, 82, 78, 65, 75, 70],
        'Interest Rates': [75, 60, 80, 45, 70, 85],
        'Trade Balance': [70, 85, 65, 90, 80, 75],
        'Market Volatility': [80, 75, 70, 60, 72, 68]
    }
    
    fig = go.Figure()
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3']
    
    for i, currency in enumerate(currencies):
        values = [strength_metrics[metric][i] for metric in strength_metrics.keys()]
        values += values[:1]  # Close the polygon
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=list(strength_metrics.keys()) + [list(strength_metrics.keys())[0]],
            fill='toself',
            name=f"{EXCHANGE_RATES[currency]['flag']} {currency}",
            line_color=colors[i]
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="🎯 Currency Strength Analysis",
        title_font_size=20
    )
    
    return fig

def create_conversion_trend_chart():
    """Create a trend chart for conversion history"""
    if not st.session_state.conversion_history:
        return None
    
    df = pd.DataFrame(st.session_state.conversion_history)
    
    # Group by currency pair and time
    df['pair'] = df['from_currency'] + '/' + df['to_currency']
    df['hour'] = df['timestamp'].dt.floor('H')
    
    # Get most recent conversions per pair
    recent_conversions = df.groupby('pair').head(10)
    
    if len(recent_conversions) < 2:
        return None
    
    fig = px.line(
        recent_conversions, 
        x='timestamp', 
        y='rate', 
        color='pair',
        title='📈 Your Conversion History Trends',
        labels={'rate': 'Exchange Rate', 'timestamp': 'Time'}
    )
    
    fig.update_layout(height=400)
    return fig

def converter_tab():
    """Main currency converter interface"""
    st.markdown("""
    <div class="currency-card">
        <h1>💱 Currency Converter Pro</h1>
        <p>Convert between multiple currencies with real-time calculations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main conversion interface
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown("### From Currency")
        # keep key so selection persists in session_state
        from_currency = st.selectbox(
            "Select source currency",
            options=list(EXCHANGE_RATES.keys()),
            format_func=lambda x: f"{EXCHANGE_RATES[x]['flag']} {x} - {EXCHANGE_RATES[x]['name']}",
            key="from_currency"
        )
        
        from_info = EXCHANGE_RATES[from_currency]
        st.markdown(f"""
        <div class="rate-card">
            <div class="flag">{from_info['flag']}</div>
            <h3>{from_info['name']}</h3>
            <p>{from_info['symbol']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Amount")
        amount = st.number_input(
            "Enter amount to convert",
            min_value=0.01,
            value=100.0,
            step=0.01,
            format="%.2f",
            key="amount_input"
        )
        st.write("")  # spacer
        
        # NOTE: do not directly reference to_currency here; use session_state fallback in handler
        if st.button("🔄 Convert Now", type="primary"):
            if amount > 0:
                # read to_currency safely from session_state (fallback to second currency)
                to_cur = st.session_state.get('to_currency', list(EXCHANGE_RATES.keys())[1])
                from_cur = st.session_state.get('from_currency', list(EXCHANGE_RATES.keys())[0])
                result = convert_currency(amount, from_cur, to_cur)
                add_to_history(amount, from_cur, to_cur, result)
                st.session_state.last_conversion = {
                    'amount': amount,
                    'from': from_cur,
                    'to': to_cur,
                    'result': result
                }
                st.success(f"Converted {EXCHANGE_RATES[from_cur]['symbol']}{amount:,.2f} → {EXCHANGE_RATES[to_cur]['symbol']}{result:,.2f}")
    
    with col3:
        st.markdown("### To Currency")
        to_currency = st.selectbox(
            "Select target currency",
            options=list(EXCHANGE_RATES.keys()),
            format_func=lambda x: f"{EXCHANGE_RATES[x]['flag']} {x} - {EXCHANGE_RATES[x]['name']}",
            key="to_currency",
            index=1
        )
        
        to_info = EXCHANGE_RATES[to_currency]
        st.markdown(f"""
        <div class="rate-card">
            <div class="flag">{to_info['flag']}</div>
            <h3>{to_info['name']}</h3>
            <p>{to_info['symbol']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Ensure we have canonical variables (safe access after all selectboxes defined)
    from_currency = st.session_state.get('from_currency', list(EXCHANGE_RATES.keys())[0])
    to_currency = st.session_state.get('to_currency', list(EXCHANGE_RATES.keys())[1])
    amount = st.session_state.get('amount_input', 100.0)
    
    # Real-time conversion display
    if amount > 0:
        result = convert_currency(amount, from_currency, to_currency)
        rate = result / amount if amount != 0 else 0
        
        st.markdown(f"""
        <div class="conversion-result">
            <div style="font-size: 18px; opacity: 0.9;">
                {EXCHANGE_RATES[from_currency]['symbol']}{amount:,.2f} {from_currency}
            </div>
            <div style="font-size: 32px; margin: 10px 0;">
                ↓
            </div>
            <div style="font-size: 28px;">
                {EXCHANGE_RATES[to_currency]['symbol']}{result:,.2f} {to_currency}
            </div>
            <div style="font-size: 14px; opacity: 0.8; margin-top: 10px;">
                Exchange Rate: 1 {from_currency} = {rate:.6f} {to_currency}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick conversion buttons
    st.markdown("### ⚡ Quick Convert")
    quick_amounts = [10, 50, 100, 500, 1000, 5000]
    cols = st.columns(len(quick_amounts))
    
    for i, quick_amount in enumerate(quick_amounts):
        with cols[i]:
            if st.button(f"{EXCHANGE_RATES[from_currency]['symbol']}{quick_amount}", key=f"quick_{quick_amount}"):
                result = convert_currency(quick_amount, from_currency, to_currency)
                add_to_history(quick_amount, from_currency, to_currency, result)
                st.info(f"{EXCHANGE_RATES[to_currency]['symbol']}{result:,.2f}")

def rates_tab():
    """Exchange rates overview and comparison"""
    st.markdown("# 📊 Exchange Rates Overview")
    
    # Current rates table
    st.subheader("💹 Current Exchange Rates (Base: INR)")
    
    rate_data = []
    for currency, info in EXCHANGE_RATES.items():
        if currency != 'INR':
            rate_data.append({
                'Currency': f"{info['flag']} {currency}",
                'Name': info['name'],
                'Symbol': info['symbol'],
                'Rate (1 INR = X)': f"{info['rate']:.6f}",
                'Reverse (1 X = Y INR)': f"{1/info['rate']:.2f}" if info['rate'] != 0 else "N/A"
            })
    
    rates_df = pd.DataFrame(rate_data)
    st.dataframe(rates_df, use_container_width=True)
    
    # Rate comparison chart
    st.plotly_chart(create_rate_comparison_chart(), use_container_width=True)
    
    # Currency strength radar
    st.plotly_chart(create_currency_strength_radar(), use_container_width=True)
    
    # Popular currency pairs
    st.subheader("🔥 Popular Currency Pairs")
    
    popular_pairs = [
        ('USD', 'EUR'), ('USD', 'GBP'), ('EUR', 'GBP'),
        ('USD', 'JPY'), ('INR', 'USD'), ('INR', 'EUR')
    ]
    
    cols = st.columns(3)
    for i, (from_cur, to_cur) in enumerate(popular_pairs):
        with cols[i % 3]:
            rate = convert_currency(1, from_cur, to_cur)
            trend = random.choice(['up', 'down'])
            trend_icon = '📈' if trend == 'up' else '📉'
            trend_color = 'trending-up' if trend == 'up' else 'trending-down'
            
            st.markdown(f"""
            <div class="metric-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 16px; font-weight: bold;">
                            {EXCHANGE_RATES[from_cur]['flag']} {from_cur}/{to_cur} {EXCHANGE_RATES[to_cur]['flag']}
                        </div>
                        <div style="font-size: 20px; margin: 5px 0;">
                            {rate:.4f}
                        </div>
                    </div>
                    <div class="{trend_color}" style="font-size: 24px;">
                        {trend_icon}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def history_tab():
    """Conversion history and analytics"""
    st.markdown("# 📈 Conversion History")
    
    if not st.session_state.conversion_history:
        st.info("No conversion history yet. Start converting currencies to see your history!")
        return
    
    # Summary statistics
    df = pd.DataFrame(st.session_state.conversion_history)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Conversions", len(df))
    with col2:
        most_from = df['from_currency'].mode().iloc[0]
        st.metric("Most Used Source", f"{EXCHANGE_RATES[most_from]['flag']} {most_from}")
    with col3:
        most_to = df['to_currency'].mode().iloc[0]
        st.metric("Most Used Target", f"{EXCHANGE_RATES[most_to]['flag']} {most_to}")
    with col4:
        avg_amount = df['amount'].mean()
        st.metric("Avg Amount", f"₹{avg_amount:,.2f}")
    
    # Conversion trend chart
    trend_chart = create_conversion_trend_chart()
    if trend_chart:
        st.plotly_chart(trend_chart, use_container_width=True)
    
    # Recent conversions
    st.subheader("🕒 Recent Conversions")
    
    recent_df = df.head(20).copy()
    recent_df['timestamp'] = recent_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    recent_df['conversion'] = recent_df.apply(
        lambda row: f"{EXCHANGE_RATES[row['from_currency']]['symbol']}{row['amount']:,.2f} → {EXCHANGE_RATES[row['to_currency']]['symbol']}{row['result']:,.2f}",
        axis=1
    )
    
    display_df = recent_df[['timestamp', 'from_currency', 'to_currency', 'conversion', 'rate']].copy()
    display_df.columns = ['Time', 'From', 'To', 'Conversion', 'Rate']
    
    st.dataframe(display_df, use_container_width=True)
    
    # Export history
    if st.button("📥 Export History"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"currency_conversion_history_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

def calculator_tab():
    """Advanced currency calculator with multiple conversions"""
    st.markdown("# 🧮 Currency Calculator")
    
    st.markdown("### Multi-Currency Converter")
    st.info("Convert one amount to multiple currencies simultaneously")
    
    # Input section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        source_currency = st.selectbox(
            "Source Currency",
            options=list(EXCHANGE_RATES.keys()),
            format_func=lambda x: f"{EXCHANGE_RATES[x]['flag']} {x}",
            key="calc_source"
        )
        
        calc_amount = st.number_input(
            "Amount to Convert",
            min_value=0.01,
            value=1000.0,
            step=0.01,
            key="calc_amount"
        )
    
    with col2:
        target_currencies = st.multiselect(
            "Target Currencies",
            options=[cur for cur in EXCHANGE_RATES.keys() if cur != source_currency],
            format_func=lambda x: f"{EXCHANGE_RATES[x]['flag']} {x}",
            default=[cur for cur in ['USD', 'EUR', 'GBP'] if cur != source_currency][:3]
        )
    
    # Conversion results
    if calc_amount > 0 and target_currencies:
        st.markdown("### 💰 Conversion Results")
        
        results = []
        for target in target_currencies:
            converted = convert_currency(calc_amount, source_currency, target)
            rate = converted / calc_amount
            results.append({
                'Currency': f"{EXCHANGE_RATES[target]['flag']} {target}",
                'Amount': f"{EXCHANGE_RATES[target]['symbol']}{converted:,.2f}",
                'Rate': f"{rate:.6f}",
                'Change': f"{random.choice(['+', '-'])}{random.uniform(0.1, 2.5):.2f}%"
            })
        
        results_df = pd.DataFrame(results)
        st.dataframe(results_df, use_container_width=True)
        
        # Visual comparison
        # Convert amounts back to numbers for plotting
        y_vals = []
        for i, result in enumerate(results):
            # Extract numeric portion (safer than replace only)
            amt_str = result['Amount']
            # remove any non-numeric except dot and comma
            numeric = ''.join(ch for ch in amt_str if (ch.isdigit() or ch in '.,'))
            numeric = numeric.replace(',', '')
            try:
                y_vals.append(float(numeric))
            except:
                y_vals.append(0.0)
        
        fig = px.bar(
            x=[result['Currency'] for result in results],
            y=y_vals,
            title=f"💹 {EXCHANGE_RATES[source_currency]['symbol']}{calc_amount:,.2f} {source_currency} Converted",
            labels={'x': 'Target Currency', 'y': 'Converted Amount'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Currency comparison matrix
    st.markdown("### 📊 Currency Comparison Matrix")
    
    selected_currencies = st.multiselect(
        "Select currencies to compare",
        options=list(EXCHANGE_RATES.keys()),
        default=['INR', 'USD', 'EUR', 'GBP'],
        key="matrix_currencies"
    )
    
    if len(selected_currencies) >= 2:
        matrix_data = []
        for from_cur in selected_currencies:
            row = {}
            for to_cur in selected_currencies:
                if from_cur == to_cur:
                    row[to_cur] = 1.0
                else:
                    row[to_cur] = convert_currency(1, from_cur, to_cur)
            matrix_data.append(row)
        
        matrix_df = pd.DataFrame(matrix_data, index=selected_currencies)
        
        # Create heatmap
        fig = px.imshow(
            matrix_df.values,
            x=selected_currencies,
            y=selected_currencies,
            color_continuous_scale='viridis',
            title="Currency Exchange Rate Matrix",
            labels={'color': 'Exchange Rate'}
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Main application
def main():
    # Sidebar: favorites & quick actions
    st.sidebar.markdown("## ⭐ Quick Actions")
    st.sidebar.markdown("Bookmark favorite pairs for faster access.")
    fav_from = st.sidebar.selectbox(
        "Favorite From",
        options=list(EXCHANGE_RATES.keys()),
        format_func=lambda x: f"{EXCHANGE_RATES[x]['flag']} {x}",
        key="fav_from"
    )
    fav_to = st.sidebar.selectbox(
        "Favorite To",
        options=list(EXCHANGE_RATES.keys()),
        format_func=lambda x: f"{EXCHANGE_RATES[x]['flag']} {x}",
        key="fav_to",
        index=1
    )
    if st.sidebar.button("Use Favorite Pair"):
        # Set the app's selectboxes via session_state
        st.session_state.from_currency = fav_from
        st.session_state.to_currency = fav_to
        st.experimental_rerun()
    
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="color: #667eea;">💱 Currency Converter Pro</h1>
        <p style="font-size: 18px; color: #666;">Professional currency conversion with advanced analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔄 Converter",
        "📊 Rates",
        "📈 History",
        "🧮 Calculator"
    ])
    
    with tab1:
        converter_tab()
    
    with tab2:
        rates_tab()
    
    with tab3:
        history_tab()
    
    with tab4:
        calculator_tab()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>💡 <strong>Tip:</strong> Bookmark your favorite currency pairs for quick access!</p>
        <p>📱 This converter works great on mobile devices too!</p>
        <p style="font-size: 12px;">⚠️ Rates are for demonstration purposes. Use real financial data for actual transactions.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
