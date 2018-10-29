import pygraphviz as pgv


nominal_style = {
    'style': 'filled',
    'fillcolor': 'lightskyblue'
}

variable_style = {
    'style': 'filled',
    'fillcolor': 'lightblue',
}

relation_style = {
    'style': 'filled',
    'fillcolor': 'honeydew'
}

property_style = {
    'style': 'filled',
    'fillcolor': 'aliceblue'
}


def role_string(role):
    return f"&lt;{role['type']}&gt; {role['target']}"


def relation_string(role):
    return f"{role['type']}"


def variable_string(variable):
    if variable['type']:
        return f"{variable['name']}: {variable['type']}"
    else:
        variable['name']


def handle_nominal(tree, graph):
    """Placeholder, currently nominals are handled just like variables."""
    handle_variable(tree, graph)
    graph.get_subgraph(f"cluster_{tree['name']}").graph_attr.update(nominal_style)


def handle_variable(tree, graph):
    graph.add_node(tree['name'], shape='Mrecord',
                   label=variable_string(tree),
                   **property_style)
    sg = graph.add_subgraph(tree['name'],
                            name=f"cluster_{tree['name']}",
                            label=variable_string(tree),
                            **variable_style)

    attributes = []
    for role in tree['roles']:
        if isinstance(role['target'], str):
            attributes.append(role_string(role))
        elif isinstance(role['target'], dict):
            sg.add_node(role['type'], label=relation_string(role))
            role_sg = sg.add_subgraph(role['type'],
                                      name=f"cluster_{role['type']}",
                                      label=relation_string(role),
                                      **relation_style)

            handle_variable(role['target'], role_sg)

            while role_sg is not None:
                role_sg.delete_node(role['type'])
                role_sg = role_sg.subgraph_parent()

    if attributes:
        label = '|'.join(a for a in attributes if isinstance(a, str))
        graph.get_node(tree['name']).attr['label'] = '{' + label + '}'
    else:
        while sg is not None:
            sg.delete_node(tree['name'])
            sg = sg.subgraph_parent()
        if not len(tree['roles']):
            graph.add_node(tree['name'], shape='box',
                           label=variable_string(tree),
                           **variable_style)


def handle_role(tree, graph):
    if isinstance(tree['target'], str):
        # Property
        graph.add_node(tree['target'], shape='Mrecord',
                       label=('{' + role_string(tree) + '}'),
                       **property_style)
    if isinstance(tree['target'], dict):
        # Relation
        graph.add_node(tree['name'], shape='Mrecord',
                       **relation_style)


def walk(tree, graph):
    handle = {
        'Nominal': handle_nominal,
        'Variable': handle_variable,
        'Role': handle_role
    }
    if isinstance(tree, dict):
        handle[tree['__class__']](tree, graph)
    if isinstance(tree, list):
        for elem in tree:
            handle[elem['__class__']](elem, graph)


def create_graph(parse):
    """Creates a single graph from a parse.

    Args:
        parse: The JSON representation of the semantic specification.
    """
    graph = pgv.AGraph()

    walk(parse, graph)

    return str(graph)


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
        graphs[k] = create_graph(v)
    return {'graphs': graphs}
