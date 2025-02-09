async def value_float_validator(value):
    try:
        if not isinstance(value, float):
            return False
        return True
    except Exception:
        return False
