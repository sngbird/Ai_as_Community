# import rule-engine
from utils import load_quests_from_xml
from random import randint
import Social

class QuestManager:
    def __init__(self, social_engine):
        #Holds data about all quests, currently possible quests, & deployed quests.
        self.quests = {} #quests are loaded straight from XML into here
        self.possible_quests = []
        self.deployed_quests = []
        self.social_engine = social_engine

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

    #-----Unfinished------
    #Add a party member to the quest. Also requires social meddling, so I haven't done this yet either.
    #Also thinking of moving this from here to be a Quest class method instead.
    def add_members(self, quest, character_name):
        print("Temp")
        able_to_add = True
        #Check if:
        #   - party is not full
        #   - character is not already in party
        #   - character is not injured
        #   - character has no conflicts

        if len(quest.current_members) >= quest.party_max:
            able_to_add = False
        elif character_name in quest.current_members: #These all have the same result, but separating them for clarity
            able_to_add = False
        #Insert "elif character not injured" here
        elif self.social_engine.is_injured(character_name) == True:
            able_to_add = False
        #Insert "elif some social conflicts" here
        for current_member_name in quest.current_members:
            relationships = self.social_engine.get_relationships(character_name, current_member_name)
            if relationships[2] is True:
                able_to_add = False
                break
        
        if able_to_add:
            quest.current_members.append(character_name)
    
    #Actually run the quest and add the results to the player's gold count/stats, plus altering social states.
    def run_quest(self, quest_name):
        print("Temp")


#Quest class!
class Quest: #each Quest is an instance of this - just stores dictionary info into a more easier-to-access format
    def __init__(self, name, info):
        #Quest-type evident
        self.title = name
        self.description = info['description']

        #Reqs & Risks
        self.requirements = info['requirements']
        self.risks = info['risks']
        
        #Party Numbers
        self.party_max = info['minimum']
        self.party_min = info['maximum']

        #Randomly rolled
        self.danger_level = randint(0, 5)
        
        #World-state determinant - haven't figured out how to do this yet
        self.time_left = 0

        #Player-state determinant
        self.current_members = []

    # def add_member(self, character):
        
