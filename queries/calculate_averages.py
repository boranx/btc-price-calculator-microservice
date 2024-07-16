# queries/calculate_averages.py
def calculate_averages(prices):
    if not prices:
        return {"avg_eur": None, "avg_czk": None}
    avg_eur = sum(p['price_eur'] for p in prices) / len(prices)
    czk_prices = [p['price_czk'] for p in prices if p['price_czk'] is not None]
    avg_czk = sum(czk_prices) / len(czk_prices) if czk_prices else None
    return {"avg_eur": avg_eur, "avg_czk": avg_czk}
