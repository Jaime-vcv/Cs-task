import tkinter as tk # It imports tkinter to create the GUI, and it is used as "tk" to facilitate usage.

# The product class to use for each type of product.
class Product:
    """
    Represents a product in inventory.
    Demonstrates ENCAPSULATION (private attribtes with getters/setters).
    """
    def __init__(self, name, sku, price, quantity): #Define the function and parameters, call each parameter by self.
        """
        Initialize a new Product.
        
        Parameters:
            name (str): Product name
            sku (str): Stock Keeping Unit (unique identifier)
            price (float): Product price (must be > 0)
            quantity (int): Product quantity (must be >= 0)
        """
        
        self._name = name 
        self._sku = sku
        self._price = price
        self._quantity = quantity
        
    @property
    def name(self):
        """Get product name."""
        return self._name
        
    @property
    def sku(self):
        """Get product SKU."""
        return self._sku
    
    @property
    def price(self):
        """Get product price."""
        return self._price
    
    @property
    def quantity(self):
        """Get product quantity."""
        return self._quantity
    
    @price.setter
    def price(self, value):
        """
        Set price with validation. 
        
        Parameters:
            value (float): New price value.
            
        Raises:
            ValueError: If price is <= 0.
        """
        
        # Bussiness rule: Free of negative prices indicate data entry errors.
        # This prevents invalid financial transactions in the system.
        if value <= 0:
            print("Error! Price must be greater than 0!")
            raise ValueError("Price must be greater than 0")
        self._price = value
    
    @quantity.setter
    def quantity(self, value):
        """
        Set quantity with validation.
        
        Parameters:
            value (int): New quantity value.
        
        Raises:
            ValueError: If quantity is < 0.
        """
        
        if value <= 0:
            print("Error! Quantity cannot be negative or 0!")
            raise ValueError("Quantity cannot be negative or 0")
        self._quantity = value
    
    def __str__(self):
        """Return string representation of product for display."""
        return f"{self._name} (SKU: {self._sku}) - ${self._price:.2f} x {self._quantity}"
    
    
