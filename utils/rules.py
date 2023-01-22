from utils import data

class RuleManager:
    # TODO:  def refresh_rules
    def __init__(self):
        self.rules = data.rules

    def check(self, text) -> (bool, list):
        result = True
        checklist = []
        for rule in self.rules:
            no_markers = True
            for marker in rule.markers:
                if marker in text.lower():
                    checklist.append((rule.name, 'OK'))
                    no_markers = False
                    break
            if no_markers:
                checklist.append((rule.name, 'X'))
                result = False
        return result, checklist

    def is_vacancy(self, text):
        for word in data.vacancy:
            if word in text.lower():
                return True
