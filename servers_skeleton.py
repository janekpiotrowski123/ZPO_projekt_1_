from abc import abstractmethod, ABC
from itertools import product
from typing import Optional, List, Dict, Union


class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def __init__(self,nazwa:str,cena:float):
        if(len(nazwa)<2 or not nazwa[0].isalpha() or not nazwa[-1].isdigit() or not nazwa.isalnum()):
            raise ValueError("niewlasciwa nazwa")
        
        
        self.name=nazwa
        self.price=cena

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        if self.name == other.name and self.price== other.price :
            return True
        return False 

    def __hash__(self):
        return hash((self.name, self.price))
    
class TooManyProductsFoundError(Exception):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class Server(ABC):
    n_max_returned_entries = 3

    @abstractmethod
    def get_entries(self, n_letters = 1):
        pass

class ListServer(Server):
    def __init__(self, products: List[Product]):
        self.products = products

    def get_entries(self, n_letters = 1) -> List[Product]:
        result = []
        for product in self.products:
            if product.name[:n_letters].isalpha() and product.name[n_letters:].isdigit() and (len(product.name) == 2 + n_letters or len(product.name) == n_letters + 3):
                result.append(product)
        if len(result) > self.n_max_returned_entries:
            raise TooManyProductsFoundError()

        result.sort(key = lambda x: x.price)
        return result
    pass


class MapServer(Server):

    def __init__(self, products: List[Product]):
        products = {p.name : p for p in products}
        self.products = products

    def get_entries(self, n_letters = 1) -> List[Product]:
        result = []
        for name, product  in self.products.items():
            if name[:n_letters].isalpha() and name[n_letters:].isdigit() and (len(name) == 2 + n_letters or len(name) == n_letters + 3):
                result.append(product)
        if len(result) > self.n_max_returned_entries:
            raise TooManyProductsFoundError()

        result.sort(key = lambda x: x.price)
        return result

    pass




class Client:
     #FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def __init__(self, server: Server) -> None:
        if not hasattr(server, "get_entries"):
            raise ValueError("Dostarczony obiekt serwera nie posiada metody „get_entries”.")
        self.server = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            entries = self.server.get_entries(n_letters) if n_letters is not None else self.server.get_entries()
            if not entries:
                return None
            return sum(entry.price for entry in entries)
        except TooManyProductsFoundError:
            return None