# The location class to use for each product location.
class Location:
    """
    Represents a storage location in warehouse.
    Demonstrates COMPOSITION (holds Product objects).
    """
    def __init__(self, row, col, capacity): # Define the function and parameters, call each parameter by self and add the product list.
        """
        Initialize a new Location.
        
        Parameters:
            row (int): Row coordinate in warehouse grid.
            col (int): Column coordinate in warehouse grid.
            capacity (int): Maximum items this location can hold.
        """
        
        self._row = row 
        self._col = col
        self._capacity = capacity
        self._products = [] # Stores all products assigned to this list.
        
    @property
    def row(self):
        """Get row coodinate."""
        return self._row
    
    @property
    def col(self):
        """Get column coodinate."""
        return self._col
    
    @property
    def capacity(self):
        """Get location capacity."""
        return self._capacity
    
    @property
    def products(self):
        """Return copy of fproducts list to prevent external modification."""
        return self._products.copy()    
        
    def add_product(self, product): # Define the function to add a product to the list.
        """
        Add a product to this location if capacity allows.
        
        Parameters:
            product (Product): The product to add.
        
        Returns:
            bool: True if added successfully, False if rejected.
        
        Raises:
            None (errors are handled intenally with print statements)
        
        """
        
        if self._capacity <= 0: # Check if new capacity its a negative value.
            print("Invalid capacity for location")
            return False
        
        if product.quantity <= 0: # Check if the new product quantity is negative.
            print("Error! Product quantity can't be negative!") # Notifies the user that a negative quantity is not allowed in the system.
            return False
            
        for existing in self._products: # Local variable "existing" is used to match each product.
            if existing.sku == product.sku: # Checks if existing products are found in the system.
                print(f"Error {product.sku} already exists in ({self._row}, {self._col})") # Notify the user the product already exists in a location.
                return False # Returns to function
            
        current_items = sum(p.quantity for p in self._products) # Sums the quantity of products to compare to the capacity, storing the quantity in a local variable.
        
        if current_items + product.quantity <= self._capacity: # Checks whether there's enoguh space by summing the total amount and comparing it to the capacity.
            self._products.append(product) # Composition: Location maintains full control over its products
            # Products are stored internally to enforce capacity limits
            return True # Returns added product.
        else:
            print(f"Location ({self._row}, {self._col}) is full") # Prints the location of where the product would have been and declares the space to be full.
            return False # Returns to function.

    def remove_product(self, sku): # Define the function to remove a product from the list using its unique identifier "SKU" (Stock Keeping Unit).
            """Remove product by SKU. """
            for product in self._products: # Iterate using "product" as a local variable troughout 'location(products)'.
                if product.sku == sku: # Compares products unique identifier for a match with the desired product to be removed.
                    self._products.remove(product) # After a successful comparison the chosen product is deleted through its location.
                    print(f"{sku} has been removed from the location ({self._row}, {self._col})") # Give a message to the user indicating that the "product" refered to by its SKU has been removed in its set location.
                    return True # Returns "removed".
            return False # Returns to loop.

    def update_quantity(self, sku, new_quantity): # Define the function to update product quantity in the warehouse.
        """
        Update product quantity of existing product.
        
        Parameters:
            sku (str): Stock Keeping Unit of product.
            new_quantity (int): New quantity value.
        
        Returns:
            bool: True if updated, False if not found or invalid.
        """
        
        if new_quantity < 0: # If new quantity is less than 0, the quantity won't be accepted since a negative quantity is not possible.
            print("Error! New quantity can't be negative!") # Notify the use a negative quantity is not allowed in the system.
            return False # Returns failure.
            
        for product in self._products: # Iterate through every product.
            if product.sku == sku: # Check if the product unique identifier matches the desired product.
                current_total = sum(p.quantity for p in self._products) # Get a total by adding up the quantity of the products.
                new_total = current_total - product.quantity + new_quantity # The new total quantity will be the "total" - the product "quantity" + "new quantity".
                
                if new_total <= self._capacity: # Check if new total is less than the capacity.
                    product.quantity = new_quantity # Set current product quantity to new quantity.
                    print(f"{sku} updated to {new_quantity}") # Notify the user that the "product" has been set to new "quantity".
                    return True # Returns new quantity.
                else:
                    print("Error! Quantity exceeds location capacity!") # Notify the user quantity goes over the capacity.
                    return False # Returns to if statement
        return False # Returns to loop.

    def update_price(self, sku, new_price): # Define function to update product price using its SKU.
        """
        Update product price of existing product.
        
        Parameters:
            sku (str): Stock Keeping Unit of product.
            new_price (float): New price value.
        
        Returns:
            bool: True if updated, False if not found or invalid
        """
        
        if new_price <= 0: # Check if price is negative or 0 as both cases are not allowed in the system.
            print("Error! Price can't be negative or free!") # Notify the user if any of the two cases has been encountered.
            return False # Returns for a failed input.
        
        for product in self._products: # Iterate through every product.
            if product.sku == sku: # Check if given SKU matches product SKU.
                product.price = new_price # Set product "price" to be "new price". 
                print(f"{sku} updated to ${new_price:.2f}") # Notify the user the product's price has been updated.
                return True # Return for success.
            
        print("Error! Product not found in location!") # Notify the user there has been an invalid entry.
        return False # Return for failed attempt
        
    
    def get_total_quantity(self): # Define the function to get total product quantity in the warehouse by going through each product.
        """Get total items in location. """
        return sum(p.quantity for p in self._products) # Sum of all products to get a total amount of products.


