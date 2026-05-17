def calculate_discount(price, vip=False, code=None):
    """Calculate discounted price."""
    discount = 0.0
    
    if vip:
        discount += 0.10
    elif code == 'SAVE10':
        discount += 0.10
    
    return price * (1 - discount)
