import sqlite3
from prettytable import PrettyTable
from database import (
    create_tables,
    add_seasonal_flavor,
    add_to_cart,
    view_cart,
    search_seasonal_flavors,
    view_seasonal_flavors,
    populate_initial_data,
    clear_cart
)

def main():
    create_tables()
    populate_initial_data()

    while True:
        print("\nIce Cream Parlor Management System")
        print("1. View Menu")
        print("2. Search")
        print("3. Add to Cart")
        print("4. View Cart")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            flavors = view_seasonal_flavors()
            display_table(flavors)
        elif choice == '2':
            keyword = input("Enter keyword to search (press enter to skip): ")
            flavors = search_seasonal_flavors(keyword=keyword)
            display_table(flavors)
        elif choice == '3':
            while True:
                flavor_id = input("Enter flavor ID to add to cart (or type 'none' to stop adding): ")
                if flavor_id.lower() == 'none':
                    break
                else:
                    add_to_cart(flavor_id)
        elif choice == '4':
            cart, total_price = view_cart()
            display_cart(cart, total_price)
        elif choice == '5':
            clear_cart()
            break
        else:
            print("Invalid choice. Please try again.")

def display_table(data):
    if not data:
        print("No data available.")
        return
    
    table = PrettyTable()
    table.field_names = ["ID", "Name", "Description", "Price"]
    for row in data:
        table.add_row([row[0], row[1], row[2], row[3]])
    print(table)

def display_cart(cart, total_price):
    if not cart:
        print("Cart is empty.")
        return
    
    table = PrettyTable()
    table.field_names = ["ID", "Name", "Price"]
    for item in cart:
        table.add_row([item[0], item[1], item[2]])
    print(table)
    print(f"Total Price: {total_price:.2f}")

if __name__ == "__main__":
    main()
