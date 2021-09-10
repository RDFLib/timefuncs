from .funcs import (
    contains,
    has_during,
    has_inside,
    finishes,
    is_after,
    is_before,
    is_contained_by,
    is_during,
    is_finished_by,
    is_inside,
    is_started_by,
    starts
)
from rdflib import Namespace
from rdflib.plugins.sparql.operators import register_custom_function

__version__ = "0.1.4"
TFUN = Namespace("https://w3id.org/timefuncs/")

register_custom_function(TFUN.contains, contains, raw=True)
register_custom_function(TFUN.hasDuring, has_during, raw=True)
register_custom_function(TFUN.hasInside, has_inside, raw=True)
register_custom_function(TFUN.finishes, finishes, raw=True)
register_custom_function(TFUN.isAfter, is_after, raw=True)
register_custom_function(TFUN.isBefore, is_before, raw=True)
register_custom_function(TFUN.isContainedBy, is_contained_by, raw=True)
register_custom_function(TFUN.isDuring, is_during, raw=True)
register_custom_function(TFUN.isFinishedBy, is_finished_by, raw=True)
register_custom_function(TFUN.isInside, is_inside, raw=True)
register_custom_function(TFUN.isStartedBy, is_started_by, raw=True)
register_custom_function(TFUN.starts, starts, raw=True)
