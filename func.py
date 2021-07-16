"""
Functions derived from OWL TIME
"""
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, TIME, XSD
TI = Namespace("http://www.w3.org/2021/time/test/individual/")

prefixes = {
    "time": TIME,
    "ti": TI,
    "xsd": XSD
}

# Example 1: Find all things that are before my object, eg:A,
# where temporal calculations are based on eg:A's time:hasTime value (a Temporal Entity)
"""
PREFIX eg: <http://example.com/>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX timef: <http://w3id.org/time-function/>

SELECT ?x
WHERE {
    eg:A time:hasTime ?aTE .

    ?x time:hasTime ?xTE .

    FILTER (timef:isBefore(?aTE, ?xTE) && !sameTerm(?aTE, ?xTE))
)
"""
# using data in time-test-individuals.ttl, this should return results as per before-true.ttl

# standards SPARQL equivalent to time:isBefore
# using time-test-individuals.ttl data
q = """
PREFIX time: <http://www.w3.org/2006/time#>
BASE <http://w3id.org/time-function/testdata/before/>

SELECT ?x
WHERE {
    BIND (<ref2b> AS ?ref)
    ?ref time:hasTime ?refTE .
    ?x time:hasTime ?xTE .
    
    {
        OPTIONAL {
            ?xTE time:before ?refTE . 
        }
    } UNION {
        OPTIONAL {
            ?refTE time:after ?xTE . 
        }
    } UNION {
        OPTIONAL {
            ?refTE time:inXSDDateTimeStamp ?refXSD .
            ?xTE time:inXSDDateTimeStamp ?xXSD .
        }
    } UNION {
        OPTIONAL {
            ?refTE time:hasBeginning/time:inXSDDateTimeStamp ?refXSD .
            ?xTE time:hasEnd/time:inXSDDateTimeStamp ?xXSD .
        }
    }

    # FILTER {
    #     IF (
    #         !?refXSD && !?xXSD,  
    #         true,
    #         ?xXSD < ?refXSD
    #     )    
    # }
    BIND (
        IF (
            !BOUND(?refXSD) && !BOUND(?xXSD),  
            true,
            ?xXSD < ?refXSD
        )    
        AS ?test 
    )
    FILTER(?test)    
}
"""
g = Graph().parse("./tests/before.ttl")
for r in g.query(q, initNs=prefixes):
    print(r)


# g = Graph()
# g.add((TIME.Interval, RDFS.subClassOf, TIME.TemporalEntity))
# g.add((TIME.Instant, RDFS.subClassOf, TIME.TemporalEntity))
# g.add((TIME.ProperInterval, RDFS.subClassOf, TIME.Interval))
