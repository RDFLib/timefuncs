"""
Functions derived from OWL TIME
"""
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import TIME
from rdflib.paths import ZeroOrMore

before_data = """
    PREFIX time: <http://www.w3.org/2006/time#>
    PREFIX : <https://w3id.org/time-function/testdata/before/>
    
    # x declared before ref
    :xA time:before :refA .
    
    # end of x declared before ref
    :xB time:hasEnd [
        time:before :refB
    ] .
    
    # ref declared after x
    :refC time:after :xC .
    
    # start of ref declared after x
    :refD time:hasBeginning [
        time:after :xD
    ] .
    
    # end of x declared before start of ref
    :refE time:hasBeginning :startE .
    :xE time:hasEnd [
        time:before :startE
    ] .
    
    # start of ref declared after end of x
    :refF time:hasBeginning [
        time:after :endF
    ] .
    :xF time:hasEnd :endF .
    
    # x calculated before ref
    :refG time:inXSDDateTimeStamp "2021-07-16T00:00:00Z" .
    :xG time:inXSDDateTimeStamp "2021-07-15T23:59:59Z" .
    
    # end of x is calculated before ref
    :refH time:inXSDDateTimeStamp "2021-07-16T00:00:00Z" .
    :xH time:hasEnd [
        time:inXSDDateTimeStamp "2021-07-15T23:59:59Z"
    ] .
    
    # beginning of ref calculated after x
    :refI time:hasBeginning [
        time:inXSDDateTimeStamp "2021-07-16T00:00:00Z" 
    ] .
    :xI time:inXSDDateTimeStamp "2021-07-15T23:59:59Z" .
    
    # end of x calculated to be before the beginning of ref
    :refJ time:hasBeginning [
        time:inXSDDateTimeStamp "2021-07-16T00:00:00Z"
    ] .
    :xJ time:hasEnd [
        time:inXSDDateTimeStamp "2021-07-15T23:59:59Z"
    ] .
    """

g = Graph().parse(data=before_data)


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

