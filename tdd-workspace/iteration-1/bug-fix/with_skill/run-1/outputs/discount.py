def apply_discount(price: float, vip: bool = False, code: str = "") -> float:
    """Apply discount to a price. VIP gets 10% off. Code 'SAVE10' gets 10% off.
    If both are supplied, the discount is only applied once."""
    if vip or code == "SAVE10":
        price = price * 0.9
    return round(price, 2)