# The Warehouse class used for locations.
class Warehouse:
    """
    Manages 2D grid of locations.
    Demonstrates AGGREGATION (collection of Location objects). 
    """
    def __init__(self, rows, cols): # Define the function and parameters, call each parameter by self.
        """
        Initialize a new Warehouse with 2D grid.
        
        Parameters:
            rows (int): Number of rows in grid.
            cols (int): Number of columns in grid.
        """
        
        self._rows = rows
        self._cols = cols
        self._locations = [[None for _ in range(cols)] for _ in range(rows)] # Allows the 2D array to exist and start functionality in warehouse by iterating rows and columns.

    @property
    def rows(self):
        """Get warehouse rows. """
        return self._rows
    
    @property
    def cols(self):
        """Get warehouse columns. """
        return self._cols

    @property
    def locations(self):
        """Get warehouse locations grid. """
        return self._locations
    
    def valid_position(self, row, col): # Define function to validate a position.
        """
        Check if coordinates are within warehouse bounds.
        
        Parameters:
            row (int): Row coordinate to check.
            col (int): column coordinate to check.
            
        Returns:
            bool: True if valid, False if out of bounds.
        """
        
        return 0 <= row < self._rows and 0 <= col < self._cols # Check if coordinates are within warehouse bounds.

    
    def find_and_remove_product(self, sku): # Define the function to find and remove a product from the list using its unique identifier "SKU" and location.
        """
        Search entire warehouse and remove product by SKU.
        
        Parameters:
            sku (str): Stock Keeping Unit of product to remove.
            
        Returns:
            bool: True if found and removed, False if not found.
        """
        
        for r in range(self._rows): # Iterate through every "r"ow and "c"olumn to access all products.
            for c in range(self._cols):
                location = self._locations[r][c] # Give out the location using the values from the iterated "r"ows and "c"olumns
                if location and location.remove_product(sku): # Check to see if there's a location and if a product is removed.
                    return True # Return removed product
        print("Product not found in warehouse!") # Notify the user there isn't any product matching the indentifier in the warehouse system.
        return False # Returns false to indicate the product was not found or update in the system.
    
    
    def find_and_update_quantity(self, sku, new_quantity): # Define the function to find and update a product quantity from the list using its unique identifier "SKU".
        """
        Search warehouse and update product quantity.
        
        Parameters:
            sku (str): Storage Keeping Unit of product.
            new_quantity (int): New quantity value.
        
        Returns:
            bool: true if updated, False if not found or invalid.
        """
        
        for r in range(self._rows): # Iterate through every "r"ow and "c"olumn to access all products.
            for c in range(self._cols):
                location = self._locations[r][c] # Give out the location using the values from the iterated "r"ows and "c"olumns.
                if location and location.update_quantity(sku, new_quantity): # Check to see if there's a location and if a product's quantity has a new quantity to update y calling its function.
                    return True # Stop loop after finding product.
        
        print("Product not found") # Notify the user the desired product has not been found in the warehouse system.
        return False # Returns false to indicate the product was not found or update in the system.
    
    def find_and_update_price(self, sku, new_price): # Define function to find and update product's price using its SKU.
        """
        Search warehouse and update product price.
        
        Parameters:
            sku (str): Storage Keeping Unit of product.
            new_price (float): New price value.
            
        Returns:
            bool: True if updated, False if not found or invalid.
        """
        
        for r in range(self._rows): # Iterate through every "r"ow and "c"olumn to access all products.
            for c in range(self._cols):
                location = self._locations[r][c] # Give out the location using the values from the iterated "r"ows and "c"olumns.
                if location and location.update_price(sku, new_price): # Check to see if there's a location and if a product's price has a new quantity to update by calling its function.
                    return True # Returns back successful change.
        print("Product not found!") # Notify the user the product has not been found in the warehouse.
        return False # Returns to failed message.
    
    def find_product(self, sku): # Define the function to find a product from the list using its unique identifier "SKU".
        """
        Find product across all warehouse locations.
        
        Parameters:
            sku (str): Storage Keeping Unit to search for product.
        
        Returns:
            Product: The found product object, or None if not found.
        """
        
        for r in range(self._rows): # Iterate through every "r"ow and "c"olumn to access all products.
            for c in range(self._cols):
                location = self._locations[r][c]
                if location: # Check to pass location.
                    for product in location.products: # Iterate through every product in each location.
                        if product.sku == sku: # Check given "SKU" to match product in warehouse.
                            print(f"Found {sku} at ({r}, {c}) with quantity {product.quantity} and price ${product.price:.2f}") # Notify the user the product has been found and provide its "SKU", quantity and price.
                            return product # Return to product.
        print("Product not found!") # Nofity the user their desired product hasn't been found.
        return None # Return nothing to user, indicating failure in finding the product.
    
    def add_location(self, row, col, capacity): # Define function to add location with rows, columns and capacity.
        """
        Add new location to warehouse grid.
        
        Parameters:
            col (str): Column coordinate.
            capacity (int): Maximum capacity for location.
            
        Return:
            bool: True if created, Flase if invalid or exists.
        """
        
        if not self.valid_position(row, col): # Check if coordinates are not valid.
            print("Invalid coordinates!") # Notify the user of invalid coordinates.
            return False # Return invalid coordinates.
        
        if self._locations[row][col] is not None: # Check if a location is not empty. 
            print("Location already exists!") # Notify the user the location exists. Therefore, a new location can't be added.
            return False # Return failed attempt

        self._locations[row][col] = Location(row, col, capacity) # Assign location and values by calling Location class.
        
        print(f"Location ({row}, {col}) created with capacity {capacity}") #Notify the user of the success and with coordinates and capacity.
        return True # Return success.
    
    def remove_location(self, row, col): # Define function to remove location using coordinates.
        """
        Remove location from warehouse if empty.
        
        Parameters:
            row (str): Row coordinate.
            col (str): Column coordinate.
            
        Return:
            bool: True if removed, False if invalid or not empty.
        """
        
        if not self.valid_position(row, col): # Check if coordinates are not valid.
            print("Invalid coordinates!") # Notify the user of invalid coordinates.
            return False # Return invalid coordinates
        self._locations[row][col] # Check if a location is not empty.
        
        location = self._locations[row][col] # Call location with coordinates using "self".
        
        if location is None: # Check if location exists.
            print("Location does not exist!") # Notify the user location does not exist.
            return False # Return failure.
               
        if location.products: # Check if location contains products.
            print("Cannot remove location, location not empty!") # Notify the user the location contains products, therefore it cannot be removed.
            return False # Return failure.
        
        self._locations[row][col] = None # Set given location to "None" therefore removing it from the warehouse.
        print(f"Location ({row}, {col}) removed") # Notify the user the location (given its coordinates) has been deleted.
        return True # Return success.
    
        
    def print_warehouse(self): # Define function to print warehouse layout as 2D Array for user understanding.
        """Text-based 2D array dsiplay."""
        print("\n --- Warehouse Layout ---") # Display name for user friendly experience.
        
        cell_width = 12 # Width of each cell
        
        header = " " * 6 # Column numbers (Times "6" since it starts at 0).
        for c in range(self.cols): # Loop trhough each column.
            header += f"{c:^{cell_width}}" # Take the column number place it centered inside using "^" and give it a width of "cell width".
        print(header) # Display header.
        
        for r in range(self._rows): # A loop that goes through all "r"ows.
            row_display = [] # Display rows in a list
            
            for c in range(self._cols): # A loop that goes through all "c"olumns
                location = self._locations[r][c] # Call location with coordinates using "self".
                
                if location: # Check for location
                    total_qty = sum(p.quantity for p in location.products) # Get total quantity of products using a loop.
                    cell = f"Total:{total_qty}" # Add total quantity product to the cell.                
                else:
                    cell = "Empty" # Add Empty to the cell if no total quantity is added.
                
                row_display.append(cell) # Add all cells inside the row display/list.
            row_line = f"Row {r:<2} " # Sets the "r"ow numbers to the left "<" by 2 spaces.
            for cell in row_display: # Iterates through every column.
                row_line += f"{cell:^{cell_width}}" # Rows and columns are added together with cells centered "^" and width "cell width".
                        
            print(row_line) # Display 2D Array as table.
        

