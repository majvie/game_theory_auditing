
import yaml
import numpy as np

from consumer import Consumer
from platform import Platform

with open("./config.yaml", "r", encoding="utf-8") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

class Game:
    def __init__(self, n_customers, n_platforms):
        # Create Customers
        self.customers = [Consumer() for _ in range(n_customers)]
        self.platforms = [Platform("Amazon", n_platforms) for _ in range(n_platforms)]
        self.lambda_trust = cfg["lambda_trust"]

    def get_trust_percentage(self, platform: Platform):
        trust_state = platform.trust_state
        trust_percentage = 1 - np.exp(-self.lambda_trust * trust_state)
        return trust_percentage


    def simulate_market(self):
        # Simulate the market
        for platform in self.platforms:
            # Make customers distrust platforms based on the trust percentage
            trust_percentage = self.get_trust_percentage(platform)
            n_distrusted_customers = int(trust_percentage * len(self.customers))
            random_distrusted_customers = np.random.choice(self.customers, size=n_distrusted_customers, replace=False)

            # reset distrust for all
            for customer in self.customers:
                customer.reset_distrust_mapping()
            # apply distrust to selected customers
            for customer in random_distrusted_customers:
                customer.distrust_mapping[platform] = True

            for customer in self.customers:
                chosen_product = customer.choose_product(self.platforms)
                if chosen_product:
                    print(f"Customer chose product with price {chosen_product.get_price()} and affiliation {chosen_product.get_affiliation()}")
                else: 
                    print("Customer did not choose any product due to distrust or no available products.")
            return 

    def get_consumer_surplus(self):
        consumer_surplus = 0
        for customer in self.customers:
            if not customer.bought_products:
                continue  # Skip customers who didn't buy any products
            chosen_product = customer.bought_products[-1]  # Get the last bought product
            if chosen_product:
                individual_surplus = customer.wtp[chosen_product.get_affiliation()] - chosen_product.get_price()
                consumer_surplus += individual_surplus
        return consumer_surplus

    def get_platform_benefit(self):
        platform_benefit = 0
        for customer in self.customers:
            if not customer.bought_products:
                continue  # Skip customers who didn't buy any products
            chosen_product = customer.bought_products[-1]  # Get the last bought product
            if chosen_product:
                benefit_per_product = chosen_product.get_platform().benefit_mapping[chosen_product.get_affiliation()]
                platform_benefit += benefit_per_product
        return platform_benefit