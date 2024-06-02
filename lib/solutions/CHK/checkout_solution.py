from typing import Dict, List

import unittest

NO_OF_ITEMS = 'numberOfItems'
PRICE = 'price'
FREE =  'free'

LEVEL_1 = 'level 1'
LEVEL_2 = 'level 2'

SPECIAL_OFFER_LEVELS = [LEVEL_1, LEVEL_2]

# Special offers table and offers are proitrised
SPECIAL_OFFERS = {
    LEVEL_1: {
        'E': [{
            NO_OF_ITEMS: 2,
            PRICE: 80,
            FREE: 'B',
        }],
        'F': [{
            NO_OF_ITEMS: 2,
            PRICE: 20,
            FREE: 'F',
        }]
    },
    LEVEL_2: {
        'A': [
            {
                NO_OF_ITEMS: 5,
                PRICE: 200,
            },
            {
                NO_OF_ITEMS: 3,
                PRICE: 130,
            },
        ],
        'B': [{
            NO_OF_ITEMS: 2,
            PRICE: 45,
        }],
    }
}

PRICE_TABLE = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15,
    'E': 40,
    'F': 10,
}


class SpecialOffer:
    def __init__(self, special_offers: Dict[str, Dict], offer_levels: List[str]) -> None:
        self._special_offers = special_offers
        self._offer_levels = offer_levels

    # return all offers for the input sku,
    # None if no offer found
    def get_offer(self, level: str, sku: str) -> List[Dict]:
        if level not in self._special_offers:
            return None
        return self._special_offers[level].get(sku)

    @property
    def offer_levels(self):
        return self._offer_levels

class Basket:
    def __init__(self, skus: str, price_table: Dict[str, int], spcial_offers: SpecialOffer) -> None:
        self._skus = skus
        self._price_table = price_table
        self._spcial_offers = spcial_offers

    # get basket and return None if invalid sku in the skus
    def get_basket(self) -> Dict[str, int]:
        basket =  {}
        for item in self._skus:
            # Validate item in the basket if it is a valid item or not?!
            if item not in PRICE_TABLE:
                return None
            if item in basket:
                basket[item] += 1
            else:
                basket[item] = 1
        return basket

    def apply_offer_to_basket(self, sku: str, offer: Dict, basket: Dict[str, int]):
        total = 0
        while basket[sku] > offer[NO_OF_ITEMS]:
            basket[sku] -= offer[NO_OF_ITEMS]
            total += offer[PRICE]
            if FREE in offer:
                free_sku = offer[FREE]
                if basket.get(free_sku, 0) > 0:
                    basket[free_sku] -= 1
        return total
    
    def checkout(self):
        total = 0

        basket = self.get_basket()
        if basket is None:
            return -1
        
        for level in self._spcial_offers.offer_levels:
            for sku in basket:
                offers = self._spcial_offers.get_offer(level, sku)
                if offers is not None:
                    for offer in offers:
                        total += self.apply_offer_to_basket(sku, offer, basket)

        for sku in basket:
            if basket[sku] > 0:
                total += basket[sku] * self._price_table[sku]

        return total


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    spcial_offers = SpecialOffer(SPECIAL_OFFERS, SPECIAL_OFFER_LEVELS)
    basket = Basket(skus, PRICE_TABLE, spcial_offers)
    return basket.checkout()


class CheckoutTestCase(unittest.TestCase):
    def test_check_invalid(self):
        res = checkout('ABHC')
        self.assertEqual(res, -1)

    def test_has_special_offer(self):
        res = checkout('ABBBACDABA')
        self.assertEqual(res, 130 + 50 + 2 * 45 + 20 + 15)

    def test_sku_a_offers(self):
        res = checkout('AAAAAAAAA')
        self.assertEqual(res, 380)

    def test_sku_e_offer(self):
        res = checkout('EEEEEBBB')
        self.assertEqual(res, 5*40 + 30)

    def test_check_2f_one_f_free(self):
        res = checkout('FFFF')
        self.assertEqual(res, 30)

if __name__=='__main__':
    unittest.main()

