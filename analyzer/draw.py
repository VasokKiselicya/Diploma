# import networkx as nx
# from networkx.drawing.nx_agraph import graphviz_layout
# import matplotlib.pyplot as plt
# G = nx.DiGraph()
#
# G.add_node("ROOT")
#
# for i in range(5):
#     G.add_node("Child_%i" % i)
#     G.add_node("Grandchild_%i" % i)
#     G.add_node("Greatgrandchild_%i" % i)
#
#     G.add_edge("ROOT", "Child_%i" % i)
#     G.add_edge("Child_%i" % i, "Grandchild_%i" % i)
#     G.add_edge("Grandchild_%i" % i, "Greatgrandchild_%i" % i)
#
# # write dot file to use with graphviz
# # run "dot -Tpng test.dot >test.png"
# nx.nx_agraph.write_dot(G,'test.dot')
# if __name__ == '__main__':
#
#     # same layout using matplotlib with no labels
#     plt.title('draw_networkx')
#     pos=graphviz_layout(G, prog='dot')
#     nx.draw(G, pos, with_labels=False, arrows=False)
#     plt.savefig('nx_test.png')


import matplotlib.pyplot as plt
import networkx as nx
import random
from analyzer.core import get_grammar_tree


def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.
    Licensed under Creative Commons Attribution-Share Alike

    If the graph is a tree this will return the positions to plot this in a
    hierarchical layout.

    G: the graph (must be a tree)

    root: the root node of current branch
    - if the tree is directed and this is not given,
      the root will be found and used
    - if the tree is directed and this is given, then
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given,
      then a random choice will be used.

    width: horizontal space allocated for this branch - avoids overlap with other branches

    vert_gap: gap between levels of hierarchy

    vert_loc: vertical location of root

    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  # allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0., xcenter=0.5, pos=None, parent=None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''

        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                     vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                     pos=pos, parent=root)
        return pos

    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


def descendants(t):
    nodes = [t]
    for i in range(0, t.getChildCount()):
        nodes.extend(descendants(t.getChild(i)))
    return nodes


def child_pairs(t, result=[]):
    children = list(Trees.getChildren(t))
    result.extend([(t, c) for c in children])
    for tc in children:
        child_pairs(tc, result)
    return result


def build_tree(cls, t, recog, result=[]):
    s = escapeWhitespace(cls.getNodeText(t, recog.ruleNames), False)

    if t.getChildCount() == 0:
        return s

    result.append(s)
    res = []
    for i in range(0, t.getChildCount()):
        if i > 0:
            res.append(build_tree(cls, t.getChild(i), recog, result[-1]))
    result.append(res)

    return result


if __name__ == '__main__':
    tree, parser = get_grammar_tree(file_path="D:\Study\Diploma\\test_save.sol")

    from antlr4.tree.Trees import Trees
    from antlr4.Utils import escapeWhitespace

    # from analyzer.solParser import solParser

    results = []
    test_tree = list(Trees.getChildren(tree))[6:7][0]
    builded = build_tree(Trees, test_tree, parser)
    print(builded)

    for line in list(Trees.getChildren(tree))[6:7]:
        res = child_pairs(line)
        res_pairs = [('program', 'line')]
        for r in res:
            if escapeWhitespace(Trees.getNodeText(r[1], None, recog=parser), False) == '\\r\\n':
                continue

            parent = escapeWhitespace(Trees.getNodeText(r[0], None, recog=parser), False)
            child = escapeWhitespace(Trees.getNodeText(r[1], None, recog=parser), False)

            print(parent, str(r[0]))
            print(child, str(r[1]))

            if parent in ('positive_number', 'row_of_numbers', 'natural_number'):
                continue

            res_pairs.append((parent, child))

        results.append(res_pairs)

    # for r in results:
    #     print(r)

    G = nx.Graph()
    G.add_edges_from(results[0])
    # print(dict(G.adjacency()) or "TEXT")
    pos = hierarchy_pos(G, 'program')
    nx.draw(G, pos=pos, with_labels=True)
    plt.show()
