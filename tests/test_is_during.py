from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import TIME
from rdflib.plugins.sparql.operators import register_custom_function

from timefuncs import is_during

TFUN = Namespace("https://w3id.org/time-function/")
ID = Namespace("https://w3id.org/time-function/testdata/isduring/")

tests_dir = Path(__file__).parent


def test_is_during():
    register_custom_function(TFUN.isDuring, is_during, raw=True)

    g = Graph().parse(str(tests_dir / "data" / "is_during.ttl"))
    q = """
        SELECT ?a ?b
        WHERE {
            ?a a time:Interval .
            ?b a time:Interval .

            FILTER tfun:isDuring(?a, ?b)
        }
        """
    expected = [
        (str(ID.a01), str(ID.b01)),
        (str(ID.a02), str(ID.b02)),
        (str(ID.a03), str(ID.b03)),
        (str(ID.a04), str(ID.b04)),
        (str(ID.a05), str(ID.b05)),
        (str(ID.a06), str(ID.b06)),
        (str(ID.a07), str(ID.b07)),
        (str(ID.a08), str(ID.b08)),
        (str(ID.a09), str(ID.b09)),
    ]

    actual = sorted([
        (str(r[0]), str(r[1]))
        for r in g.query(
            q,
            initNs={"time": TIME, "tfun": TFUN}
        )
    ])

    assert actual == expected
