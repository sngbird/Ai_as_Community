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
                sameSCK = social.social_engine.compare_sck_opinions_same(charA['name'], charB['name'])
                classList = ["Knight", "Healer", "Rogue", "Barbarian", "Mage"]

                #def hasOpinion(motiveList, opinion=0, opinionValue=50, greaterThan=True, volition=10)

                # Alliance Up setup ============================================================================================================================<>
                allianceUp = 0
                if (opinions[0] >= 50):
                    allianceUp += 2
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
                    
                    if volition > allianceUp:
                        for trait in charATraits:
                            if trait in classList and trait in charBTraits:
                                volition += 10
                                motives.append(charA['name'] + " and " + charB['name'] + " are the same class.")
                                break # can only have 1 class, so if you find it might as well stop
                        charASuggestions.append(suggestion("Increase Alliance", "Bond Over Shared Interest", volition=volition, motives=motives))

                # Alliance Down setup ============================================================================================================================<>
                allianceDown = 0
                if (opinions[0] <= 50):
                    allianceDown += 2

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
                if (opinions[1] >= 50):
                    romanceUp += 2

                if romanceUp > 0:
                    # Flirt ------------------------------------------------------------------------>
                    # setup
                    volition = romanceUp
                    motives = []

                    # Determine whether to include suggestion
                    if (opinions[1] >= 80):
                        volition += 2
                        motives.append(charA['name'] + " is very romantically interested in " + charB['name'] + ".")

                    if volition > allianceUp:
                        # Determine further desire to include suggestion
                        if (opinions[2] >= 50):
                            volition += 10
                            motives.append(charA['name'] + " thinks " + charB['name'] + " is extraordinary.")
                        if "charming" in charBTraits:
                            volition += 5
                            motives.append(charB['name'] + " is charming.")
                        # Add suggestion
                        charASuggestions.append(suggestion("Increase Romance", "Flirt", volition=volition, motives=motives))
                
                # Romance Down setup ============================================================================================================================<>
                romanceDown = 0
                if (opinions[1] <= 50):
                    romanceDown += 2

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
                if (opinions[2] >= 50):
                    reverenceUp += 2

                if reverenceUp > 0:
                    # Brag ------------------------------------------------------------------------>
                    volition = reverenceUp
                    motives = []

                    # Determine whether to include suggestion
                    if (opinions[2] >= 80):
                        volition += 2
                        motives.append(charA['name'] + " thinks " + charB['name'] + " is extraordinary.")

                    if volition > allianceUp:
                        # Determine further desire to include suggestion
                        if (opinions[1] >= 50):
                            volition += 10
                            motives.append(charA['name'] + " is romantically interested in " + charB['name'] + ".")
                        # Add suggestion
                        charASuggestions.append(suggestion("Increase Reverence", "Brag", volition=volition, motives=motives))

                # Reverence Down setup ============================================================================================================================<>
                reverenceDown = 0
                if (opinions[2] >= 50):
                    reverenceDown += 2

                if reverenceDown > 0:
                    # Weird Out ------------------------------------------------------------------------>
                    volition = reverenceDown
                    motives = []

                    # Determine whether to include suggestion
                    if (opinions[2] <= 30):
                        volition += 2
                        motives.append(charA['name'] + " thinks " + charB['name'] + " is boring.")

                    if volition > allianceUp:
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

                if becomeLovers > 0 and not relationships[1]:
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
            charASuggestions[:5]
        # Input into suggestion dict
        suggestionStorage[charA['name']][charB['name']] = charASuggestions

