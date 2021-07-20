from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import TIME
from rdflib.plugins.sparql.operators import register_custom_function

from timefuncs import is_before

TFUN = Namespace("https://w3id.org/time-function/")
BEFORE = Namespace("https://w3id.org/time-function/testdata/before/")

tests_dir = Path(__file__).parent


def test_is_before():
    register_custom_function(TFUN.isBefore, is_before, raw=True)

    g = Graph().parse(str(tests_dir / "data" / "before.ttl"))
    q = """
        SELECT ?a ?b
        WHERE {
            ?a a time:TemporalEntity .
            ?b a time:TemporalEntity .

            FILTER tfun:isBefore(?a, ?b)
        }
        """
    expected = [
        (str(BEFORE.a01), str(BEFORE.b01)),
        (str(BEFORE.a02), str(BEFORE.b02)),
        (str(BEFORE.a03), str(BEFORE.b03)),
        (str(BEFORE.a04), str(BEFORE.b04)),
        (str(BEFORE.a05), str(BEFORE.b05)),
        (str(BEFORE.a06), str(BEFORE.b06)),
        (str(BEFORE.a07), str(BEFORE.b07)),
        (str(BEFORE.a07), str(BEFORE.b08)),
        (str(BEFORE.a07), str(BEFORE.b09)),
        (str(BEFORE.a07), str(BEFORE.b10)),
        (str(BEFORE.a08), str(BEFORE.b07)),
        (str(BEFORE.a08), str(BEFORE.b08)),
        (str(BEFORE.a08), str(BEFORE.b09)),
        (str(BEFORE.a08), str(BEFORE.b10)),
        (str(BEFORE.a09), str(BEFORE.b07)),
        (str(BEFORE.a09), str(BEFORE.b08)),
        (str(BEFORE.a09), str(BEFORE.b09)),
        (str(BEFORE.a09), str(BEFORE.b10)),
        (str(BEFORE.a10), str(BEFORE.b07)),
        (str(BEFORE.a10), str(BEFORE.b08)),
        (str(BEFORE.a10), str(BEFORE.b09)),
        (str(BEFORE.a10), str(BEFORE.b10))
    ]

    actual = sorted([
        (str(r[0]), str(r[1]))
        for r in g.query(
            q,
            initNs={"time": TIME, "tfun": TFUN}
        )
    ])

    assert actual == expected
