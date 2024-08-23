import xml.etree.ElementTree as ET

def load_characters_from_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    character_names = [character_elem.get('name') for character_elem in root.findall('Character')]

    characters = []
    for character_elem in root.findall('Character'):
        character_name = character_elem.get('name')

        character = {
            'name': character_name,
            'traits': {},
            'social_history': [],
            'relationships': [], #This is for building the relationship matrix from XML given values
            'SCK': [], #Builds cultural_opinion matrix
        }

        # Load traits
        for trait_elem in character_elem.find('Traits').findall('Trait'):
            trait_name = trait_elem.get('name')
            trait_value = bool(trait_elem.get('value'))
            character['traits'][trait_name] = trait_value

        # Load social history
        for history_elem in character_elem.find('SocialHistory').findall('History'):
            target_name = history_elem.get('name')
            alliance = float(history_elem.get('alliance', '0.0'))
            romance = float(history_elem.get('romance', '0.0'))
            reverence = float(history_elem.get('reverence', '0.0'))
            character['social_history'].append((target_name, (alliance, romance, reverence)))
        # Get those relationships, baby
        for relationship_elem in character_elem.find('Relationships').findall('Relationship'):
            target_name = relationship_elem.get('name')
            friends = relationship_elem.get('friends') == 'true'
            couples = relationship_elem.get('dating') == 'true'
            enemies = relationship_elem.get('enemies') == 'true'
            teammates = relationship_elem.get('party_member') == 'true'
            character['relationships'].append((target_name, (friends, couples, enemies, teammates)))
        # How do we feel about stuff?
        for knowledge_elem in character_elem.find('SCK').findall('Knowledge'):
            sck_elem = character_elem.find('SCK')
            if sck_elem is not None:
                target_name = knowledge_elem.get('name')
                feeling = knowledge_elem.get('opinion')
                character['SCK'].append((target_name, feeling))

        characters.append(character)

    return characters

def load_sck_from_xml(filename, social_engine):
    """
    Load shared cultural knowledge from an XML file and populate the SCK matrix in the Social class.
    Called from within __init__ of Social class.
    Args:
        filename (str): Path to the XML file.
        social_engine (Social): The Social class instance to populate with SCK data.
    """
    tree = ET.parse(filename)
    root = tree.getroot()
    
    for knowledge in root.findall('Knowledge'):
        name = knowledge.get('name')
        opinion = knowledge.get('opinion')
        print(opinion)
        social_engine.shared_cultural_matrix[name] = opinion