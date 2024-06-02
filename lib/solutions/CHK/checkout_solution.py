from typing import Dict, List

import unittest

SKUS = 'SKUs'
NO_OF_ITEMS = 'numberOfItems'
PRICE = 'price'
FREE =  'free'
GROUP_DISCOUNT_OFFER = '#'


LEVEL_1 = 'level 1'
LEVEL_2 = 'level 2'

SPECIAL_OFFER_LEVELS = [LEVEL_1, LEVEL_2]

# Special offers table and offers are proitrised
SPECIAL_OFFERS = {
    LEVEL_1: {
        GROUP_DISCOUNT_OFFER: [{
            SKUS: 'ZYSTX',
            NO_OF_ITEMS: 3,
            PRICE: 45
        }],
        'E': [{
            NO_OF_ITEMS: 2,
            PRICE: 80,
            FREE: 'B',
        }],
        'F': [{
            NO_OF_ITEMS: 2,
            PRICE: 20,
            FREE: 'F',
        }],
        'N': [{
            NO_OF_ITEMS: 3,
            PRICE: 120,
            FREE: 'M',
        }],
        'R': [{
            NO_OF_ITEMS: 3,
            PRICE: 150,
            FREE: 'Q',
        }],
        'U': [{
            NO_OF_ITEMS: 3,
            PRICE: 120,
            FREE: 'U',
        }],
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
        'H': [
            {
                NO_OF_ITEMS: 10,
                PRICE: 80,
            },
            {
                NO_OF_ITEMS: 5,
                PRICE: 45,
            },
        ],
        'K': [
            {
                NO_OF_ITEMS: 2,
                PRICE: 120,
            },
        ],
        'P': [
            {
                NO_OF_ITEMS: 5,
                PRICE: 200,
            },
        ],
        'Q': [
            {
                NO_OF_ITEMS: 3,
                PRICE: 80,
            },
        ],
        'V': [
            {
                NO_OF_ITEMS: 3,
                PRICE: 130,
            },
            {
                NO_OF_ITEMS: 2,
                PRICE: 90,
            },
        ],
    }
}

PRICE_TABLE = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15,
    'E': 40,
    'F': 10,
    'G': 20,
    'H': 10,
    'I': 35,
    'J': 60,
    'K': 70,
    'L': 90,
    'M': 15,
    'N': 40,
    'O': 10,
    'P': 50,
    'Q': 30,
    'R': 50,
    'S': 20,
    'T': 20,
    'U': 40,
    'V': 50,
    'W': 20,
    'X': 17,
    'Y': 20,
    'Z': 21,
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

    def apply_offer_to_basket(self, sku: str, offer: Dict, basket: Dict[str, int]) -> int:
        total = 0
        while basket.get(sku, 0) >= offer[NO_OF_ITEMS]:
            basket[sku] -= offer[NO_OF_ITEMS]
            total += offer[PRICE]
            if FREE in offer:
                free_sku = offer[FREE]
                if basket.get(free_sku, 0) > 0:
                    basket[free_sku] -= 1
        return total
    
    def check_and_apply_offers(self, level: int, sku: str, basket: Dict[str, int]) -> int:
        offers = self._spcial_offers.get_offer(level, sku)
        if offers is not None:
            for offer in offers:
                return self.apply_offer_to_basket(sku, offer, basket)
        return 0
    
    def checkout(self):
        total = 0

        basket = self.get_basket()
        if basket is None:
            return -1
        
        for level in self._spcial_offers.offer_levels:
            # Check and apply group discount offer
            total += self.check_and_apply_offers(level, GROUP_DISCOUNT_OFFER, basket)

            # Check and apply special offers
            for sku in basket:
                total += self.check_and_apply_offers(level, sku, basket)
            
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
        res = checkout('ABHC#')
        self.assertEqual(res, -1)

    def test_has_special_offer(self):
        res = checkout('AAAABBBBCD')
        self.assertEqual(res, 130 + 50 + 2 * 45 + 20 + 15)

    def test_sku_a_offers(self):
        res = checkout('A'*9)
        self.assertEqual(res, 200+130+50)

    def test_sku_e_offer(self):
        res = checkout('EEEEEBBB')
        self.assertEqual(res, 5*40 + 30)

    def test_check_2f_one_f_free(self):
        res = checkout('FFFF')
        self.assertEqual(res, 30)

    def test_check_FFFFFF(self):
        res = checkout('FFFFFF')
        self.assertEqual(res, 40)

    def test_check_FFFFFF(self):
        res = checkout('FFFFFF')
        self.assertEqual(res, 40)

    def test_H(self):
        res = checkout('H'*16)
        self.assertEqual(res, 80+45+10)

    def test_K(self):
        res = checkout('K'*5)
        self.assertEqual(res, 120*2+70)

    def test_N(self):
        res = checkout('N'*7+'M'*1)
        self.assertEqual(res, 40*7)

    def test_P(self):
        res = checkout('P'*16)
        self.assertEqual(res, 200*3+50)

    def test_Q(self):
        res = checkout('Q'*4)
        self.assertEqual(res, 80*1+30)

    def test_R(self):
        res = checkout('R'*7+'QQQ')
        self.assertEqual(res, 50*7+30)

    def test_VVVV(self):
        res = checkout('V'*4)
        self.assertEqual(res, 130+50)

    def test_VVVVV(self):
        res = checkout('V'*5)
        self.assertEqual(res, 130+90)


if __name__=='__main__':
    unittest.main()