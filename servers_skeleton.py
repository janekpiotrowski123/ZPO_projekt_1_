from typing import Optional


class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def __init__(self,nazwa:str,cena:float):
        if(len(nazwa)<2 or not nazwa[0].isalpha() or not nazwa[-1].isdigit() or not nazwa.isalnum()):
            raise ValueError("niewlasciwa nazwa")
        
        
        self.name=nazwa
        self.price=cena

    def __eq__(self, other):
        if self.name == other.name and self.price== other.price :
            return True
        return False 

    def __hash__(self):
        return hash((self.name, self.price))
    
class TooManyProductsFoundError:
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class ListServer:
    pass


class MapServer:
    pass




class Client:
     #FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def __init__(self, server) -> None:
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
