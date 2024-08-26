import random

class ShoppingCart:

    def __init__(self, customer_id, customer_name, phone_number):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.phone_number = phone_number
        self.cart = []
        self.locations = ('Ad', 'Bn', 'In', 'Tn')

    def register_online(self):
        print("Ad- Adyar, Bn - Besant Nagar, In - Indira Nagar, Tn - T-Nagar")
        self.location = input("Enter your location (Ad/Bn/In/Tn):").capitalize()
        while self.location not in self.locations:
            print("Please enter a valid location (Ad, Bn, In, Tn).")
            self.location = input("Enter your location (Ad/Bn/In/Tn):").capitalize()

        self.permanent_location = input('Enter the delivery location: ')
        self.customer_id = f'Abc{str(random.randint(1000, 9999))}{self.location}'
        print("Registration successful")
        print("Your Customer ID is ", self.customer_id)
        print("Your Name: ", self.customer_name)
        print("Your Mobile Number: ", self.phone_number)
        
    def verify_customer_id(self):
        if len(self.customer_id) != 9 or not self.customer_id.startswith("Abc") or self.customer_id[-2:] not in self.locations:
            print("Invalid customer ID. Please register online.")
            self.register_online()
            return False
        else:
            print("Welcome to our Supermarket!")
            print("Your Customer ID: ", self.customer_id)
            print("Your Name: ", self.customer_name)
            print("Your Mobile Number: ", self.phone_number)
            return True
        
class Supermarket(ShoppingCart):
    
    def __init__(self, customer_id, customer_name, phone_number):
        super().__init__(customer_id, customer_name, phone_number)
        self.item = {'Sugar': 50, 'Rice': 80, 'Atta': 40, 'Ragi': 60, 'Dates': 50, 'Salt': 20}
        self.delivery_charges = {'Ad': 20, 'Bn': 40, 'In': 50, 'Tn': 70}

    def display_items(self):
        print("Available Items:")
        for item, price in self.item.items():
            print(f"{item}: Rs. {price}")

    def discount(self, item, quantity):
        discounts = {
            'Sugar': {1: 0.05, 5: 0.1}, 
            'Rice': {10: 0.04, 25: 0.08},
            'Atta': {5: 0.06, 10: 0.12},
            'Ragi': {5: 0.05, 12: 0.015},
            'Dates': {1: 0.02, 3: 0.02},
            'Salt': {1: 0.02, 5: 0.05}
        }
        if item in discounts:
            item_discounts = discounts[item]
            for quantity_limit, discount_percentage in sorted(item_discounts.items(), reverse=True):
                if quantity >= quantity_limit:
                    return self.item[item] * quantity * discount_percentage
        return 0

    def add_to_cart(self, item, quantity):
        if item not in self.item:
            print("Item not available.")
            return
        price_per_unit = self.item[item]
        total_price_before_discount = price_per_unit * quantity
        discount_amount = self.discount(item, quantity)
        total_price_after_discount = total_price_before_discount - discount_amount

        self.cart.append((item, quantity, total_price_after_discount))
        print(f"{item} added to cart. Total price (after discount): Rs. {total_price_after_discount}")

    def generate_receipt(self, delivery_location):
        total_item_price = sum(item[2] for item in self.cart)
        total_amount = total_item_price + self.delivery_charges.get(delivery_location, 0)

        receipt = f"Receipt:\nCustomer Name: {self.customer_name}\nCustomer ID: {self.customer_id}\nPhone Number: {self.phone_number}\nItems Purchased:\n"
        for item, quantity, price in self.cart:
            receipt += f"{quantity} Kgs {item}: Rs. {price}\n"
        receipt += f"Total Item Price: Rs. {total_item_price}\n"
        receipt += f"Total Amount (including delivery): Rs. {total_amount}\n"
        return receipt

    def write_to_file(self, filename, receipt_data):
        with open(filename, 'a') as file:
            file.write(receipt_data)
            file.write("\n")

    def read_from_file(self, filename):
        with open(filename, 'r') as file:
            print(file.read())

# Main Program Execution
print("Are you a new customer or an existing customer?")
customer_type = input("Enter 'new' for new customer or 'existing' for existing customer: ")
if customer_type.lower() == 'new':
    customer_name = input("Enter your name: ")
    while customer_name.isdigit():
        print("Please enter a valid name with alphabetic characters only.")
        customer_name = input("Enter your name: ")

    phone_number = input("Enter your phone number: ")
    while len(phone_number) != 10:
        print("Please enter a 10-digit phone number.")
        phone_number = input("Enter your phone number: ")

    customer = Supermarket('', customer_name, phone_number)
    customer.register_online()
    customer.display_items()
else:
    customer_id = input("Enter customer ID: ")
    customer_name = input("Enter customer name: ")
    phone_number = input("Enter phone number: ")
    customer = Supermarket(customer_id, customer_name, phone_number)
    if customer.verify_customer_id():
        customer.display_items()
    else:
        print("Registration failed. Exiting program.")

while True:
    item = input("Enter item to add to cart (Sugar, Rice, Atta, Ragi, Dates, Salt): ").capitalize()
    if item not in ("Sugar", "Rice", "Atta", "Ragi", "Dates", "Salt"):
        print("Invalid item. Please choose from Sugar, Rice, Atta, Ragi, Dates or Salt.")
        continue
    quantity = int(input("Enter quantity: "))
    customer.add_to_cart(item, quantity)

    add_more = input("Do you want to add more items? (yes/no): ")
    if add_more.lower() != "yes":
        break

delivery_location = input("Enter delivery location (Ad, Bn, In, Tn): ").capitalize()
receipt_data = customer.generate_receipt(delivery_location)
print(receipt_data)
customer.write_to_file('receipts.txt', receipt_data)
print("Receipt saved to file.")
