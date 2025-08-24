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
        compounds[compound_id] = name.replace('cpd:', '')
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

def get_graphml(graphml_file, reactions, compounds, orthology):
    # make a directed graph
    G = nx.DiGraph()
    for reaction in reactions:
        reaction_id = reaction['id']
        reaction_name = reaction['name']
        reaction_type = reaction['type']
        substrates = reaction['substrates']
        products = reaction['products']

        ko = sorted(orthology.get(reaction_id, []))
        
        # add the reaction as a node
        G.add_node(reaction_id, type='reaction', name=reaction_name, reaction_type=reaction_type, ko=str(ko))
        
        # add the substrates as nodes and connect them to the reaction
        for substrate in substrates:
            substrate_name = compounds.get(substrate, substrate)
            G.add_node(substrate, type='compound', name=substrate_name, color ='#FFAAAA')
            G.add_edge(substrate, reaction_id)
        
        # add the products as nodes and connect them to the reaction
        for product in products:
            product_name = compounds.get(product, product)
            G.add_node(product, type='compound', name=product_name, color ='#AAFFAA')
            G.add_edge(reaction_id, product)
    return G


if __name__ == '__main__':
    kegg_xml_file = 'kegg_xml_and_images/ko00220.xml'
    graphml_file = kegg_xml_file.replace('.xml', '.graphml')

    tree = ET.parse(kegg_xml_file)
    root = tree.getroot()

    reactions = get_reactions(root)
    compounds = get_compounds(root)
    orthology = get_orthology(root)

    G = get_graphml(graphml_file, reactions, compounds, orthology)
    # add compounds to the reactions
    
    # save the graph to a graphml file
    nx.write_graphml(G, graphml_file)
    print(f"Graph saved to {graphml_file}")

    