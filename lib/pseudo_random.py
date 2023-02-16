from dataclasses import dataclass
import random
from typing import List
from typing_extensions import TypedDict



@dataclass
class Product:
    name: str
    quantity: int
    rarity: bool = None

    def __post_init__(self):
        if self.rarity is None:
            if self.quantity == 1:
                self.rarity = True
            else:
                self.rarity = False
        else:
            pass


@dataclass
class Settings:
    calls_limit: int
    rare_per_limit: int


class Response(TypedDict):
    position: str


class Stock:

    def __init__(self):
        self.__products: list = []
        self.__calls = 1
        self.__calls_limit = 15
        self.__rare_count = 0
        self.__rare_per_limit = 3

    @property
    def products(self):
        return self.__products

    @products.setter
    def products(self, value: List[Product]):
        self.__products.extend(value)


    @property
    def calls_limit(self):
        return self.__calls_limit

    @calls_limit.setter
    def calls_limit(self, value: int):
        if value >= 1:
            self.__calls_limit = value
        else:
            raise Exception

    @property
    def rare_per_limit(self):
        return self.__rare_per_limit

    @rare_per_limit.setter
    def rare_per_limit(self, value):
        if value >= 1:
            self.__rare_per_limit = value
        else:
            raise Exception

    def get_product(self):
        if len(self.__products) > 0:

            while True:
                product = random.choice(self.products)
                if product.quantity != 0:
                    if product.quantity == -1:
                        self.__calls += 1
                        return product
                    else:
                        if product.rarity:
                            if self.__rare_count < (self.__rare_per_limit * (self.__calls / self.__calls_limit)):
                                print(self.__rare_count)
                                product.quantity -= 1
                                self.__calls += 1
                                self.__rare_count += 1
                                return product
                            else:
                                continue
                        else:
                            product.quantity -= 1
                            self.__calls += 1
                            return product
                else:
                    self.products.remove(product)
                    continue
        else:
            raise Exception




