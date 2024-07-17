import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt
global net_savings

class CSV:
    CSV_FILE = "CHECKING_Transactions_2024-06-01_2024-06-30.csv" #class variable
    COLUMNS = ["Processed Date", "Amount", "Credit or Debit", "Description"]
    FORMAT = "%m/%d/%Y" #mm/dd/yyyy format

    @classmethod #gives access to class itself, but not an instance of the class
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE) #tries to load in the CSV file if it exists
        except FileNotFoundError: #creates CSV file if not found
            df = pd.DataFrame(columns = cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index = False) #exports df to a csv, but not going to be indexing the csv

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = { #dictionary
            "Processed Date": date,
            "Amount": amount,
            "Credit or Debit": category,
            "Description": description
        }
        with open(cls.CSV_FILE, "a", newline = "") as csvfile: #opened in append mode to add new entries to end of file, also automatically closes file and memory leaks
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS) #creates a CSV writer to write dict into csv
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["Processed Date"] = pd.to_datetime(df["Processed Date"], format = CSV.FORMAT, errors='coerce') #converts all dates in date column to datetime object, ignoring errors
        start_date = datetime.strptime(start_date, CSV.FORMAT) #convert start date to datetime objects
        end_date = datetime.strptime(end_date, CSV.FORMAT) #convert end date to datetime objects

        mask = (df["Processed Date"] >= start_date) & (df["Processed Date"] <= end_date) #mask that checks if data in current date row is greater than start date 
                                                                     #and if data in current row is less than end date
        filtered_df = df.loc[mask] #returns a new filtered df that only has rows where date > start_date and date < end_date (located all rows where matches mask)

        if filtered_df.empty: 
            print("No transactions found in the given date range.")
        else:
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}") #converts dates to strings again
            print(filtered_df.to_string(index=False, formatters = {"date": lambda x: x.strftime(CSV.FORMAT)})) #formats all data in date column into FORMAT using lambda function

            total_income = filtered_df[filtered_df["Credit or Debit"] == "Credit"][
                "Amount"
            ].sum() #gets all values in the income category, and sums them to get total income
            total_expense =filtered_df[filtered_df["Credit or Debit"] == "Debit"][
                "Amount"
            ].sum()

            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}") #prints total income rounded to 2 decimals
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")
            
        return filtered_df

def add():
    CSV.initialize_csv()
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", 
         allow_default=True
        )
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("df is not a pandas DataFrame. Please ensure it is properly initialized and passed to the function.")
    
    if df is None:
        raise ValueError("DataFrame is None. Please ensure it is properly initialized and passed to the function.")
    df['Processed Date'] = pd.to_datetime(df["Processed Date"])  # Ensure date is in datetime format
    df.set_index("Processed Date", inplace = True)

    income_df = (df[df["Credit or Debit"] == "Credit"] #creates income df to use as own line in graph
        .resample("D") #resample shows graph as daily values to fill in missing days
        .sum() #sum values to aggregate rows that have same date and add them together
        .reindex(df.index, fill_value = 0) #reindex to fill in missing values with 0
    )
    expense_df = (df[df["Credit or Debit"] == "Debit"] #creates expense df to use as own line in graph
        .resample("D") 
        .sum() 
        .reindex(df.index, fill_value = 0) 
    )


    plt.figure(figsize = (10, 5)) #sets up graph
    plt.plot(income_df.index, income_df["Amount"], label = "Income", color = "g") #x axis = dates (index) y axis = amount, green line
    plt.plot(expense_df.index, expense_df["Amount"], label = "Expense", color = "r") #x axis = dates (index) y axis = amount, red line
    #plt.axhline(net_savings, color = "b", label = "Net Savings") adds horizontal line to graph
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend() #enables legend
    plt.grid(True) #turns on grid
    plt.show() #shows plot on screen
    

def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date) #gets transactions btwn two dates
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")

if __name__ == "__main__":
    main()