# Test Data:
# Test Products.
product1 = Product(name= "Widget", sku="WDG001", price=10.99, quantity=50) # Indicate product number, name,unique identifier, price and, quantity. 
product2 = Product(name="Gizmo", sku="GZM002", price=19.99, quantity=30) 
product3 = Product(name="Thingamajig", sku="THM003", price=5.99, quantity=100) 
product4 = Product(name= "Doohickey", sku="DHI004", price=15.99, quantity=20) 
product5 = Product (name="Gadget", sku="GDT005", price=8.99, quantity=25) 
product6 = Product (name="Contraption", sku="CNT006", price=12.99, quantity=15) 
product7 = Product (name="Apparatus", sku="APT007", price=6.99, quantity=40) 
product8 = Product (name= "Tool", sku="TL008", price=9.99, quantity=35) 
product9 = Product (name="Accessory", sku="ACC009", price=14.99, quantity=10) 
product10 = Product(name="Implement", sku="IMP010", price=7.99, quantity=45) 
product11 = Product(name="Utensil", sku="UTL011", price=11.99, quantity=20) 
product12 = Product (name="Device", sku="DEV012", price=16.99, quantity=30) 
product13 = Product(name="Equipment", sku="EQT013", price=18.99, quantity=25) 
product14 = Product(name="Fixture", sku="FIX014", price=22.99, quantity=5)


