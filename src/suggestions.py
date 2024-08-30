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
            # if characterA != characterB
    global suggestionStorage
    suggestionStorage = {}
    for charA in social.social_engine.characters:
        suggestionStorage[charA['name']] = {}
        for charB in social.social_engine.characters:
            if charA != charB:
                charASuggestions = []
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
                sameSCK = social.social_engine.compare_sck_opinions_same(charA['name'], charB['name'])
                classList = ["Knight", "Healer", "Rogue", "Barbarian", "Mage"]
                # shared relationships
                sharedAllies = []
                sharedEnemies = []
                charAConflictingAllies = [] # Ally of A but enemy of B
                charBConflictingAllies = []# Ally of B but enemy of A
                for person in charA["relationships"]:
                    for personB in charB["relationships"]:
                        if person[0] == personB[0]: #each person is formatted as ("name", (ally,lover,enemy,partymember))
                            if person[1][0] == personB[1][0]:
                                sharedAllies.append(person[0])
                            if person[1][2] == personB[1][2]:
                                sharedEnemies.append(person[0])
                            if person[1][0] == True and personB[1][2] == True: #A is allies but B is enemies
                                charAConflictingAllies.append(person[0])
                            if person[1][2] == True and personB[1][0] == True: #A is allies but B is enemies
                                charBConflictingAllies.append(person[0])

                # PRIORITY FUNCTION CHECK SETUP =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-={}
                motives = [] # Declared here so that the functions can access it. will reset every time 
                # The below functions determine the motives and resulting volition based on different aspects of the current gamestate.

                #def hasOpinion(motiveList, opinion=0, opinionValue=50, greaterThan=True, volition=10)

                def hasTrait(traitName, isClass=False, val=10):
                    if traitName in charATraits:
                        if isClass:
                            motives.append(charA['name'] + "'s class is " + traitName + ".")
                        else:
                            motives.append(charA['name'] + " is " + traitName + ".")
                        return val
                    return 0

                def haveSharedAlly(val=10):
                    totalVal = 0
                    for person in sharedAllies:
                        motives.append(charA['name'] + " and " + charB['name'] + " are both allies with " + person + ".")
                        totalVal += val
                    return totalVal
                
                def haveSharedEnemy(val=10):
                    totalVal = 0
                    for person in sharedEnemies:
                        motives.append(charA['name'] + " and " + charB['name'] + " are both enemies with " + person + ".")
                        totalVal += val
                    return totalVal

                #Adds motive/val for every person that charA is allied with that charB is enemies with. If sourceCharA=False, switches charA and charB
                def alliedWithEnemy(sourceCharA=True,val=10):
                    totalVal = 0
                    if sourceCharA:
                        for person in charAConflictingAllies:
                            motives.append(charA['name'] + " is allied with " + charB['name'] + "'s enemy " + person + ".")
                            totalVal += val
                    else:
                        for person in charBConflictingAllies:
                            motives.append(charB['name'] + " is allied with " + charA['name'] + "'s enemy " + person + ".")
                            totalVal += val
                    return totalVal

                # SUGGESTION SETUP =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-={}
                # Each section is as follows:
                # requirements for specific suggestion type (1 of any works)
                #   requirements for specific suggestion (either 1 of any or all depending on layout)
                #       priority bonus for suggestion
                #       Add suggestion
                #   ...
                # ...

                # Alliance Up setup ============================================================================================================================<>
                allianceUp = 0
                if (opinions[0] >= 40):
                    allianceUp += 2
                if (opinions[1] >= 60): # mildly romantically interested
                    allianceUp += 1
                if (opinions[2] >= 60): # thinks they're cool
                    allianceUp += 1
                allianceUp += hasTrait("cheerful",val=1)
                if hasTrait("overprotective",val=1) >= 1: # If A is overprotective, they will consider allUp less for every ally who has B as an enemy
                    allianceUp += alliedWithEnemy(val=-1)
                
                # Consider alliance Up suggestions
                if allianceUp > 0:
                    # Be Kind ------------------------------------------------------------------------>
                    # setup
                    volition = allianceUp
                    motives = []

                    # Determine whether to include suggestion
                    if (opinions[0] >= 80):
                        volition += 2
                        motives.append(charA['name'] + " is close friends with " + charB['name'])
                    volition += haveSharedAlly()

                    if volition > allianceUp:
                        # Determine further desire to include suggestion
                        if (opinions[2] >= 50):
                            volition += 10
                            motives.append(charA['name'] + " thinks " + charB['name'] + " is extraordinary.")
                        # Add suggestion
                        charASuggestions.append(suggestion("Increase Alliance", "Be Kind", volition=volition, motives=motives))
                    
                    # Bond Over Shared Interest ------------------------------------------------------------------------>
                    volition = allianceUp
                    motives = []

                    for item, value in sameSCK: # if share opinion on SCK
                        volition += 2
                        motives.append(charA['name'] + " and " + charB['name'] + " both " + value + " " + item + ".")
                    volition += haveSharedAlly()
                    volition += haveSharedEnemy()
                    
                    if volition > allianceUp:
                        for trait in charATraits:
                            if trait in classList and trait in charBTraits:
                                volition += 10
                                motives.append(charA['name'] + " and " + charB['name'] + " are the same class.")
                                break # can only have 1 class, so if you find it might as well stop
                        volition += haveSharedAlly()
                        volition += haveSharedEnemy()
                        charASuggestions.append(suggestion("Increase Alliance", "Bond Over Shared Interest", volition=volition, motives=motives))

                # Alliance Down setup ============================================================================================================================<>
                allianceDown = 0
                if (opinions[0] <= 60):
                    allianceDown += 2
                if (opinions[1] >= 60): # mildly romantically interested
                    allianceDown += 1
                if (opinions[2] <= 40): # thinks they're boring
                    allianceDown += 1
                allianceDown += hasTrait("aggressive",val=1)
                allianceDown += hasTrait("loyal",val=-1)
                allianceDown += alliedWithEnemy(val=1)

                if allianceDown > 0:
                    # Be Rude ------------------------------------------------------------------------>
                    volition = allianceDown
                    motives = []

                    if (opinions[0] <= 30):
                        volition += 2
                        motives.append(charA['name'] + " dislikes " + charB['name'])

                    if volition > allianceDown:
                        # Determine further desire to include suggestion
                        if (opinions[2] <= 50):
                            volition += 10
                            motives.append(charA['name'] + " thinks " + charB['name'] + " is boring.")
                        # Add suggestion
                        charASuggestions.append(suggestion("Decrease Alliance", "Be Rude", volition=volition, motives=motives))

                    # Argue Over Topic ------------------------------------------------------------------------>
                    volition = allianceDown
                    motives = []

                    for item, value in diffSCK: # if diff opinion on SCK
                        volition += 2
                        motives.append(charA['name'] + " and " + charB['name'] + " disagree on " + item + ".")
                    
                    if volition > allianceDown:
                        for trait in charATraits:
                            if trait in classList and not (trait in charBTraits):
                                volition += 10
                                motives.append(charA['name'] + " and " + charB['name'] + " are different classes.")
                                break # can only have 1 class, so if you find it might as well stop
                        charASuggestions.append(suggestion("Decrease Alliance", "Argue Over Topic", volition=volition, motives=motives))

                # Romance Up setup ============================================================================================================================<>
                romanceUp = 0
                if (opinions[1] >= 40):
                    romanceUp += 2
                if (opinions[0] >= 60): # on good terms
                    romanceUp += 1
                if (opinions[2] >= 60): # thinks they're cool
                    romanceUp += 1
                romanceUp = hasTrait("romantic",val=1)

                if romanceUp > 0:
                    # Flirt ------------------------------------------------------------------------>
                    # setup
                    volition = romanceUp
                    motives = []

                    # Determine whether to include suggestion
                    if (opinions[1] >= 80):
                        volition += 2
                        motives.append(charA['name'] + " is very romantically interested in " + charB['name'] + ".")

                    if volition > romanceUp:
                        # Determine further desire to include suggestion
                        if (opinions[2] >= 70):
                            volition += 10
                            motives.append(charA['name'] + " thinks " + charB['name'] + " is extraordinary.")
                        if "charming" in charBTraits:
                            volition += 5
                            motives.append(charB['name'] + " is charming.")
                        # Add suggestion
                        charASuggestions.append(suggestion("Increase Romance", "Flirt", volition=volition, motives=motives))
                
                # Romance Down setup ============================================================================================================================<>
                romanceDown = 0
                if (opinions[1] <= 60):
                    romanceDown += 2
                if (opinions[0] <= 40): # on bad terms
                    romanceDown += 1
                if (opinions[2] <= 40): # thinks they're boring
                    romanceDown += 1
                romanceDown = hasTrait("alcoholic",val=1) # character is drunk and makes bad decisions? bit odd but it works

                if romanceDown > 0:
                    # Disrespect ------------------------------------------------------------------------>
                    volition = romanceDown
                    motives = []

                    if (opinions[1] <= 30):
                        volition += 2
                        motives.append(charA['name'] + " wants nothing to do with " + charB['name'] + ".")

                    if volition > romanceDown:
                        if (opinions[2] <= 50):
                            volition += 10
                            motives.append(charA['name'] + " thinks " + charB['name'] + " is boring.")
                        if "charming" in charBTraits: #Negative effect on volition
                            volition -= 5
                            motives.append(charB['name'] + " is charming.")
                        # Add suggestion
                        charASuggestions.append(suggestion("Decrease Romance", "Disrespect", volition=volition, motives=motives))

                # Reverence Up setup ============================================================================================================================<>
                reverenceUp = 0
                if (opinions[2] >= 40):
                    reverenceUp += 2
                if (opinions[0] >= 60): # on good terms
                    reverenceUp += 1
                if (opinions[1] >= 60): # mildly romantically interested
                    reverenceUp += 1
                reverenceUp = hasTrait("cunning",val=1)

                if reverenceUp > 0:
                    # Brag ------------------------------------------------------------------------>
                    volition = reverenceUp
                    motives = []

                    # Determine whether to include suggestion
                    if (opinions[2] >= 80):
                        volition += 2
                        motives.append(charA['name'] + " thinks " + charB['name'] + " is extraordinary.")

                    if volition > reverenceUp:
                        # Determine further desire to include suggestion
                        if (opinions[1] >= 50):
                            volition += 10
                            motives.append(charA['name'] + " is romantically interested in " + charB['name'] + ".")
                        # Add suggestion
                        charASuggestions.append(suggestion("Increase Reverence", "Brag", volition=volition, motives=motives))

                # Reverence Down setup ============================================================================================================================<>
                reverenceDown = 0
                if (opinions[2] >= 60):
                    reverenceDown += 2
                if (opinions[0] <= 40): # on bad terms
                    reverenceDown += 1
                if (opinions[2] <= 40): # mildly romantically disinterested
                    reverenceDown += 1
                reverenceDown = hasTrait("secretive",val=1)

                if reverenceDown > 0:
                    # Weird Out ------------------------------------------------------------------------>
                    volition = reverenceDown
                    motives = []

                    # Determine whether to include suggestion
                    if (opinions[2] <= 30):
                        volition += 2
                        motives.append(charA['name'] + " thinks " + charB['name'] + " is boring.")
                    for item, value in diffSCK: # if diff opinion on SCK
                        volition += 1
                        motives.append(charA['name'] + " and " + charB['name'] + " disagree on " + item + ".")

                    if volition > reverenceDown:
                        # Determine further desire to include suggestion
                        if (opinions[1] <= 30):
                            volition += 10
                            motives.append(charA['name'] + " wants nothing to do with " + charB['name'] + ".")
                        # Add suggestion
                        charASuggestions.append(suggestion("Decrease Reverence", "Weird Out", volition=volition, motives=motives))

                # Become Allies setup ============================================================================================================================<>
                becomeAllies = 0
                if (opinions[0] > 80):
                    becomeAllies += 2

                if becomeAllies > 0 and not relationships[0]: # No reason to become allies with someone you're already allies with
                    # Befriend ------------------------------------------------------------------------>
                    volition = becomeAllies
                    motives = []

                    # Befriend has no requirements.
                    if True:
                        # Determine further desire to include suggestion
                        if (opinions[1] >= 50):
                            volition += 10
                            motives.append(charA['name'] + " is romantically interested in " + charB['name'] + ".")
                        # Add suggestion
                        charASuggestions.append(suggestion("Become Allies", "Befriend", volition=volition, motives=motives))

                # End Allies setup ============================================================================================================================<>
                endAllies = 0
                if (opinions[0] < 30):
                    endAllies += 2

                if endAllies > 0 and relationships[0]:
                    # Split up ------------------------------------------------------------------------>
                    volition = endAllies
                    motives = []

                    # Split Up has no requirements.
                    if True:
                        # Determine further desire to include suggestion
                        if (opinions[1] <= 30):
                            volition += 10
                            motives.append(charA['name'] + " wants nothing to do with " + charB['name'] + ".")
                        # Add suggestion
                        charASuggestions.append(suggestion("End Allies", "Split up", volition=volition, motives=motives))
                # Become Lovers setup ============================================================================================================================<>
                becomeLovers = 0
                if (opinions[1] > 80):
                    becomeLovers += 2
                becomeLovers = hasTrait("overly confident",val=1)

                if becomeLovers > 0 and not relationships[1] and not relationships[2]: # cant be lovers while enemies
                    # Ask Out ------------------------------------------------------------------------>
                    volition = becomeLovers
                    motives = []

                    # Ask Out has no requirements.
                    if True:
                        # Determine further desire to include suggestion
                        if (opinions[0] >= 50):
                            volition += 10
                            motives.append(charA['name'] + " is on good terms with " + charB['name'] + ".")
                        # Add suggestion
                        charASuggestions.append(suggestion("Become Lovers", "Ask Out", volition=volition, motives=motives))

                # End Lovers setup ============================================================================================================================<>
                endLovers = 0
                if (opinions[0] < 30):
                    endLovers += 2

                if endLovers > 0 and relationships[1]:
                    # Break up ------------------------------------------------------------------------>
                    volition = endLovers
                    motives = []

                    # Break Up has no requirements.
                    if True:
                        # Determine further desire to include suggestion
                        if (opinions[0] <= 30):
                            volition += 10
                            motives.append(charA['name'] + " is on bad terms with " + charB['name'] + ".")
                        # Add suggestion
                        charASuggestions.append(suggestion("End Lovers", "Break up", volition=volition, motives=motives))

                # Become Enemies setup ============================================================================================================================<>
                becomeEnemies = 0
                if (opinions[0] < 30):
                    becomeEnemies += 2

                if becomeEnemies > 0 and not relationships[2]:
                    # Start Feud ------------------------------------------------------------------------>
                    volition = becomeEnemies
                    motives = []

                    # Start Feud has no requirements.
                    if True:
                        # Determine further desire to include suggestion
                        if (opinions[1] <= 30):
                            volition += 10
                            motives.append(charA['name'] + " wants nothing to do with " + charB['name'] + ".")
                        # Add suggestion
                        charASuggestions.append(suggestion("Become Enemies", "Start Feud", volition=volition, motives=motives))

                # End Enemies setup ============================================================================================================================<>
                endEnemies = 0
                if (opinions[0] > 50):
                    endEnemies += 2

                if endEnemies > 0 and not relationships[2]:
                    # Make Peace ------------------------------------------------------------------------>
                    volition = endEnemies
                    motives = []

                    # Make Peace has no requirements.
                    if True:
                        # Determine further desire to include suggestion
                        if (opinions[1] >= 50):
                            volition += 10
                            motives.append(charA['name'] + " is romantically interested in " + charB['name'] + ".")
                        # Add suggestion
                        charASuggestions.append(suggestion("Become Enemies", "Make Peace", volition=volition, motives=motives))

                # ... after rest of setup
                # Order by volition, highest to lowest
                charASuggestions.sort(key=lambda sugg: sugg.volition, reverse=True)
                # Include only the top 5, if longer than 5
                if len(charASuggestions) > 5:
                    charASuggestions = charASuggestions[:5]
                # Input into suggestion dict
                suggestionStorage[charA['name']][charB['name']] = charASuggestions
                #print(charA['name'] + " to " + charB['name'] + ": " + str(len(charASuggestions)))

