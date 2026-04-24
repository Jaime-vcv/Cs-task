import tkinter as tk # It imports tkinter to create the GUI, and it is used as "tk" to facilitate usage.


# Warehouse error handling
class WarehouseError(Exception):
    """Custom exception for warehouse operations.
    Demonstrates INHERITANCE (inherits from Exception)."""
    pass


# The product class to use for each type of product.
class Product:
    """
    Represents a product in inventory.
    Demonstrates ENCAPSULATION (private attributes with getters/setters).
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
        if price <= 0: # Validation price check.
            raise WarehouseError("Price must be greater than 0!")
        
        if quantity <= 0: # Validation quantity check.
            raise WarehouseError("Quantity must be greater than 0!")
        
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
    
    # OOP: ENCAPSULATION - Private attributes accessed via property decorators.
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
        
        # Business rule: Free of negative prices indicate data entry errors.
        # This prevents invalid financial transactions in the system.
        if value <= 0:
            print("Error! Price must be greater than 0!")
            raise WarehouseError("Price must be greater than 0")
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
            raise WarehouseError("Quantity cannot be negative or 0")
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
        """Get row coordinate."""
        return self._row
    
    @property
    def col(self):
        """Get column coordinate."""
        return self._col
    
    @property
    def capacity(self):
        """Get location capacity."""
        return self._capacity
    
    @property
    def products(self):
        """Return copy of products list to prevent external modification."""
        return self._products.copy()    
    
    def __str__(self):
        """POLYMORPHISM: Same method as Product different behavior."""
        items = len(self._products)
        return f"Location ({self._row},{self._col}) - {items} items stored."
        
    def add_product(self, product): # Define the function to add a product to the list.
        """
        Add a product to this location if capacity allows.
        
        Parameters:
            product (Product): The product to add.
        
        Returns:
            bool: True if added successfully, False if rejected.
        
        Raises:
            None (errors are handled internally with print statements)
        
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
        # LOGIC: Calculate total quantity to check against capacity    
        current_items = sum(p.quantity for p in self._products) # Sums the quantity of products to compare to the capacity, storing the quantity in a local variable.
        
        if current_items + product.quantity <= self._capacity: # Checks whether there's enough space by summing the total amount and comparing it to the capacity.
            self._products.append(product) # Composition: Location maintains full control over its products
            # Products are stored internally to enforce capacity limits
            return True # Returns added product.
        else:
            print(f"Location ({self._row}, {self._col}) is full") # Prints the location of where the product would have been and declares the space to be full.
            return False # Returns to function.

    def remove_product(self, sku): # Define the function to remove a product from the list using its unique identifier "SKU" (Stock Keeping Unit).
            """Remove product by SKU. """
            for product in self._products: # Iterate using "product" as a local variable throughout 'location(products)'.
                if product.sku == sku: # Compares products unique identifier for a match with the desired product to be removed.
                    self._products.remove(product) # After a successful comparison the chosen product is deleted through its location.
                    print(f"{sku} has been removed from the location ({self._row}, {self._col})") # Give a message to the user indicating that the "product" referred to by its SKU has been removed in its set location.
                    return True # Returns successful removed product.
            return False # Returns to warehouse for message handling.

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
                    return False # Returns to if statement.
        return False # Returns to loop.

    def update_price(self, sku, new_price): # Define function to update product price using its SKU.
        # FIXED: Removed "Product not found in Location print from here"
        # Warehouse.find_and_update_price() now handles the single
        # "not found" message after searching all Locations, preventing
        # duplicate error spam (One duplicate per empty Location in warehouse)
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
        print(f"Product {sku} not found in any location!") # Notify the user there isn't any product matching the identifier in the warehouse system.
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
        
        print(f"Product {sku} not found in any location!") # Notify the user the desired product has not been found in the warehouse system.
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
        print(f"Product {sku} not found in any location!") # Notify the user the product has not been found in the warehouse.
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
    # Parameters: Document expected inputs.
    
    def find_products_by_name(self, name): # Define function to find product by its name.
        """
        Search for products by name across all locations.
        
        Parameters:
            name (str): Product name to search for (partial match allowed).
            
        Returns:
            list: List of tuples (row, col, product) for matches.
        """
        results = [] # Store search results in a list.
        search_name = name.lower() # Local variable "search name" used to refer to name for searching.
        
        for r in range(self._rows): # Iterate through every "r"ow and "c"olumn to access all products.
            for c in range(self._cols):
                location = self._locations[r][c]
                if location: # Check to pass location.
                    for product in location.products: # Iterate through every product in each location.
                        if search_name in product.name.lower(): # Match the searched name with the name in warehouse.
                            results.append((r, c, product)) # Add results including the coordinates.
        
        return results
    
    def find_product_flexible(self, identifier): # Define function to find product with either name or SKU.
        """
        Find product by SKU or name.
        Tries SKU first, then falls back to name search.
        
        Parameters:
            identifier (str): SKU or product name to search.
            
        Returns:
            tuple: (product, row, col) if found, (None, None, None) if not found.
            list: If multiple name matches found, returns list of options.
        """
        # Try exact SKU match first
        for r in range(self._rows): # Iterate through every "r"ow and "c"olumn to access all products.
            for c in range(self._cols):
                location = self._locations[r][c]
                if location: # Check to pass location.
                    for product in location.products: # Iterate through every product in each location.
                        if product.sku == identifier: # Check for matching SKUs in products
                            return (product, r, c, "sku") # Give back results including coordinates and "sku".
        
        # Fallback: search by name
        name_results = self.find_products_by_name(identifier) # Call a search by name only.
        
        if len(name_results) == 0: # Check if there's a name.
            print(f"No product found with SKU or name '{identifier}'") # Notify the user no product has been found.
            return (None, None, None, None) # Give out none values. Therefore, NOTHING!!!!
        
        elif len(name_results) == 1: # If there's name
            # Single match found by name
            r, c, product = name_results[0] # Use values from warehouse and print result.
            print(f"Found '{product.name}' (SKU: {product.sku}) at ({r}, {c})") # Notify the user their product has been found successfully.
            return (product, r, c, "name") # Give out the product with coordinates and name.
        
        else:
            # Multiple matches — return list for user selection
            print(f"\nMultiple products found matching '{identifier}':") # Notify the user when more than one product matches the search.
            for i, (r, c, product) in enumerate(name_results, 1): # Iterate through results.
                print(f"  {i}. {product.name} (SKU: {product.sku}) at ({r}, {c})") # Print search results.
            return (name_results, None, None, "multiple") # Give out the products.
    
    def add_location(self, row, col, capacity): # Define function to add location with rows, columns and capacity.
        """
        Add new location to warehouse grid.
        
        Parameters:
            col (str): Column coordinate.
            capacity (int): Maximum capacity for location.
            
        Return:
            bool: True if created, False if invalid or exists.
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
    
    def remove_location(self, row, col, force = False): # Define function to remove location using coordinates.
        """
        Remove location from warehouse.
        IF products exist and force=False, signals confirmation needed.
        
        Parameters:
            row (str): Row coordinate.
            col (str): Column coordinate.
            force (bool): If True, remove even if products exists.
            
        Return:
            bool: True if removed, False if invalid.
            str: "has_products" if confirmation needed.
        """
        
        if not self.valid_position(row, col): # Check if coordinates are not valid.
            print("Invalid coordinates!") # Notify the user of invalid coordinates.
            return False # Return invalid coordinates
        
        location = self._locations[row][col] # Call location with coordinates using "self".
        
        if location is None: # Check if location exists.
            print("Location does not exist!") # Notify the user location does not exist.
            return False # Return failure.
               
        if location.products and not force: # Check if location contains products.
            return "has_products"
        
        self._locations[row][col] = None # Set given location to "None" therefore removing it from the warehouse.
        print(f"Location ({row}, {col}) removed") # Notify the user the location (given its coordinates) has been deleted.
        return True # Return success.
    
        
    def print_warehouse(self): # Define function to print warehouse layout as 2D Array for user understanding.
        """Text-based 2D array display."""
        print("\n --- Warehouse Layout ---") # Display name for user friendly experience.
        
        cell_width = 12 # Width of each cell
        
        header = " " * 6 # Column numbers (Times "6" since it starts at 0).
        for c in range(self.cols): # Loop through each column.
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
    
    
    def print_inventory_report(self): # Define function to iterate through warehouse and print a report based on the inventory.
        """
        Print detailed inventory report shwoing all products across warehouse.
        
        Returns:
            None
        """
        print("\n" + "=" * 60) # Add lines for better design.
        print("INVENTORY REPORT".center(60)) # Inventory title.
        print("=" * 60)
        
        total_products = 0 # Local variable used to represent total amount of products in warehouse.
        total_value = 0.0 # Local variable used to represent total value of products in warehouse.
        found_any = False # Local variable with a "False" boolean to represent a not found product in warehouse.
        
        for r in range(self._rows): # Iterate through every "r"ow and "c"olumn.
            for c in range(self._cols):
                location = self._locations[r][c] # Set location to be row and column coordinates.
                if location and location.products: # Check if a location has a product.
                    found_any = True # Set found to be "True" therefore passing product as found in warehouse.
                    print(f"-" * 40) # Add a line for better design.
                    for product in location.products: # Iterate through every product for a location with products.
                        total_products += 1 # Add one per product found.
                        value = product.price * product.quantity # Set value to be the product's price times the product's quantity
                        total_value += value # Set the total value of the warehouse to be the value from the product's price and quantity 
                        
                        print(f" Name: {product.name}") # Print each product's name, SKU, price (limited to 2 decimal places), quantity and value(limited to 2 decimal places)
                        print(f" SKU:  {product.sku}")
                        print(f" Price: ${product.price:.2f}")
                        print(f" Quantity: {product.quantity}")
                        print(f" Value: {value:.2f}")
        if not found_any: # If any product has not been found after iterating through the warehouse.
            print("No products were found in the Warehouse.") # Notify the user of the absence of products in the warehouse.
        else:
            print("=" * 60) # Add lines for better design.
            print(f"Total product types: {total_products}") # Print total product types:
            print(f"Total Inventory value ${total_value:.2f}") # Print total inventory value of the warehouse (limited to 2 decimal places).
            print("=" * 60)
                

# Populate Warehouse with data
def setup_warehouse():
    warehouse = Warehouse(5, 5) # Create a 5 by 5 warehouse.

    products = [
        Product(name= "Widget", sku="WDG001", price=10.99, quantity=50), # Indicate product number, name,unique identifier, price and, quantity. 
        Product(name="Gizmo", sku="GZM002", price=19.99, quantity=30), 
        Product(name="Thingamajig", sku="THM003", price=5.99, quantity=100), 
        Product(name= "Doohickey", sku="DHI004", price=15.99, quantity=20), 
        Product(name="Gadget", sku="GDT005", price=8.99, quantity=25), 
        Product(name="Contraption", sku="CNT006", price=12.99, quantity=15), 
        Product(name="Apparatus", sku="APT007", price=6.99, quantity=40), 
        Product(name= "Tool", sku="TL008", price=9.99, quantity=35), 
        Product(name="Accessory", sku="ACC009", price=14.99, quantity=10), 
        Product(name="Implement", sku="IMP010", price=7.99, quantity=45), 
        Product(name="Utensil", sku="UTL011", price=11.99, quantity=20), 
        Product(name="Device", sku="DEV012", price=16.99, quantity=30), 
        Product(name="Equipment", sku="EQT013", price=18.99, quantity=25), 
        Product(name="Fixture", sku="FIX014", price=22.99, quantity=5)
    ]


    locations_data = [ # Give each location a row a column a maximum capacity and its corresponding product.
                      
            # FIXED: Capacity changed from 5 to 200 because original capacity
            
            # was smaller than product quantities (50, 30, 100), causing
            
            # add_product() to silently return False with no items added.
            
     (0, 0, 200, [0, 1]), # Widget, Gizmos

     (1, 1, 200, [2, 3]), # Thingamajig, Doohickey

     (2, 2, 200, [4, 5]), # Gadget, Contraption

     (3, 3, 200, [6, 7]), # Apparatus, Tool

     (4, 4, 200, [8, 9]), # Accessory, Implement

     (2, 4, 200, [10]), # Utensil

     (3, 1, 200, [11]), # Device

     (1, 4, 200, [12]), # Equipment

     (4, 2, 200, [13]) # Fixture
     
 ]


    for row, col, capacity, product_indices in locations_data: # Collect all product primary data.
        warehouse.add_location(row, col, capacity) # Add products to location with their respective data.
        for idx in product_indices: # Using indices/coordinates.
            warehouse.locations[row][col].add_product(products[idx]) # Use the coordinate/indices to be added to the warehouse.
    return warehouse # Give back warehouse with inserted products.


# Test warehouse capabilities
def run_unit_tests():
    """
    Unit testing for core functionality.
    Demonstrates validations of critical methods.
    
    Returns:
        bool: True if all tests  pass, False otherwise.
    """
    print("\n=== RUNNING UNIT TESTS ===")
    all_passed = True
    
    # Test 1: Product creation and validation.
    try:
        p = Product("Test", "TST001", 10.0, 5)
        assert p.name == "Test"
        assert p.sku == "TST001"
        print("Pass: Product creation and getters")
    except Exception as e:
        print(f"Fail: Product creation - {e}")
        all_passed = False
        
    
    # Test 2: Price validation (exception handling)
    try:
        p = Product("Test2", "TST002", 10.0, 5)
        p.price = -5
        print("Fail: Price validation should have raised exception")
        all_passed = False
    except WarehouseError:
        print ("PASS: Price validation rejects negative values")
    except Exception as e:
        print(f"FAIL: Price validation wrong exception - {e}")
        all_passed = False
    
    
    # Test 3: Location capacity enforcement
    try:
       loc = Location(0, 0, 100)
       p1 = Product("A", "A001", 5.0, 60)
       p2 = Product("B", "B002", 5.0, 50)
       result1 = loc.add_product(p1)
       result2 = loc.add_product(p2)
       assert result1 == True, "Should add first product!"
       assert result2 == False, "Should reject second product since (60+50 > 100)"
       print("PASS: Location capacity enforcement")
    except Exception as e:
        print(f"FAIL: Location capacity - {e}")
        all_passed = False
        
    
    # Test 4: Valid position checking
    try:
        wh = Warehouse(5, 5)
        assert wh.valid_position(0, 0) == True
        assert wh.valid_position(4, 4) == True
        assert wh.valid_position(5, 5) == False
        assert wh.valid_position(-1, 0) == False
        print("PASS: Position validation")
    except Exception as e:
        print(f"FAIL: Position validation - {e}")
        all_passed = False
        
    
    # Test 5: Duplicate SKU prevention
    try:
        loc = Location(0, 0, 200)
        p1 = Product("Item", "SAME001", 10.0, 5)
        p2 = Product("Item2", "SAME001", 15.0, 10)
        loc.add_product(p1)
        result = loc.add_product(p2)
        assert result == False, "Should reject duplicate SKU"
        print("PASS: Duplicate SKU prevention")
    except Exception as e:
        print(f"FAIL: Duplicate SKU - {e}")
        all_passed = False
    
    if all_passed:
        print("=== ALL TESTS PASSED! ===")
    else:
        print("=== SOME TESTS FAILED ===")
    
    return all_passed


# Create Tkinter GUI ("Graphical User Interface") so the user has access to the 2D Array.
def display_warehouse(warehouse): # Define the displaying function for the warehouse.
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
    
    
# Identify a product in the warehouse.
def get_product_identifier():
    """
    Prompt user for product identifier and validate input.
    
    Returns:
        str: SKU or name entered by user.
    """
    return input("Enter SKU or product name: ").strip()
    
def menu(warehouse): # Define function to be a menu for users to view and manipulate the warehouse.
    """
    Command Line Interface for the Inventory Management System.
    
    Provides a text_based menu allowing users to:
    - View warehouse GUI (Option 1)
    - Add/remove/update products (Options 2-5)
    - Search for products (Option 6)
    - Add/remove locations (Option 7-8)
    - Print inventory report (Option 9)
    - Print warehouse layout (Options 10)
    - Run unit tests (Option 11)
    - Exit the system (Option 12)
    
    Parameters:
        warehouse (Warehouse): The warehouse object to manage.
    Returns:
        None
    
    Note:
        Uses infinite loop until user selects exit (Option 12).
        Input validation prevents crashes from invalid data types.
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
        print("9. Print Inventory Report!") # Display a message to the user indicating which number to input to remove a location (Even if it contains products)
        print("10. Print Warehouse Layout!") # Display a message to the user indicating which number to input to print the Warehouse Layout.        
        print("11. Run Unit Tests!") # Display a message to the user indicating which number to input to run unit tests. 
        print("12. Exit!") # Display a message to the user indicating which number to input to exit the system.
            
        choice = input("Please enter choice: ").strip() # Local variable "choice" used to determine what the user desires to do in the "IMS".
            
        if choice == "1": # User chooses to view the warehouse.
            display_warehouse(warehouse) # Call to the "GUI".
        
        elif choice == "2": # User chooses to add a product.
            name = input("Enter product name: ") # User chooses to input the new product's name and SKU.
            sku = input("Enter sku: ")
            try: # Handles user input conversion and prevents errors caused by invalid input for price, quantity and coordinates.
                price = float(input("Enter price: ")) # User inputs product's price, quantity, row and, column.
                quantity = int(input("Enter quantity: "))
                row = int(input("Enter row: "))
                col = int(input("Enter column: "))
                # VALIDATION: Check bounds before accessing grid.
                if not warehouse.valid_position(row, col): # Call function to validate position for rows and columns.
                    print("Invalid Row/Column Index!")
                    continue
                
                location = warehouse.locations[row][col] # The validated coordinates are used to assign the expected location to the new added product.
                
                if location is None: # Check if location has not value. Therefore is completely empty (including capacity).
                     capacity = int(input("Enter location capacity: ")) # User inputs new location capacity.
                     location = Location(row, col, capacity) # New location is set with the previous coordinates and capacities given by the user by calling the Location Class.
                     warehouse.locations[row][col] = location # New location is added to the warehouse storage.
                
                product = Product(name, sku, price, quantity) # New product is given its values from the user by calling the Product class.
                
                if location.add_product(product): # Check if product has been added successfully to location.
                    print("Product added to warehouse!") # Notify the user product has been added successfully.
                else:
                    print("Product not added to warehouse...") # If previous check fails, notify the user on failure.
            except ValueError:
                print("Invalid entry! \/ (Try again)") # If there's any errors notify the user of invalid entry and encourage to try again for user friendly experience.
                            
        elif choice == "3": # User chooses to remove a product using its SKU or name.
            identifier = get_product_identifier() # Use the identifier variable for a match.
            result = warehouse.find_product_flexible(identifier) # Call in the function to use both SKU and Name for removal.
            
            if result[3] == "multiple": # Check if more than 1 product appears as a "match".
                options = result[0] # Call out options for user choice.
                try:
                    selection = int(input("Enter number of product to remove (0 to cancel): ")) # Give the user the option to remove a product out of multiple products.
                    if 1 <= selection <= len(options): # Print product's values based on user choice.
                        r, c, product = options[selection - 1] # Check for user's answer, on whether they cancel or choose a product.
                        warehouse.locations[r][c].remove_product(product.sku) # Remove selected product.
                    elif selection == 0:
                        print("Removal cancelled.") # Notify the user of the cancellation of the process.
                except ValueError:
                    print("Invalid selection.") # Call "ValueError" to handle errors.
            elif result[0] is not None: # When there's a product matching search and not multiple.
                product, r, c, _ = result
                warehouse.locations[r][c].remove_product(product.sku) # Iterate through warehouse and call in to delete the matched product.
            else:
                print("Product not found.") # Notify the user product has not been found in the warehouse.
                
        elif choice == "4": # User chooses to update a products quantity using its SKU or Name.
            identifier = get_product_identifier() # Use the identifier variable for a match.
            result = warehouse.find_product_flexible(identifier) # Call in the function to use both SKU and Name for updating.
            
            if result[3] == "multiple": # Check if more than 1 product appears as a "match".
                options = result[0] # Call out options for user choice.
                try:
                    selection = int(input("Enter number of product to update (0 to cancel): ")) # The user is given the option to update a product out of the multiple options.
                    if 1 <= selection <= len(options): # Print product's values based on user choice.
                        r, c, product = options[selection - 1] # Check for user's answer, on whether they cancel or choose a product.
                        try:
                            new_qty = int(input("Enter new product quantity: ")) # Enter new product's quantity and assign it to the variable new_qty.
                            warehouse.locations[r][c].update_quantity(product.sku, new_qty) # In warehouse, in locations of warehouse, update the quantity of product for new quantity.
                        except ValueError:
                            print("Invalid quantity.") # Notify the user of an invalid entry for new quantity.
                    elif selection == 0: # User chooses to cancel the process.
                        print("Update cancelled.") # Notify the user of the cancellation of the process.
                except ValueError: # Value error handling.
                    print("Invalid selection.") # Notify the user of the invalid selection.
            elif result[0] is not None: # When there's a product matching search and not multiple.
                product, r, c, _ = result # Have coordinates and "nothing" for the quantity.
                try:
                    new_qty = int(input("Enter new product quantity: ")) # Use local variable to assign new quantity.
                    warehouse.locations[r][c].update_quantity(product.sku, new_qty) # In warehouse, in locations of warehouse, update the quantity of product for new quantity.
                except ValueError: # Call ValueError for error handling.
                    print("Invalid quantity.") # Notify the user of invalid quantity.
            else:
                print("Product not found.") # Notify the user their desired product hasn't been found.
                       
        elif choice == "5": # User chooses to update a product's price.
            identifier = get_product_identifier() # Use the identifier variable for a match.
            result = warehouse.find_product_flexible(identifier) # Call in the function to use both SKU and Name for updating.
            
            if result[3] == "multiple": # Check if more than 1 product appears as a "match".
                options = result[0] # Call out options for user choice.
                try:
                    selection = int(input("Enter number of product to update (0 to cancel): ")) # The user is given the option to update a product out of the multiple options
                    if 1 <= selection <= len(options): # Check for user's answer, on whether they cancel or choose a product.
                        r, c, product = options[selection - 1]
                        try:
                            new_price = float(input("New Price: "))
                            warehouse.locations[r][c].update_price(product.sku, new_price)
                        except ValueError:
                            print("Invalid price.")
                    elif selection == 0:
                        print("Update cancelled.")
                except ValueError:
                    print("Invalid selection.")
            elif result[0] is not None:
                product, r, c, _ = result
                try:
                    new_price = float(input("New Price: "))
                    warehouse.locations[r][c].update_price(product.sku, new_price)
                except ValueError:
                    print("Invalid price.")
            else:
                print("Product not found.")
                
        elif choice == "6": # User chooses to find a product in the warehouse using its SKU or Name.
            identifier = input("Enter SKU or product name to search: ").strip() # Use the identifier variable to match any search. (leave no space in input ensuring no induced error).
            result = warehouse.find_product_flexible(identifier) # Call in the function search for both options (SKU or Name).
            
            if result[3] == "multiple": # Check if more than 1 product appears as a "match".
                # User must select from multiple matches
                options = result[0] # Call out options for user choice.
                try:
                    selection = int(input("Enter number of product to select (0 to cancel): ")) # Give the user the choice to choose from multiple products for their desired selection.
                    if 1 <= selection <= len(options): # Check for user's answer, on whether they cancel or choose a product.
                        r, c, product = options[selection - 1] # Take a product based in user selection.
                        print(f"\nSelected: {product.name}") # Print and notify: Product selected(name), SKU, price(2 decimal places), quantity and location/coordinate.
                        print(f"  SKU:      {product.sku}")
                        print(f"  Price:    ${product.price:.2f}")
                        print(f"  Quantity: {product.quantity}")
                        print(f"  Location: ({r}, {c})")
                    elif selection == 0: # Cancel search is user decided to stop.
                        print("Search cancelled.") # User gets notified of the cancellation of the process.
                except ValueError: # Use "ValueError" for error handling.
                    print("Invalid selection.") # Notify the user of an invalid selection.
            
            elif result[0] is not None: # When there's a product matching search and not multiple.
                product, r, c, match_type = result
                print(f"\n{'SKU' if match_type == 'sku' else 'Name'} match found:") # Print all product details.
                print(f"  Name:     {product.name}")
                print(f"  SKU:      {product.sku}")
                print(f"  Price:    ${product.price:.2f}")
                print(f"  Quantity: {product.quantity}")
                print(f"  Location: ({r}, {c})")
                            
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
                   result = warehouse.remove_location(row, col) # Call function to remove location using validated coordinates.
                   if result == "has_products": # Check if there are products in location.
                        confirm = input("There are products in this location. Do you still want to remove it (YES/NO) ").strip().upper() # Notify the user of the existence of products in location, ask if they want to proceed on deletion (YES/NO) "no space & capitals"
                        if confirm == "YES": # User chooses to continue with removal of location and its products.
                            warehouse.remove_location(row, col, force =True) # Call function to remove location.
                        else:
                            print("Removal cancelled.") # If user decides to cancel procedure.
                else:
                    print("Invalid Row/Column index!") # Notify the user of invalid coordinates
            except ValueError: # If "try" encounters an error in input except calls to continue and the user gets notified.
                print("Invalid input")
        
        elif choice == "9": # User chooses to print inventory report.
            warehouse.print_inventory_report() # Calls the function to print the inventory report through warehouse.
        
        elif choice == "10": # User chooses to print the warehouse
            if warehouse is None:
                print("Warehouse could not be started")
            else:
                warehouse.print_warehouse() # Calls function to print warehouse layout.
               
        elif choice == "11": # User chooses to run unit tests
            run_unit_tests()       
                    
        elif choice == "12": # User chooses to exit the warehouse after viewing and/or manipulating it.
            print("Closing warehouse!") # Notifies the user the warehouse is being closed.
            break # Stop the ongoing loop of "while true"
            
        else:
            print("Invalid input!! Choose between 1 to 12!") # Notify the user their entry is invalid and must choose from 1 - 12, ensuring a user friendly experience.


# Call to run the menu program.
if __name__ == "__main__":
    #FIXED: Originally wrote!! 'warehouse = setup_warehouse' (missing parentheses)
    # which assigned the function object instead of calling it, causing:
    # AttributeError: 'function' object has not attribute 'rows'
    # This error happened twice, now I make sure to type in my parentheses.
    warehouse = setup_warehouse()
    menu(warehouse)
