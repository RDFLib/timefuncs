from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import TIME
from rdflib.plugins.sparql.operators import register_custom_function

from timefuncs import has_during

TFUN = Namespace("https://w3id.org/time-function/")
HD = Namespace("https://w3id.org/time-function/testdata/hasduring/")

tests_dir = Path(__file__).parent


def test_has_during():
    register_custom_function(TFUN.hasDuring, has_during, raw=True)

    g = Graph().parse(str(tests_dir / "data" / "has_during.ttl"))
    q = """
        SELECT ?a ?b
        WHERE {
            ?a a time:Interval .
            ?b a time:Interval .

            FILTER tfun:hasDuring(?a, ?b)
        }
        """
    expected = [
        (str(HD.a01), str(HD.b01)),
        (str(HD.a02), str(HD.b02)),
        (str(HD.a03), str(HD.b03)),
        (str(HD.a04), str(HD.b04)),
        (str(HD.a05), str(HD.b05)),
        (str(HD.a06), str(HD.b06)),
        (str(HD.a07), str(HD.b07)),
        (str(HD.a08), str(HD.b08)),
        (str(HD.a09), str(HD.b09)),
    ]

    actual = sorted([
        (str(r[0]), str(r[1]))
        for r in g.query(
            q,
            initNs={"time": TIME, "tfun": TFUN}
        )
    ])

    assert actual == expected
