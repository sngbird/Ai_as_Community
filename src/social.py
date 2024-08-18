import rule_engine
from utils import load_characters_from_xml


class Social:
    def __init__(self):
        # Initialize rules here
        self.rules = []
        self.setup_rules()

    def setup_rules(self):

        pass

    def apply_rules(self, context):
        for rule in self.rules:
            if rule.matches(context):
                print("Rule applied:", rule)
            else:
                print("Rule violated:", rule)

    def initialize_opinions(self, character):
        # Convert the tuples into a dictionary for easier manipulation
        opinions_dict = dict(character['opinions'])
        social_history_dict = dict(character['social_history'])

        for name, history_value in social_history_dict.items():
            if name in opinions_dict:
                opinions_dict[name] += history_value
            else:
                opinions_dict[name] = history_value

        # Convert the dictionary back to a list of tuples
        character['opinions'] = list(opinions_dict.items())

        # Now apply the rules to see if they are satisfied
        self.apply_rules(character)

context = rule_engine.Context(type_resolver=rule_engine.type_resolver_from_dict({
    'name': rule_engine.DataType.STRING,
    'traits': rule_engine.DataType.LIST,
    'social_history': rule_engine.DataType.LIST,
    'relationships': rule_engine.DataType.LIST,
    'opinions': rule_engine.DataType.LIST,
}))


social_engine = Social()

characters = load_characters_from_xml('characters.xml')
for character in characters:
    print(f"Character: {character['name']}")
    print(f"Traits: {character['traits']}")
    print(f"Social History: {character['social_history']}")
    print(f"Relationships: {character['relationships']}")
    print(f"Opinions: {character['opinions']}")
    print()

for character in characters:
    print(f"Character: {character['name']}")
    print(f"Opinions: {character['opinions']}")
    print()

# Initialize opinions based on social history for all characters
for character in characters:
    social_engine.initialize_opinions(character)

# Output the characters to see the modified opinions
for character in characters:
    print(f"Character: {character['name']}")
    print(f"Opinions: {character['opinions']}")
    print()

