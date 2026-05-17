def calculate_discount(price, vip=False, code=None):
    """Calculate discounted price."""
    if vip or code == 'SAVE10':
        discount = 0.10
    else:
        discount = 0.0

    return price * (1 - discount)
