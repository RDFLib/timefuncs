"""
Functions derived from OWL TIME
"""
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import TIME
from rdflib.paths import ZeroOrMore


g = Graph().parse("test_isBefore_data.ttl")


def isBefore(g: Graph, ref: URIRef, x: URIRef):
    # ?x time:hasEnd?/time:before ?ref .
    if (x, TIME.hasEnd*ZeroOrMore/TIME.before, ref) in g:
        return True

    # ?ref time:hasBeginning?/time:after ?x .
    if (ref, TIME.hasBeginning*ZeroOrMore/TIME.after, x) in g:
        return True

    # ?ref time:hasBeginning?/time:after ?z .
    # ?x time:hasEnd ?z .
    for z in g.objects(ref, TIME.hasBeginning*ZeroOrMore/TIME.after):
        if (x, TIME.hasEnd, z) in g:
            return True

    # ?ref time:hasBeginning ?z .
    # ?x time:hasEnd?/time:before ?z .
    for z in g.objects(ref, TIME.hasBeginning):
        if (x, TIME.hasEnd*ZeroOrMore/TIME.before, z) in g:
            return True

    # ?ref time:hasBeginning?/time:inXSDDateTimeStamp ?refXSD .
    # ?x time:hasEnd?/time:inXSDDateTimeStamp ?xXSD .
    # FILTER (?xXSD < ?refXSD)

    # if the latest date of x is smaller than the earliest date of ref...
    ref_xsds = list(g.objects(ref, TIME.hasBeginning*ZeroOrMore/TIME.inXSDDateTimeStamp))
    x_xsds = list(g.objects(x, TIME.hasEnd*ZeroOrMore/TIME.inXSDDateTimeStamp))
    if len(ref_xsds) > 0 and len(x_xsds) > 0:
        if sorted(x_xsds)[-1] < sorted(ref_xsds)[0]:
            return True

    return False


def test_isBefore():
    BEFORE = Namespace("https://w3id.org/time-function/testdata/before/")

    assert isBefore(g, BEFORE.refA, BEFORE.xA)
    assert isBefore(g, BEFORE.refB, BEFORE.xB)
    assert isBefore(g, BEFORE.refC, BEFORE.xC)
    assert isBefore(g, BEFORE.refD, BEFORE.xD)
    assert isBefore(g, BEFORE.refE, BEFORE.xE)
    assert isBefore(g, BEFORE.refF, BEFORE.xF)
    assert isBefore(g, BEFORE.refG, BEFORE.xG)
    assert isBefore(g, BEFORE.refH, BEFORE.xH)
    assert isBefore(g, BEFORE.refI, BEFORE.xI)
    assert isBefore(g, BEFORE.refJ, BEFORE.xJ)

    assert not isBefore(g, BEFORE.refA, BEFORE.xB)
    assert not isBefore(g, BEFORE.foo, BEFORE.bar)
    assert not isBefore(g, BEFORE.xA, BEFORE.refA)
    assert not isBefore(g, BEFORE.xG, BEFORE.refG)
    assert not isBefore(g, BEFORE.xJ, BEFORE.refJ)