# Gets the result of a suggestion. Input is the suggestion object, the charA object, and the charB object
def GetSuggestionResult(suggestion, charAName, charBName):
    # Info pull
    # [alliance, love, reverence]
    opinionsB = social.social_engine.get_opinions(charAName, charBName)
    # [allies, lovers, enemies, partyMembers]
    relationships = social.social_engine.get_relationships(charAName, charBName)
    # {Traitname: true/false, ...}
    charATraits = social.social_engine.get_traits(charAName)
    charBTraits = social.social_engine.get_traits(charBName)
    # {SCKName: 'like'/'dislike'/etc ...}
    charASCK = social.social_engine.get_sck_opinions(charAName)
    charBSCK = social.social_engine.get_sck_opinions(charBName)
    # {SCKName: ??? ...}
    diffSCK = social.social_engine.compare_sck_opinions(charAName, charBName)
    sameSCK = social.social_engine.compare_sck_opinions_same(charAName, charBName)
    classList = ["Knight", "Healer", "Rogue", "Barbarian", "Mage"]

    
    # shared relationships
    sharedAllies = []
    sharedEnemies = []
    charAConflictingAllies = [] # Ally of A but enemy of B
    charBConflictingAllies = [] # Ally of B but enemy of A
    # Need the below for these relationships specifically.
    charA = None
    charB = None
    for person in social.social_engine.characters:
        if person['name'] == charAName:
            charA = person
            continue
        elif person['name'] == charBName:
            charB = person
            continue
        if charA != None and charB != None:
            break
    # charA and charB should always get assigned by the loop, any failures would have occured in "Info Pull" section
    # (also yeah the below is copy+paste of the equivalent section in suggestion setup. Would consider adding it to social but I don't want to cause merge conflicts so soon to the due date)
    for person in charA["relationships"]:
        for personB in charB["relationships"]:
            if person[0] == personB[0]: #each person is formatted as ("name", (ally,lover,enemy,partymember))
                if person[1][0] == personB[1][0]:
                    sharedAllies.append(person[0])
                if person[1][2] == personB[1][2]:
                    sharedEnemies.append(person[0])
                if person[1][0] == True and personB[1][2] == True: #A is allies but B is enemies
                    charAConflictingAllies.append(person[0])
                if person[1][2] == True and personB[1][0] == True: #A is allies but B is enemies
                    charBConflictingAllies.append(person[0])

    # Determines which outcome to run based off the type of suggestion chosen
    match suggestion.name:
        # Alliance Up ============================================================================================================================<>
        case "Be Kind":
            #Determine success score
            success = 1
            if "charming" in charATraits:
                success += 1
            if "aggressive" in charATraits:
                success -= 1
            success += 0.25 * len(sameSCK)
            success -= 0.125 * len(diffSCK)
            success += 0.5 * len(sharedAllies)
            success += ((50 - opinionsB[0]) / 50) # Every ally point above the midpoint = + 0.02 success. Every below is -0.02
            
            #Determine if succeed/failure, and results
            if success > 0:
                social.social_engine.update_opinion(charBName,charAName,10,0,0)
                social.social_engine.update_opinion(charAName,charBName,10,0,0)
            else:
                social.social_engine.update_opinion(charBName,charAName,-10,0,0)
        case "Bond Over Shared Interest":
            success = 0
            success += 2 * len(sameSCK) # agreement worth twice as much as disagreement
            for trait in charATraits:
                if trait in classList and trait in charBTraits:
                    success += 1
            success -= len(diffSCK)
            success += 0.5 * len(sharedAllies)
            success += max(0, (50 - opinionsB[0]) / 50) # potential negative effect of low current alliance is ignored here

            if success > 0:
                social.social_engine.update_opinion(charBName,charAName,15,0,0)
                social.social_engine.update_opinion(charAName,charBName,15,0,0)
            else:
                social.social_engine.update_opinion(charBName,charAName,-10,0,0)
        # Alliance Down ============================================================================================================================<>
        case "Be Rude":
            success = 1
            if "aggressive" in charATraits:
                success += 1
            if "charming" in charATraits:
                success -= 1
            success += 0.25 * len(diffSCK)
            success -= 0.125 * len(sameSCK)
            success += 0.25 * len(charAConflictingAllies)
            success += - ( (50 - opinionsB[0]) / 50) # inverted version of Be Kind
            
            if success > 0:
                social.social_engine.update_opinion(charBName,charAName,-10,0,0)
                social.social_engine.update_opinion(charAName,charBName,-10,0,0)
            else:
                # No result if failure here
                social.social_engine.update_opinion(charBName,charAName,0,0,0)
        case "Argue Over Topic":
            success = 0
            success += 2 * len(diffSCK) # agreement worth twice as much as disagreement
            for trait in charATraits:
                if trait in classList and not (trait in charBTraits):
                    success += 1
            success -= len(sameSCK)
            success += 0.25 * len(charAConflictingAllies)
            success += max(0, - ( (50 - opinionsB[0]) / 50))

            if success > 0:
                social.social_engine.update_opinion(charBName,charAName,-15,0,0)
                social.social_engine.update_opinion(charAName,charBName,-15,0,0)
            else:
                social.social_engine.update_opinion(charBName,charAName,10,0,0)
        # Romance Up ============================================================================================================================<>
        case "Flirt":
            #Determine success score
            success = 1
            if "charming" in charATraits:
                success += 1
            if "romantic" in charATraits:
                success += 1
            if "aggressive" in charATraits:
                success -= 1
            if "oblivious" in charBTraits:
                success -= 1
            success += 0.25 * len(sameSCK)
            success -= 0.125 * len(diffSCK)
            success += 0.5 * len(sharedAllies)
            success += 0.5 * max(0, (70 - opinionsB[0]) / 50) # give minor bonus if high alliance
            success += 0.5 * max(0, (70 - opinionsB[2]) / 50) # give minor bonus if high coolness
            success += (50 - opinionsB[1] / 50)
            
            #Determine if succeed/failure, and results
            if success > 0:
                social.social_engine.update_opinion(charBName,charAName,0,10,0)
                social.social_engine.update_opinion(charAName,charBName,0,10,0)
            else:
                social.social_engine.update_opinion(charBName,charAName,0,-10,0)
        # Romance Down ============================================================================================================================<>
        case "Disrespect":
            #Determine success score
            success = 1
            if "aggressive" in charATraits:
                success += 1
            if "charming" in charATraits:
                success -= 1
            if "oblivious" in charBTraits:
                success -= 1
            success += 0.25 * len(diffSCK)
            success -= 0.125 * len(sameSCK)
            success += 0.5 * max(0, - ( (30 - opinionsB[0]) / 50)) # if below 30 ally, give small bonus
            success += - (50 - opinionsB[1] / 50)
            
            #Determine if succeed/failure, and results
            if success > 0:
                social.social_engine.update_opinion(charBName,charAName,0,-10,0)
                social.social_engine.update_opinion(charAName,charBName,0,-10,0)
            else:
                social.social_engine.update_opinion(charBName,charAName,0,10,0)
        # Reverence Up ============================================================================================================================<>
        case "Brag":
            #Determine success score
            success = 1
            if "charming" in charATraits:
                success += 1
            if "clumsy" in charATraits:
                success -= 1
            success += 0.25 * len(sharedAllies)
            success += 0.25 * len(sameSCK) # brags about something related to the SCK(s)?
            success += 0.25 * ((50 - opinionsB[2]) / 50) # easier if B already thinks A is cool
            
            #Determine if succeed/failure, and results
            if success > 0:
                social.social_engine.update_opinion(charBName,charAName,0,0,10)
                social.social_engine.update_opinion(charAName,charBName,0,0,10)
            else:
                social.social_engine.update_opinion(charBName,charAName,0,0,-10)
        # Reverence Down ============================================================================================================================<>
        case "Weird Out":
            #Determine success score
            success = 1
            if "oddball" in charATraits:
                success += 1
            if "charming" in charATraits:
                success -= 1
            success += 0.25 * len(diffSCK)
            success += - 0.25 * ((50 - opinionsB[2]) / 50)
            
            #Determine if succeed/failure, and results
            if success > 0:
                social.social_engine.update_opinion(charBName,charAName,0,0,10)
                social.social_engine.update_opinion(charAName,charBName,0,0,10)
            else:
                social.social_engine.update_opinion(charBName,charAName,0,0,-10)
        # Become Allies ============================================================================================================================<>
        case "Befriend":
            #Determine success score
            success = 1
            if "charming" in charATraits:
                success += 1
            if "aggressive" in charATraits:
                success -= 1
            success += 0.5 * len(sharedAllies)
            success += 2 * ((50 - opinionsB[0]) / 50)
            
            #Determine if succeed/failure, and results
            if success > 0: # Become friends, and end current enemies if have one
                social.social_engine.update_relationship_name(charBName,charAName,[True] + relationships[1] + [False] + relationships[3:])
                social.social_engine.update_relationship_name(charAName,charBName,[True] + relationships[1] + [False] + relationships[3:])
            else:
                social.social_engine.update_relationship_name(charBName,charAName,[False] + relationships[1:])
                social.social_engine.update_relationship_name(charAName,charBName,[False] + relationships[1:])
        # End Allies ============================================================================================================================<>
        case "Split up":
            #Determine success score
            success = 1
            if "aggressive" in charATraits:
                success += 1
            if "charming" in charATraits:
                success -= 1
            success += 0.5 * len(sharedAllies)
            success += 2 * ((50 - opinionsB[0]) / 50)
            
            #Determine if succeed/failure, and results
            if success > 0:
                social.social_engine.update_relationship_name(charBName,charAName,[False] + relationships[1:])
                social.social_engine.update_relationship_name(charAName,charBName,[False] + relationships[1:])
            else:
                social.social_engine.update_relationship_name(charBName,charAName,[True] + relationships[1:])
                social.social_engine.update_relationship_name(charAName,charBName,[True] + relationships[1:])
        # Become Lovers ============================================================================================================================<>
        case "Ask Out":
            #Determine success score
            success = 1
            if "charming" in charATraits:
                success += 1
            if "romantic" in charATraits:
                success += 1
            if "aggressive" in charATraits:
                success -= 1
            success += 0.5 * len(sharedAllies)
            success += 2 * ((50 - opinionsB[1]) / 50)
            success += 0.5 * ((50 - opinionsB[2]) / 50) # How cool A seems to B slightly affects the odds
            
            #Determine if succeed/failure, and results
            if success > 0:
                social.social_engine.update_relationship_name(charBName,charAName,relationships[:1] + [True] + relationships[2:])
                social.social_engine.update_relationship_name(charAName,charBName,relationships[:1] + [True] + relationships[2:])
            else:
                social.social_engine.update_relationship_name(charBName,charAName,relationships[:1] + [False] + relationships[2:])
                social.social_engine.update_relationship_name(charAName,charBName,relationships[:1] + [False] + relationships[2:])
        # End Lovers ============================================================================================================================<>
        case "Break Up":
            #Determine success score
            success = 1
            if "aggressive" in charATraits:
                success += 1
            if "charming" in charATraits:
                success -= 1
            if "romantic" in charATraits:
                success -= 1
            success += - 2 * ((50 - opinionsB[1]) / 50)
            success += - 0.5 * ((50 - opinionsB[2]) / 50)
            
            #Determine if succeed/failure, and results
            if success > 0:
                social.social_engine.update_relationship_name(charBName,charAName,relationships[:1] + [False] + relationships[2:])
                social.social_engine.update_relationship_name(charAName,charBName,relationships[:1] + [False] + relationships[2:])
            else:
                social.social_engine.update_relationship_name(charBName,charAName,relationships[:1] + [True] + relationships[2:])
                social.social_engine.update_relationship_name(charAName,charBName,relationships[:1] + [True] + relationships[2:])
        # Become Enemies ============================================================================================================================<>
        case "Start Feud":
            #Determine success score
            success = 1
            if "aggressive" in charATraits:
                success += 1
            if "charming" in charATraits:
                success -= 1
            success += 0.5 * (len(charAConflictingAllies) + len(charBConflictingAllies))
            success += - 2 * ((50 - opinionsB[0]) / 50)
            
            #Determine if succeed/failure, and results
            if success > 0: # Become enemies, and end current alliance + lover if True
                social.social_engine.update_relationship_name(charBName,charAName,[False, False, True] + relationships[3:])
                social.social_engine.update_relationship_name(charAName,charBName,[False, False, True] + relationships[3:])
            else:
                social.social_engine.update_relationship_name(charBName,charAName,relationships[:2] + [False] + relationships[3:])
                social.social_engine.update_relationship_name(charAName,charBName,relationships[:2] + [False] + relationships[3:])
        # End Enemies ============================================================================================================================<>
        case "Make Peace":
            #Determine success score
            success = 1
            if "charming" in charATraits:
                success += 1
            if "aggressive" in charATraits:
                success -= 1
            success += - 0.25 * (len(charAConflictingAllies) + len(charBConflictingAllies))
            success += 2 * ((50 - opinionsB[0]) / 50)
            
            #Determine if succeed/failure, and results
            if success > 0:
                social.social_engine.update_relationship_name(charBName,charAName,relationships[:2] + [False] + relationships[3:])
                social.social_engine.update_relationship_name(charAName,charBName,relationships[:2] + [False] + relationships[3:])
            else:
                social.social_engine.update_relationship_name(charBName,charAName,relationships[:2] + [True] + relationships[3:])
                social.social_engine.update_relationship_name(charAName,charBName,relationships[:2] + [True] + relationships[3:])