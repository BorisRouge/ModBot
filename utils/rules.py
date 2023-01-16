class RuleManager:
    #  def refresh_rules
    pass

class Rule:
    def __init__(self):
        self._name = ''
        self._markers = {}  # TODO: move to an external file, should be refreshable on demand
        self._triggered = False

    def check(self, text):
        if self._markers not in text:
            self._triggered = True