# Gets the result of a suggestion. Input is the suggestion object, the charA object, and the charB object
def GetSuggestionResult(suggestion, charA, charB):
    # Info pull
    # [alliance, love, reverence]
    opinions = social.social_engine.get_opinions(charA['name'], charB['name'])
    # [allies, lovers, enemies, partyMembers]
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

    # Determines which outcome to run based off the type of suggestion chosen
    match suggestion.name:
        # Alliance Up ============================================================================================================================<>
        case "Be Kind":
            #Determine success score
            success = 1
            if "charming" in charATraits:
                success += 1
            if "agressive" in charATraits:
                success -= 1
            
            #Determine if succeed/failure, and results
            if success > 0:
                social.social_engine.update_opinion(charB['name'],charA['name'],10,0,0)
                social.social_engine.update_opinion(charA['name'],charB['name'],10,0,0)
            else:
                social.social_engine.update_opinion(charB['name'],charA['name'],-10,0,0)
        case "Bond Over Shared Interest":
            success = 0
            success += 2 * len(sameSCK) # agreement worth twice as much as disagreement
            for trait in charATraits:
                if trait in classList and trait in charBTraits:
                    success += 1
            success -= len(diffSCK)

            if success > 0:
                social.social_engine.update_opinion(charB['name'],charA['name'],15,0,0)
                social.social_engine.update_opinion(charA['name'],charB['name'],15,0,0)
            else:
                social.social_engine.update_opinion(charB['name'],charA['name'],-10,0,0)
        # Alliance Down ============================================================================================================================<>
        case "Be Rude":
            success = 1
            if "agressive" in charATraits:
                success += 1
            if "charming" in charATraits:
                success -= 1
            
            if success > 0:
                social.social_engine.update_opinion(charB['name'],charA['name'],-10,0,0)
                social.social_engine.update_opinion(charA['name'],charB['name'],-10,0,0)
            else:
                # No result if failure here
                social.social_engine.update_opinion(charB['name'],charA['name'],0,0,0)
        case "Argue Over Topic":
            success = 0
            success += 2 * len(diffSCK) # agreement worth twice as much as disagreement
            for trait in charATraits:
                if trait in classList and not (trait in charBTraits):
                    success += 1
            success -= len(sameSCK)

            if success > 0:
                social.social_engine.update_opinion(charB['name'],charA['name'],-15,0,0)
                social.social_engine.update_opinion(charA['name'],charB['name'],-15,0,0)
            else:
                social.social_engine.update_opinion(charB['name'],charA['name'],10,0,0)
        # Romance Up ============================================================================================================================<>
        case "Flirt":
            #Determine success score
            success = 1
            if "charming" in charATraits:
                success += 1
            if "romantic" in charATraits:
                success += 1
            if "agressive" in charATraits:
                success -= 1
            
            #Determine if succeed/failure, and results
            if success > 0:
                social.social_engine.update_opinion(charB['name'],charA['name'],0,10,0)
                social.social_engine.update_opinion(charA['name'],charB['name'],0,10,0)
            else:
                social.social_engine.update_opinion(charB['name'],charA['name'],0,-10,0)
        # Romance Down ============================================================================================================================<>
        case "Disrespect":
            #Determine success score
            success = 1
            if "agressive" in charATraits:
                success += 1
            if "charming" in charATraits:
                success -= 1
            
            #Determine if succeed/failure, and results
            if success > 0:
                social.social_engine.update_opinion(charB['name'],charA['name'],0,-10,0)
                social.social_engine.update_opinion(charA['name'],charB['name'],0,-10,0)
            else:
                social.social_engine.update_opinion(charB['name'],charA['name'],0,10,0)
        # Reverence Up ============================================================================================================================<>
        case "Brag":
            #Determine success score
            success = 1
            if "charming" in charATraits:
                success += 1
            if "clumsy" in charATraits:
                success -= 1
            
            #Determine if succeed/failure, and results
            if success > 0:
                social.social_engine.update_opinion(charB['name'],charA['name'],0,0,10)
                social.social_engine.update_opinion(charA['name'],charB['name'],0,0,10)
            else:
                social.social_engine.update_opinion(charB['name'],charA['name'],0,0,-10)
        # Reverence Down ============================================================================================================================<>
        case "Weird Out":
            #Determine success score
            success = 1
            if "oddball" in charATraits:
                success += 1
            if "charming" in charATraits:
                success -= 1
            
            #Determine if succeed/failure, and results
            if success > 0:
                social.social_engine.update_opinion(charB['name'],charA['name'],0,0,10)
                social.social_engine.update_opinion(charA['name'],charB['name'],0,0,10)
            else:
                social.social_engine.update_opinion(charB['name'],charA['name'],0,0,-10)
        # Become Allies ============================================================================================================================<>
        case "Befriend":
            #Determine success score
            success = 1
            if "charming" in charATraits:
                success += 1
            if "aggressive" in charATraits:
                success -= 1
            
            #Determine if succeed/failure, and results
            if success > 0:
                social.social_engine.update_relationship(charB['name'],charA['name'],[True] + relationships[1:])
                social.social_engine.update_relationship(charA['name'],charB['name'],[True] + relationships[1:])
            else:
                social.social_engine.update_relationship(charB['name'],charA['name'],[False] + relationships[1:])
                social.social_engine.update_relationship(charA['name'],charB['name'],[False] + relationships[1:])
        # End Allies ============================================================================================================================<>
        case "Split up":
            #Determine success score
            success = 1
            if "aggressive" in charATraits:
                success += 1
            if "charming" in charATraits:
                success -= 1
            
            #Determine if succeed/failure, and results
            if success > 0:
                social.social_engine.update_relationship(charB['name'],charA['name'],[False] + relationships[1:])
                social.social_engine.update_relationship(charA['name'],charB['name'],[False] + relationships[1:])
            else:
                social.social_engine.update_relationship(charB['name'],charA['name'],[True] + relationships[1:])
                social.social_engine.update_relationship(charA['name'],charB['name'],[True] + relationships[1:])
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
            
            #Determine if succeed/failure, and results
            if success > 0:
                social.social_engine.update_relationship(charB['name'],charA['name'],relationships[:1] + [True] + relationships[2:])
                social.social_engine.update_relationship(charA['name'],charB['name'],relationships[:1] + [True] + relationships[2:])
            else:
                social.social_engine.update_relationship(charB['name'],charA['name'],relationships[:1] + [False] + relationships[2:])
                social.social_engine.update_relationship(charA['name'],charB['name'],relationships[:1] + [False] + relationships[2:])
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
            
            #Determine if succeed/failure, and results
            if success > 0:
                social.social_engine.update_relationship(charB['name'],charA['name'],relationships[:1] + [False] + relationships[2:])
                social.social_engine.update_relationship(charA['name'],charB['name'],relationships[:1] + [False] + relationships[2:])
            else:
                social.social_engine.update_relationship(charB['name'],charA['name'],relationships[:1] + [True] + relationships[2:])
                social.social_engine.update_relationship(charA['name'],charB['name'],relationships[:1] + [True] + relationships[2:])
        # Become Enemies ============================================================================================================================<>
        case "Start Feud":
            #Determine success score
            success = 1
            if "aggressive" in charATraits:
                success += 1
            if "charming" in charATraits:
                success -= 1
            
            #Determine if succeed/failure, and results
            if success > 0:
                social.social_engine.update_relationship(charB['name'],charA['name'],relationships[:2] + [True] + relationships[3:])
                social.social_engine.update_relationship(charA['name'],charB['name'],relationships[:2] + [True] + relationships[3:])
            else:
                social.social_engine.update_relationship(charB['name'],charA['name'],relationships[:2] + [False] + relationships[3:])
                social.social_engine.update_relationship(charA['name'],charB['name'],relationships[:2] + [False] + relationships[3:])
        # End Enemies ============================================================================================================================<>
        case "Make Peace":
            #Determine success score
            success = 1
            if "charming" in charATraits:
                success += 1
            if "aggressive" in charATraits:
                success -= 1
            
            #Determine if succeed/failure, and results
            if success > 0:
                social.social_engine.update_relationship(charB['name'],charA['name'],relationships[:2] + [False] + relationships[3:])
                social.social_engine.update_relationship(charA['name'],charB['name'],relationships[:2] + [False] + relationships[3:])
            else:
                social.social_engine.update_relationship(charB['name'],charA['name'],relationships[:2] + [True] + relationships[3:])
                social.social_engine.update_relationship(charA['name'],charB['name'],relationships[:2] + [True] + relationships[3:])