import rule_engine
import re
from utils import load_characters_from_xml, load_sck_from_xml

debug = True

class Social:
    def __init__(self, characters):
        """
        Initialize the Social class with the given character names.

        Args:
            character_names (list of str): List of character names to initialize the matrices.
        """
        #Preparing Context and DataStructures
        #Create the Matrices for Character Opinions and Relationship information
        self.characters = characters
        character_names = [character['name'] for character in characters]
        self.character_names = character_names
        self.num_characters = len(character_names)
        # Initialize 2D matrices for relationships and opinions
        self.relationships_matrix = [
            [{name: [False, False, False, False] for name in character_names} for _ in range(self.num_characters)]
            for _ in range(self.num_characters)
        ]
        self.opinions_matrix = [
            [{name: [0.0, 0.0, 0.0] for name in character_names} for _ in range(self.num_characters)]
            for _ in range(self.num_characters)
        ]
        #Setup for SCK Matrix (holds SCK and which Opinions is associated )
        self.shared_cultural_matrix = {}
        load_sck_from_xml('SCK.xml',self) #Loads the SCK directly into the shared_cultural_matrix
        #and SCK_Character_Opinion_Matrix (which holds each characters opinions of the knowledge items)
        self.cultural_opinion_matrix = {}

        # Initialize opinions based on social history for all characters
        for i, character in enumerate(characters):
            self.initialize_opinions(i, character['social_history'])
            self.initialize_relationships(i, character['relationships'])
            self.initialize_sck(i, character['SCK'])
        #Rules Section
        self.rules = []
        self.setup_rules()

    def update_opinion(self, source_index, target_index, alliance, romance, reverence):
        """
            Update the opinion matrix with the given values, performing element-wise addition.

            Args:
                source_index (int): Index of the source character in the matrix.
                target_index (int): Index of the target character in the matrix.
                alliance (float): Alliance value to update.
                romance (float): Romance value to update.
                reverence (float): Reverence value to update.
            """
        target_name = self.character_names[target_index]
        current_opinions = self.opinions_matrix[source_index][target_index].get(target_name, [0.0, 0.0, 0.0])
        updated_opinions = [
            current_opinions[0] + alliance,
            current_opinions[1] + romance,
            current_opinions[2] + reverence
        ]
        self.opinions_matrix[source_index][target_index][target_name] = updated_opinions

    def update_relationship(self, source_index, target_index, relationship_status):
        """
        Update the relationship matrix with the given status, performing an "and" operation.

        Args:
            source_index (int): Index of the source character in the matrix.
            target_index (int): Index of the target character in the matrix.
            relationship_status (list of bool): List indicating the relationship status [friends, dating, enemies, party_member].
        """
        target_name = self.character_names[target_index]
        current_status = self.relationships_matrix[source_index][target_index].get(target_name, [False, False, False, False])
        
        # Perform logical "and" operation between the existing status and the new status
        updated_status = [current or new for current, new in zip(current_status, relationship_status)]
        
        self.relationships_matrix[source_index][target_index][target_name] = updated_status

    def initialize_opinions(self, index, social_history):
        """
        Initialize opinions for a character based on their social history.

        Args:
            index (int): Index of the character in the matrix.
            social_history (list of tuples): List where each tuple contains (target_name, (alliance, romance, reverence)).
        """
        for target_name, (alliance, romance, reverence) in social_history:
            if target_name in self.character_names:
                target_index = self.character_names.index(target_name)
                self.update_opinion(index, target_index, alliance, romance, reverence)
    
    def initialize_relationships(self, index, relationships):
        """
        Initialize relationships for a character based on their relationships data.

        Args:
            index (int): Index of the character in the matrix.
            relationships (list of tuples): List where each tuple contains (target_name, (friends, couples, enemies, teammates)).
        """
        for target_name, (friends, couples, enemies, teammates) in relationships:
            if target_name in self.character_names:
                target_index = self.character_names.index(target_name)
                self.update_relationship(index, target_index, [friends, couples, enemies, teammates])
    
    def initialize_sck(self, index, sck):
        """
        Initialize SCK opinions for a character based on their SCK.

        Args:
            index (int): Index of the character in the matrix.
            sck (list of tuples): List where each tuple contains (target_name, opinion).
        """
        for knowledge_item_name, opinion_value in sck:
            print(knowledge_item_name)
            print(opinion_value)
            if knowledge_item_name not in self.cultural_opinion_matrix:
                    self.cultural_opinion_matrix[knowledge_item_name] = {}
            self.cultural_opinion_matrix[knowledge_item_name][self.character_names[index]] = opinion_value
                

    def setup_rules(self):
        self.rules.append(rule_engine.Rule('reflexive_relationships()'))

    def reflexive_relationships(self):
        #Checks if the character has a relationship status that violates the reflexivity rule
        for i, source_name in enumerate(self.character_names):
            for j, target_name in enumerate(self.character_names):
                if i != j:
                    source_relationships = self.get_relationships(source_name, target_name)
                    target_relationships = self.get_relationships(target_name, source_name)

                    # Check reflexivity for Alliance, Lover, and Enemy
                    if source_relationships[0] == True or target_relationships[0] == True:
                        if source_relationships[0] != target_relationships[0]:
                            if debug: print(f"Updated {target_name}'s relationship towards {source_name} to match reflexive status.")
                            self.update_relationship(j, i, source_relationships)
                    elif source_relationships[1] == True or target_relationships[1] == True:
                        if source_relationships[1] != target_relationships[1]:
                            if debug: print(f"Updated {target_name}'s relationship towards {source_name} to match reflexive status.")
                            self.update_relationship(j, i, source_relationships)
                    elif source_relationships[2] == True or target_relationships[2] == True:
                        if source_relationships[2] != target_relationships[2]:
                            if debug: print(f"Updated {target_name}'s relationship towards {source_name} to match reflexive status.")
                            self.update_relationship(j, i, source_relationships)
                
    def apply_rules(self):
        """
        Apply all the rules to the given list of characters.

        Args:
            characters (list of dict): List where each dict contains character data, including 'name', 'traits', and 'social_history'.
        """
        print("Apply Rule")
        for rule in self.rules:
            print(f"Applying rule: {rule}")
            # Directly call the reflexive_relationships function
            if self.reflexive_relationships():
                print("Reflexive relationship rule applied.")
            else:
                print("All relationships are already reflexive.")

    def get_traits(self, character_name):
        """
        Get the traits of a specific character by name.

        Args:
            character_name (str): Name of the character whose traits are to be retrieved.

        Returns:
            dict: Dictionary of traits for the specified character. Keys are trait names, and values are boolean.
        """
        for character in characters:
            if character['name'] == character_name:
                return character.get('traits', {})
        return {}

    def get_opinions(self, source_name, target_name):
        """
        Get the opinions from one character to another.

        Args:
            source_name (str): Name of the source character.
            target_name (str): Name of the target character.

        Returns:
            list of float: List with three values representing (alliance, romance, reverence).
        """
        source_index = self.character_names.index(source_name)
        target_index = self.character_names.index(target_name)
        opinion = self.opinions_matrix[source_index][target_index].get(target_name, (0.0,0.0,0.0))

        return self.opinions_matrix[source_index][target_index]

    def get_relationships(self, source_name, target_name):
        """
        Get the relationship status between two characters.

        Args:
            source_name (str): Name of the source character.
            target_name (str): Name of the target character.

        Returns:
            list of bool: List indicating the relationship status [friends, dating, enemies, party_member].
        """
        source_index = self.character_names.index(source_name)
        target_index = self.character_names.index(target_name)
        relationship_status = self.relationships_matrix[source_index][target_index].get(target_name, [False, False, False, False])

        return relationship_status


