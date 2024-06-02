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
}


# prepare basket and return None if invalid sku in the skus
def get_basket(skus):
    basket =  {}
    for item in skus:
        # Validate item in the basket if it is a valid item or not?!
        if item not in PRICE_TABLE:
            return None
        
        if item in basket:
            basket[item] += 1
        else:
            basket[item] = 1
    return basket


# return all offers for the input sku,
# None if no offer found
def get_offer(level, sku):
    if level not in SPECIAL_OFFERS:
        return None
    return SPECIAL_OFFERS[level].get(sku)


def apply_offer_to_basket(sku, offer, basket):
    total = 0
    n = basket[sku] // offer[NO_OF_ITEMS]
    if n > 0:
        basket[sku] -= n * offer[NO_OF_ITEMS]
        total += n * offer[PRICE]
        if FREE in offer:
            free_sku = offer[FREE]
            if basket.get(free_sku, 0) > 0:
                basket[free_sku] -= n
    return total

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    total = 0

    basket = get_basket(skus)
    if basket is None:
        return -1
    
    for level in SPECIAL_OFFER_LEVELS:
        for sku in basket:
            offers = get_offer(level, sku)
            if offers is not None:
                for offer in offers:
                    total += apply_offer_to_basket(sku, offer, basket)

    for sku in basket:
        if basket[sku] > 0:
            total += basket[sku] * PRICE_TABLE[sku]

    return total


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
        self.assertEqual(res, 120 + 30)

if __name__=='__main__':
    unittest.main()

