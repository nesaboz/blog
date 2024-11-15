import streamlit as st
import numpy as np
import numpy_financial as npf
import pandas as pd
import altair as alt

def main():
    st.title("Investment Strategies Comparison with Home Purchase Decision")

    # Input parameters
    st.sidebar.header("Input Parameters")

    # Monthly income parameter
    monthly_income = st.sidebar.number_input(
        "Monthly Income ($)",
        value=10000,  # Default value
        step=1000
    )

    # Monthly expenses parameter
    monthly_expenses = st.sidebar.number_input(
        "Monthly Expenses ($)",
        value=3000,  # Default value
        step=100
    )

    # Home price
    home_price = st.sidebar.number_input("Home Price ($)", value=2500000, step=10000)

    # Down payment
    down_payment = st.sidebar.number_input("Down Payment ($)", value=500000, step=10000)

    # Loan amount
    loan_amount = home_price - down_payment
    st.sidebar.write(f"Loan Amount: ${loan_amount:,.2f}")

    # Interest rate
    annual_interest_rate = st.sidebar.slider(
        "Annual Interest Rate (%)",
        min_value=0.0,
        max_value=10.0,
        value=6.7,
        step=0.1
    )
    monthly_interest_rate = annual_interest_rate / 100 / 12

    # Loan term
    loan_term_years = st.sidebar.slider(
        "Loan Term (Years)",
        min_value=1,
        max_value=30,
        value=30,
        step=1
    )
    loan_term_months = loan_term_years * 12

    # Tax rate
    tax_rate = st.sidebar.slider(
        "Marginal Tax Rate (%)",
        min_value=0.0,
        max_value=50.0,
        value=40.0,
        step=0.1
    ) / 100

    # Investment return rate
    investment_return_rate = st.sidebar.slider(
        "Investment Return Rate (%)",
        min_value=0.0,
        max_value=20.0,
        value=6.7,
        step=0.1
    ) / 100  # Convert percentage to decimal

    # House appreciation rate
    house_appreciation_rate = st.sidebar.slider(
        "Annual House Appreciation Rate (%)",
        min_value=0.0,
        max_value=20.0,
        value=6.7,  # Default to 6.7%
        step=0.1
    ) / 100  # Convert percentage to decimal

    # Annual rent increase rate
    annual_rent_increase_rate = st.sidebar.slider(
        "Annual Rent Increase Rate (%)",
        min_value=0.0,
        max_value=10.0,
        value=2.0,
        step=0.1
    ) / 100  # Convert percentage to decimal

    # Starting monthly rent
    initial_rent = st.sidebar.number_input(
        "Starting Monthly Rent ($)",
        value=6100,
        step=100
    )

    # Property tax rate (fixed at 1.1%)
    property_tax_rate = 1.1 / 100  # 1.1%

    # Annual upkeeping cost
    upkeeping = st.sidebar.number_input(
        "Annual Upkeeping Cost ($)",
        value=10000,
        step=1000
    )
    monthly_upkeeping_cost = upkeeping / 12

    # Maximum number of years to display in the plot
    max_years = st.sidebar.number_input(
        "Maximum Years to Plot",
        min_value=1,
        max_value=loan_term_years,
        value=5,  # Default to 5 years
        step=1
    )

    # Number of years until selling the house
    sell_in_years = st.sidebar.number_input(
        "Years Until House Sale",
        min_value=1,
        max_value=loan_term_years,
        value=5,  # Default to 5 years
        step=1
    )
    sell_in_months = int(sell_in_years * 12)

    # Calculate monthly payment
    monthly_payment = npf.pmt(monthly_interest_rate, loan_term_months, -loan_amount)

    st.write(f"### Monthly Mortgage Payment: ${monthly_payment:,.2f}")

    # Amortization schedule
    schedule = amortization_schedule(loan_amount, monthly_interest_rate, loan_term_months)

    # Limit interest deduction to interest on $750,000 of mortgage debt
    max_deductible_loan = min(loan_amount, 750000)
    max_deductible_interest = calculate_total_interest(
        max_deductible_loan,
        monthly_interest_rate,
        loan_term_months
    )

    # Total interest paid
    total_interest = schedule['Interest'].sum()
    st.write(f"**Total Interest Paid Over the Loan Term:** ${total_interest:,.2f}")

    # Tax savings
    annual_deductible_interest = min(
        schedule['Interest'][:12].sum(),
        max_deductible_interest / loan_term_years
    )
    annual_tax_savings = annual_deductible_interest * tax_rate
    st.write(f"**Estimated Annual Tax Savings from Mortgage Interest Deduction:** ${annual_tax_savings:,.2f}")

    # Calculate house value over time
    house_value_schedule = house_value_over_time(home_price, house_appreciation_rate, loan_term_months)

    # Create property tax schedule with corrected function
    property_tax_schedule_df = property_tax_schedule(loan_term_months, home_price, property_tax_rate)

    # Create upkeeping schedule
    upkeeping_schedule_df = upkeeping_schedule(loan_term_months, monthly_upkeeping_cost)

    # Combine schedules
    combined_schedule = pd.merge(schedule, house_value_schedule, on='Month')
    combined_schedule = pd.merge(combined_schedule, property_tax_schedule_df, on='Month')
    combined_schedule = pd.merge(combined_schedule, upkeeping_schedule_df, on='Month')

    # Add cumulative property tax and upkeeping costs
    combined_schedule['Cumulative Property Tax'] = combined_schedule['Monthly Property Tax'].cumsum()
    combined_schedule['Cumulative Upkeeping Costs'] = combined_schedule['Monthly Upkeeping Cost'].cumsum()

    # Add 'Year' column
    combined_schedule['Year'] = combined_schedule['Month'] / 12
    schedule['Year'] = schedule['Month'] / 12

    # Generate investment strategies
    investment_strategy1_df, investment_strategy2_df = investment_strategies(
        loan_term_months,
        monthly_income,
        monthly_expenses,
        monthly_payment,
        property_tax_schedule_df['Monthly Property Tax'],
        monthly_upkeeping_cost,
        investment_return_rate
    )

    # Checkbox options for each line
    st.sidebar.header("Plot Options")
    show_house_value = st.sidebar.checkbox("Show House Value", value=True)
    show_cumulative_property_tax = st.sidebar.checkbox("Show Cumulative Property Tax", value=False)
    show_cumulative_upkeeping = st.sidebar.checkbox("Show Cumulative Upkeeping Costs", value=False)
    show_investment_strategy1 = st.sidebar.checkbox("Show Investment Strategy 1 (No House Purchase)", value=True)
    show_investment_strategy2 = st.sidebar.checkbox("Show Investment Strategy 2 (After House Expenses)", value=True)

    # Initialize plot data with 'Year' and 'Month'
    plot_data = combined_schedule[['Month', 'Year']].copy()
    plot_data['Month'] = plot_data['Month'].astype(int)

    # Add data based on selected checkboxes
    if show_house_value:
        plot_data['House Value'] = combined_schedule['House Value']

    if show_cumulative_property_tax:
        plot_data['Cumulative Property Tax'] = combined_schedule['Cumulative Property Tax']

    if show_cumulative_upkeeping:
        plot_data['Cumulative Upkeeping Costs'] = combined_schedule['Cumulative Upkeeping Costs']

    if show_investment_strategy1:
        plot_data = plot_data.merge(investment_strategy1_df[['Month', 'Investment Balance (No House Purchase)']], on='Month', how='left')

    if show_investment_strategy2:
        plot_data = plot_data.merge(investment_strategy2_df[['Month', 'Investment Balance (After House Expenses)']], on='Month', how='left')

    # Limit the data to max_years
    plot_data = plot_data[plot_data['Year'] <= max_years]

    # Melt data for plotting
    plot_data_melted = plot_data.melt('Year', var_name='Type', value_name='Amount')

    # Plot the selected data
    chart = alt.Chart(plot_data_melted).mark_line().encode(
        x=alt.X('Year', title='Year'),
        y=alt.Y('Amount', title='Amount ($)'),
        color='Type'
    ).properties(
        width=700,
        height=400,
        title='Investment Strategies and House Value Over Time'
    )

    st.altair_chart(chart, use_container_width=True)

    # Investment balances at the time of sale
    investment_balance_strategy1_at_sale = investment_strategy1_df.loc[sell_in_months - 1, 'Investment Balance (No House Purchase)']
    investment_balance_strategy2_at_sale = investment_strategy2_df.loc[sell_in_months - 1, 'Investment Balance (After House Expenses)']

    # Calculations at the time of sale
    sale_house_value = house_value_schedule.loc[sell_in_months - 1, 'House Value']
    brokerage_fee = 0.06 * sale_house_value
    remaining_mortgage_balance = schedule.loc[sell_in_months - 1, 'Balance']
    net_proceeds = sale_house_value - brokerage_fee - remaining_mortgage_balance

    cumulative_interest_paid = schedule.loc[:sell_in_months - 1, 'Interest'].sum()
    cumulative_principal_paid = schedule.loc[:sell_in_months - 1, 'Principal'].sum()

    # Cumulative property tax and upkeeping costs up to the time of sale
    cumulative_property_tax_paid = property_tax_schedule_df.loc[:sell_in_months - 1, 'Monthly Property Tax'].sum()
    cumulative_upkeeping_paid = upkeeping_schedule_df.loc[:sell_in_months - 1, 'Monthly Upkeeping Cost'].sum()

    # Total costs incurred
    total_costs_incurred = (
        down_payment +
        cumulative_principal_paid +
        cumulative_interest_paid +
        cumulative_property_tax_paid +
        cumulative_upkeeping_paid
    )

    # Net Gain/Loss
    net_gain_loss = net_proceeds - total_costs_incurred

    # Total money after selling the house
    total_money_after_sale = net_proceeds

    # Display updated financial summary
    st.write(f"## Financial Summary at Year {sell_in_years}")
    st.write(f"**Investment Balance (No House Purchase) at Sale:** ${investment_balance_strategy1_at_sale:,.2f}")
    st.write(f"**Investment Balance (After House Expenses) at Sale:** ${investment_balance_strategy2_at_sale:,.2f}")
    st.write(f"**House Value at Sale:** ${sale_house_value:,.2f}")
    st.write(f"**Brokerage Fee (6%):** ${brokerage_fee:,.2f}")
    st.write(f"**Remaining Mortgage Balance:** ${remaining_mortgage_balance:,.2f}")
    st.write(f"**Net Proceeds from Sale:** ${net_proceeds:,.2f}")
    st.write(f"**Cumulative Interest Paid:** ${cumulative_interest_paid:,.2f}")
    st.write(f"**Cumulative Principal Paid:** ${cumulative_principal_paid:,.2f}")
    st.write(f"**Cumulative Property Tax Paid:** ${cumulative_property_tax_paid:,.2f}")
    st.write(f"**Cumulative Upkeeping Costs Paid:** ${cumulative_upkeeping_paid:,.2f}")
    st.write(f"**Total Costs Incurred (Down Payment + Mortgage Payments + Property Tax + Upkeeping):** ${total_costs_incurred:,.2f}")
    st.write(f"**Net Gain/Loss (Net Proceeds - Total Costs Incurred):** ${net_gain_loss:,.2f}")
    st.write(f"**Total Money After Sale:** ${total_money_after_sale:,.2f}")

    # Display amortization schedule
    if st.checkbox("Show Amortization Schedule"):
        # Optionally, limit the amortization schedule displayed to max_years
        display_schedule = schedule[schedule['Year'] <= max_years]
        st.dataframe(display_schedule.style.format({
            'Principal': '${:,.2f}',
            'Interest': '${:,.2f}',
            'Cumulative Principal': '${:,.2f}',
            'Cumulative Interest': '${:,.2f}',
            'Balance': '${:,.2f}',
            'Year': '{:.2f}'
        }))

