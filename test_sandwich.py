import inspect
import unittest
import random
import re
# Attempt to account for some typos
try:
    from sandwich import Sandwich
except ImportError:
    from sandwich import Sandwhich as Sandwich
try:
    from sandwich import Meal
except ImportError:
    from sandwich import meal as meal
try:
    from sandwich import KidsMeal
except ImportError:
    from sandwich import Kids as KidsMeal


def make_arg(name):
    name = name.lower()
    if "order" in name or "number" in name or "num" in name or "ord" in name:
        return random.randint(100, 300)
    elif "bread" in name or "bred" in name:
        # Went to wikipedia and started copying
        return random.choice(["Strucia", "Sangak", "Sourdough", "White bread", "Wholewheat", "Rye", "Ciabatta",
                              "Pumpernickel", "Challah", "Brioche", "Focaccia", "Aish merahrah", "Anadana", "Anpan",
                              "Appam", "Arboud", "Arepa", "Babka", "Bakarkhani", "Balep korkun", "Bammy", "Bánh mì",
                              "Bannock", "Barmbrack", "Barbari", "Bazin", "Bazlama", "Bhakri", "Bialy", "Bibingka",
                              "Bing", "Biscotti", "Blaa", "Bolani", "Borlengo", "Borodinsky", "Boule", "Broa",
                              "Catalán", "Chapati", "Cuban"])
    elif "meat" in name or "met" in name:
        return random.choice(["Spam", "Spam", "Spam", "Ham", "Bef", "Turkey", "Chicken Salad", "Rotisserie Chicken",
                              "Rotisserie Turkey", "Turkey", "Spam", "Roast Beef", "Bologna", "Meatloaf", "Bacon",
                              "Pimento Cheese"])
    elif "veg" in name:
        return random.choice(["Tomato", "Guac", "Cucumber", "Spinach"])
    elif "drink" in name or "drk" in name or "liquid" in name:
        return random.choice(["Water", "Dr. Pepper", "Coke", "Pepsi", "Mountain Dew", "Sprite", "Orange Juice",
                              "Starry", "Powerade", "H2O", "Milk", "Sprite", "Sprite Cranberry", "Fanta", "Apple Juice",
                              "Coffee", "Fruit Punch", "Grape Juice", "Tea", "Sweet Tea", "Chocolate Milk"])
    elif "side" in name or "sd" in name or "fries" in name or "chips" in name:
        return random.choice(["Fries", "Chips", "Cookie", "Apple Sauce", "Onion Rings", "Apples", "Soup", "Tater Tots",
                              "Potato Wedges", "Fried Potatoes", "Curly Fries", "Stuffed Peppers", "Corn Chips",
                              "Doritos", "Beans and Rice", "Banana"])
    elif "toy" in name or "ty" in name or "kid" in name:
        return random.choice(["Action figure", "Animal figure", "Tiny skateboard", "Movie toy"])
    elif "topping" in name or "tops" in name:
        return []
    return "Something"


