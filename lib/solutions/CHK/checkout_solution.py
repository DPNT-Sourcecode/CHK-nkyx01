import unittest

NO_OF_ITEMS = 'numberOfItems'
PRICE = 'price'
SPECIAL_OFFERS = {
    'A': {
        NO_OF_ITEMS: 3,
        PRICE: 130,
    },
    'B': {
        NO_OF_ITEMS: 2,
        PRICE: 45,
    }
}

PRICE_TABLE = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15
}

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    total = 0
    basket =  {}
    for x in skus:
        if x not in PRICE_TABLE:
            return -1
        
        if x in basket:
            basket[x] += 1
        else:
            basket[x] = 1
    print(basket)
    for x in basket:
        if x in SPECIAL_OFFERS:
            special_offer_no = SPECIAL_OFFERS[x][NO_OF_ITEMS]
            n = basket[x] // special_offer_no
            if n > 0:
                basket[x] -= n * special_offer_no
                total += n * SPECIAL_OFFERS[x][PRICE]

        if basket[x] > 0:
            total += basket[x] * PRICE_TABLE[x]

    return total


class CheckoutTestCase(unittest.TestCase):
    def test_check_invalid(self):
        res = checkout('ABHC')
        self.assertEqual(res, -1)

    def test_has_special_offer(self):
        res = checkout('ABBBACDABA')
        self.assertEqual(res, 130 + 50 + 2 * 45 + 20 + 15)

if __name__=='__main__':
    unittest.main()