import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_amortization(loan_amount, loan_term, interest_rate, extra_payment=0):
    monthly_rate = interest_rate / 12 / 100
    n_payments = loan_term * 12

    # Monthly payment calculation
    monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** n_payments) / ((1 + monthly_rate) ** n_payments - 1)
    
    # Initialize variables
    balance = loan_amount
    total_interest = 0
    original_amortization = []
    accelerated_amortization = []
    month = 1

    while balance > 0:
        interest = balance * monthly_rate
        principal = monthly_payment - interest

        # Adjust for the last payment
        if balance - principal < 0:
            principal = balance
            monthly_payment = principal + interest

        original_amortization.append([month, monthly_payment, principal, interest, balance])

        balance -= principal
        total_interest += interest
        month += 1

    # Reset for accelerated payments
    balance = loan_amount
    total_interest_extra = 0
    month = 1

    while balance > 0:
        interest = balance * monthly_rate
        principal = monthly_payment - interest

        # Apply extra payment only if balance remains after the regular principal
        if balance - (principal + extra_payment) < 0:
            principal = balance
            extra_payment = 0  # No extra payment needed for the last month
            monthly_payment = principal + interest

        accelerated_amortization.append(
            [month, monthly_payment + extra_payment, principal + extra_payment, interest, balance]
        )

        balance -= principal + extra_payment
        total_interest_extra += interest
        month += 1

    return (
        pd.DataFrame(
            original_amortization,
            columns=["Month", "Payment", "Principal", "Interest", "Balance"],
        ),
        pd.DataFrame(
            accelerated_amortization,
            columns=["Month", "Payment", "Principal", "Interest", "Balance"],
        ),
        total_interest,
        total_interest_extra,
    )


def main():
    st.title("Loan Amortization Calculator")

    # Input fields
    loan_amount = st.number_input("Loan Amount", value=100000.0, step=1000.0)
    loan_term = st.number_input("Loan Term (years)", value=30, step=1)
    interest_rate = st.number_input("Interest Rate (Annual %)", value=5.0, step=0.1)
    extra_payment = st.number_input("Extra Monthly Payment", value=0.0, step=100.0)

    if st.button("Calculate"):
        (
            original_amortization,
            accelerated_amortization,
            total_interest,
            total_interest_extra,
        ) = calculate_amortization(loan_amount, loan_term, interest_rate, extra_payment)

        st.subheader("Original Amortization Table")
        st.dataframe(original_amortization)

        st.subheader("Accelerated Amortization Table")
        st.dataframe(accelerated_amortization)

        st.subheader("Comparison")
        total_savings = total_interest - total_interest_extra
        st.write(f"Total Interest Paid (Original Loan): ${total_interest:,.2f}")
        st.write(f"Total Interest Paid (with Snowball): ${total_interest_extra:,.2f}")
        st.write(f"Total Savings: ${total_savings:,.2f}")

        # Plotting
        fig, ax = plt.subplots()
        ax.plot(
            original_amortization["Month"],
            original_amortization["Balance"],
            label="Original Loan",
        )
        ax.plot(
            accelerated_amortization["Month"],
            accelerated_amortization["Balance"],
            label="with Snowball",
        )
        ax.set_xlabel("Month")
        ax.set_ylabel("Balance")
        ax.set_title("Loan Balance Over Time")
        ax.legend()

        st.pyplot(fig)

if __name__ == "__main__":
    main()
