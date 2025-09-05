import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# ---------------------------
# Helper functions
# ---------------------------

def normalize_nse_ticker(ticker: str):
    ticker = ticker.strip().upper()
    if not ticker:
        return ""
    if "." not in ticker:
        ticker = ticker + ".NS"
    return ticker

@st.cache_data(show_spinner=False)
def fetch_data(ticker: str, start_date: str, end_date: str):
    try:
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        if data.empty:
            return None
        data.index = pd.to_datetime(data.index)
        return data
    except Exception:
        return None

def add_technical_indicators(df: pd.DataFrame, sma_short=20, sma_long=50):
    df = df.copy()
    df[f"SMA_{sma_short}"] = df["Close"].rolling(window=sma_short, min_periods=1).mean()
    df[f"SMA_{sma_long}"] = df["Close"].rolling(window=sma_long, min_periods=1).mean()
    df["Signal"] = 0
    df.loc[df[f"SMA_{sma_short}"] > df[f"SMA_{sma_long}"], "Signal"] = 1
    df.loc[df[f"SMA_{sma_short}"] < df[f"SMA_{sma_long}"], "Signal"] = -1
    df["Crossover"] = df["Signal"].diff().fillna(0)
    return df

def generate_trade_points(df: pd.DataFrame):
    buys = df[df["Crossover"] == 2]
    sells = df[df["Crossover"] == -2]
    return buys, sells

def create_lag_features(df: pd.DataFrame, lags=5):
    df = df.copy()
    for lag in range(1, lags+1):
        df[f"lag_{lag}"] = df["Close"].shift(lag)
    df = df.dropna()
    return df

def train_predict_lr(df: pd.DataFrame, lags=5, predict_days=5):
    """
    Simple Linear Regression on lag features to predict next day's Close.
    Then recursively predict predict_days ahead.
    """
    df_feat = create_lag_features(df, lags=lags)
    X = df_feat[[f"lag_{i}" for i in range(1, lags+1)]].values
    y = df_feat["Close"].values
    if len(X) < 20:
        return None, None, None
    model = LinearRegression()
    model.fit(X, y)
    last_row = df_feat.iloc[-1]
    preds = []
    # ensure 1-D array of lags
    current_input = np.array([last_row[f"lag_{i}"] for i in range(1, lags+1)]).ravel()
    for i in range(predict_days):
        p = float(model.predict(current_input.reshape(1, -1))[0])
        preds.append(p)
        # slide lags - ensure flatten
        new_lags = np.concatenate((np.array([p]), current_input[:-1].ravel()))
        current_input = new_lags
    y_pred_in_sample = model.predict(X)
    rmse = float(np.sqrt(mean_squared_error(y, y_pred_in_sample)))
    return preds, model, rmse

def compute_portfolio_metrics(price_df: pd.DataFrame, weights: np.ndarray, trading_days=252):
    daily_returns = price_df.pct_change().dropna()
    port_returns = daily_returns.dot(weights)
    cum_returns = (1 + port_returns).cumprod()
    total_return = cum_returns.iloc[-1] - 1
    days = (price_df.index[-1] - price_df.index[0]).days
    years = days / 365.25 if days > 0 else 1/365.25
    cagr = (1 + total_return) ** (1/years) - 1 if years > 0 else 0.0
    ann_vol = port_returns.std() * np.sqrt(trading_days)
    ann_return = port_returns.mean() * trading_days
    sharpe = (ann_return / ann_vol) if ann_vol != 0 else np.nan
    rolling_max = cum_returns.cummax()
    drawdown = cum_returns / rolling_max - 1
    max_dd = drawdown.min()
    metrics = {
        "Total Return": float(total_return),
        "CAGR": float(cagr),
        "Annual Return": float(ann_return),
        "Annual Volatility": float(ann_vol),
        "Sharpe Ratio": float(sharpe) if not np.isnan(sharpe) else None,
        "Max Drawdown": float(max_dd)
    }
    return metrics, port_returns, cum_returns

