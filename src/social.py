import rule_engine
from utils import load_characters_from_xml


class Social:
    def __init__(self):
        # Initialize rules here
        self.rules = []
        self.setup_rules()

    def setup_rules(self):
        rule = rule_engine.Rule(
            # match books published by DC
            'self.name == "BucketKnight"'
            )
        self.rules.append(rule)
        #self.rules.append(rule_engine.Rule('Array.opinion[0] >= 10.0',context))
        

  

    def apply_rules(self, context):
        for rule in self.rules:
            if rule.matches(context):
                print("Rule applied:", rule)
            else:
                print("Rule violated:", rule)
    
    def check_opinion_and_update_relationship(self, context):
        # Extract the character's name and opinions from the context
        character_name = context.get('name')
        opinions = context.get('opinions', [])
        
        for opinion in opinions:
            other_name, (alliance, _, _) = opinion
            if alliance > 10:
                relationship = context.get('relationships')
                relationship[0] = True
                break
    
    def update_relationship_status(self, current_character_name, other_character_name):
    # Access the relationships from the context
        relationships = context.get('relationships', {})
    
        # Ensure that the current character and other character have entries in the relationships
        if current_character_name in relationships and other_character_name in relationships:
            # Update the status (assuming the status is a list with the same structure as described)
            current_status = relationships[current_character_name]
            
            # For demonstration, let's say we want to set 'friends' to True (index 0)
            # You should adjust this based on the actual index and status you want to update
            current_status[0] = True
            
            # Save the updated status back
            relationships[current_character_name] = current_status
            
            # If relationships need to be updated in both directions
            other_status = relationships[other_character_name]
            other_status[0] = True  # Update status for the other character as well
            relationships[other_character_name] = other_status

            print(f"Updated relationship status for {current_character_name} and {other_character_name}")
        else:
            print(f"One or both characters not found in relationships: {current_character_name}, {other_character_name}")       

    def initialize_opinions(self, character):
        # Convert the tuples into a dictionary for easier manipulation
        opinions_dict = dict(character['opinions'])
        social_history_dict = dict(character['social_history'])

        for name, history_value in social_history_dict.items():
            if name in opinions_dict:
                print('test')
                print(opinions_dict[name])
                print(history_value)
                result = [x + y for x, y in zip(opinions_dict[name], history_value)]
                opinions_dict[name] = result
            else:
                opinions_dict[name] = history_value

        # Convert the dictionary back to a list of tuples
        character['opinions'] = list(opinions_dict.items())

        # Now apply the rules to see if they are satisfied
        #self.apply_rules(character)

context = rule_engine.Context(type_resolver=rule_engine.type_resolver_from_dict({
    'name': rule_engine.DataType.STRING,
    'traits': rule_engine.DataType.ARRAY,
    'social_history': rule_engine.DataType.ARRAY,
    'relationships': rule_engine.DataType.ARRAY,
    'opinions': rule_engine.DataType.ARRAY,
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

social_engine.apply_rules(context)