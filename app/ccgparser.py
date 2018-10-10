from tatsu import parse
from tatsu.util import asjson


GRAMMAR = r"""

start
    = semspec $
    ;

semspec
    = nominal
    | term
    | conjunction
    | expression
    ;

conjunction
    = @:expression '^' ~ @:conjunction
    | @:expression
    ;

expression
    = role_expression
    | nominal_expression
    | variable_expression
    | atom_expression
    ;

role_expression
    = role:role
    ;

variable_expression
    = variable:variable
    ;

nominal_expression
    = nominal:nominal
    ;

atom_expression
    = atom:atom
    ;

term
    = '(' ~ @:conjunction ')'
    ;

nominal
    = '@' ~ nominal:variable roles:term
    ;

role
    = '<' type:atom '>' target:variable
    | '<' type:atom '>' target:term
    | '<' type:atom '>' target:atom
    ;

variable
    = /[a-z]\d+(:[a-zA-Z\-]+)*/
    ;

atom
    = /[a-zA-Z\-\.]+/
    ;
"""


def ccg_to_json(to_parse):
    """Parses an OpenCCG string into a more easily digestiable JSON format.

    Args:
        to_parse: The OpenCCG string.
    Returns:
        A JSON representation of the OpenCCG string.
    """
    return asjson(parse(GRAMMAR, to_parse))
