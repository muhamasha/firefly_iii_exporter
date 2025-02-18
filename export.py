from dataclasses import dataclass
import logging
import requests
import csv
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

# Firefly III API details
API_TOKEN = os.getenv("FIREFLY_III_API_TOKEN")
BASE_URL = os.getenv("FIREFLY_III_BASE_URL")

headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Accept': 'application/json',
}

# Define the date range for fetching expenses
start_date = '2024-10-01'  # Replace with your start date (including this date)
end_date = '2024-12-31'    # Replace with your end date (including this date)

file_name = 'expenses.csv'


@dataclass
class Expense:
    date: str
    amount: float
    currency_code: str
    category: str
    budget: str
    tags: str
    account_from: str
    account_to: str
    description: str
    note: str
    external_url: str


def fetch_expenses(start_date, end_date):
    expenses = []
    url = f"{BASE_URL}transactions"
    params = {
        'start': start_date,
        'end': end_date,
        'type': 'withdrawal',  # Expense type
        'page': 1,
    }

    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            logging.ERROR(f"Error fetching expenses: {response.status_code} - {response.text}")
            break

        data = response.json()
        expenses.extend(data['data'])
        logging.info(f"Fetched page {data['meta']['pagination']['current_page']} of {data['meta']['pagination']['total_pages']}")

        if data['meta']['pagination']['current_page'] == data['meta']['pagination']['total_pages']:
            break
        params['page'] += 1

    return expenses

def write_to_csv(expenses, filename='expenses.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['Date', 'Amount', 'Currency', 'Category', 'Budget', 'Tags', 'Account From', 'Account To', 'Description', 'Note', 'External URL'])

        for expense in expenses:
            for transaction in expense['attributes']['transactions']:
                expense = Expense(
                    date=transaction['date'],
                    amount=transaction['amount'],
                    currency_code=transaction['currency_code'],
                    category=transaction['category_name'],
                    budget=transaction['budget_name'],
                    tags=', '.join([tag for tag in transaction['tags']]),
                    account_from=transaction['source_name'],
                    account_to=transaction['destination_name'],
                    description=transaction['description'],
                    note=transaction['notes'],
                    external_url=transaction['external_url'],
                )

                # Write row
                writer.writerow(expense.__dict__.values())


if __name__ == '__main__':

    # Setup logging to print logs to console
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    expenses = fetch_expenses(start_date, end_date)
    if expenses:
        write_to_csv(expenses)
        logging.info(f"Expenses exported to {file_name}")
    else:
        logging.info("No expenses found in the given date range.")
