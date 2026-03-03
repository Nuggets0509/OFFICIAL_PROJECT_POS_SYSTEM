import time
import sys
import os

# Get the folder where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Build accounts file path in the same folder as the script
ACCOUNTS = os.path.join(SCRIPT_DIR, "accounts.txt")

with open(ACCOUNTS, "a"):  # Create file if nonexistent
    pass

def checkUsername(user):
    sameUsername = False
    with open(ACCOUNTS, "r") as f:  # Open accounts file:
        lines = f.readlines()
    
    for line in lines:
        # Get each usernames
        prevUsername = line.split(",")
        if prevUsername[0] == user:
            prevUsername = ""
            sameUsername = True
            break
        else:
            sameUsername = False

    if sameUsername:
        return True
    else:
        return False

        
def create():
    print("\n")
    invalidUsername = True  # Determines if user entered a name same to the person
    invalidPw = True        # Determines if password has been entered
    
    while invalidUsername:
        
        username = ""
        prevUsername = "" # Scans previous 

        while True:
            username = input("Enter your chosen Papi-zza username: ")  # Make account if the name does not match any previous usernames
            if username == '':
                pass
            elif username.count(" ") > 0:
                print("Your Papi-zza username must have no spaces.")
            else:
                break

        # Check if username has already been used
        if checkUsername(username) == True:
                print("This Papi-zza username has already been used. Please choose another.")
                restart = True
                invalidUsername = True
        else:
                invalidUsername = False
                restart = False

        if restart == True:
            continue

        while invalidPw:
            password = input("Enter your password: ")
            if password == "":
                pass
            else:
                invalidPw = False
                
        f = open(ACCOUNTS, "a")
        f.write(f"\n{username}, {password}")
        print("Account successfully created!")
        f.close()
    return True

        ## Enter menu

def login():
    f = open(ACCOUNTS, "r")  # Open accounts file
    lines = f.readlines()
    f.close()
    
    password = ""
    scanUsername = ""
    invalidUsername = True
    
    # Ask for username and password
    while invalidUsername:
        option1 = ""
        username = input("\nEnter your username: ")
        if checkUsername(username):     # See if username has been registered
            for line in lines:
                scanUsername = line.split(",")
                if scanUsername[0] == username:
                    userPass = scanUsername[1].strip()
                    invalidUsername = False           
        else:
            while True:
                option1 = input("Username is not found. Enter your username again (y) or go back to menu(n)? ").lower()
                if option1 == 'y':
                    break
                elif option1 == 'n':
                    return False
                
    # Get password after username is found
    while password != userPass.strip():
        option2 = ""
        password = input(f"Enter password for {username}: ").strip()
        if password != userPass:
            while True:
                option2 = input("You entered the wrong password. Try again (y) or go back to menu (n)? ")
                if option2 == 'y':
                    break
                elif option2 == 'n':
                    return False
                
        else:
            print("Login successful!")
            return True
        
    
# Graphics
rerun = True
while rerun:
    graphic = """\t\t\t\t\t\t\t╔═╗┌─┐┌─┐┬  ╔═╗┌─┐┌┬┐┬─┐┌─┐┌─┐  ╔═╗┬┌─┐┌─┐┌─┐┬─┐┬┌─┐
    \t\t\t\t\t\t\t╠═╝├─┤├─┘│  ╠═╝├┤  ││├┬┘│ │└─┐  ╠═╝│┌─┘┌─┘├┤ ├┬┘│├─┤
    \t\t\t\t\t\t\t╩  ┴ ┴┴  ┴  ╩  └─┘─┴┘┴└─└─┘└─┘  ╩  ┴└─┘└─┘└─┘┴└─┴┴ ┴"""

    # Options
    print(graphic.center(80))

    print("\n")

    print("1: Create your Papi-zza Account")
    print("2: Login to your Papi-zza Account")
    print("3: Exit")

    option = ""
    while option != '1' and option != '2' and option != '3':
        option = input("Please select an option: ")


    match(option):
        case '1':
            if create():
                rerun = False
                print("Redirecting to the menu...")
                time.sleep(2)
        case '2':
            if login():
                rerun = False
                print("Redirecting to the menu...")
                time.sleep(2)
            else:
                rerun = True
        case '3':
            print("Thank you for visiting Papi Pedro's Pizzeria!")
            time.sleep(2)
            sys.exit()
            

    
