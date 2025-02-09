async def value_validator(value, type):
    try:
        if not isinstance(value, type):
            return False
        return True
    except Exception:
        return False
