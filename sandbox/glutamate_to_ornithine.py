# import networkx as nx
# import matplotlib.pyplot as plt

#Wire information
    # Connect the .at() and .to() positions with lines depending on shape
    # Parameters:
    # shape – Determines shape of wire: 
    #     -: straight line 
    #     |-: right-angle line starting vertically 
    #     -|: right-angle line starting horizontally 
    #     ‘z’: diagonal line with horizontal end segments 
    #     ‘N’: diagonal line with vertical end segments 
    #     n: n- or u-shaped lines 
    #     c: c- or ↄ-shaped lines
    # k – Distance before the wire changes directions in n and c shapes.
    # arrow – arrowhead specifier, such as ‘->’, ‘<-’, ‘<->’, or ‘-o’


import schemdraw
from schemdraw import flow

# Set default flowchart box fill colors
flow.Box.defaults['fill'] = '#eeffff'
flow.Start.defaults['fill'] = '#ffeeee'
flow.Decision.defaults['fill'] = '#ffffee'

flow.Box.defaults['fill'] = '#eeffff'
flow.Start.defaults['fill'] = '#ffeeee'
flow.Decision.defaults['fill'] = '#ffffee'

with schemdraw.Drawing() as d:
    d.config(fontsize=11)
    # d5 = flow.Decision(w=5, h=3.6, E='YES', S='NO').label('BUT YOU\nJUST FOLLOWED\nTHEM TWICE!')
    # flow.Arrow().right().at(d5.E)
    # question = flow.Box(w=3.5, h=1.75).anchor('W').label("(THAT WASN'T\nA QUESTION.)")
    
    # flow.Wire(shape='n', k=1, arrow='->').at(d5.N).to(question.N)


    # d1 = flow.RoundBox().label('Glutamate').at((0, 0))
    # a1 = flow.Arrow().right().at(d1.E)
    # d2 = flow.Box().label('2.3.1.1').at(a1.end).anchor('W')
    # a2 = flow.Arrow().down().at(d1.S)
    # d3 = flow.Box().label('6.3.2.60').at(a2.end).anchor('N')

    gene_height = 2
    meta_height = 2


    d1 = flow.RoundBox(h=meta_height).label('Glutamate').at((0, 0))             #glutamate
    a1 = flow.Wire(shape='-', arrow='->').at(d1.E).to((d1.E[0]+2, d1.E[1]))     #arrow glutamate to 2.3.1.1
    d2 = flow.Box(h=gene_height).label('2.3.1.1 hello world!').at(a1.end).anchor('W')   #2.3.1.1
    a2 = flow.Wire(shape='|-', k=1, arrow='->').at(d1.S).to((d2.W[0], d2.W[1]-3))   #arrow glutamate to 6.3.2.60, anchor 3 units below 2.3.1.1
    d3 = flow.Box(h=gene_height).label('ArgX\n6.3.2.60')                        #6.3.2.60
    a3 = flow.Wire(shape='-', arrow='->').at(d2.E).to((d2.E[0]+2, d2.E[1]))     #arrow 2.3.1.1 to N-Acetyl-glutamate
    d4 = flow.RoundBox(h=meta_height).label('N-Acetyl-glutamate').at(a3.end).anchor('W') # N-Acetyl-glutamate
    a4 = flow.Wire(shape='-', arrow='->').at(d3.E).to((d4.W[0], d3.E[1]))     #arrow 6.3.2.60 to LysW-glutamate
    d5 = flow.RoundBox(h=meta_height).label('LysW-glutamate').at(a4.end).anchor('W') # LysW-glutamate
    a5 = flow.Wire(shape='-', arrow='->').at(d4.E).to((d4.E[0]+2, d4.E[1]))     #arrow N-Acetyl-glutamate to 2.7.2.8
    d6 = flow.Box(h=gene_height).label('2.7.2.8').at(a5.end).anchor('W')   #2.7.2.8
    
    

    
