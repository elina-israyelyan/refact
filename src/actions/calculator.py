from .base import ActionSet


class MathActions(ActionSet):
    @staticmethod
    def sum(a: float, b: float) -> float:
        return float(a + b)

    @staticmethod
    def subtract(a: float, b: float) -> float:
        return float(a - b)

    @staticmethod
    def multiply(a: float, b: float) -> float:
        return float(a * b)

    @staticmethod
    def divide(a: float, b: float) -> float:
        return float(a / b)

    @staticmethod
    def power(a: float, b: float) -> float:
        return float(a ** b)

if __name__ == "__main__":
    print(MathActions().list_action_methods())