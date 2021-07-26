from rdflib import Graph
from rdflib.namespace import TIME
from timefuncs import TFUN


def test_001():
    data = """
        PREFIX : <http://example.com/>
        PREFIX time: <http://www.w3.org/2006/time#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        
        :e01 a time:TemporalEntity .
        :f01 a time:TemporalEntity .
        :e01 time:inXSDDate "2021-01-01"^^xsd:date . 
        :f01 time:inXSDDate "2022-01-01"^^xsd:date .
        """

    q = """
        SELECT ?x ?y
        WHERE {
            ?x a time:TemporalEntity .
            ?y a time:TemporalEntity .
            
            FILTER tfun:isBefore(?x, ?y)
        }
        """
    res = 0
    for r in Graph().parse(data=data, format="turtle").query(q, initNs={"time": TIME, "tfun": TFUN}):
        res += 1
    assert res == 1, "before not working"

    q = """
        SELECT ?x ?y
        WHERE {
            ?x a time:TemporalEntity .
            ?y a time:TemporalEntity .
    
            FILTER tfun:isAfter(?x, ?y)
        }
        """
    res = 0
    for r in Graph().parse(data=data, format="turtle").query(q, initNs={"time": TIME, "tfun": TFUN}):
        res += 1
    assert res == 1, "after not working"

