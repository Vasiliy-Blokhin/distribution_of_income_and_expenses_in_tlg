async def value_validator(message, state, value, type):
    try:
        if not isinstance(type(value), type):
            await message.answer(
                'Вы ввели неверные данные. \n'
                'Ознакомтесь с правилами еще раз'
            )
            await state.clear()
            return False
        return value
    except Exception:
        await message.answer(
            'Вы ввели неверные данные. \n'
            'Ознакомтесь с правилами еще раз'
        )
        await state.clear()
        return False
