# import rule-engine
from utils import load_quests_from_xml
from random import randint, choice
from social import Social
import random
import copy

class QuestManager:
    def __init__(self, social_engine):
        #Holds data about all quests, currently possible quests, & deployed quests.
        raw_quests = load_quests_from_xml('quests.xml',self)
        self.quests = {
            name: Quest(
                name,
                info['description'],
                info['requirements'],
                info['risks'],
                info['minimum'],
                info['maximum']
            )
            for name, info in raw_quests.items()
        }
        self.possible_quests = []
        self.deployed_quests = []
        self.social_engine = social_engine
        self.all_members = social_engine.character_names
        self.available_members = []
        for name in self.all_members:
            self.available_members.append(name)
        self.unavailable_members = []

    #Add a slightly varying number (3-5?) of quests for the week.
    def add_quests_weekly(self):
        if len(self.possible_quests)>= 1:
            return
        random_quest_name, random_quest_info = random.choice(list(self.quests.items()))  # Randomly select a quest        
        self.possible_quests.append(random_quest_info)

    #Helper for selecting quests - checks if the quest is already deployed
    def quest_in_bowl(self, quest_name):
        for quest in self.possible_quests:
            if quest.name == quest_name:
                return True
        return False

    #Deploy quest (remove it from possible, add it to deployed)
    def deploy_quest(self, quest):
        #To do: make sure all requirements are fulfilled
        if quest.requirements_fulfilled():
            if len(quest.get_current_members()) >= quest.get_minimum:
                self.possible_quests.remove(quest)
                self.deployed_quests.append(quest)
                return "Quest successfully deployed!"
            else:
                return "Quest not deployed; not enough party members!"
        else:
            return "Quest not deployed; does not fulfill all requirements" #quest not deployed

    #Remove a character from a quest
    def remove_members(self, quest, character_name):
        quest.current_members.remove(character_name)
        self.move_character_to_available(character_name)
        return f"{character_name} Removed From Party"

    #-----Unfinished------
    #Add a party member to the quest. Also requires social meddling, so I haven't done this yet either.
    #Also thinking of moving this from here to be a Quest class method instead.
    def add_members(self, quest, character_name):
        able_to_add = True
        rule = None
        #Check if:
        #   - party is not full
        #   - character is not already in party
        #   - character is not injured
        #   - character has no conflicts
        while able_to_add is True:
            if len(quest.current_members) >= int(quest.party_max):
                able_to_add = False
                rule = f"Party Is Max Size"
            elif character_name in quest.current_members: #These all have the same result, but separating them for clarity
                able_to_add = False
                rule = f"{character_name} in Current Party"
            elif character_name in self.unavailable_members:
                rule = f"{character_name} in another Party"
                able_to_add = False
            elif self.social_engine.is_injured(character_name) == True:
                rule = f"{character_name} in Injured"
                able_to_add = False
            #Insert "elif some social conflicts" here
            for current_member_name in quest.current_members:
                relationships = self.social_engine.get_relationships(character_name, current_member_name)
                if relationships[2] is True:
                    able_to_add = False
                    rule = f"they are enemies with {current_member_name}"
            break       
        if able_to_add:
            quest.current_members.append(character_name)
            self.move_character_to_unavailable(character_name)
            return None
        else:
            return f"{character_name} Can't Join Party because {rule}"
    
    #Actually run the quest and add the results to the player's gold count/stats, plus altering social states.
    def run_quest(self, quest):
        injuries_multiplier = quest.danger_level + quest.risks_taken(self.social_engine)
        if injuries_multiplier > quest.max_party_size:
            injuries_multiplier = quest.max_party_size
        injuries_num = randint(0, injuries_multiplier) #yeah I simplified this a bit. It's not what's most important.
        actual_injuries = 0
        for injury in range(injuries_num):
            #Injure a random character in the party. (If they're already injured, do nothing and continue.)
            injured_char = choice(quest.get_current_members())
            if not self.social_engine.get_injury(injured_char):
                actual_injuries += 1
            self.social_engine.set_injury(injured_char, True)
        quest_score = (1/(1+actual_injuries)) * (len(quest.get_current_members()) * quest.get_num_dif_classes())
        return f"Quest score of {quest_score}"

    def get_quests_description(self, quest_type):
        if quest_type == 'all':
            return [(quest.title, quest.description) for quest in self.quests.values()]
        elif quest_type == 'possible':
            return [(quest.title, quest.description) for quest in self.possible_quests]
        elif quest_type == 'deployed':
            return [(quest.title, quest.description) for quest in self.deployed_quests]
        else:
            raise ValueError("Invalid quest type specified. Choose 'all', 'possible', or 'deployed'.")
        
    def get_quest_by_title(self, title):
        quest = self.quests.get(title)
        if quest:
            return quest
        else:
            raise ValueError(f"No quest found with title: {title}")
        
    def get_available_characters(self):
        return self.available_members

    # Get a list of unavailable characters
    def get_unavailable_characters(self):
        return self.unavailable_members

    # Move a character to the unavailable list
    def move_character_to_unavailable(self, character_name):
        if character_name in self.available_members:
            self.available_members.remove(character_name)
            self.unavailable_members.append(character_name)
            return (f"moved {character_name} to unavailable")

    # Move a character to the available list
    def move_character_to_available(self, character_name):
        if character_name in self.unavailable_members:
            self.unavailable_members.remove(character_name)
            self.available_members.append(character_name)
            return (f"moved {character_name} to available")