def amortization_schedule(loan_amount, monthly_interest_rate, loan_term_months):
    balance = loan_amount
    schedule = []
    cumulative_interest = 0
    cumulative_principal = 0
    monthly_payment = npf.pmt(monthly_interest_rate, loan_term_months, -loan_amount)

    for n in range(1, loan_term_months + 1):
        interest = balance * monthly_interest_rate
        principal = monthly_payment - interest
        balance -= principal
        cumulative_interest += interest
        cumulative_principal += principal
        schedule.append({
            'Month': n,
            'Principal': principal,
            'Interest': interest,
            'Cumulative Principal': cumulative_principal,
            'Cumulative Interest': cumulative_interest,
            'Balance': max(balance, 0),
            'Year': n / 12
        })
    return pd.DataFrame(schedule)

def calculate_total_interest(loan_amount, monthly_interest_rate, loan_term_months):
    monthly_payment = npf.pmt(monthly_interest_rate, loan_term_months, -loan_amount)
    total_payment = monthly_payment * loan_term_months
    total_interest = total_payment - loan_amount
    return total_interest

def house_value_over_time(initial_value, appreciation_rate, loan_term_months):
    house_values = []
    value = initial_value
    monthly_appreciation_rate = (1 + appreciation_rate) ** (1/12) - 1
    for n in range(1, loan_term_months + 1):
        value *= (1 + monthly_appreciation_rate)
        house_values.append({
            'Month': n,
            'House Value': value
        })
    return pd.DataFrame(house_values)

