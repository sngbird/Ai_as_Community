# import rule-engine
from utils import load_quests_from_xml
from random import randint
from social import Social

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
        self.available_members = social_engine.character_names
        self.unavailable_members = []

    #Add a slightly varying number (3-5?) of quests for the week.
    def add_quests_weekly(self):
        random_quest_name, random_quest_info = self.quests.items()[randint(0,len(self.quests.keys()))] #Pick a random quest
        while self.quest_in_bowl(random_quest_name):
            random_quest_name, random_quest_info = self.quests.items()[randint(0,len(self.quests.keys()))]
        new_quest = Quest(random_quest_name, random_quest_info)
        self.possible_quests.append(new_quest)

    #Helper for selecting quests - checks if the quest is already deployed
    def quest_in_bowl(self, quest_name):
        for quest in self.possible_quests:
            if quest.name == quest_name:
                return True
        return False

    #Deploy quest (remove it from possible, add it to deployed)
    def deploy_quest(self, quest):
        self.possible_quests.remove(quest)
        self.deployed_quests.append(quest)

    #Remove a character from a quest
    def remove_members(self, quest, character_name):
        quest.current_members.remove(character_name)
        self.move_character_to_unavailable(character_name)

    #-----Unfinished------
    #Add a party member to the quest. Also requires social meddling, so I haven't done this yet either.
    #Also thinking of moving this from here to be a Quest class method instead.
    def add_members(self, quest, character_name):
        able_to_add = True
        #Check if:
        #   - party is not full
        #   - character is not already in party
        #   - character is not injured
        #   - character has no conflicts
        while able_to_add is True:
            if len(quest.current_members) >= int(quest.party_max):
                able_to_add = False
            elif character_name in quest.current_members: #These all have the same result, but separating them for clarity
                able_to_add = False
            elif character_name in self.unavailable_members:
                able_to_add = False
            elif self.social_engine.is_injured(character_name) == True:
                able_to_add = False
            #Insert "elif some social conflicts" here
            for current_member_name in quest.current_members:
                relationships = self.social_engine.get_relationships(character_name, current_member_name)
                if relationships[2] is True:
                    able_to_add = False
                    
        
        if able_to_add:
            quest.current_members.append(character_name)
            self.move_character_to_unavailable(character_name)
            return "Successfully Added"
        else:
            return "Character Can't Join Party"
    
    #Actually run the quest and add the results to the player's gold count/stats, plus altering social states.
    def run_quest(self):
        #Instead of giving a name, it will just run the ones in deployed for simplicity
        print("Temp")

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

    # Move a character to the available list
    def move_character_to_available(self, character_name):
        if character_name in self.unavailable_members:
            self.unavailable_members.remove(character_name)
            self.available_members.append(character_name)
#Quest class!
# quest.py

class Quest:
    def __init__(self, name, description, requirements, risks, min_party_size, max_party_size):
        self.title = name
        self.description = description
        self.requirements = requirements
        self.risks = risks
        self.party_min = min_party_size
        self.party_max = max_party_size
        self.danger_level = randint(0, 5)  # or any other default value or calculation
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
    
# social_engine = Social()
# quest_man = QuestManager(social_engine)
# #print(quest_man.get_quests_description('all'))