# Test examples

characters = load_characters_from_xml('characters.xml')


# Create the Social engine
social_engine = Social(characters)


# # Test getters
# print("Getter Test: Traits: BucketKnight")
# print(social_engine.get_traits('BucketKnight'))  
# print("Getter Test: Opinions: BucketKnight and SheepGirl ")
# print(social_engine.get_opinions('BucketKnight', 'SheepGirl'))

# print("Relationship between SheepGirl and BucketKnight: ")
# print(social_engine.get_relationships('SheepGirl', 'BucketKnight'))  
# print(social_engine.get_relationships('BucketKnight', 'SheepGirl'))

# print("Relationship between SheepGirl and VanessaConfessa: ")
# print(social_engine.get_relationships('SheepGirl', 'VanessaConfessa'))
# print(social_engine.get_relationships('VanessaConfessa', 'SheepGirl'))  



# social_engine.apply_rules()

# print("Relationship between SheepGirl and BucketKnight: ")
# print(social_engine.get_relationships('SheepGirl', 'BucketKnight'))  
# print(social_engine.get_relationships('BucketKnight', 'SheepGirl'))  

# print("Relationship between SheepGirl and VanessaConfessa: ")
# print(social_engine.get_relationships('SheepGirl', 'VanessaConfessa'))
# print(social_engine.get_relationships('VanessaConfessa', 'SheepGirl'))  

#print(social_engine.get_opinions('BucketKnight', 'SheepGirl'))  
print(social_engine.shared_cultural_matrix)
print(social_engine.cultural_opinion_matrix)