# Test Locations.
location1 = Location(0, 0, 200) # Give each location a number, a row and column and a maximum capacity.
location1.add_product(product1) # Give each numbered location 2 or 1 product.
location1.add_product(product2)

location2 = Location(1, 1, 200)
location2.add_product(product3)
location2.add_product(product4)

location3 = Location(2, 2, 200)
location3.add_product(product5)
location3.add_product(product6)

location4 = Location(3, 3, 200)
location4.add_product(product7)
location4.add_product(product8)

location5 = Location(4, 4, 200)
location5.add_product(product9)
location5.add_product(product10)

location6 = Location(2, 4, 200)
location6.add_product(product11)

location7 = Location(3, 1, 200)
location7.add_product(product12)

location8 = Location(1, 4, 200)
location8.add_product(product13)

location9 = Location(4, 2, 200)
location9.add_product(product14)


# Test Warehouse locations.
warehouse = Warehouse(5, 5) # The parameters indicate a warehouse/array of 5x5.
warehouse.locations[0][0] = location1 # Use numbered locations to be put on their respective row and column inside the warehouse.
warehouse.locations[1][1] = location2
warehouse.locations[2][2] = location3
warehouse.locations[3][3] = location4
warehouse.locations[4][4] = location5
warehouse.locations[2][4] = location6
warehouse.locations[3][1] = location7
warehouse.locations[1][4] = location8
warehouse.locations[4][2] = location9

# Create Tkinter GUI ("Graphical User Interface") so the user has access to the 2D Array.
def display_warehouse(): # Define the displaying function for the warehouse.
    """
    Create and display the Tkinter GUI for warehouse visualization.
    
    Parameters:
        warehouse (Warehouse): The warehouse object to display.
        
    Note:
        This functions blocks until the GUI window is closed!.
    """
    
    window = tk.Tk() # Open the window/interface using Tkinter.
    window.title("Inventory Management system") #Assign a name to the window for user friendly usage.
    
    for i in range(warehouse.rows): # A loop with range of rows that allow the windows and rows to stretch.
        window.grid_rowconfigure(i, weight=1)
                
    for i in range(warehouse.cols): # A loop with range of columns that allow the windows and rows to stretch.
        window.grid_columnconfigure(i, weight=1)
    
    for r in range(warehouse.rows): # Iterate through every "r"ow and "c"olumn to access all products.
        for c in range(warehouse.cols):
            location = warehouse.locations[r][c] # Give out the location using the values from the iterated "r"ows and "c"olumns.
            
            if location is None: # If the location of a product is empty, the grid tile will display the text"Empty" and the background colour will be white.
                text = "Empty"
                bg_color = "white"
                 
            else:
                names = [f"{p.name} (${p.price:.2f}, x{p.quantity})" for p in location.products] # Iterates through products to extract the "names", "price", "quantity" and display them.
                text = "\n".join(names[:4]) if names else "Empty"# Show and limit names to only 4 and give each name its own line.
            
                total_qty = sum(p.quantity for p in location.products) # Total quantity of products for each grid.
                capacity = f"Capacity:{location.capacity}\n" # Shows capacity in location.

                        
                if total_qty == 0: # If total quantity is "0", the background colour is set to white indicating "free"/"empty" space.
                    bg_color = "white"
                elif total_qty < location.capacity * 0.5: # If the total quantity is less than half of the capacity, the colour is set to "green" indicating plenty of space.
                    bg_color = "#90EE90"
                elif total_qty < location.capacity: # If the total quantity is more than half, but less than the full capacity the colour is set to "orange" indicating not much space is left.
                    bg_color = "#FFC44F"
                else: # If the total quantity is the same as the capacity the colour is set to "red" indicating the location to be "full".
                    bg_color = "#FFB6C1"

                text = f"Capacity:{location.capacity}\n{text}"
                
            # 1.Tkinter creates a label inside the window which becomes the main display for each product giving height, width, border width, "solid" to ensure the borders give:
            label = tk.Label(window, text = text, width=22, height=6, borderwidth=1, relief="solid", bg=bg_color) #1.the square shape needed, and it sets the colours to green, white or red
                            
            # This places the label into the grid. Therefore, giving rows and columns as it loops and allowing it to stretch all directions while giving space between columns
            label.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)
    
        
    window.mainloop() # Loop which keeps the window running until a change/input happens.
    
    
