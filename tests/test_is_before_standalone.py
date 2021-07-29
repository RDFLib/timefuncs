from typing import Union, List, Tuple
from typing import Literal as TLiteral
from pathlib import Path
from rdflib import Graph, Namespace, URIRef, BNode
from rdflib import TIME
from rdflib.paths import ZeroOrMore, OneOrMore

tests_dir = Path(__file__).parent
g = Graph().parse(str(tests_dir / "data" / "before.ttl"))


def is_before_sparql(g: Graph, a: URIRef, b: URIRef):
    q = """
        PREFIX time: <http://www.w3.org/2006/time#>
        
        ASK 
        WHERE {
            BIND (<aaa> AS ?a)
            BIND (<bbb> AS ?b)            
          
            {
                SELECT *
                WHERE {
                    {
                      ?a time:hasEnd?/time:before+ ?b .
                    } UNION {
                      ?b time:hasBeginning?/time:after+ ?a .
                    } UNION {
                      ?b time:hasBeginning?/time:after ?z .
                      ?a time:hasEnd ?z .
                    } UNION {
                      ?b time:hasBeginning ?z .
                      ?a time:hasEnd?/time:before ?z .
                    }    
                }
            }
            UNION
            {
                SELECT *
                WHERE {
                    ?a time:hasEnd?/time:inXSDDateTimeStamp ?aXSD .
                    ?b time:hasBeginning?/time:inXSDDateTimeStamp ?bXSD .                    
        
                    FILTER (?aXSD < ?bXSD)
                }
            }
        }
        """.replace("bbb", b).replace("aaa", a)
    return bool(g.query(q))


def is_before_rdflib(g: Graph, a: URIRef, b: URIRef):
    for s, o in g.subject_objects(TIME.before):
        g.add((o, TIME.after, s))

    # ?x time:hasEnd?/time:before ?ref .
    if (a, TIME.hasEnd * ZeroOrMore / TIME.before*OneOrMore, b) in g:
        return True

    # ?ref time:hasBeginning?/time:after ?x .
    if (b, TIME.hasBeginning * ZeroOrMore / TIME.after*OneOrMore, a) in g:
        return True

    # ?ref time:hasBeginning?/time:after ?z .
    # ?x time:hasEnd ?z .
    for z in g.objects(b, TIME.hasBeginning * ZeroOrMore / TIME.after):
        if (a, TIME.hasEnd, z) in g:
            return True

    # ?ref time:hasBeginning ?z .
    # ?x time:hasEnd?/time:before ?z .
    for z in g.objects(b, TIME.hasBeginning):
        if (a, TIME.hasEnd * ZeroOrMore / TIME.before, z) in g:
            return True

    # ?ref time:hasBeginning?/time:inXSDDateTimeStamp ?refXSD .
    # ?x time:hasEnd?/time:inXSDDateTimeStamp ?xXSD .
    # FILTER (?xXSD < ?refXSD)

    # if the latest date of x is smaller than the earliest date of ref...
    ref_xsds = list(g.objects(b, TIME.hasBeginning * ZeroOrMore / TIME.inXSDDateTimeStamp))
    x_xsds = list(g.objects(a, TIME.hasEnd * ZeroOrMore / TIME.inXSDDateTimeStamp))
    if len(ref_xsds) > 0 and len(x_xsds) > 0:
        if sorted(x_xsds)[-1] < sorted(ref_xsds)[0]:
            return True

    if _path_exists(g, a, b, [(TIME.before, "outbound"), (TIME.after, "inbound")]):
        return True

    return False


def _path_exists(
    g: Graph,
    a: Union[URIRef, BNode],
    b: Union[URIRef, BNode],
    predicates: List[Tuple[URIRef, TLiteral["outbound", "inbound"]]],
) -> bool:
    """Finds if any path between RDF nodes a and b in graph g exists,
    following any of the predicates supplied, in any order.

    This function is a support function for the names TIME functions such as is_before."""

    if a == b:
        return False

    def _get_next_nodes(node, preds):
        """Finds any nodes linked to a given node, 'node' via any of the given predicates 'pred'.

        Looks for both s pred o and o pred s (inverse)"""
        next_nodes = []

        for p in preds:
            if p[1] == "outbound":
                for o in g.objects(subject=node, predicate=p[0]):
                    next_nodes.append(o)
            elif p[1] == "inbound":
                for s in g.subjects(predicate=p[0], object=node):
                    next_nodes.append(s)

        return next_nodes

    # standard breadth-first search
    def bfs(node):
        visited = []
        queue = []
        visited.append(node)
        queue.append(node)

        while queue:
            s = queue.pop(0)
            for x in _get_next_nodes(s, predicates):
                if x == b:
                    return True
                if x not in visited:
                    visited.append(x)
                    queue.append(x)
        return False

    return bfs(a)


def test_is_before_sparql():
    BEFORE = Namespace("https://w3id.org/timefuncs/testdata/before/")

    assert is_before_sparql(g, BEFORE.a01, BEFORE.b01)
    assert is_before_sparql(g, BEFORE.a02, BEFORE.b02)
    assert is_before_sparql(g, BEFORE.a03, BEFORE.b03)
    assert is_before_sparql(g, BEFORE.a04, BEFORE.b04)
    assert is_before_sparql(g, BEFORE.a05, BEFORE.b05)
    assert is_before_sparql(g, BEFORE.a06, BEFORE.b06)
    assert is_before_sparql(g, BEFORE.a07, BEFORE.b07)
    assert is_before_sparql(g, BEFORE.a08, BEFORE.b08)
    assert is_before_sparql(g, BEFORE.a09, BEFORE.b09)
    assert is_before_sparql(g, BEFORE.a10, BEFORE.b10)
    assert is_before_sparql(g, BEFORE.a11, BEFORE.b11)

    assert not is_before_sparql(g, BEFORE.a01, BEFORE.b02)
    assert not is_before_sparql(g, BEFORE.foo, BEFORE.bar)
    assert not is_before_sparql(g, BEFORE.b01, BEFORE.a01)
    assert not is_before_sparql(g, BEFORE.b04, BEFORE.a06)
    assert not is_before_sparql(g, BEFORE.b10, BEFORE.a10)


def test_is_before_rdflib():
    BEFORE = Namespace("https://w3id.org/timefuncs/testdata/before/")

    assert is_before_rdflib(g, BEFORE.a01, BEFORE.b01)
    assert is_before_rdflib(g, BEFORE.a02, BEFORE.b02)
    assert is_before_rdflib(g, BEFORE.a03, BEFORE.b03)
    assert is_before_rdflib(g, BEFORE.a04, BEFORE.b04)
    assert is_before_rdflib(g, BEFORE.a05, BEFORE.b05)
    assert is_before_rdflib(g, BEFORE.a06, BEFORE.b06)
    assert is_before_rdflib(g, BEFORE.a08, BEFORE.b08)
    assert is_before_rdflib(g, BEFORE.a09, BEFORE.b09)
    assert is_before_rdflib(g, BEFORE.a10, BEFORE.b10)
    assert is_before_rdflib(g, BEFORE.a11, BEFORE.b11)

    assert not is_before_rdflib(g, BEFORE.a01, BEFORE.b02)
    assert not is_before_rdflib(g, BEFORE.foo, BEFORE.bar)
    assert not is_before_rdflib(g, BEFORE.b01, BEFORE.a01)
    assert not is_before_rdflib(g, BEFORE.b07, BEFORE.a07)
    assert not is_before_rdflib(g, BEFORE.b10, BEFORE.a10)
