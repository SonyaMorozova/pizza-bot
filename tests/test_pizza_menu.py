import json
import unittest
from itertools import product

from bot import pizza_menu


class TestPizzaMenu(unittest.TestCase):

    def test_recipes_keyboard(self):
        keyboard = json.loads(pizza_menu.recipes_keyboard())
        buttons = keyboard["inline_keyboard"]

        callback_data = [
            button["callback_data"]
            for row in buttons
            for button in row
        ]

        self.assertCountEqual(callback_data, [
            "margherita",
            "pepperoni",
            "four_cheese",
            "hawaiian",
            "napoletano",
        ])

    def test_sizes_keyboard(self):
        keyboard = json.loads(pizza_menu.sizes_keyboard())
        buttons = keyboard["inline_keyboard"]

        callback_data = [
            button["callback_data"]
            for row in buttons
            for button in row
        ]

        self.assertCountEqual(callback_data, [
            "small",
            "medium",
            "large",
        ])

    def test_drinks_keyboard(self):
        keyboard = json.loads(pizza_menu.drinks_keyboard())
        buttons = keyboard["inline_keyboard"]

        callback_data = [
            button["callback_data"]
            for row in buttons
            for button in row
        ]

        self.assertCountEqual(callback_data, [
            "juice",
            "morse",
            "tea",
            "cola",
            "none",
        ])

    def test_order_summary(self):
        order = {
            "recipe": "pepperoni",
            "size": "large",
            "drink": "none",
        }

        summary = pizza_menu.format_order_summary(order)

        self.assertIn("Пепперони", summary)
        self.assertIn("Большая", summary)
        self.assertIn("Без напитка", summary)

    def test_all_order_combinations(self):
        combinations = list(product(
            pizza_menu.RECIPES,
            pizza_menu.SIZES,
            pizza_menu.DRINKS,
        ))

        self.assertEqual(len(combinations), 75)

        for recipe, size, drink in combinations:
            with self.subTest(recipe=recipe, size=size, drink=drink):
                order = {
                    "recipe": recipe[0],
                    "size": size[0],
                    "drink": drink[0],
                }

                summary = pizza_menu.format_order_summary(order)

                self.assertIn(recipe[1], summary)
                self.assertIn(size[1], summary)
                self.assertIn(drink[1], summary)


if __name__ == "__main__":
    unittest.main()