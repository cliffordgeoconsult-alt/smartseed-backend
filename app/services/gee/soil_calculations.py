def calculate_base_saturation(calcium, magnesium, potassium, cec):

    if not cec or cec == 0:
        return None

    total_bases = 0

    if calcium:
        total_bases += calcium
    if magnesium:
        total_bases += magnesium
    if potassium:
        total_bases += potassium

    return (total_bases / cec) * 100