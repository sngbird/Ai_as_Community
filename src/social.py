import rule_engine

class Social:
    def __init__(self):
        # Initialize rules here
        self.rules = []
        self.setup_rules()

    def setup_rules(self):
        # Example rule: reflexivity of friends if X -> Y then Y -> X
        rule = rule_engine.Rule("Friend Tim Jerry, Friend Jerry Tim")
        self.rules.append(rule)

    def apply_rules(self, context):
        for rule in self.rules:
            if not rule.matches(context):
                print("Rule violated:", rule)