class TestLab5(unittest.TestCase):
    def setUp(self) -> None:
        # Instantiate the Sandwich class
        sandwich_const_args = [param for param in
                               list(inspect.signature(Sandwich.__init__).parameters) if param != "self"]
        sandwich_args = (make_arg(arg_name) for arg_name in sandwich_const_args)
        self.sandwich = Sandwich(*sandwich_args)
        # Get the methods, ignoring private methods and dunder methods
        self.sandwich_methods = [method for method in dir(self.sandwich) if not method.startswith("_")]

        # Instantiate the Meal class
        meal_const_args = [param for param in
                           list(inspect.signature(Meal.__init__).parameters) if param != "self"]
        meal_args = (make_arg(arg_name) for arg_name in meal_const_args)
        self.meal = Meal(*meal_args)
        # Get the methods, ignoring private methods and dunder methods
        self.meal_methods = [method for method in dir(self.meal) if not method.startswith("_")]

        # Instantiate the KidsMeal Class
        kids_meal_const_args = [param for param in
                                list(inspect.signature(KidsMeal.__init__).parameters) if param != "self"]
        kids_meal_args = (make_arg(arg_name) for arg_name in kids_meal_const_args)
        self.kids_meal = KidsMeal(*kids_meal_args)
        # Get the methods, ignoring private methods and dunder methods
        self.kids_meal_methods = [method for method in dir(self.kids_meal) if not method.startswith("_")]

    def test_sandwich_order(self):
        # Figure out what the order method is
        order_method = [method for method in self.sandwich_methods if "order" in method.lower() or "number" in
                        method.lower()][0]
        # make sure we have it, then make sure it is a property
        self.assertTrue(len(order_method) > 0, msg="You did not define an order property")
        self.assertFalse(callable(getattr(self.sandwich, order_method)),
                         msg="You defined an order method without the property decorator")

    def test_sandwich_bread(self):
        # Figure out what the bread method is
        bread_method = [method for method in self.sandwich_methods if "bread" in method.lower() or "brd" in
                        method.lower()][0]
        # make sure we have it, then make sure it is a property
        self.assertTrue(len(bread_method) > 0, msg="You did not define a bread property")
        self.assertFalse(callable(getattr(self.sandwich, bread_method)),
                         msg="You defined a bread method without the property decorator")

        # This will throw an exception if it is not a setter
        # setattr(self.sandwich, bread_method, "Pan")

    def test_sandwich_meat(self):
        # Figure out what the meat method is
        meat_method = \
            [method for method in self.sandwich_methods if "meat" in method.lower() or "met" in method.lower() or "veg"
             in method.lower() or "mainfill" in method.lower()][0]
        # make sure we have it, then make sure it is a property
        self.assertTrue(len(meat_method) > 0, msg="You did not define a meat/veggie property")
        self.assertFalse(callable(getattr(self.sandwich, meat_method)),
                         msg="You defined a meat/veggie method without the property decorator")
        # This will throw an exception if it is not a setter
        # setattr(self.sandwich, meat_method, "Carne")

    def test_sandwich_price_info(self):
        # Figure out what the price method is
        price_method = [method for method in self.sandwich_methods if "price" in method.lower() or "prc" in
                        method.lower()][0]
        # make sure we have it, then make sure it is a property
        self.assertTrue(len(price_method) > 0, msg="You did not define a price property for Sandwich")
        self.assertFalse(callable(getattr(self.sandwich, price_method)),
                         msg="You defined a price method for Sandwich without the property decorator")

        self.assertEqual(getattr(self.sandwich, price_method), 3.75,
                         msg="Your price without toppings for Sandwich is incorrect")

        # Figure out what the topping methods are
        topping_methods = [method for method in self.sandwich_methods if "get" not in method.lower() and
                           "top" in method.lower() or "filln" in method.lower()]
        add_topping_method = [method for method in topping_methods if "add" in method.lower() or "remove" not in
                              method.lower()][0]
        remove_topping_method = [method for method in topping_methods if "remove" in method.lower() or
                                 "rmv" in method.lower() or "add" not in method.lower()][0]
        # Make sure we have the methods
        self.assertTrue(len(add_topping_method) > 0, msg="You do not have a method to add toppings for Sandwich")
        self.assertTrue(len(remove_topping_method) > 0, msg="You do not have a method to remove toppings for Sandwich")

        # If they're callable (done correctly), use them
        if callable(getattr(self.sandwich, add_topping_method)) and \
                callable(getattr(self.sandwich, remove_topping_method)):
            # Add some toppings
            getattr(self.sandwich, add_topping_method)("Tomato")
            getattr(self.sandwich, add_topping_method)("Lettuce")

            # Check the price
            self.assertEqual(getattr(self.sandwich, price_method), 4.75,
                             msg="Your price for two toppings is incorrect")

            # Remove a topping
            getattr(self.sandwich, remove_topping_method)("Lettuce")

            # Check the price again
            self.assertEqual(getattr(self.sandwich, price_method), 4.25,
                             msg="Your price for one topping is incorrect")

        # If they're setters (why, I don't know), use it as a setter
        else:
            print("=" * 20 + "\nAttempting secondary test. This might fail\n" + "=" * 20)
            # Add some toppings
            setattr(self.sandwich, add_topping_method, "Tomato")
            setattr(self.sandwich, add_topping_method, "Lettuce")

            # Check the price
            self.assertEqual(getattr(self.sandwich, price_method), 4.75,
                             msg="Your price for two toppings in Sandwich is incorrect")

            # Remove a topping. This will probably fail
            setattr(self.sandwich, remove_topping_method, "Tomato")

            # Check the price again
            self.assertEqual(getattr(self.sandwich, price_method), 4.25,
                             msg="Your price for one topping in Sandwich is incorrect")

        # Figure out what the info method is
        info_method = [method for method in self.sandwich_methods if "info" in method.lower()][0]

        # Make sure we can use it
        self.assertTrue(len(info_method) > 0, msg="You do not have an info method for Sandwich")

        if callable(getattr(self.sandwich, info_method)):
            # Use it
            print("=" * 20 + "\nSandwich:\n")
            getattr(self.sandwich, info_method)()
            print("=" * 20)
        else:
            # Use it
            print("=" * 20 + "\nSandwich (as a property):\n")
            getattr(self.sandwich, info_method)
            print("=" * 20)

    def test_meal_subclass(self):
        # Short circuit redundant testing?
        self.assertTrue(issubclass(Meal, Sandwich), msg="You did not make Meal a subclass of Sandwich")

    def test_meal_drink(self):
        # Figure out what the drink method is
        drink_method = \
            [method for method in self.meal_methods if "drink" in method.lower() or "drk" in method.lower() or "liquid"
             in method.lower()][0]
        # make sure we have it, then make sure it is a property
        self.assertTrue(len(drink_method) > 0, msg="You did not define a drink property")
        self.assertFalse(callable(getattr(self.meal, drink_method)),
                         msg="You defined a drink method without the property decorator")
        # This will throw an exception if it is not a setter
        setattr(self.sandwich, drink_method, "Water")

    def test_meal_side(self):
        # Figure out what the drink method is
        side_method = \
            [method for method in self.meal_methods if "side" in method.lower() or "sd" in method.lower() or "fries" in
             method.lower()][0]
        # make sure we have it, then make sure it is a property
        self.assertTrue(len(side_method) > 0, msg="You did not define a side property")
        self.assertFalse(callable(getattr(self.meal, side_method)),
                         msg="You defined a side method without the property decorator")
        # This will throw an exception if it is not a setter
        setattr(self.sandwich, side_method, "Le Potat")

    def test_meal_price_info(self):
        # Figure out what the price method is
        price_method = [method for method in self.meal_methods if "price" in method.lower() or "prc" in
                        method.lower()][0]
        # make sure we have it, then make sure it is a property
        self.assertTrue(len(price_method) > 0, msg="You did not define a price property for meal")
        self.assertFalse(callable(getattr(self.meal, price_method)),
                         msg="You defined a price method for meal without the property decorator")

        self.assertEqual(getattr(self.meal, price_method), 6.75,
                         msg="Your price without toppings for meal is incorrect")

        # Figure out what the topping methods are
        topping_methods = [method for method in self.meal_methods if "get" not in method.lower() and
                           "top" in method.lower() or "filln" in method.lower()]
        add_topping_method = [method for method in topping_methods if "add" in method.lower() or "remove"
                              not in method.lower()][0]
        remove_topping_method = [method for method in topping_methods if "remove" in method.lower() or
                                 "rmv" in method.lower() or "add" not in method.lower()][0]
        # Make sure we have the methods
        self.assertTrue(len(add_topping_method) > 0, msg="You do not have a method to add toppings for meal")
        self.assertTrue(len(remove_topping_method) > 0, msg="You do not have a method to remove toppings for meal")

        # If they're callable (done correctly), use them
        if callable(getattr(self.meal, add_topping_method)) and \
                callable(getattr(self.meal, remove_topping_method)):
            # Add some toppings
            getattr(self.meal, add_topping_method)("Tomato")
            getattr(self.meal, add_topping_method)("Lettuce")

            # Check the price
            self.assertEqual(getattr(self.meal, price_method), 7.75,
                             msg="Your price for two toppings in meal is incorrect")

            # Remove a topping
            getattr(self.meal, remove_topping_method)("Lettuce")

            # Check the price again
            self.assertEqual(getattr(self.meal, price_method), 7.25,
                             msg="Your price for one topping in meal is incorrect")

        # If they're setters (why, I don't know), use it as a setter
        else:
            print("=" * 20 + "\nAttempting secondary test. This might fail\n" + "=" * 20)
            # Add some toppings
            setattr(self.meal, add_topping_method, "Tomato")
            setattr(self.sandwich, add_topping_method, "Lettuce")

            # Check the price
            self.assertEqual(getattr(self.meal, price_method), 7.75,
                             msg="Your price for two toppings in meal is incorrect")

            # Remove a topping. This will probably fail
            setattr(self.meal, remove_topping_method, "Tomato")

            # Check the price again
            self.assertEqual(getattr(self.meal, price_method), 7.25,
                             msg="Your price for one topping in meal is incorrect")

        # Figure out what the info method is
        info_method = [method for method in self.meal_methods if "info" in method.lower()][0]

        # Make sure we can use it
        self.assertTrue(len(info_method) > 0, msg="You do not have an info method for meal")

        if callable(getattr(self.meal, info_method)):
            # Use it
            print("=" * 20 + "\nMeal:\n")
            getattr(self.meal, info_method)()
            print("=" * 20)
        else:
            # Use it
            print("=" * 20 + "\nMeal (as a property):\n")
            getattr(self.meal, info_method)
            print("=" * 20)

    def test_kids_meal_subclass(self):
        # Short circuit redundant testing?
        self.assertTrue(issubclass(KidsMeal, Meal), msg="You did not make KidsMeal a subclass of Meal")

    def test_kids_meal_toy(self):
        # Figure out what the toy method is
        toy_method = [method for method in self.kids_meal_methods if "toy" in method.lower() or "play" in
                      method.lower()][0]
        # make sure we have it, then make sure it is a property
        self.assertTrue(len(toy_method) > 0, msg="You did not define a toy property")
        self.assertFalse(callable(getattr(self.kids_meal, toy_method)),
                         msg="You defined a toy method without the property decorator")
        # This will throw an exception if it is not a setter
        setattr(self.kids_meal, toy_method, "Stuffed Animal")

    def test_kids_meal_price_info(self):
        # Figure out what the price method is
        price_method = [method for method in self.kids_meal_methods if "price" in method.lower() or "prc" in
                        method.lower()][0]
        # make sure we have it, then make sure it is a property
        self.assertTrue(len(price_method) > 0, msg="You did not define a price property for KidsMeal")
        self.assertFalse(callable(getattr(self.kids_meal, price_method)),
                         msg="You defined a price method for KidsMeal without the property decorator")

        self.assertEqual(getattr(self.kids_meal, price_method), 4.75,
                         msg="Your price without toppings for KidsMeal is incorrect")

        # Figure out what the topping methods are
        topping_methods = [method for method in self.kids_meal_methods if "get" not in method.lower() and
                           "top" in method.lower() or "filln" in method.lower()]
        add_topping_method = [method for method in topping_methods if "add" in method.lower() or "remove" not in
                              method.lower()][0]
        remove_topping_method = [method for method in topping_methods if "remove" in method.lower() or
                                 "rmv" in method.lower() or "add" not in method.lower()][0]
        # Make sure we have the methods
        self.assertTrue(len(add_topping_method) > 0, msg="You do not have a method to add toppings for KidsMeal")
        self.assertTrue(len(remove_topping_method) > 0, msg="You do not have a method to remove toppings for KidsMeal")

        # If they're callable (done correctly), use them
        if callable(getattr(self.kids_meal, add_topping_method)) and \
                callable(getattr(self.kids_meal, remove_topping_method)):
            # Add some toppings
            getattr(self.kids_meal, add_topping_method)("Tomato")
            getattr(self.kids_meal, add_topping_method)("Lettuce")

            # Check the price
            self.assertEqual(getattr(self.kids_meal, price_method), 5.35,
                             msg="Your price for two toppings in KidsMeal is incorrect")

            # Remove a topping
            getattr(self.kids_meal, remove_topping_method)("Lettuce")

            # Check the price again
            self.assertEqual(getattr(self.kids_meal, price_method), 5.05,
                             msg="Your price for one topping in KidsMeal is incorrect")

        # If they're setters (why, I don't know), use it as a setter
        else:
            print("=" * 20 + "\nAttempting secondary test. This might fail\n" + "=" * 20)
            # Add some toppings
            setattr(self.meal, add_topping_method, "Tomato")
            setattr(self.sandwich, add_topping_method, "Lettuce")

            # Check the price
            self.assertEqual(getattr(self.meal, price_method), 5.35)

            # Remove a topping. This will probably fail
            setattr(self.meal, remove_topping_method, "Tomato")

            # Check the price again
            self.assertEqual(getattr(self.kids_meal, price_method), 5.05,
                             msg="Your price for one topping in KidsMeal is incorrect")

        # Figure out what the info method is
        info_method = [method for method in self.meal_methods if "info" in method.lower()][0]

        # Make sure we can use it
        self.assertTrue(len(info_method) > 0, msg="You do not have an info method for KidsMeal")

        if callable(getattr(self.meal, info_method)):
            # Use it
            print("=" * 20 + "\nKidsMeal:\n")
            getattr(self.kids_meal, info_method)()
            print("=" * 20)
        else:
            # Use it
            print("=" * 20 + "\nKidsMeal (as a property):\n")
            getattr(self.kids_meal, info_method)
            print("=" * 20)

    def test_num_prop(self):
        with open("Sandwich.py", "r") as sandwich_file:
            sandwich = sandwich_file.read()

        # Should be 9, but only 8 are specified
        self.assertTrue(8 <= sandwich.count("@property"),
                        msg="You use the property decorator an insufficient number of times for this assignment. You "
                            "should use the property decorator for (at minimum):\n- Sandwich: order number, bread type,"
                            " meat type, and price\n- Meal: drink, side, and price\n- KidsMeal: toy and price")

    def test_num_set(self):
        with open("Sandwich.py", "r") as sandwich_file:
            sandwich = sandwich_file.read()

        # Should be 5, but only 3 are specified
        self.assertTrue(3 <= len(re.findall(r"\s*@\w+\.setter\n", sandwich)),
                        msg="You used the setter decorator an insufficient number of times for this assignment. You "
                            "should use the setter decorator for (at minimum):\n- Sandwich: None\n- Meal: drink, "
                            "side\n- KidsMeal: toy")


if __name__ == '__main__':
    unittest.main()