def property_tax_schedule(loan_term_months, home_price, property_tax_rate):
    property_taxes = []
    monthly_property_tax = home_price * property_tax_rate / 12
    for i in range(1, loan_term_months + 1):
        property_taxes.append({
            'Month': i,
            'Monthly Property Tax': monthly_property_tax
        })
    return pd.DataFrame(property_taxes)

def upkeeping_schedule(loan_term_months, monthly_upkeeping_cost):
    upkeeping_list = []
    for month in range(1, loan_term_months + 1):
        upkeeping_list.append({
            'Month': month,
            'Monthly Upkeeping Cost': monthly_upkeeping_cost
        })
    return pd.DataFrame(upkeeping_list)

def investment_strategies(
    loan_term_months,
    monthly_income,
    monthly_expenses,
    monthly_payment,  # Mortgage payment
    monthly_property_tax_series,
    monthly_upkeeping_cost,
    investment_return_rate
):
    # Monthly compounding rate for investments
    monthly_return_rate = (1 + investment_return_rate) ** (1/12) - 1

    # Initialize investment balances
    investment_balance_strategy1 = 0  # Did not buy a house
    investment_balance_strategy2 = 0  # Did buy a house

    # Lists to store balances over time
    investment_strategy1 = []
    investment_strategy2 = []

    for month in range(1, loan_term_months + 1):
        # Strategy 1: Did not buy a house
        # Monthly investment amount
        monthly_investment1 = monthly_income - monthly_expenses
        monthly_investment1 = max(monthly_investment1, 0)
        # Update investment balance with monthly investment and compounding
        investment_balance_strategy1 = (investment_balance_strategy1 + monthly_investment1) * (1 + monthly_return_rate)
        investment_strategy1.append({
            'Month': month,
            'Investment Balance (No House Purchase)': investment_balance_strategy1
        })

        # Strategy 2: Did buy a house
        # Monthly property tax is constant now
        monthly_property_tax = monthly_property_tax_series.iloc[0]
        total_monthly_expenses = (
            monthly_payment +
            monthly_property_tax +
            monthly_upkeeping_cost +
            monthly_expenses
        )
        monthly_investment2 = monthly_income - total_monthly_expenses
        monthly_investment2 = max(monthly_investment2, 0)
        # Update investment balance with monthly investment and compounding
        investment_balance_strategy2 = (investment_balance_strategy2 + monthly_investment2) * (1 + monthly_return_rate)
        investment_strategy2.append({
            'Month': month,
            'Investment Balance (After House Expenses)': investment_balance_strategy2
        })

    # Convert to DataFrames
    investment_strategy1_df = pd.DataFrame(investment_strategy1)
    investment_strategy2_df = pd.DataFrame(investment_strategy2)

    return investment_strategy1_df, investment_strategy2_df

if __name__ == "__main__":
    main()