import streamlit as st
import matplotlib.pyplot as plt

def home_page():
    st.title("Personal Finance and Budgeting Tool")
    st.write("Welcome to the Personal Finance Tool! Track your income, expenses, and savings goals.")

def budgeting_section():
    st.subheader("Enter Your Budget Details")
    
    # Input directly in INR
    income = st.number_input("Monthly Income (INR)", min_value=0)
    savings_goal = st.number_input("Savings Goal (INR)", min_value=0)
    
    st.write("### Add Expenses")
    expense_names = []
    expense_amounts = []
    expense_categories = []
    
    num_expenses = st.number_input("Number of Expenses", min_value=1, step=1)
    for i in range(num_expenses):
        name = st.text_input(f"Expense {i + 1} Name")
        amount = st.number_input(f"Expense {i + 1} Amount (INR)", min_value=0)
        category = st.text_input(f"Expense {i + 1} Category")
        
        if name and amount and category:
            expense_names.append(name)
            expense_amounts.append(amount)
            expense_categories.append(category)
    
    total_expenses = sum(expense_amounts)
    balance = income - total_expenses
    
    st.write(f"Remaining Balance: ₹{balance}")
    
    if balance >= savings_goal:
        st.success(f"You have achieved your savings goal of ₹{savings_goal}!")
    else:
        st.warning(f"You need ₹{savings_goal - balance} more to reach your savings goal.")
    
    # Store expenses in session state for visualization
    st.session_state['income'] = income
    st.session_state['expenses'] = expense_amounts
    st.session_state['expense_names'] = expense_names
    st.session_state['expense_categories'] = expense_categories
    st.session_state['total_expenses'] = total_expenses
    st.session_state['balance'] = balance
    st.session_state['savings_goal'] = savings_goal

def visualize_finances():
    st.subheader("Financial Visualization")
    income = st.session_state.get('income', 0)
    expenses = st.session_state.get('expenses', [])
    expense_names = st.session_state.get('expense_names', [])
    expense_categories = st.session_state.get('expense_categories', [])
    
    # Pie Chart for Expense Distribution by Category
    st.write("### Expense Distribution by Category")
    if expenses and expense_categories:
        category_totals = {}
        for i, category in enumerate(expense_categories):
            if category in category_totals:
                category_totals[category] += expenses[i]
            else:
                category_totals[category] = expenses[i]
        
        fig1, ax1 = plt.subplots()
        ax1.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)
    
    # Bar Graph for Expenses by Name
    st.write("### Expenses by Name")
    if expense_names and expenses:
        fig2, ax2 = plt.subplots()
        ax2.bar(expense_names, expenses, color='orange')
        ax2.set_ylabel("Amount (₹)")
        ax2.set_title("Expenses by Name")
        plt.xticks(rotation=45)
        st.pyplot(fig2)

def summary_section():
    st.subheader("Summary of Finances")
    income = st.session_state.get('income', 0)
    total_expenses = st.session_state.get('total_expenses', 0)
    balance = st.session_state.get('balance', 0)
    savings_goal = st.session_state.get('savings_goal', 0)
    expense_names = st.session_state.get('expense_names', [])
    expense_amounts = st.session_state.get('expenses', [])
    expense_categories = st.session_state.get('expense_categories', [])
    
    # Income and Expenses Overview
    st.write("### Income and Expenses Overview")
    st.write(f"**Total Monthly Income**: ₹{income}")
    st.write(f"**Total Monthly Expenses**: ₹{total_expenses}")
    st.write(f"**Remaining Balance**: ₹{balance}")

    # Savings Goal Status
    st.write("### Savings Goal Status")
    if balance >= savings_goal:
        st.write(f"**Savings Goal of ₹{savings_goal}**: Achieved 🎉")
    else:
        st.write(f"**Savings Goal of ₹{savings_goal}**: Not Achieved. You need ₹{savings_goal - balance} more.")

    # Detailed Expense Breakdown
    st.write("### Detailed Expense Breakdown")
    for name, amount, category in zip(expense_names, expense_amounts, expense_categories):
        st.write(f"- **{name}**: ₹{amount} ({category})")

    # Amount Available for Investment
    investable_amount = balance - savings_goal
    if investable_amount > 0:
        st.write(f"### You can invest ₹{investable_amount} based on your current balance and savings goal!")
    else:
        st.write("### No amount available for investment as savings goal has not been achieved yet.")

    # Links to Visualizations
    st.write("### Visualizations")
    st.write("- **[Expense Distribution by Category](#expense-distribution-by-category)**: Visualizes expenses grouped by category.")
    st.write("- **[Expenses by Name](#expenses-by-name)**: Bar chart showing each expense amount by name.")

def main():
    menu = ["Home", "Budgeting", "Visualization", "Summary"]
    choice = st.sidebar.selectbox("Choose a Section", menu)
    
    if choice == "Home":
        home_page()
    elif choice == "Budgeting":
        budgeting_section()
    elif choice == "Visualization":
        visualize_finances()
    elif choice == "Summary":
        summary_section()

if __name__ == "__main__":
    main()
