from pathlib import Path
from rdflib import Graph, Namespace, URIRef
from rdflib import TIME
from rdflib.paths import ZeroOrMore

tests_dir = Path(__file__).parent
g = Graph().parse(str(tests_dir / "data" / "before.ttl"))


def is_before_sparql(g: Graph, ref: URIRef, x: URIRef):
    q = """
        PREFIX time: <http://www.w3.org/2006/time#>
        
        ASK 
        WHERE {
            BIND (<xxx> AS ?ref)
            BIND (<yyy> AS ?x)
          
            {
                SELECT *
                WHERE {
                    {
                      ?x time:hasEnd?/time:before ?ref .
                    } UNION {
                      ?ref time:hasBeginning?/time:after ?x .
                    } UNION {
                      ?ref time:hasBeginning?/time:after ?z .
                      ?x time:hasEnd ?z .
                    } UNION {
                      ?ref time:hasBeginning ?z .
                      ?x time:hasEnd?/time:before ?z .
                    }    
                }
            }
            UNION
            {
                SELECT *
                WHERE {
                    ?ref time:hasBeginning?/time:inXSDDateTimeStamp ?refXSD .
                    ?x time:hasEnd?/time:inXSDDateTimeStamp ?xXSD .
        
                    FILTER (?xXSD < ?refXSD)
                }
            }
        }
        """.replace("xxx", ref).replace("yyy", x)
    return bool(g.query(q))


def is_before_rdflib(g: Graph, ref: URIRef, x: URIRef):
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


def test_is_before_sparql():
    BEFORE = Namespace("https://w3id.org/time-function/testdata/before/")

    assert is_before_sparql(g, BEFORE.refA, BEFORE.xA)
    assert is_before_sparql(g, BEFORE.refB, BEFORE.xB)
    assert is_before_sparql(g, BEFORE.refC, BEFORE.xC)
    assert is_before_sparql(g, BEFORE.refD, BEFORE.xD)
    assert is_before_sparql(g, BEFORE.refE, BEFORE.xE)
    assert is_before_sparql(g, BEFORE.refF, BEFORE.xF)
    assert is_before_sparql(g, BEFORE.refG, BEFORE.xG)
    assert is_before_sparql(g, BEFORE.refH, BEFORE.xH)
    assert is_before_sparql(g, BEFORE.refI, BEFORE.xI)
    assert is_before_sparql(g, BEFORE.refJ, BEFORE.xJ)

    assert not is_before_sparql(g, BEFORE.refA, BEFORE.xB)
    assert not is_before_sparql(g, BEFORE.foo, BEFORE.bar)
    assert not is_before_sparql(g, BEFORE.xA, BEFORE.refA)
    assert not is_before_sparql(g, BEFORE.xG, BEFORE.refG)
    assert not is_before_sparql(g, BEFORE.xJ, BEFORE.refJ)


def test_is_before_rdflib():
    BEFORE = Namespace("https://w3id.org/time-function/testdata/before/")

    assert is_before_rdflib(g, BEFORE.refA, BEFORE.xA)
    assert is_before_rdflib(g, BEFORE.refB, BEFORE.xB)
    assert is_before_rdflib(g, BEFORE.refC, BEFORE.xC)
    assert is_before_rdflib(g, BEFORE.refD, BEFORE.xD)
    assert is_before_rdflib(g, BEFORE.refE, BEFORE.xE)
    assert is_before_rdflib(g, BEFORE.refF, BEFORE.xF)
    assert is_before_rdflib(g, BEFORE.refG, BEFORE.xG)
    assert is_before_rdflib(g, BEFORE.refH, BEFORE.xH)
    assert is_before_rdflib(g, BEFORE.refI, BEFORE.xI)
    assert is_before_rdflib(g, BEFORE.refJ, BEFORE.xJ)

    assert not is_before_rdflib(g, BEFORE.refA, BEFORE.xB)
    assert not is_before_rdflib(g, BEFORE.foo, BEFORE.bar)
    assert not is_before_rdflib(g, BEFORE.xA, BEFORE.refA)
    assert not is_before_rdflib(g, BEFORE.xG, BEFORE.refG)
    assert not is_before_rdflib(g, BEFORE.xJ, BEFORE.refJ)
