#All functions related to getting entries from user are stored here
from datetime import datetime

date_format = "%m/%d/%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}

def get_date(prompt, allow_default=False): 
    #prompt: what is asked to user, will allow user to hit enter for current date
    #recursive function that runs until user enters valid date
    date_str = input(prompt)
    if allow_default and not date_str: #if user pressed enter, and allowed the default
        return datetime.today().strftime(date_format) #gets date, converts to a string, formats as dd-mm-yyyy
    
    try:
        valid_date = datetime.strptime(date_str,date_format) #tries to convert to date-time object that is valid
        return valid_date.strftime(date_format) #converts back into string format to return back
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format")
        return get_date(prompt, allow_default)

def get_amount():
    try: 
        amount = float(input("Enter the amount: ")) #try to convert to float to see if valid input
        if amount <= 0:
            raise ValueError("Amount must be a non-negative non-zero value.")
        return amount
    except ValueError as e: 
        print(e)
        return get_amount()


def get_category():
    #recurses until user enters valid category
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper() #converts category to uppercase
    if category in CATEGORIES:
        return CATEGORIES[category]
    
    print("Invalid category. Please enter 'I' for Income or 'E' for Expense.")
    return get_category()


def get_description():
    return input("Enter a description (optional): ")