import yaml

from game import Game
from consumer import Consumer
from platform import Platform

with open("./config.yaml", "r", encoding="utf-8") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)


def main():
    n_customers = cfg["n_customers"]
    n_platforms = cfg["n_platforms"]
    max_time = cfg["max_time"]

    game = Game(n_customers, n_platforms)

    total_consumer_surplus = 0
    total_platform_benefit = 0
    for t in range(max_time):
        print(f"Time step {t + 1}:")
        game.simulate_market()
        consumer_surplus = game.get_consumer_surplus()
        platform_benefit = game.get_platform_benefit()
        total_consumer_surplus += consumer_surplus
        total_platform_benefit += platform_benefit

    print(f"Total consumer surplus: ${total_consumer_surplus:.2f}")
    print(f"Total platform benefit: ${total_platform_benefit:.2f}")

if __name__ == "__main__":
    main()
