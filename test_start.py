import asyncio
from decimal import Decimal
import unittest

from start import recommend_price


class RecommendPriceTests(unittest.TestCase):
    def test_recommends_discounted_competitor_price(self):
        async def fetch_offers():
            return {
                "status": "success",
                "offers": [
                    {"seller": "MYSHOP", "price": Decimal("4300.00"), "delivery_days": 1},
                    {"seller": "PARTS", "price": Decimal("4800.00"), "delivery_days": 3},
                ],
            }

        result = asyncio.run(
            recommend_price(fetch_offers, Decimal("4900.00"), Decimal("4500.00"))
        )

        self.assertEqual(
            result,
            {
                "price": Decimal("4728.00"),
                "decision": "APPLY",
                "reason": "Найдена минимальная цена конкурента",
            },
        )

    def test_timeout_holds_current_price(self):
        async def fetch_offers():
            await asyncio.sleep(0.05)
            return {"status": "success", "offers": []}

        result = asyncio.run(
            recommend_price(
                fetch_offers,
                Decimal("4900.00"),
                Decimal("4500.00"),
                timeout_s=0.001,
            )
        )

        self.assertEqual(result["price"], Decimal("4900.00"))
        self.assertEqual(result["decision"], "HOLD")


if __name__ == "__main__":
    unittest.main()
