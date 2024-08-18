def load_characters_from_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    characters = []

    for character_elem in root.findall('Character'):
        character = {
            'name': character_elem.get('name'),
            'traits': {},
            'social_history': [],
            'relationships': [],
            'opinions': [],
        }

        # Load traits
        for trait_elem in character_elem.find('Traits').findall('Trait'):
            trait_name = trait_elem.get('name')
            trait_value = int(trait_elem.get('value'))
            character['traits'][trait_name] = trait_value

        # Load social history
        for history_elem in character_elem.find('SocialHistory').findall('History'):
            history_name = history_elem.get('name')
            history_value = int(history_elem.get('value'))
            character['social_history'].append((history_name, history_value))

        # Load relationships
        for relationship_elem in character_elem.find('Relationships').findall('Relationship'):
            relationship_name = relationship_elem.get('name')
            relationship_values = [
                relationship_elem.get('friends') == 'true',
                relationship_elem.get('dating') == 'true',
                relationship_elem.get('enemies') == 'true',
                relationship_elem.get('party_member') == 'true',
            ]
            character['relationships'].append((relationship_name, relationship_values))

        # Load opinions
        for opinion_elem in character_elem.find('Opinions').findall('Opinion'):
            opinion_name = opinion_elem.get('name')
            alliance = float(opinion_elem.get('alliance', '0.0'))
            romance = float(opinion_elem.get('romance', '0.0'))
            reverence = float(opinion_elem.get('reverence', '0.0'))
            character['opinions'].append((opinion_name, (alliance, romance, reverence)))

        characters.append(character)

    return characters