def plot_price_with_signals(df: pd.DataFrame, buys: pd.DataFrame, sells: pd.DataFrame, sma_short, sma_long):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df["Close"], label="Close")
    ax.plot(df.index, df[f"SMA_{sma_short}"], label=f"SMA_{sma_short}")
    ax.plot(df.index, df[f"SMA_{sma_long}"], label=f"SMA_{sma_long}")
    if not buys.empty:
        ax.scatter(buys.index, buys["Close"], marker="^", color="green", s=80, label="Buy")
    if not sells.empty:
        ax.scatter(sells.index, sells["Close"], marker="v", color="red", s=80, label="Sell")
    ax.set_title("Price with SMA and Buy/Sell signals")
    ax.legend()
    ax.grid(True)
    return fig

# ---------------------------
# Streamlit UI
# ---------------------------

st.set_page_config(page_title="Indian Stock Predictor & Portfolio Analyzer", layout="wide")
st.title("📈 Indian Stock Price Predictor & Portfolio Analyzer (Educational Demo)")

st.sidebar.header("Inputs")
tickers_input = st.sidebar.text_input("Enter NSE tickers (comma separated, e.g., RELIANCE, TCS, INFY)", value="RELIANCE, TCS")
start_date = st.sidebar.date_input("Start date", value=datetime.today() - timedelta(days=365*2))
end_date = st.sidebar.date_input("End date", value=datetime.today())
sma_short = st.sidebar.number_input("SMA short window (days)", min_value=5, max_value=200, value=20)
sma_long = st.sidebar.number_input("SMA long window (days)", min_value=10, max_value=400, value=50)
predict_days = st.sidebar.number_input("Forecast horizon (days)", min_value=1, max_value=30, value=5)
lags = st.sidebar.number_input("Lag features for LR model", min_value=1, max_value=20, value=5)
investment_amt = st.sidebar.number_input("Investment amount (INR)", min_value=1000.0, value=100000.0, step=1000.0)
run_button = st.sidebar.button("Run Analysis")

st.sidebar.markdown("---")
st.sidebar.markdown("**Disclaimer:** Educational only. Not financial advice.")

