"""
Functions derived from OWL TIME
"""
from rdflib import Graph, Namespace, URIRef

g = Graph().parse("test_isBefore_data.ttl")


def isBefore(g: Graph, ref: URIRef, x: URIRef):
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
