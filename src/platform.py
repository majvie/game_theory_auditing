from typing import List
import yaml 
import random


with open("./config.yaml", "r", encoding="utf-8") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)


class Platform:
    def __init__(self, name, n_products: int):
        self.name = name
        self.products = self.generate_products(n_products)
        maximum_trust_state = cfg["maximum_trust_state"]
        self.trust_state = random.randrange(0, maximum_trust_state)

        self.benefit_mapping = {
            "affiliated": cfg["benefit_affiliated"],
            "non_affiliated": cfg["benefit_non_affiliated"],
        }  # product affiliation: benefit

    def offer_products(self): 
        return self.products

    def generate_products(self, num_products: int):
        products = []

        for _ in range(num_products): 
            price_affiliated = cfg["price_affiliated"]
            price_non_affiliated = cfg["price_non_affiliated"]
            products.append(Product(price_affiliated, self, "affiliated"))
            products.append(Product(price_non_affiliated, self, "non_affiliated"))

        return products

    

class Product: 
    def __init__(self, price: float, platform: Platform, affiliation: str):
        self.price = price
        self.platform = platform
        self.affiliation = affiliation

    def get_price(self):
        return self.price

    def get_affiliation(self):
        return self.affiliation

    def get_platform(self):
        return self.platform