if run_button:
    with st.spinner("Fetching data..."):
        tickers = [normalize_nse_ticker(t) for t in tickers_input.split(",") if t.strip()]
        data_map = {}
        failed = []
        for t in tickers:
            df = fetch_data(t, start_date.strftime("%Y-%m-%d"), (end_date + timedelta(days=1)).strftime("%Y-%m-%d"))
            if df is None or df.empty:
                failed.append(t)
            else:
                data_map[t] = df
    if failed:
        st.error(f"Failed to fetch data for: {', '.join(failed)}.")
    if not data_map:
        st.stop()

    st.success("Data fetched successfully.")
    primary_ticker = tickers[0]
    st.header(f"Single Stock Analysis — {primary_ticker}")

    df_primary = data_map[primary_ticker].copy()
    df_primary = add_technical_indicators(df_primary, sma_short=sma_short, sma_long=sma_long)
    buys, sells = generate_trade_points(df_primary)

    latest_signal = df_primary["Signal"].iloc[-1]
    signal_text = "BUY" if latest_signal == 1 else ("SELL" if latest_signal == -1 else "HOLD/NEUTRAL")
    st.metric(label="Latest SMA Signal", value=signal_text)

    fig = plot_price_with_signals(df_primary, buys, sells, sma_short, sma_long)
    st.pyplot(fig)

    st.subheader("Recent Buy/Sell points (last 30 rows)")
    recent_bs = pd.concat([
        buys[["Close"]].rename(columns={"Close": "Buy_Price"}) if not buys.empty else pd.DataFrame(),
        sells[["Close"]].rename(columns={"Close": "Sell_Price"}) if not sells.empty else pd.DataFrame()
    ], axis=1).dropna(how='all').tail(30)
    st.dataframe(recent_bs)

    st.subheader("Short-term Price Prediction (Simple Linear Regression on lags)")
    preds, model, rmse = train_predict_lr(df_primary, lags=lags, predict_days=predict_days)
    if preds is None:
        st.info("Not enough data for prediction with chosen lag size.")
    else:
        last_date = df_primary.index[-1]
        pred_index = [last_date + timedelta(days=i+1) for i in range(len(preds))]
        pred_series = pd.Series(data=preds, index=pred_index)
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.plot(df_primary.index[-60:], df_primary["Close"].iloc[-60:], label="Recent Close")
        ax2.plot(pred_series.index, pred_series.values, marker='o', linestyle='--', label="Predicted Close")
        ax2.set_title("Recent Close and Predicted Prices")
        ax2.legend()
        ax2.grid(True)
        st.pyplot(fig2)
        st.write(f"Model in-sample RMSE: {rmse:.4f}")

        last_pred = float(preds[-1])
        last_actual = float(df_primary["Close"].iloc[-1])
        if last_pred > last_actual:
            st.success("Prediction suggests upward short-term trend (educational).")
        else:
            st.warning("Prediction suggests downward/flat short-term trend (educational).")

    st.header("Portfolio Analysis")

    # --------- FIXED: build list of 1-D Series with explicit names ----------
    series_list = []
    for t in data_map.keys():
        s = data_map[t]["Close"]
        # if for some reason Close is a DataFrame (rare), take its first column
        if isinstance(s, pd.DataFrame):
            # try to extract first column as series
            s = s.iloc[:, 0]
        # ensure it's a Series
        s = s.copy()
        s.name = t  # set series name to ticker
        series_list.append(s)
    # concat along columns, inner-join by default (align on index)
    if series_list:
        all_close = pd.concat(series_list, axis=1, join='inner').dropna(how='all')
    else:
        st.error("No price series available for portfolio.")
        st.stop()
    # --------------------------------------------------------------------

    # Input weights: user-provided or equal weights
    weight_input = st.text_input("Portfolio weights (comma separated in same order as tickers) or leave blank for equal weights:", value="")
    if weight_input.strip():
        try:
            ws = [float(x) for x in weight_input.split(",")]
            weights = np.array(ws) / np.sum(ws)
        except Exception:
            st.error("Invalid weights. Using equal weights.")
            weights = np.array([1/len(all_close.columns)]*len(all_close.columns))
    else:
        weights = np.array([1/len(all_close.columns)]*len(all_close.columns))

    metrics, port_returns, cum_returns = compute_portfolio_metrics(all_close, weights)
    st.subheader("Portfolio Metrics")
    metrics_display = {
        "Total Return (%)": round(metrics["Total Return"]*100, 2),
        "CAGR (%)": round(metrics["CAGR"]*100, 2),
        "Annual Return (%)": round(metrics["Annual Return"]*100, 2),
        "Annual Volatility (%)": round(metrics["Annual Volatility"]*100, 2),
        "Sharpe Ratio": round(metrics["Sharpe Ratio"], 3) if metrics["Sharpe Ratio"] is not None else None,
        "Max Drawdown (%)": round(metrics["Max Drawdown"]*100, 2)
    }
    st.table(pd.DataFrame.from_dict(metrics_display, orient='index', columns=["Value"]))

    fig3, ax3 = plt.subplots(figsize=(10, 5))
    for col in all_close.columns:
        (all_close[col].pct_change().dropna().add(1).cumprod()-1).plot(ax=ax3, label=col)
    cum_returns.plot(ax=ax3, label="Portfolio", linewidth=2, linestyle='--', color='black')
    ax3.set_title("Cumulative Returns")
    ax3.legend()
    ax3.grid(True)
    st.pyplot(fig3)

    st.subheader("Allocation")
    alloc_df = pd.DataFrame({
        "Ticker": all_close.columns,
        "Weight": weights
    })
    st.write(alloc_df.set_index("Ticker"))

    latest_prices = all_close.iloc[-1]
    num_shares = (weights * investment_amt) / latest_prices.values
    port_value_df = (num_shares * all_close).sum(axis=1)
    fig4, ax4 = plt.subplots(figsize=(10,4))
    ax4.plot(port_value_df.index, port_value_df.values)
    ax4.set_title(f"Simulated Portfolio Value (initial {investment_amt:.0f} INR)")
    ax4.grid(True)
    st.pyplot(fig4)

    agg_signals = []
    for t in all_close.columns:
        df_tmp = add_technical_indicators(data_map[t], sma_short=sma_short, sma_long=sma_long)
        agg_signals.append(df_tmp["Signal"].iloc[-1])
    agg_sum = sum(agg_signals)
    if agg_sum > 0:
        st.success("Portfolio-level signal: MORE BUY signals (educational).")
    elif agg_sum < 0:
        st.warning("Portfolio-level signal: MORE SELL signals (educational).")
    else:
        st.info("Portfolio-level signal: Neutral/Mixed signals.")

    st.markdown("---")
    st.info("Again — this tool is a learning/demo app. Do not use this alone to trade.")
