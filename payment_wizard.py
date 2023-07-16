# import for clearing console functionality
import os

# import for parsing json
import json

# used for the occasional delay needed to wait for a webpage to finish loading
import time

# selenium imports for opening up new Chrome window and interacting with webpages
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# file that contains the payment information that will be displayed to the user
payment_json_file_name = "payment_wizard.json"
# used to determine whether the selected payment has any links to determine whether to display that category or not
payment_has_links = False
# used to determine whether the functionality for allowing the user to edit the selected payment's details is enabled or not
toggle_edit_payments = False
# used to determine whether the user has modified the payment details to see if the program will re-write the data of the payment information json file
payment_data_has_changed = False
# used to determine if the program will prompt the user for inputs or execute a test run
enable_prompting_user = True
# used to determine if the program will clear the console so you don't see the past text
toggle_clear_console = True
# ussed to determine whether the chrome window will be a normal or incognito window
# default is not toggled (not incognito)
toggle_incognito = False

# color escape sequences (used for coloring the text output of the program)
COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_RESET = '\033[0m'

# objects for the selenium webdriver and wait
driver = None
wait = None
payment_data = None
payment_objects = []

# payment class definition
class payment:
    # init function
    def __init__(self, name, amount_due, due_date, payment_source, notes, links, index):
        self.name = name
        self.amount_due = amount_due
        self.due_date = due_date
        self.payment_source = payment_source
        self.notes = notes
        self.links = links
        self.index = index

def configure_driver() -> None:
    chrome_options = Options()
    if(toggle_incognito == True):
        chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options)

def configure_driver_wait_time(time_in_seconds: int) -> None:
    wait = WebDriverWait(driver, time_in_seconds)

# function to clear program console outputs
def clear_console_if_enabled() -> None:
    if toggle_clear_console == True:
        if os.name == 'nt':
            # For Windows
            os.system('cls')
        else:
            # For UNIX-based systems (e.g., Linux, macOS)
            os.system('clear')

# function that waits a certain amount of time for a select element to appear in the HTML and then selects it
def wait_to_select_from_a_select_element(select_x_path, choice) -> None:
    select = Select(wait.until(EC.visibility_of_element_located((By.XPATH, select_x_path))))
    select.select_by_visible_text(choice)

# function to prompt user to change payment details
def prompt_user_to_change_payment_details(payment_obj_changing: payment) -> None:
    clear_console_if_enabled()
    new_amount_due = input("Enter new amount due (w/o \'$\' sign): ")
    payment_obj_changing.amount_due = new_amount_due
    
    clear_console_if_enabled()
    new_due_date = input("Enter new due date (mm/dd/yyyy): ")
    payment_obj_changing.due_date = new_due_date

# function to parse json data from file and return it as an existing python data type
def parse_json_data(json_file_path: str) -> object:
    with open(json_file_path, 'r') as json_file:
        return json.load(json_file)

# function to turn a payment dictionary into an object of the payment class
# the keys of the payment dictionary correspond with the attributes of the payment object
# "-> payment" signifies that the function returns a data of type payment (an object of the payment class)
def turn_payment_dict_into_payment_obj(payment_dict: dict) -> payment:
    
    # initialize new payment object
    # initializing the object attributes using the dictionary data
    # index is not assigned yet, will be assigned once the list that contains the payment objects is sorted based on name
    new_payment_obj = payment(
        name = payment_dict["name"],
        amount_due = payment_dict["amount_due"],
        due_date = payment_dict["due_date"],
        payment_source = payment_dict["payment_source"],
        notes = payment_dict["notes"],
        links = payment_dict["links"],
        index = None
    )
    
    return new_payment_obj

def print_out_payments(payment_objects: list) -> None:
    print("Select a payment to view: ")
    for i in range(0, len(payment_objects)):
        current_payment_obj = payment_objects[i]
        string_to_print_out = str(current_payment_obj.index) + ". " + current_payment_obj.name
        if(i % 2 == 0): # if the current index is even
            string_to_print_out = COLOR_RED + string_to_print_out
        else: # if the current index is odd
            string_to_print_out = COLOR_GREEN + string_to_print_out
        
        string_to_print_out = string_to_print_out + COLOR_RESET
        print(string_to_print_out)
            
    

# main function
if (__name__ == "__main__"):
    
    payment_data = parse_json_data(payment_json_file_name)
    for payment_dict in payment_data:
        new_payment_obj = turn_payment_dict_into_payment_obj(payment_dict)
        payment_objects.append(new_payment_obj)
        
    print_out_payments(payment_objects)