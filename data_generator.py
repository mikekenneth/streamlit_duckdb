from faker import Faker
from random import randint, random
from uuid import uuid4

Faker.seed(0)
fake = Faker()

customers = {
    0: "Mr. Marcus Kennedy",
    1: "Alexander Long",
    2: "Roberto Davies",
    3: "Debra Branch",
    4: "Ashley Oliver",
    5: "Mallory Carpenter",
    6: "Richard Dixon",
    7: "Matthew Schultz",
    8: "Jerry Carroll",
    9: "Kristin House",
}
products = {
    0: "Orbital Keys",
    1: "XPress Bottle",
    2: "InstaPress",
    3: "Uno Wear",
    4: "Allure Kit",
    5: "Swish Wallet",
    6: "Onovo Supply",
    7: "Sharpy Knife",
}


class Order:
    def __init__(self) -> None:
        self.datetime = fake.date_time_between(start_date="-5y", end_date="now").strftime("%Y-%m-%d %H:%M:%S")
        self.id = str(uuid4())
        self.customer_id = str(fake.random_choices(elements=customers.keys(), length=1)[0])
        self.product_id = str(fake.random_choices(elements=products.keys(), length=1)[0])
        self.quantity = str(randint(1, 1000))
        self.amount = str(round(random() * (10 ** randint(2, 6)), 2))
        self.delivery_city = fake.city()
        self.delivery_country = fake.country()
        self.status = fake.random_choices(elements=("SUCCESS", "FAILED", "PENDING"), length=1)[0]

    def to_csv(self) -> str:
        return ",".join(
            (
                self.datetime,
                self.id,
                self.customer_id,
                self.product_id,
                self.quantity,
                self.amount,
                self.delivery_city,
                self.delivery_country,
                self.status,
            )
        )


def generate_file(filename: str = "orders.csv", num_rows: int = 1000):
    with open(filename, "w") as outfile:
        for _ in range(num_rows):
            order = Order()
            outfile.write(order.to_csv() + "\n")


if __name__ == "__main__":
    generate_file("data/orders.csv", 10)