def menu(): # Define function to be a menu for users to view and manipulate the warehouse.
    """
    Command Line Interface for the Inevntory Management System.
    
    Provides a text_based menu allowing users to:
    - View warehouse GUI (Option 1)
    - Add/remove/update products (Options 2-5)
    - Search for products (Option 6)
    - Add/remove locations (Option 7-8)
    - Print warehouse layout (Options 9)
    - Exit the syetem (Option 10)
    
    Paramaters:
        warehouse (Warehouse): The warehouse object to manage
    Returns:
        None
    
    Note:
        Uses infinite loop until user selects exit (Option 10).
        Input validation prevents crashes from invalid data types
    """
    while True: # Keeps an infinite loop until a break or stop happens.
        print("\n --- Inventory Management System ---") # Display in a new line the name of the system: "Inventory Management System".
        print("1. Display Warehouse!") # Display a message to the user indicating which number to input to view the warehouse.
        print("2. Add Product!") # Display a message to the user indicating which number to input to add a product.
        print("3. Remove Product!") # Display a message to the user indicating which number to input to remove a product.
        print("4. Update Product quantity!") # Display a message to the user indicating which number to input to update a product's quantity.
        print("5. Update Product Price!") # Display a message to the user indicating which number to input to update a product's price.
        print("6. Search Product!") # Display a message to the user indicating which number to input to search for a product.        
        print("7. Add Location!") # Display a message to the user indicating which number to input to add a location.
        print("8. Remove Location!") # Display a message to the user indicating which number to input to remove a location.
        print("9. Print Warehouse Layout!") # Display a message to the user indicating which number to input to print the Warehouse Layout.        
        print("10. Exit!") # Display a message to the user indicating which number to input to exit the system.
            
        choice = input("Please enter choice: ").strip() # Local varaiable "choice" used to determine what the user desires to do in the "IMS".
            
        if choice == "1": # User chooses to view the warehouse.
            display_warehouse() # Call to the "GUI".
        
        elif choice == "2": # User chooses to add a product.
            name = input("Enter product name: ") # User chooses to input the new product's name and SKU.
            sku = input("Enter sku: ")
            try: # Handles user input conversion and prevents errors caused by invalid input for price, quantity and coordinates.
                price = float(input("Enter price: ")) # User inputs product's price, quantity, row and, column.
                quantity = int(input("Enter quantity: "))
                row = int(input("Enter row: "))
                col = int(input("Enter column: "))
                
                if not warehouse.valid_position(row, col): # Call function to validate position for rows and columns
                    print("Invalid Row/Column Index!")
                    continue
                
                location = warehouse.locations[row][col] # The validated coordinates are used to assign the expected location to the new addded product.
                
                if location is None: # Check if location has not value. Therefore is completely empty (including capacity).
                     capacity = int(input("Enter location capacity: ")) # User inputs new location capacity.
                     location = Location(row, col, capacity) # New location is set with the previous coordinates and capacities given by the user by calling the Location Class.
                     warehouse.locations[row][col] = location # New location is added to the warehouse storage.
                
                product = Product(name, sku, price, quantity) # New product is given its values from the user by calling the Product class.
                
                if location.add_product(product): # Check if product has been added successfully to location.
                    print("Product added to warehouse!") # Notify the user product has been added successfully.
                else:
                    print("Product not added to warehouse...") # If prevoius check fails, notify the user on failure.
            except ValueError:
                print("Invalid entry! \/ (Try again)") # If there's any errors notify the user of invalid entry and encourage to try again for user friendly experience.
                            
        elif choice == "3": # User chooses to input SKU to remove a product.
            sku = input("Enter SKU to remove product: ") # User inputs SKU to identify the product.
            warehouse.find_and_remove_product(sku) # Call in the function to find and remove the product using the SKU.
                
        elif choice == "4": # User chooses to update a product using its SKU.
            sku = input("Enter SKU to update product quantity: ") # User inputs product's SKU.
            try: # Handles user input conversion and prevents errors caused by invalid input in new quantity.
                new_qty = int(input("Enter new product quantity: ")) # User inputs new quantity.
                warehouse.find_and_update_quantity(sku, new_qty) # Call function to find and update product quantity.
            except ValueError: # If "try" encounters an error in input except calls to continue and the user gets notified.
                 print("!Invalid entry! 'Only numbers within the system are allowed'") # User gets notified that there has been an error with their number input.
        
        elif choice == "5": # User chooses to update a product's price using its SKU.
            sku = input("Enter SKU to update price: ") # User inputs product's SKU.
            try: # Handles user input conversion and prevents errors caused by invalid input in new price.
                price = float(input("New Price: ")) # User inputs new price.
                warehouse.find_and_update_price(sku, price) # Call function to find and update product's price using the SKU.
            except ValueError: # If "try" encounters an error in input except calls to continue and the user gets notified.
                print("Invalid input!") # Notify the user of an invalid input.
                
        elif choice == "6": # User chooses to find a product using its SKU.
            sku = input("Enter SKU to find a product: ") # User inputs desired product's SKU.
            warehouse.find_product(sku) # Call function to find product using its SKU.
            
        elif choice == "7": # User chooses to find add a location.
            try: # Handles user input conversion and prevents errors caused by invalid input in new location.
                row = int(input("Enter row: ")) # User inputs rows, columns and capacity.
                col = int(input("Enter col: "))
                capacity = int(input("Enter capacity: "))
                if warehouse.valid_position(row, col): # Call function to validate position for rows and columns.
                    warehouse.add_location(row, col, capacity) # Call function to assign location with capacity and validated coordinates.
                else:
                    print("Invalid Row/Column index!") # Notify the user of invalid coordinates
            except ValueError: # If "try" encounters an error in input except calls to continue and the user gets notified.
                print("Invalid input") # Notify the user of invalid input.
        
        elif choice == "8": # User chooses to remove a location.
            try: # Handles user input conversion and prevents errors caused by invalid input in new location.
                row = int(input("Enter row: ")) # User inputs rows and columns
                col = int(input("Enter col: "))
                if warehouse.valid_position(row, col): # Call function to validate position for rows and columns.
                    warehouse.remove_location(row, col) # Call function to remove location using validated coordinates.
                else:
                    print("Invalid Row/Column index!") # Notify the user of invalid coordinates
            except ValueError: # If "try" encounters an error in input except calls to continue and the user gets notified.
                print("Invalid input")
        
        elif choice == "9": # User chooses to print the warehouse
            if warehouse is None:
                print("Warehouse could not be started")
            warehouse.print_warehouse() # Calls function to print warehouse layout.
                    
        elif choice == "10": # User chooses to exit the warehouse after viewing and/or manipulating it.
            print("Closing warehouse!") # Notifies the user the warehouse is being closed.
            break # Stop the ungoing loop of "while true"
            
        else:
            print("Invalid input!! Choose between 1 to 10!") # Notify the user their entry is invalid and must choose from 1 - 5, ensuring a user friendly experience.


# Call to run the menu program.
if __name__ == "__main__":
    menu()
