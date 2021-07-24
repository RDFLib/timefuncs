from pathlib import Path
from rdflib import Graph, Namespace, URIRef
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
                    {b
                      ?a time:hasEnd?/time:before ?b .
                    } UNION {
                      ?b time:hasBeginning?/time:after+ ?a .
                    } UNION {
                      ?a time:hasBeginning?/time:after ?z .
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
                    ?a time:hasEnd?/time:inXSDDateTimeStamp ?xXSD .
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

    def _get_next_before_after_as_before(n):
        nexts = []
        for o in g.objects(n, TIME.before):
            nexts.append(o)
        for s in g.subjects(TIME.after, n):
            nexts.append(s)
        return nexts

    chain = [a]
    while True:
        next = []
        for c in chain:
            next.append(_get_next_before_after_as_before(c))
        # there are no next items
        if not next:
            break
        # one of the next items is b
        if b in next:
            return True
        chain = next
        print(next)

    return False


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
