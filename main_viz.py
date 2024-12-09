import os
import json
import pandas as pd
import matplotlib.pyplot as plt

# Folder containing the JSON reports
folder_path = 'userdata/monthlyreports'

def load_json_files(folder_path):
    data = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            with open(os.path.join(folder_path, file_name), 'r') as f:
                data.append(json.load(f))
    return data

def process_financial_data(data):
    reports = []

    for entry in data:
        year = entry['year']
        month = entry['month']
        total_income = float(entry['overview']['total_income'])
        total_expense = float(entry['overview']['total_expense'])
        total_savings = float(entry['overview']['total_savings'])
        expense_by_category = {k.split('.')[-1]: float(v) for k, v in entry['expense_by_category'].items()}
        
        reports.append({
            'year': year,
            'month': month,
            'total_income': total_income,
            'total_expense': total_expense,
            'total_savings': total_savings,
            'expense_by_category': expense_by_category
        })
    return reports

def create_dataframe(reports):
    df = pd.DataFrame(reports)
    df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))
    df.set_index('date', inplace=True)
    df.sort_values('date', inplace=True)
    return df

def plot_combined_graph(df):
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))  # Create a 2x2 grid for subplots
    fig.suptitle('Financial Overview', fontsize=16)  # Overall title for the figure

    # Plot Income vs Expense
    df[['total_income', 'total_expense']].plot(ax=axs[0, 0], marker='o', color=['blue', 'red'])
    axs[0, 0].set_title('Income vs Expense Over Time')
    axs[0, 0].set_xlabel('Date')
    axs[0, 0].set_ylabel('Amount (€)')
    axs[0, 0].grid(True)

    # Plot Savings Trend
    df['total_savings'].plot(ax=axs[0, 1], marker='o', color='green')
    # Calculate cumulative savings and plot it
    df['cumulative_savings'] = df['total_savings'].cumsum()
    df['cumulative_savings'].plot(ax=axs[0, 1], marker='x', color='blue', linestyle='--', label='Cumulative Savings')
    axs[0, 1].set_title('Savings Trend Over Time')
    axs[0, 1].set_xlabel('Date')
    axs[0, 1].set_ylabel('Savings (€)')
    axs[0, 1].grid(True)

    # Plot Expense by Category Over Time (stacked bar)
    df['expense_by_category'].apply(pd.Series).plot(kind='bar', stacked=True, ax=axs[1, 0])
    axs[1, 0].set_title('Expenses by Category Over Time')
    axs[1, 0].set_xlabel('Date')
    axs[1, 0].set_ylabel('Amount (€)')
    axs[1, 0].grid(True)

    # Plot Combined Savings, Income, Expense
    df[['total_income', 'total_expense', 'total_savings']].plot(ax=axs[1, 1], marker='o', color=['blue', 'red', 'green'])
    axs[1, 1].set_title('Income, Expense, and Savings Over Time')
    axs[1, 1].set_xlabel('Date')
    axs[1, 1].set_ylabel('Amount (€)')
    axs[1, 1].grid(True)

    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to make room for the main title
    plt.show()

def main():
    # Load JSON files
    json_data = load_json_files(folder_path)

    # Process the financial data
    financial_reports = process_financial_data(json_data)

    # Create a DataFrame for analysis
    df = create_dataframe(financial_reports)

    # Plot all graphs
    plot_combined_graph(df)

if __name__ == '__main__':
    main()
