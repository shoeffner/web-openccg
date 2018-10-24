import pygraphviz as pgv


def create_graph(key, parse):
    G = pgv.AGraph()
    G.graph_attr['label'] = key
    G.add_edge('b', 'c')
    return G.string()


def create_graphs(json_parses):
    """Creates graphs for each json_parse.

    Args:
        json_parses: A dictionary of keys to json_parses as provided from
                     tatsu's OpenCCG outputs.
    Returns:
        A dictionary of identifiers mapped to their graph definitions.
    """
    graphs = {}
    for k, v in json_parses.items():
        graphs[k] = create_graph(k, v)
    return {'graphs': graphs}
