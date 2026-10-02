from typing import List
import numpy as np
import yaml

from platform import Platform, Product

with open("./config.yaml", "r", encoding="utf-8") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

class Consumer: 
    def __init__(self):
        wtp_affiliated = cfg["wtp_affiliated"]
        wtp_non_affiliated = cfg["wtp_non_affiliated"]
        wtp_affiliated_var = cfg["wtp_affiliated_var"]
        wtp_non_affiliated_var = cfg["wtp_non_affiliated_var"]
        self.wtp = {
            "affiliated": np.random.normal(wtp_affiliated, wtp_affiliated_var, 1)[0],
            "non_affiliated": np.random.normal(wtp_non_affiliated, wtp_non_affiliated_var, 1)[0]
        }
        self.distrust_mapping = {} # platform_name: boolean
        self.bought_products = []

    def choose_product(self, platforms: List[Platform]):
        products_on_platforms = []
        for platform in platforms: 
            products = platform.offer_products()
            products_on_platforms.append(products)

        # Calculate the individual surplus for each product (wtp - price)
        individual_surpluses = {} # product: wtp-price
        for products_on_platform in products_on_platforms: 
            for product in products_on_platform:
                if product.get_platform() in self.distrust_mapping:
                    continue  # Skip products from distrusted platforms
                individual_surplus = self.wtp[product.get_affiliation()] - product.get_price()
                individual_surpluses[product] = individual_surplus

        # Choose the product with the highest individual surplus (wtp - price)
        if individual_surpluses:
            chosen_product = max(individual_surpluses, key=individual_surpluses.get)
            self.bought_products.append(chosen_product)
            return chosen_product
        return None

    def reset_bought_products(self):
        self.bought_products = []

    def reset_distrust_mapping(self):
        self.distrust_mapping = {}