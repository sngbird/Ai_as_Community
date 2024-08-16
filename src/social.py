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


# match a literal first name and applying a regex to the email
rule = rule_engine.Rule(
    'first_name == "Luke" and email =~ ".*@rebels.org$"'
) # => <Rule text='first_name == "Luke" and email =~ ".*@rebels.org$"' >
rule.matches({
    'first_name': 'Luke', 'last_name': 'Skywalker', 'email': 'luke@rebels.org'
}) # => True
rule.matches({
   'first_name': 'Darth', 'last_name': 'Vader', 'email': 'dvader@empire.net'
}) # => False



characters = [
  {
    'name': 'BucketKnight',
    'Class': 'Defender',
  },
  {
    'name': 'SheepGirl',
    'Class': 'Healer',
  },
]

context = rule_engine.Context(type_resolver=rule_engine.type_resolver_from_dict({
    'first_name': rule_engine.DataType.STRING,
    'age': rule_engine.DataType.FLOAT
}))

# receive an error when an unknown symbol is used
rule = rule_engine.Rule('last_name == "Vader"', context=context)
# => SymbolResolutionError: last_name

# receive an error when an invalid operation is used
rule = rule_engine.Rule('first_name + 1', context=context)
# => EvaluationError: data type mismatch