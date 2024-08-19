import rule_engine
import re
from utils import load_characters_from_xml

debug = True

class Social:
    def __init__(self,context):
        # Initialize rules here
        self.rules = []
        self.setup_rules(context)

    def setup_rules(self,context):
        #Alliance Threshold Check
        self.rules.append(rule_engine.Rule('opinions[0][1][0] >= 10.0', context=context))
        #Alliance Reflexivity
        self.rules.append(rule_engine.Rule('relationships[0][0] == 1', context=context))

    def apply_rules(self, context):
        if debug: print(self.rules)
        for rule in self.rules:
            if rule.matches(context):
                print(context['name'] + ' applied: ', rule)
                self.update_relationship_status(context,rule)
            #else:
                #if debug: print(context['name'] + ' violated: ', rule)
    
    def update_relationship_status(self, context, rule):
    # Access the relationships from the context
        relationships = context.get('relationships', {})
        #Parse the rule to perform appropriate relationship update
        match = re.search(r'(>=|<=|>|<|==|!=)', str(rule))
        if match.group() == ">=":
            #This is super barebones and will only work on this test example for proof of concept.
            #We need a more robust method when we want to include more people
            relationships[0] = [True,False,False,False]

    def initialize_opinions(self, character):
        # Convert the tuples into a dictionary for easier manipulation
        opinions_dict = dict(character['opinions'])
        social_history_dict = dict(character['social_history'])

        for name, history_value in social_history_dict.items():
            if name in opinions_dict:
                result = [x + y for x, y in zip(opinions_dict[name], history_value)]
                opinions_dict[name] = result
            else:
                opinions_dict[name] = history_value

        # Convert the dictionary back to a list of tuples
        character['opinions'] = list(opinions_dict.items())


context = rule_engine.Context(type_resolver=rule_engine.type_resolver_from_dict({
    'name': rule_engine.DataType.STRING,
    'traits': rule_engine.DataType.ARRAY,
    'social_history': rule_engine.DataType.ARRAY,
    'relationships': rule_engine.DataType.ARRAY,
    'opinions': rule_engine.DataType.ARRAY,
}))


social_engine = Social(context)

characters = load_characters_from_xml('characters.xml')
if debug:
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
    print('Adding social_history to opinions')
    print()
for character in characters:
    social_engine.initialize_opinions(character)

# Output the characters to see the modified opinions
if debug:
    for character in characters:
        print(f"Character: {character['name']}")
        print(f"Opinions: {character['opinions']}")
        print()
for character in characters:
    # Create context with character's data
    context_data = {
        'name': character['name'],
        'traits': character['traits'],
        'social_history': character['social_history'],
        'relationships': character['relationships'],
        'opinions': character['opinions'],
    }
    # Apply rules for the current character
    social_engine.apply_rules(context_data)
    if debug:
        print(f"Character: {character['name']}")
        print(f"Relationships: {character['relationships']}")
        print()