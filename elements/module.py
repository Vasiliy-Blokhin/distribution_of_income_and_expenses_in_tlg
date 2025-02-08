async def value_validator(message, state, value):
    try:
        if not isinstance(int(value), int):
            await message.answer(
                'Вы ввели неверные данные. \n'
                'Ознакомтесь с правилами еще раз'
            )
            await state.clear()
            return False
    except Exception:
        await message.answer(
            'Вы ввели неверные данные. \n'
            'Ознакомтесь с правилами еще раз'
        )
        await state.clear()
        return False
    return True
