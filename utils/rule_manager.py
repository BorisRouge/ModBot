from utils import rules


class RuleManager:
    def __init__(self):
        self.chat_rules = rules.to_be_used

    def check(self, text) -> (bool, list):
        """Принимает строку на проверку, проверяет по модулю rules,
        возвращает кортеж с результатом проверки и контрольным листом."""
        result = True
        checklist = []
        for rule in self.chat_rules:
            result, checklist = rule.apply(text, checklist, result)
        return result, checklist

    def is_vacancy(self, text)-> bool:
        """Проверяет, является ли сообщение вакансией."""
        for word in rules.vacancy:
            if word in text.lower():
                return True

    def refresh_rules(self):
        """Используется в случае обновления модуля с правилами."""
        self.chat_rules = rules.to_be_used