#Quest class!

class Quest:
    def __init__(self, name, description, requirements, risks, min_party_size, max_party_size):
        self.title = name
        self.description = description
        self.requirements = requirements
        self.risks = risks
        self.party_min = min_party_size
        self.party_max = max_party_size
        self.danger_level = randint(0, max_party_size-2)  # or any other default value or calculation
        self.current_members = []

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_requirements(self):
        return self.requirements

    def get_risks(self):
        return self.risks

    def get_minimum(self):
        return self.party_min

    def get_maximum(self):
        return self.party_max

    def get_danger_level(self):
        return self.danger_level

    def get_current_members(self):
        return self.current_members

    def representation(self):
        return f"Quest(title={self.title}, description={self.description})"
    
    def get_current_members(self):
        return self.current_members

    def print_current_members(self):
        if not self.current_members:
            return "No current members in the party."
        return "Current party members:\n" + "\n".join(self.current_members)
    
    def get_num_dif_classes(self, social_engine):
        existing_classes = []
        for character in self.current_members:
            char_class = social_engine.get_traits(character).keys()[0]
            if char_class not in existing_classes:
                existing_classes.append(char_class)
        return len(existing_classes)
    
    def requirements_done(self, social_engine):
        requirements_unfulfilled = self.requirements
        for requirement in self.requirements:
            for party_member in self.current_members:
                #Class
                if requirement['type'] == "Class" and (social_engine.get_traits(party_member).keys()[0] == requirement['value'] or
                                                       ('alt_value' in requirement.keys() and 
                                                       social_engine.get_traits(party_member).keys()[0] == requirement['alt_value'])):
                    requirements_unfulfilled.remove(requirement)
                    continue
                #Trait
                elif requirement['type'] == "Trait":
                    fulfilled = False
                    for trait in social_engine.get_traits(party_member).keys()[1:]:
                        if trait == requirement['value'] or ('alt_value' in requirement.keys() and 
                                                             trait == requirement['alt_value']):
                            fulfilled = True
                            requirements_unfulfilled.remove(requirement)
                            break
                    if fulfilled:
                        continue
                #SCK doesn't require alt value, thankfully (I say this but I added the alt values in the first place)
                elif requirement['type'] == "SCK":
                    fulfilled = False
                    for knowledge, opinion in social_engine.get_sck_opinions(party_member).items():
                        if requirement['value'] == knowledge and requirement['opinion'] == opinion:
                            fulfilled = True
                            requirements_unfulfilled.remove(requirement)
                            break
        if len(requirements_unfulfilled) == 0:
            return True
        else:
            return False
    
    def risks_taken(self, social_engine): #risks is an array of dictionaries with keys: type, value, quantity, alt_value. Quantity is kind of pointless tho
        total_risks = 0
        for risk in self.risks: #Outermost loop: check risks
            for party_member in self.current_members: #Next loop: loop through party members
                # If it's Class, just look at the first trait. 
                if risk['type'] == "Class" and social_engine.get_traits(party_member).keys()[0] == risk['value']:
                    total_risks+=1
                    continue
                # If it's Trait, look at all but the first trait.
                elif risk['type'] == "Trait":
                    has_risk = False #only count any character's risk once, a character can only be so much of a walking red flag
                    for trait in social_engine.get_traits(party_member).keys()[1:]:
                        if trait == risk['value']:
                            total_risks+=1
                            has_risk = True
                            break
                    if has_risk:
                        continue
                # If it's SCK, look at the SCK instead of traits.
                elif risk['type'] == "SCK":
                    has_risk = False
                    for knowledge, opinion in social_engine.get_sck_opinions(party_member).items():
                        if risk['value'] == knowledge and risk['opinion'] == opinion:
                            total_risks+= 1
                            has_risk = True
                            break
                    if has_risk:
                        continue
        return total_risks

    
# social_engine = Social()
# quest_man = QuestManager(social_engine)
# #print(quest_man.get_quests_description('all'))