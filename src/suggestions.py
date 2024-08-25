import social
import rule_engine

# Dictionary that stores suggestions formatted {"CharA": {"CharB": [sugg1,sugg2,...], ...}, ...}
# Might switch to storing this info somewhere else if it's easier for everyone else.
suggestionStorage = {}

class suggestion:
    def __init__(self, intention, name, volition = 0, motives = []):
        self.intent = intention
        #intention should be:
        # 'increase'/'decrease' + 'alliance'/'romance'/'reverence'
        # or 'become'/'end' + 'Allies'/'Enemies'/'Lovers'
        self.name = name
        self.volition = volition
        self.motives = motives

#Sets up the suggestions for each and every combination of characters
def suggestionSetup():
    # for characterA in social.characters,
        # and for every characterB in social.characters
        # if characterA == characterB
            # continue #skip to next loop
    global suggestionStorage
    suggestionStorage = {}
    for charA in social.social_engine.characters:
        charASuggestions = []
        for charB in social.social_engine.characters:
            if charA != charB:

                # Info pull
                # [alliance, love, reverence]
                opinions = social.social_engine.get_opinions(charA['name'], charB['name'])
                # [allies, lovers, enemies]
                relationships = social.social_engine.get_relationships(charA['name'], charB['name'])
                # {Traitname: true/false, ...}
                charATraits = social.social_engine.get_traits(charA['name'])
                charBTraits = social.social_engine.get_traits(charB['name'])
                # {SCKName: 'like'/'dislike'/etc ...}
                charASCK = social.social_engine.get_sck_opinions(charA['name'])
                charBSCK = social.social_engine.get_sck_opinions(charB['name'])
                # {SCKName: ??? ...}
                diffSCK = social.social_engine.compare_sck_opinions(charA['name'], charB['name'])
                classList = ["Knight", "Healer", "Rogue", "Barbarian", "Mage"]

                # Alliance Up setup ==============================================================<>
                allianceUp = 0
                if (opinions[0] >= 50):
                    allianceUp += 2
                # Consider alliance Up suggestions
                if allianceUp > 0:
                    # Be Kind ------------------------------------>
                    # setup
                    volition = allianceUp
                    motives = []

                    # Determine whether to include suggestion
                    if (opinions[0] >= 80):
                        volition += 2
                        motives.append(charA['name'] + " is close friends with " + charB['name'])

                    if volition > allianceUp:
                        # Determine further desire to include suggestion
                        if (opinions[2] >= 50):
                            volition += 10
                            motives.append(charA['name'] + " thinks " + charB['name'] + " is extraordinary.")
                        # Add suggestion
                        charASuggestions.append(suggestion("Increase Alliance", "Be Kind", volition=volition, motives=motives))
                    
                    # Bond Over Shared Interest ------------------------------------>
                    volition = allianceUp
                    motives = []

                    for item, value in charASCK:
                        if item in charBSCK and value == charBSCK[item]: # if share opinion on SCK
                            volition += 2
                            motives.append(charA['name'] + " and " + charB['name'] + " both " + value + " " + item)
                    
                    if volition > allianceUp:
                        for trait in charATraits:
                            if trait in classList and trait in charBTraits:
                                volition += 10
                                motives.append(charA['name'] + " and " + charB['name'] + " are the same class.")
                                break # can only have 1 class, so if you find it might as well stop
                        charASuggestions.append(suggestion("Increase Alliance", "Bond Over Shared Interest", volition=volition, motives=motives))

                # Alliance Down setup ==============================================================<>
                allianceDown = 0
                if (opinions[0] <= 50):
                    allianceDown += 2

                if allianceDown > 0:
                    # Be Rude ------------------------------------>
                    volition = allianceDown
                    motives = []
                    

        # ... after rest of setup
        # Order by volition, highest to lowest
        charASuggestions.sort(key=lambda sugg: sugg.volition, reverse=True)
        # Include only the top 5, if longer than 5
        if len(charASuggestions) > 5:
            charASuggestions[:5]
        # Input into suggestion dict
        suggestionStorage[charA['name']][charB['name']] = charASuggestions

# Gets the result of a suggestion. Input is the suggestion object, the charA object, and the charB object
def GetSuggestionResult(suggestion, charA, charB):
    # Info pull
    # [alliance, love, reverence]
    opinions = social.social_engine.get_opinions(charA['name'], charB['name'])
    # [allies, lovers, enemies]
    relationships = social.social_engine.get_relationships(charA['name'], charB['name'])
    # {Traitname: true/false, ...}
    charATraits = social.social_engine.get_traits(charA['name'])
    charBTraits = social.social_engine.get_traits(charB['name'])
    # {SCKName: 'like'/'dislike'/etc ...}
    charASCK = social.social_engine.get_sck_opinions(charA['name'])
    charBSCK = social.social_engine.get_sck_opinions(charB['name'])
    # {SCKName: ??? ...}
    diffSCK = social.social_engine.compare_sck_opinions(charA['name'], charB['name'])
    classList = ["Knight", "Healer", "Rogue", "Barbarian", "Mage"]

    match suggestion.name:
        case "Be Kind":
            #Determine success score
            success = 1
            if "charming" in charATraits:
                success += 1
            if "agressive" in charATraits:
                success -= 1
            
            #Determine if succeed/failure, and results
            if success > 0:
                #ASK IF UPDATE_OPINION CAN BE CHANGED FROM INT TO NAME STR, OR IF THERE'S A WAY TO GET THE INDEX FROM THE NAME/OBJECT
                social.social_engine.update_opinion(charB['name'],charA['name'],10,0,0)
                social.social_engine.update_opinion(charA['name'],charB['name'],10,0,0)
            else:
                social.social_engine.update_opinion(charB['name'],charA['name'],-10,0,0)
        case "Bond Over Shared Interest":
            success = 1
            for item, value in charASCK:
                if item in charBSCK and value == charBSCK[item]:
                    success += 2 # agreement worth twice as much as disagreement
            for trait in charATraits:
                if trait in classList and trait in charBTraits:
                    success += 1
            success -= len(diffSCK)

            if success > 0:
                social.social_engine.update_opinion(charB['name'],charA['name'],15,0,0)
                social.social_engine.update_opinion(charA['name'],charB['name'],15,0,0)
            else:
                social.social_engine.update_opinion(charB['name'],charA['name'],-10,0,0)

    