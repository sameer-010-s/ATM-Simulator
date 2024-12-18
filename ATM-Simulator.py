import streamlit as st

# Sample user data with joint and individual accounts
users = {
    "1234": {"name": "Gotam Kumar", "balance": 5000.0, "transactions": [], "daily_withdrawn": 0.0},
    "5678": {"name": "Joint Account (Sameer & Zamin)", "balance": 8000.0, "transactions": [], "daily_withdrawn": 0.0},
    "admin": {"name": "Admin", "balance": 0.0, "transactions": []}
}

# Constants
DAILY_WITHDRAW_LIMIT = 2000.0

# Session state initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

# Helper functions
def record_transaction(user, transaction):
    users[user]["transactions"].append(transaction)
    if len(users[user]["transactions"]) > 5:  # Limit to last 5 transactions
        users[user]["transactions"].pop(0)

# Login
if not st.session_state.authenticated:
    st.title("💳 Welcome to the Advanced ATM Simulator")
    pin = st.text_input("Enter your PIN", type="password")
    if st.button("Login"):
        if pin in users:
            st.session_state.authenticated = True
            st.session_state.current_user = pin
            st.session_state.failed_attempts = 0  # Reset failed attempts
            st.success(f"Welcome, {users[pin]['name']}!")
        else:
            st.session_state.failed_attempts += 1
            if st.session_state.failed_attempts >= 3:
                st.error("Too many failed attempts! Account locked.")
            else:
                st.error(f"Invalid PIN. Attempts left: {3 - st.session_state.failed_attempts}")
else:
    # Main menu
    current_user = st.session_state.current_user
    st.title(f"🏦 Welcome, {users[current_user]['name']}")

    choice = st.radio(
        "Select an option:",
        ["Check Balance", "Deposit Money", "Withdraw Money", "Transfer Money", "View Transactions",
         "Change PIN", "Rename Account", "View Summary", "Apply for Loan", "Logout"]
    )

    if choice == "Check Balance":
        st.write(f"💰 Your current balance is: *${users[current_user]['balance']:.2f}*")

    elif choice == "Deposit Money":
        deposit_amount = st.number_input("Enter the amount to deposit:", min_value=0.0, step=0.01)
        if st.button("Deposit"):
            if deposit_amount > 0:
                users[current_user]['balance'] += deposit_amount
                record_transaction(current_user, f"Deposited ${deposit_amount:.2f}")
                st.success(f"${deposit_amount:.2f} deposited successfully!")
            else:
                st.error("Please enter a valid amount.")

    elif choice == "Withdraw Money":
        withdraw_amount = st.number_input("Enter the amount to withdraw:", min_value=0.0, step=0.01)
        if st.button("Withdraw"):
            if 0 < withdraw_amount <= users[current_user]['balance']:
                if users[current_user]["daily_withdrawn"] + withdraw_amount > DAILY_WITHDRAW_LIMIT:
                    st.error("Daily withdrawal limit exceeded!")
                else:
                    users[current_user]['balance'] -= withdraw_amount
                    users[current_user]["daily_withdrawn"] += withdraw_amount
                    record_transaction(current_user, f"Withdrew ${withdraw_amount:.2f}")
                    st.success(f"${withdraw_amount:.2f} withdrawn successfully!")
            elif withdraw_amount > users[current_user]['balance']:
                st.error("Insufficient funds!")
            else:
                st.error("Please enter a valid amount.")

    elif choice == "Transfer Money":
        recipient_pin = st.text_input("Enter recipient's PIN:", type="password")
        transfer_amount = st.number_input("Enter the amount to transfer:", min_value=0.0, step=0.01)
        if st.button("Transfer"):
            if recipient_pin in users and recipient_pin != current_user:
                if transfer_amount > 0 and transfer_amount <= users[current_user]['balance']:
                    users[current_user]['balance'] -= transfer_amount
                    users[recipient_pin]['balance'] += transfer_amount
                    record_transaction(current_user, f"Transferred ${transfer_amount:.2f} to {users[recipient_pin]['name']}")
                    record_transaction(recipient_pin, f"Received ${transfer_amount:.2f} from {users[current_user]['name']}")
                    st.success(f"${transfer_amount:.2f} transferred to {users[recipient_pin]['name']}!")
                else:
                    st.error("Insufficient funds or invalid amount.")
            else:
                st.error("Invalid recipient PIN.")

    elif choice == "View Transactions":
        st.write("📜 Transaction History:")
        transactions = users[current_user]["transactions"]
        if transactions:
            for i, transaction in enumerate(transactions, 1):
                st.write(f"{i}. {transaction}")
        else:
            st.write("No transactions yet.")

    elif choice == "Change PIN":
        new_pin = st.text_input("Enter a new PIN:", type="password")
        if st.button("Change PIN"):
            if new_pin and new_pin != current_user:
                users[new_pin] = users.pop(current_user)
                st.session_state.current_user = new_pin
                st.success("PIN changed successfully!")
            else:
                st.error("Invalid or duplicate PIN.")

    elif choice == "Rename Account":
        new_name = st.text_input("Enter a new account name:")
        if st.button("Rename"):
            if new_name:
                users[current_user]["name"] = new_name
                st.success("Account name updated successfully!")
            else:
                st.error("Please enter a valid name.")

    elif choice == "View Summary":
        deposits = sum(float(tx.split()[1][1:]) for tx in users[current_user]["transactions"] if "Deposited" in tx)
        withdrawals = sum(float(tx.split()[1][1:]) for tx in users[current_user]["transactions"] if "Withdrew" in tx)
        st.write(f"💳 *Account Summary for {users[current_user]['name']}:*")
        st.write(f"🔵 Total Deposited: ${deposits:.2f}")
        st.write(f"🔴 Total Withdrawn: ${withdrawals:.2f}")

    elif choice == "Apply for Loan":
        loan_amount = st.number_input("Enter the loan amount you need:", min_value=0.0, step=0.01)
        if st.button("Apply"):
            if loan_amount > 0:
                users[current_user]["balance"] += loan_amount
                record_transaction(current_user, f"Loan approved for ${loan_amount:.2f}")
                st.success(f"Loan of ${loan_amount:.2f} approved and added to your balance!")
            else:
                st.error("Please enter a valid loan amount.")

    elif choice == "Logout":
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.success("Logged out successfully!")

# Footer
st.caption("Advanced ATM Simulator | Made with 💻 in Python")
