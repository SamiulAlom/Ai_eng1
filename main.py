from calculator import add, multiply
from message import welcome


def main():
    print(welcome("Samiul"))

    result1 = add(10, 5)
    result2 = multiply(10, 5)

    print("Addition:", result1)
    print("Multiplication:", result2)


if __name__ == "__main__":
    main()