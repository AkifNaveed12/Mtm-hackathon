from decimal import Decimal, ROUND_HALF_UP

def decimal(value) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def money(value) -> float:
    return float(decimal(value))

def total(values) -> float:
    return money(sum((decimal(value) for value in values), Decimal(0)))
