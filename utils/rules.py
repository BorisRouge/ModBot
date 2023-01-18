from utils import data


class RuleManager:
    #  def refresh_rules
    def __init__(self):
        self.rules = data.rules

    def check(self, text) -> (bool, list):

        print(data.rules, data.format.markers)

        result = True
        checklist = []
        for rule in self.rules:
            for marker in rule.markers:
                if marker in text:
                    checklist.append((rule.name, True))
                    break
                else:
                    checklist.append((rule.name, False))
                    result = False
                    break
        return result, checklist

    def is_vacancy(self, text):
        if '#Вакансия' in text:  #TODO: накидать вариаций
            return True





