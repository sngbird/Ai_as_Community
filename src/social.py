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


context = rule_engine.Context(type_resolver=rule_engine.type_resolver_from_dict({
    'name': rule_engine.DataType.STRING,
    'class': rule_engine.DataType.ARRAY,
    'social_history': rule_engine.DataType.ARRAY,
    'relationships': rule_engine.DataType.ARRAY,
    'opinions': rule_engine.DataType.ARRAY,
    #'sck': rule_engine.DataType.ARRAY
}))
# Classes Defender = index 0, Healer 1, ...
# social_history float values to be added to opinions at start of game
# relationships [Friends, Dating, Enemies, Current Party Member], discrete values
# Opinions threshold values, updated dynamically, each index represents other potential party members
characters = [
  {
    'name': 'BucketKnight',
    'class': [1,0],
    'social_history': [0,0],
    'relationships': [1,0,0,1],
    'opnions': [0,0],
  },
  {
    'name': 'SheepGirl',
    'class': [0,1],
    'social_history': [0,0],
    'relationships': [1,0,0,1],
    'opnions': [0,0],
  },
]

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

# receive an error when an unknown symbol is used
rule = rule_engine.Rule('class == "Defender"', context=context)
# => SymbolResolutionError: last_name

# receive an error when an invalid operation is used
rule = rule_engine.Rule('first_name + 1', context=context)
# => EvaluationError: data type mismatch