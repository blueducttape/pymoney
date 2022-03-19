from typing import Union
from parser import data, day, month, year


class Money:
    """
    класс, описывающий деньги на счете
    Валюта, в которой деньги хранятся на счете должны быть из списка, представленного в файле price
    Если при инициализации не указать валюту, то автоматически создается экземпляр класса в рублях.
    Денежные средства, находящиеся на счете, могут быть конвертированы в другие валюты по текущему курсу ЦБ
    (или по последнему курсу, когда был доступ в интернет).
    :param value - денежная сумма
    :param: str charcode - трёхбуквенный код валюты
    Методы класса:
    convert_to_usd(): Конвертирует денежные средства, находящиеся на счете в доллары США
    convert_to_valute(): Конвертирует денежные средства, находящиеся на счете в любую валюту из списка
    """
    def __init__(self, value: float, charcode: str):
        """
        Инициализация экземплаяра класса Money
        :param value: Количество денег
        :param charcode: Наименование валюты в виде трех заглавных букв латинского алфавита.
        Используются международные общепринятые наименования (смотри файл price)
        """
        self.value = value
        self.charcode = charcode

    def __str__(self):
        return f"{self.value} {self.charcode}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value}, {self.charcode})"

    def __add__(self, add_money):
        """
        "магический" метод для сложения сумм денег
        :param add_money:
        :return: сумму денег, при условии что они в одной и той же валюте
        """
        if isinstance(add_money, Money):
            if self.charcode == add_money.charcode:
                return Money(round(self.value + add_money.value, 2), self.charcode)
            else:
                raise TypeError("Разные валюты")
        else:
            return NotImplemented

    def __sub__(self, sub_money):
        """
                "магический" метод для вычитания сумм денег
                :param sub_money:
                :return: разность денег, при условии что они в одной и той же валюте
                """
        if isinstance(sub_money, Money):
            if self.charcode == sub_money.charcode:
                return Money(round(self.value - sub_money.value, 2), self.charcode)
            else:
                raise TypeError("Разные валюты")
        else:
            return NotImplemented

    def __mul__(self, num):
        """
        "магический" метод для умножения сумм денег
         :param int, float num:
          :return: произведение
                """
        if isinstance(num, (int, float)):
            return Money(round(self.value * num, 2), self.charcode)
        else:
            return NotImplemented

    def __truediv__(self, num):
        """
        "магический" метод для деления сумм денег
         :param int, float num:
        :return: частное
        """
        if isinstance(num, (int, float)):
            return Money(round(self.value / num, 2), self.charcode)
        else:
            return NotImplemented

    def __gt__(self, other) -> bool:
        """
        "магический" метод для сравнения сумм денег
        :param other:
        :return: возвращает True, если 1 сумма > 2ой
        """
        if isinstance(other, Money):
            return self.value > other.value
        else:
            return NotImplemented

    def __lt__(self, other) -> bool:
        """
        "магический" метод для сравнения сумм денег
        :param other:
        :return: возвращает True, если 1 сумма < 2ой
         """
        if isinstance(other, Money):
            return self.value < other.value
        else:
            return NotImplemented

    def __ge__(self, other) -> bool:
        """
        "магический" метод для сравнения сумм денег
        :param other:
        :return: возвращает True, если 1 сумма >= 2ой
        """
        if isinstance(other, Money):
            return self.value >= other.value
        else:
            return NotImplemented

    def __le__(self, other) -> bool:
        """
        "магический" метод для сравнения сумм денег
        :param other:
        :return: возвращает True, если 1 сумма <= 2ой
        """
        if isinstance(other, Money):
            return self.value <= other.value
        else:
            return NotImplemented

    def __eq__(self, other) -> bool:
        """
        "магический" метод для сравнения сумм денег
        :param other:
        :return: возвращает True, если 1 сумма == 2ой
        """
        if isinstance(other, Money):
            return self.value == other.value
        else:
            return NotImplemented

    def __ne__(self, other) -> bool:
        """
        "магический" метод для сравнения сумм денег
        :param other:
        :return: возвращает True, если 1 сумма != 2ой
        """
        if isinstance(other, Money):
            return self.value != other.value
        else:
            return NotImplemented

    def convert_to_usd(self) -> float:
        """
        метод для конвертации валюты в доллары
        :return: возвращает денежную сумму, конвертированную в доллары
        """
        if self.charcode == "USD":
            return self.value

        elif self.charcode in data["Valute"]:
            value1 = data["Valute"][self.charcode]["Value"] / data["Valute"][self.charcode]["Nominal"]
            value2 = data["Valute"]["USD"]["Value"]
            self.value = round(self.value * value1 / value2, 2)
            self.charcode = "USD"
            print(f"Конвертация в USD прошла по курсу на {day}.{month}.{year}\n{self.value} {self.charcode}")
            return self.value

        elif self.charcode == "RUB":
            self.value = round(self.value / data["Valute"]["USD"]["Value"], 2)
            self.charcode = "USD"
            return self.value

        else:
            raise TypeError("Валюты, которую вы хотите поменять, не принимают в обменнике")

    def convert_to_valute(self, valute: str) -> Union[float|None]:
        """
        метод для конвертации валюты в в любую другую валюту
        :return: возвращает конвертированную денежную сумму
        """
        if valute == self.charcode:
            print(f"Деньги находятся уже в той валюте, в которую вы хотите их конвертировать")
            return None

        elif valute in data["Valute"]:
            value1 = data["Valute"][self.charcode]["Value"] / data["Valute"][self.charcode]["Nominal"]
            value2 = data["Valute"][valute]["Value"] / data["Valute"][valute]["Nominal"]
            self.value = round(self.value * value1 / value2, 2)
            self.charcode = valute
            print(f"Конвертация в {valute} прошла по курсу на {day}.{month}.{year}\n{self.value} {self.charcode}")
            return self.value

        elif valute == "RUB":
            value1 = data["Valute"][self.charcode]["Value"]
            value2 = data["Valute"][self.charcode]["Nominal"]
            self.value = round(self.value * value1 / value2, 2)
            self.charcode = valute
            print(f"Конвертация в {valute} прошла по курсу на {day}.{month}.{year}\n{self.value} {self.charcode}")
            return self.value

        else:
            raise TypeError("Нет такой валюты")


class Yen(Money):
    """
    дочерний класс класса Money, описывающий японскую йену
    """
    def __init__(self, value: float):
        self.value = value
        self.charcode = 'JPY'

    def get_yen(self) -> None:
        exchange_rate = data["Valute"]["JPY"]["Value"]
        return print(f'текущий курс йены = {round(exchange_rate, 2)}')

    def convert_to_rub(self) -> Money:
        """
        Метод, который конвертирует валюту в рубли создает экземпляр класса Money в рублях
        :return: возвращает экземпляр класса Money в рублях
        """
        value1 = data["Valute"][self.charcode]["Value"] / data["Valute"][self.charcode]["Nominal"]
        self.value = round(self.value * value1, 2)
        self.charcode = "RUB"
        print(f"Конвертация в RUB прошла по курсу на {day}.{month}.{year}\n{self.value} {self.charcode}")
        return Money(self.value, "RUB")


if __name__ == '__main__':

    money1 = Money(500, "CZK")
    money2 = Money(145.52, "USD")
    money3 = Money(650.96, "EUR")

    print(money1, money2, money3)
    money1.convert_to_valute("EUR")
    money2.convert_to_valute("USD")
    money3.convert_to_usd()
    print(money2+ money3)
    print(money1*3)
    print(money1 == money2)
    money4 = Yen(400)
    Yen.get_yen(money4)
    Yen.convert_to_rub(money4)
