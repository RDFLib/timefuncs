from .funcs import (
    contains,
    has_during,
    has_inside,
    is_after,
    is_before,
    is_contained_by,
    is_during,
    is_inside,
)
from pathlib import Path
from rdflib import Namespace
from rdflib.plugins.sparql.operators import register_custom_function


def get_version():
    with open(Path(__file__).parent.parent / "CHANGELOG.md") as file_:
        return file_.readlines()[0]


__version = get_version()
TFUN = Namespace("https://w3id.org/timefuncs/")

register_custom_function(TFUN.contains, contains, raw=True)
register_custom_function(TFUN.hasDuring, has_during, raw=True)
register_custom_function(TFUN.hasInside, has_inside, raw=True)
register_custom_function(TFUN.isAfter, is_after, raw=True)
register_custom_function(TFUN.isBefore, is_before, raw=True)
register_custom_function(TFUN.isContainedBy, is_contained_by, raw=True)
register_custom_function(TFUN.isDuring, is_during, raw=True)
register_custom_function(TFUN.isInside, is_inside, raw=True)
