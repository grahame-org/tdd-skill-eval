from discount import calculate_discount

def test_no_discount_for_regular_customer():
    assert calculate_discount(100) == 100.0

def test_vip_gets_10_percent_discount():
    assert calculate_discount(100, vip=True) == 90.0

def test_save10_code_gets_10_percent_discount():
    assert calculate_discount(100, code='SAVE10') == 90.0

def test_vip_and_save10_discount_applied_once():
    # vip=True + code='SAVE10' should give only 10% off (not 20%)
    assert calculate_discount(100, vip=True, code='SAVE10') == 90.0
