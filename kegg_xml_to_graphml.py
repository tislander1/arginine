import xml.etree.ElementTree as ET
import re
import networkx as nx

def get_reactions(root):
    # get all <reaction> elements
    reactions = []
    for reaction in root.findall('.//reaction'):
        reaction_id = reaction.get('id')
        name = reaction.get('name')
        type = reaction.get('type')
        substrates = []
        products = []
        for substrate in reaction.findall('./substrate'):
            substrates.append(substrate.get('id'))
        for product in reaction.findall('./product'):
            products.append(product.get('id'))
        reactions.append({
            'id': reaction_id,
            'name': name,
            'type': type,
            'substrates': substrates,
            'products': products
        })
    return reactions

def get_compounds(root):
    # get all <entry> elements with type="compound"
    compounds = {}
    for entry in root.findall('.//entry[@type="compound"]'):
        compound_id = entry.get('id')
        name = entry.get('name')
        compounds[compound_id] = name
    return compounds

def get_orthology(root):
    # get all <entry> elements with type="ortholog".  For each one, get the reaction and name attributes.  Store them in a dictionary with the reaction as the key and the name as the value
    orthology = {}
    for entry in root.findall('.//entry[@type="ortholog"]'):
        reaction = entry.get('reaction')
        name = entry.get('name').replace('ko:', '')
        name = name.split(' ')
        if reaction and name:
            orthology[reaction] = name
    return orthology

if __name__ == '__main__':
    kegg_xml_file = 'kegg_xml_and_images/ko00220.xml'
    graphml_file = kegg_xml_file.replace('.xml', '.graphml')

    tree = ET.parse(kegg_xml_file)
    root = tree.getroot()

    reactions = get_reactions(root)
    compounds = get_compounds(root)
    orthology = get_orthology(root)
    # add compounds to the reactions
    x = 2

    