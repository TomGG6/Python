import pickle

from Selenium_controller.controller import Controller

PATH = "C://Program Files (x86)/chromedriver.exe"
URL = "https://automationbookstore.dev/"

def print_menu():
    print("====Menu====")
    print("1. Check product titles")
    print("2. Check product authors")
    print("3. Check product prices")
    print("4. Save data to file")
    print("5. Load data")
    print("0. Quit")
    print("Enter:", end=" ")


def print_comparison(data_from_file, checked_data):
    print("Previous data: ", end=" ")
    print(data_from_file)
    print("Current data: ", end=" ")
    print(checked_data)
    print()
    if data_from_file == checked_data:
        print("The data has no changed")
    else:
        print("Data changed")


if __name__ == "__main__":
    tester = Controller(PATH, URL)
    file_name = ""
    while True:
        print_menu()
        choice = int(input())
        if choice == 1:
            file_name = input("Choose file to compare: ")
            data_file = open(file_name, "rb")
            saved_data = pickle.load(data_file)
            data_file.close()
            print_comparison(saved_data, tester.check_titles())
        elif choice == 2:
            file_name = input("Choose file to compare: ")
            data_file = open(file_name, "rb")
            saved_data = pickle.load(data_file)
            data_file.close()
            print_comparison(saved_data, tester.check_authors())
        elif choice == 3:
            file_name = input("Choose file to compare: ")
            data_file = open(file_name, "rb")
            saved_data = pickle.load(data_file)
            data_file.close()
            print_comparison(saved_data, tester.check_prices())
        elif choice == 4:
            file_name = input("Choice file to save: ")
            while True:
                data_type = input("What type of data you want to save [titles/authors/data]: ")
                if data_type == "titles":
                    saved_data = open(file_name, "wb")
                    pickle.dump(tester.titles, saved_data)
                    saved_data.close()
                    break
                elif data_type == "authors":
                    saved_data = open(file_name, "wb")
                    pickle.dump(tester.authors, saved_data)
                    saved_data.close()
                    break
                elif data_type == "prices":
                    saved_data = open(file_name, "wb")
                    pickle.dump(tester.prices, saved_data)
                    saved_data.close()
                    break
        elif choice == 5:
            tester.get_current_data()
            print("Data loaded")
        elif choice == 0:
            break
