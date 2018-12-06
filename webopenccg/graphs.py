import pygraphviz as pgv
from itertools import cycle


class GraphGenerator:
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

    variable_colors = [
        '#8b008b',  # darkmagenta
        '#ff7f50',  # coral
        '#dc143c',  # crimson
        '#ffd700',  # gold
        '#ff1493',  # deeppink
        '#adff2f',  # greenyellow
    ]

    def __init__(self):
        self.nodes = {}
        self.variables = {}

    def get(self, parse):
        graph = pgv.AGraph()

        self.walk(parse, graph)
        self.color_same_variables(graph)

        return str(graph)

    def color_same_variables(self, graph):
        default_style = {'color': 'black', 'penwidth': 1.0}

        colors = cycle(GraphGenerator.variable_colors)
        for name, alternatives in self.variables.items():
            if len(alternatives) == 1:
                continue

            style = {'color': next(colors), 'penwidth': 4.0}
            for alternative in alternatives:
                sg = self.find_subgraph(graph, f'cluster_{alternative}')
                if sg is None:
                    continue
                sg.graph_attr.update(**style)
                parent = sg.subgraph_parent()
                if parent is not None and parent.has_node(alternative):
                    node = parent.get_node(alternative)
                    if not node.attr['label'].startswith('{'):
                        node.attr.update(**style)
                for ssg in sg.subgraphs_iter():
                    if ssg.graph_attr['color'] == '':
                        ssg.graph_attr.update(**default_style)

    def find_subgraph(self, graph, subgraph_name):
        for sg in graph.subgraphs_iter():
            if sg.name == subgraph_name:
                return sg
            found = self.find_subgraph(sg, subgraph_name)
            if found is not None:
                return found

    def role_string(self, role):
        return f"&lt;{role['type']}&gt; {role['target']}"

    def relation_string(self, role):
        return f"{role['type']}"

    def variable_string(self, variable):
        if variable['type'] is not None:
            return f"{variable['name']}: {variable['type']}"
        else:
            return variable['name']

    def handle_nominal(self, tree, graph):
        """Placeholder, currently nominals are handled just like variables."""
        self.handle_variable(tree, graph, GraphGenerator.nominal_style)

    def handle_variable(self, tree, graph, style=None):
        name = tree['name']
        while name in self.nodes:
            name += '_'
        if name.rstrip('_') in self.variables:
            self.variables[name.rstrip('_')].append(name)
        else:
            self.variables[name] = [name]

        graph.add_node(name, shape='Mrecord',
                       label=self.variable_string(tree),
                       **GraphGenerator.property_style)
        if style is None:
            style = GraphGenerator.variable_style
        sg = graph.add_subgraph(name,
                                name=f"cluster_{name}",
                                label=self.variable_string(tree),
                                **style)
        self.nodes[name] = sg

        attributes = []
        for role in tree['roles']:
            if isinstance(role['target'], str):
                attributes.append(self.role_string(role))
            elif isinstance(role['target'], dict):
                sg.add_node(role['type'], label=self.relation_string(role))
                role_sg = sg.add_subgraph(role['type'],
                                          name=f"cluster_{role['type']}",
                                          label=self.relation_string(role),
                                          **GraphGenerator.relation_style)

                self.handle_variable(role['target'], role_sg)

                while role_sg is not None:
                    role_sg.delete_node(role['type'])
                    role_sg = role_sg.subgraph_parent()

        if attributes:
            label = '|'.join(a for a in attributes if isinstance(a, str))
            graph.get_node(name).attr['label'] = '{' + label + '}'
        else:
            while sg is not None:
                sg.delete_node(name)
                sg = sg.subgraph_parent()
            if not len(tree['roles']):
                graph.add_node(name, shape='box',
                               label=self.variable_string(tree),
                               **GraphGenerator.variable_style)

    def handle_role(self, tree, graph):
        if isinstance(tree['target'], str):
            # Property
            graph.add_node(tree['target'], shape='Mrecord',
                           label=('{' + self.role_string(tree) + '}'),
                           **GraphGenerator.property_style)
        if isinstance(tree['target'], dict):
            # Relation
            graph.add_node(tree['name'], shape='Mrecord',
                           **GraphGenerator.relation_style)

    def walk(self, tree, graph):
        handle = {
            'Nominal': self.handle_nominal,
            'Variable': self.handle_variable,
            'Role': self.handle_role
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
    return GraphGenerator().get(parse)


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
