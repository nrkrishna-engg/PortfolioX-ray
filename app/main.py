import streamlit as st
import pandas as pd
import os
from dataprocessing import process_excel_file, calculate_exposure
from visualizations import plot_treemap
from styles import apply_custom_style


st.set_page_config(page_title="Portfolio X-ray", layout="wide")

# Display Banner Image
st.image("banner.png", use_container_width=True)

# Apply custom styling
st.markdown(apply_custom_style(), unsafe_allow_html=True)

    
def main():
    #st.title("Portfolio X-ray")

    # Add description with native Streamlit formatting
    st.markdown("""
    ## What is Portfolio X-ray?
    """)
    
    st.info("""
    An investor typically invests in a mixture of Mutual funds, ETFs, and individual stocks. Mutual funds and ETFs, in turn, invest in 
    individual stocks. Want to know what percentage of your portfolio is invested in individual stocks aggregated over all 
    your investments? This tool is for you.
    """)
    
    st.markdown("""
    ## How to use:
    You can input your investments in two ways:
    """)
    
    st.success("""
    1. **Manual Input**: Enter your investments directly in the form below
    2. **Excel File Upload**: Upload an Excel file with exactly 3 columns:
       * Column 1: Fund type (Use `MF` for mutual funds, `ETF` for exchange traded funds, `IS` for individual stocks)
       * Column 2: Ticker symbol
       * Column 3: Investment amount in dollars
    """)
    
    # Add a small checkbox for Excel upload option
    use_excel = st.checkbox("Use Excel file instead?")
    
    if use_excel:
        uploaded_file = st.file_uploader("Upload your portfolio Excel file", type=['xlsx', 'xls'])
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
                if len(df.columns) != 3:
                    st.error("Excel file must have exactly 3 columns: Fund Type (ETF/MF/IS), Ticker, Amount")
                    return
                etfs, mutualfunds, stocks = process_excel_file(df)
                
                if st.button("Take X-ray"):
                    exposure = calculate_exposure(etfs, mutualfunds, stocks)
                    
                    col_data, col_chart = st.columns([1, 1.5])
                    with col_data:
                        st.subheader("X-ray Data:")
                        exposure_df = pd.DataFrame(exposure.items(), columns=["Stock", "Portfolio Exposure (%)"])
                        exposure_df.index = exposure_df.index + 1
                        exposure_df["Portfolio Exposure (%)"] = exposure_df["Portfolio Exposure (%)"].round(2)
                        st.dataframe(exposure_df)
                    
                    with col_chart:
                        st.subheader("X-ray Tree map:")
                        treemap_img = plot_treemap(exposure)
                        st.image(treemap_img)
            
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    
    else:  # Manual Input (default)
        col1, col2, col3 = st.columns(3)
        
        # ETFs Input
        with col1:
            st.subheader("ETFs")
            etfs = []
            num_etfs = st.number_input("Number of ETFs", min_value=0, max_value=10, step=1, key="etf_count")
            for i in range(num_etfs):
                cols = st.columns([1, 2])
                ticker = cols[0].text_input(f"Ticker {i+1}", key=f"etf_ticker_{i}")
                amount = cols[1].number_input(f"Amount {i+1}", min_value=0.0, key=f"etf_amount_{i}")
                if ticker and amount:
                    etfs.append({"ticker": ticker, "amount": amount})

        # Mutual Funds Input
        with col2:
            st.subheader("Mutual Funds")
            mutualfunds = []
            num_mutualfunds = st.number_input("Number of Mutual Funds", min_value=0, max_value=10, step=1, key="mf_count")
            for i in range(num_mutualfunds):
                cols = st.columns([1, 2])
                ticker = cols[0].text_input(f"Ticker {i+1}", key=f"mf_ticker_{i}")
                amount = cols[1].number_input(f"Amount {i+1}", min_value=0.0, key=f"mf_amount_{i}")
                if ticker and amount:
                    mutualfunds.append({"ticker": ticker, "amount": amount})

        # Stocks Input
        with col3:
            st.subheader("Stocks")
            stocks = []
            num_stocks = st.number_input("Number of Stocks", min_value=0, max_value=10, step=1, key="stock_count")
            for i in range(num_stocks):
                cols = st.columns([1, 2])
                ticker = cols[0].text_input(f"Ticker {i+1}", key=f"stock_ticker_{i}")
                amount = cols[1].number_input(f"Amount {i+1}", min_value=0.0, key=f"stock_amount_{i}")
                if ticker and amount:
                    stocks.append({"ticker": ticker, "amount": amount})

        if st.button("Take X-ray"):
            if not (etfs or mutualfunds or stocks):
                st.warning("Please add at least one asset.")
            else:
                exposure = calculate_exposure(etfs, mutualfunds, stocks)
                
                col_data, col_chart = st.columns([1, 1.5])
                with col_data:
                    st.subheader("X-ray Data:")
                    exposure_df = pd.DataFrame(exposure.items(), columns=["Stock", "Portfolio Exposure (%)"])
                    exposure_df.index = exposure_df.index + 1
                    exposure_df["Portfolio Exposure (%)"] = exposure_df["Portfolio Exposure (%)"].round(2)
                    st.dataframe(exposure_df)
                
                with col_chart:
                    st.subheader("X-ray Tree map:")
                    treemap_img = plot_treemap(exposure)
                    st.image(treemap_img)

if __name__ == "__main__":
    main()
    