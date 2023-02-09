""" Модуль с правилами можно выгружать через команду админа /get,
 редактировать и обновлять в работающем боте через команду /set.
Для правильной работы контроллера правил требуется, чтобы новое правило
принимало в качестве аргументов `text`, `result`, `checklist`
и имело метод `apply`, возвращающий `result` и `checklist`."""

import re


class KeywordRule:
    """Правило, работающее по ключевым словам."""
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


class ForkRule:
    """Условное правило, срабатывает только
    при удовлетворенном правиле 'Вознаграждение'."""
    def __init__(self, name):
        self.name = name

    def apply(self, text: str, checklist: list, result: bool) -> (bool, list):
        for item in checklist:
            if item == ('Вознаграждение', 'OK'):
                # Находим все числа, похожие на суммы.
                amounts = re.findall(r'(\d{1,3}[.,\s]\d{3}|\d{3,})', text)
                if len(amounts) >= 2:  # Ищем суммы, похожие на вилку.
                    if text.index(amounts[1]) - text.index(amounts[0]) <= 30:
                        if not self._check_fork(amounts):
                            checklist.append((self.name, 'X'))
                            result = False
        return result, checklist

    def _clean(self, amount) -> int:
        """Очистка суммы от разделителей."""
        for separator in (" ", ",", "."):
            amount = amount.replace(separator, "")
        return int(amount)

    def _check_fork(self, amounts) -> bool:
        """Проверка предполагаемой вилки на установленный разброс."""
        difference = 5*10**(len(str(self._clean(amounts[0])))-2) # 500 или 50 000.
        return self._clean(amounts[1])-self._clean(amounts[0]) <= difference


"""KeywordRules"""
format = KeywordRule(name='Формат работы',
                  keywords={'формат', 'удален', 'офис', 'гибрид'})
schedule = KeywordRule(name='Занятость',
                    keywords={'полн', 'частичн', 'проект', 'занятост', 'график'})
name = KeywordRule(name='Название',
                keywords={'компан', 'назван', 'работодат'})
income = KeywordRule(name='Вознаграждение',
                  keywords={'зп', 'оклад', 'вилка', 'заработн', 'вознагражд',
                            'зарплат', 'зп', 'з//п', 'з\\п', 'оплат'})
employment = KeywordRule(name='Варианты трудоустройства',
                      keywords={'трудоустройств', 'официальн', 'самозанятост', 'ИП', 'ООО'})


"""ConditionalRules"""
fork = ForkRule('Вилка')


"""Переменные, которые используются контроллером правил (rule_manager.py)"""
# Список правил для применения. Условные идут после своих основных правил.
to_be_used = [format, income, schedule, name, employment, fork]
# Тэг, на который срабатывает проверка.
vacancy = {'#вакансия','# вакансия','#vacancy','# vacancy'}
