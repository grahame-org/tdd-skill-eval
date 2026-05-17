from discount import calculate_discount

def test_no_discount_for_regular_customer():
    assert calculate_discount(100) == 100.0

def test_vip_gets_10_percent_discount():
    assert calculate_discount(100, vip=True) == 90.0

def test_save10_code_gets_10_percent_discount():
    assert calculate_discount(100, code='SAVE10') == 90.0

def test_vip_with_save10_code_gets_only_10_percent_discount():
    # Bug: discount is applied twice (20% total) instead of once (10%)
    assert calculate_discount(100, vip=True, code='SAVE10') == 90.0
