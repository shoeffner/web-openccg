from tatsu.util import asjson
from tatsu.model import ModelBuilderSemantics

from generated_openccg_parser import OpenCCGParser


def ccg_to_json(to_parse):
    """Parses an OpenCCG string into a more easily digestiable JSON format.

    Args:
        to_parse: The OpenCCG string.
    Returns:
        A JSON representation of the OpenCCG string.
    """
    return asjson(OpenCCGParser().parse(to_parse,
                                        semantics=ModelBuilderSemantics(),
                                        parseinfo=False))
