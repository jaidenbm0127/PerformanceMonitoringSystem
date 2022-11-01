import psutil


def calculate_percentage_difference(val1, val2):
    return round(((val1 - val2) / val2 * 100), 1)
