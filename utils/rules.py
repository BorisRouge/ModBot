from utils import data

class RuleManager:
    # TODO:  def refresh_rules
    def __init__(self):
        self.rules = data.rules

    def check(self, text) -> (bool, list):
        result = True
        checklist = []
        for rule in self.rules:
            result, checklist = rule.apply(text, checklist, result)
        return result, checklist

    def is_vacancy(self, text):
        for word in data.vacancy:
            if word in text.lower():
                return True
