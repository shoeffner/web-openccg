from tatsu.ast import AST
from tatsu.util import asjson

from generated_openccg_parser import OpenCCGParser, OpenCCGSemantics


def ccg_to_json(to_parse):
    """Parses an OpenCCG string into a more easily digestiable JSON format.

    Args:
        to_parse: The OpenCCG string.
    Returns:
        A JSON representation of the OpenCCG string.
    """
    return asjson(OpenCCGParser().parse(to_parse,
                                        semantics=OpenCCGCustomSemantics(),
                                        parseinfo=False))


class OpenCCGCustomSemantics(OpenCCGSemantics):
    """The custom semantics are used to flatten the role structure
    caused by right-deep trees of the conjunction parses."""

    def variable_expression(self, ast):
        if ast['roles'] and len(ast['roles']) >= 2:
            if isinstance(ast['roles'][-1], list):
                role = ast['roles'][-1][0]
                del ast['roles'][-1][0]
                if len(ast['roles'][-1]) == 0:
                    del ast['roles'][-1]
                ast['roles'].insert(-1, role)
        return ast

    def role(self, ast):
        if isinstance(ast['target'], str):
            return ast
        if ast['target']['roles'] and len(ast['target']['roles']) >= 2:
            for i, maybe_role in enumerate(ast['target']['roles']):
                if isinstance(maybe_role, list):
                    role = ast['target']['roles'][i][0]
                    del ast['target']['roles'][i][0]
                    if len(ast['target']['roles'][i]) == 0:
                        del ast['target']['roles'][i]
                    ast['target']['roles'].insert(i, role)

            if len(ast['target']['roles']) >= 3:
                for i, role in enumerate(ast['target']['roles']):
                    if isinstance(role, list):
                        r0, r1 = role
                        del ast['target']['roles'][i]
                        ast['target']['roles'].insert(i, r1)
                        ast['target']['roles'].insert(i, r0)

        return ast
