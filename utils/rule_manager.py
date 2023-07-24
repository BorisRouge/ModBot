from utils import rules


LEN_CUTOFF = 400  # Отсечка по кол-ву знаков для доп. оценки на вакансистость.
SUS_COEFF = 0.7   # Насыщенность соблюденными правилами в подозрительном сообщении.

class RuleManager:

    def __init__(self):
        self.chat_rules = rules.to_be_used

    def check(self, text, message) -> (bool, list):
        """Принимает строку на проверку, проверяет по модулю rules,
        возвращает кортеж с результатом проверки и контрольным листом."""
        result = True
        checklist = []
        for rule in self.chat_rules:
            result, checklist = rule.apply(text, checklist, result, message=message)
        return result, checklist

    def is_vacancy(self, text) -> bool:
        """Проверяет, является ли сообщение вакансией."""
        for word in rules.vacancy:
            if word in text.lower():
                return True
                
    def is_cv(self, text) -> bool:
        """Проверяет, является ли сообщение резюме."""
        for word in rules.cv:
            if word in text.lower():
                return True

    def is_suspicious(self, checklist, text):
        """Проверяет, не похоже ли сообщение на вакансию."""
        if len(text) > LEN_CUTOFF:
            positives = 0
            for item in checklist:
                if item[1]:
                    positives += 1
            #if positives / len(checklist) > SUS_COEFF:
            if positives > 1:
                return True

    def refresh_rules(self):
        """Используется в случае обновления модуля с правилами."""
        self.chat_rules = rules.to_be_used
