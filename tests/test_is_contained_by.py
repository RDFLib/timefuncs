from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import TIME
from rdflib.plugins.sparql.operators import register_custom_function

from timefuncs import is_contained_by

TFUN = Namespace("https://w3id.org/time-function/")
ICB = Namespace("https://w3id.org/time-function/testdata/iscontainedby/")

tests_dir = Path(__file__).parent


def test_is_contained_by():
    register_custom_function(TFUN.isContainedBy, is_contained_by, raw=True)

    g = Graph().parse(str(tests_dir / "data" / "is_contained_by.ttl"))
    q = """
        SELECT ?a ?b
        WHERE {
            ?a a time:Interval .
            ?b a time:Interval .

            FILTER tfun:isContainedBy(?a, ?b)
        }
        """
    expected = [
        (str(ICB.a01), str(ICB.b01)),
        (str(ICB.a02), str(ICB.b02)),
        (str(ICB.a03), str(ICB.b03)),
        (str(ICB.a04), str(ICB.b04)),
        (str(ICB.a05), str(ICB.b05)),
    ]

    actual = sorted([
        (str(r[0]), str(r[1]))
        for r in g.query(
            q,
            initNs={"time": TIME, "tfun": TFUN}
        )
    ])

    assert actual == expected
