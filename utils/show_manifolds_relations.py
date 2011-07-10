import pydot, os
from geometry import all_manifolds

from pydot import Node, Edge

def embedding_type2color(t):
    t2color = {   'lie': 'blue',
                  'user': 'green',
                  'derived': 'darkgreen'}
    if not t in t2color:

        print('Warning, unknown type %s' % t)
        color = 'yellow'
    else:
        color = t2color[t]
    return color

def isomorphism_type2color(t):
    t2color = {'lie': 'blue',
                  'user': 'red',
                  'derived': 'darkred'}
    if not t in t2color:
        print('Warning, unknown type %s' % t)
        color = 'yellow'
    else:
        color = t2color[t]
    return color
            
def main():
    g = pydot.Dot('manifolds', graph_type='digraph') 
    
    only_direct = True
    
    for m in all_manifolds:
        g.add_node(Node(str(m), rank=m.dimension))
        
    for m in all_manifolds:
        for m2, rel in m._embedding.items():
            
            steps = rel.steps
            direct = len(steps) == 1
            
            if only_direct and not direct: continue
            
            color = embedding_type2color(rel.type)
            g.add_edge(Edge(Node(str(m)), Node(str(m2)), color=color))

        for m2, rel in m._isomorphisms.items():
            
            steps = rel.steps
            direct = len(steps) == 1
            
            color = isomorphism_type2color(rel.type)
            if only_direct and not direct: continue
                
            if id(m) < id(m2):
                g.add_edge(Edge(Node(str(m)), Node(str(m2)), color=color,
                            undirected=True, dir='none'))
                #g.add_edge(Edge(Node(str(m)), Node(str(m2)), color='red'))

                
    out = 'manifolds.dot'
    print('Writing to %r' % out)
    g.write(out)
    cmd = 'dot manifolds.dot -T png -o manifolds.png'
    print('$ %s' % cmd)
    os.system(cmd)
    
if __name__ == '__main__':
    main() 
