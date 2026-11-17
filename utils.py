"""Общие функции ввода и отображения."""


def read_float(prompt: str) -> float:
    """Считывает положительное число с плавающей точкой."""
    value = float(input(prompt))
    if value <= 0:
        raise ValueError("Значение должно быть больше нуля.")
    return value


def read_int(prompt: str) -> int:
    """Считывает положительное целое число."""
    value = int(input(prompt))
    if value <= 0:
        raise ValueError("Количество должно быть больше нуля.")
    return value
