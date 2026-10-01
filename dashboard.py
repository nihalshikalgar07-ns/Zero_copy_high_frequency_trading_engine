import os
import time
import streamlit as st
import pandas as pd

from mmap_reader import MMapReader
from engine import TradeEngine

st.set_page_config(
    page_title="HFT Engine Dashboard",
    page_icon="⚡",
    layout="wide"
)




st.title("HFT Matching Engine Dashboard")

st.caption(
    "mmap → Order Reader → Trade Engine → Matching Engine"
)



# SESSION STATE

if "results" not in st.session_state:
    st.session_state.results = []

if "running" not in st.session_state:
    st.session_state.running = False


# SIDEBAR

st.sidebar.header("Engine Control")

mmap_file = st.sidebar.text_input(
    "mmap file",
    "orders.mmap"
)


# START ENGINE

if st.sidebar.button("Start Engine"):

    if not os.path.exists(mmap_file):

        st.sidebar.error(
            f"{mmap_file} not found"
        )

    else:

        st.session_state.results = []

        reader = MMapReader(mmap_file)
        engine = TradeEngine()

        while True:

            order = reader.read_order()

            if order is None:
                break

            result = engine.process_order(order)

            st.session_state.results.append(result)

        reader.close()

        st.sidebar.success(
            "Engine processing completed"
        )


# CLEAR

if st.sidebar.button("Clear Results"):

    st.session_state.results = []


# GET RESULTS


results = st.session_state.results


# CALCULATE METRICS

total_orders = len(results)

total_trades = sum(
    len(result["trades"])
    for result in results
)

latencies = [
    result["engine_latency_ns"]
    for result in results
]


if latencies:

    avg_latency = sum(latencies) / len(latencies)

    min_latency = min(latencies)

    max_latency = max(latencies)

else:

    avg_latency = 0
    min_latency = 0
    max_latency = 0


# TOP METRICS

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Orders",
        total_orders
    )


with col2:

    st.metric(
        "Executed Trades",
        total_trades
    )


with col3:

    st.metric(
        "Avg Latency",
        f"{avg_latency:.0f} ns"
    )


with col4:

    st.metric(
        "Min Latency",
        f"{min_latency} ns"
    )


# MAX LATENCY

st.metric(
    "Max Latency",
    f"{max_latency} ns"
)


st.divider()


# ORDER TABLE

st.subheader("Orders")


if results:

    order_data = []

    for result in results:

        order_data.append({

            "Order ID":
                result["order_id"],

            "Side":
                "BUY"
                if result["side"] == "B"
                else "SELL",

            "Price":
                result["price"],

            "Remaining Qty":
                result["quantity"],

            "Entry (ns)":
                result["engine_entry_ns"],

            "Exit (ns)":
                result["engine_exit_ns"],

            "Latency (ns)":
                result["engine_latency_ns"],

            "Trades":
                len(result["trades"])
        })


    order_df = pd.DataFrame(order_data)

    st.dataframe(
        order_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No orders processed yet."
    )


# TRADE TABLE

st.subheader("💱 Executed Trades")


all_trades = []


for result in results:

    for trade in result["trades"]:

        all_trades.append({

            "BUY Order":
                trade["buy_order_id"],

            "SELL Order":
                trade["sell_order_id"],

            "Price":
                trade["price"],

            "Quantity":
                trade["quantity"]
        })


if all_trades:

    trade_df = pd.DataFrame(
        all_trades
    )

    st.dataframe(
        trade_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No trades executed."
    )



# LATENCY GRAPH

st.subheader("📈 Engine Latency")


if results:

    latency_df = pd.DataFrame({

        "Order":
            [
                result["order_id"]
                for result in results
            ],

        "Latency (ns)":
            [
                result["engine_latency_ns"]
                for result in results
            ]
    })

    latency_df = latency_df.set_index("Order")

    st.line_chart(
        latency_df
    )

else:

    st.info(
        "Latency graph will appear after processing orders."
    )


# ENGINE STATUS

st.divider()

if results:

    st.success(
        "ENGINE STATUS: COMPLETED"
    )

else:

    st.warning(
        "ENGINE STATUS: IDLE"
    )