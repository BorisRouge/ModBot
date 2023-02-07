import re

class KeywordRule:
    """"""
    def __init__(self, name, keywords):
        self.name = name
        self.keywords = keywords

    def apply(self, text: str, checklist: list, result: bool) -> (bool, list):
        not_found = True
        for kw in self.keywords:
            if kw in text.lower():
                checklist.append((self.name, 'OK'))
                not_found = False
                break
        if not_found:
            checklist.append((self.name, 'X'))
            result = False
        return result, checklist


# class ConditionalRule:
#     def __init__(self, name: str, keywords: list, condition: (str, str)):
#         self.name = name
#         self.keywords = keywords
#         self.condition = condition
#
#     def apply(self, text: str, checklist: list, result: bool) -> (bool, list):
#         for item in checklist:
#             if item[1] == self.condition:
#                 for kw in self.keywords:
#                     if kw in text.lower():
#
# class AddressRule():
#     def __init__(self, name):
#         self.name = name
#
#     def apply(self, text: str, checklist: list, result: bool) -> (bool, list):
#         for item in checklist:
#             if item[1] == ('Формат работы', 'OK'):
#                 pass
#
#
class ForkRule:
    """Условное правило, срабатывает только
    при удовлетворенном правиле 'Вознаграждение'."""
    def __init__(self, name):
        self.name = name

    def apply(self, text: str, checklist: list, result: bool) -> (bool, list):
        for item in checklist:
            if item == ('Вознаграждение', 'OK'):
                amounts = re.findall(r'(\d{1,} \d{3}|\d{3,})', text)  # list of all numbers that are >= 3 characters
                if len(amounts) >= 2:  # are they close?
                    if text.index(amounts[1]) - text.index(amounts[0]) <= 30:
                        if not self.check_fork(amounts):
                            checklist.append((self.name, 'X'))
                            result = False
                elif len(amounts) == 1:
                    pass
                else:
                    pass

        return result, checklist

    def check_fork(self, amounts):
        def prepare(amount):
            for separator in (" ", ",", "."):
                amount = amount.replace(separator, "")
            return int(amount)

        difference = 5*10**(len(str(prepare(amounts[0])))-2)  # to calculate the length of the difference
        print(difference)
        if prepare(amounts[1])-prepare(amounts[0]) > difference:
            print('splash', int(amounts[1])-int(amounts[0]))

#
# class TaxRule():
#     def __init__(self, name):
#         self.name = name
#
#     def apply(self, text: str, checklist: list, result: bool) -> (bool, list):
#         for item in checklist:
#             if item[1] == ('Вознаграждение', 'OK'):
#                 pass

"""KeywordRules"""
format = KeywordRule(name='Формат работы',
                  keywords={'формат', 'удален', 'офис', 'гибрид'})  # TODO: если офис то где?
schedule = KeywordRule(name='Занятость',
                    keywords={'полн', 'частичн', 'проект', 'занятост', 'график'})
name = KeywordRule(name='Название',                                    # TODO: что если тут просто название компании
                keywords={'компан', 'назван', 'работодат'})  # TODO: под удаление
income = KeywordRule(name='Вознаграждение',
                  keywords={'зп', 'оклад', 'вилка', 'вознагражд', 'зарплат', 'зп', 'з//п', 'з\\п',})
employment = KeywordRule(name='Варианты трудоустройства',
                      keywords={'трудоустройств', 'официальн', 'самозанятост', 'ИП', 'ООО'})


"""ConditionalRules"""
fork = ForkRule('Вилка')


"""output"""
to_be_used = [format, income, schedule, name, employment, fork]  # TODO: make the class autoappend here
vacancy = {'#вакансия','# вакансия'}

# TODO: - с корректным указанием валюты
# TODO: - размерности (писать 300к, а не просто 300)
# TODO: - с указанием до/после уплаты налогов
# TODO: - если почасовый рейт, то указывать по таким же критериям (если вы ищете несколько позиций, обязательно разделяйте их на несколько вакансий)
# TODO: - разброс вилки не должен быть более ±50к руб./$500/€500
