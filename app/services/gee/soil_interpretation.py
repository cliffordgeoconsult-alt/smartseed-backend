def classify_ph(value):
    if value < 5.5:
        return "Strongly acidic"
    elif value < 6.0:
        return "Moderately acidic"
    elif value <= 7.5:
        return "Optimal"
    else:
        return "Alkaline"


def classify_texture(clay, sand, silt):
    if clay > 40:
        return "Clay soil"
    elif sand > 70:
        return "Sandy soil"
    elif 20 < clay < 40 and 30 < sand < 60:
        return "Loam soil"
    else:
        return "Mixed texture"