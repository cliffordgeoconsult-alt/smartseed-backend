def calculate_base_saturation(calcium, magnesium, potassium, sodium, cec):

    if not cec or cec == 0:
        return None

    return {
        "calcium_bs": (calcium / cec) * 100 if calcium else 0,
        "magnesium_bs": (magnesium / cec) * 100 if magnesium else 0,
        "potassium_bs": (potassium / cec) * 100 if potassium else 0,
        "sodium_bs": (sodium / cec) * 100 if sodium else 0,
    }