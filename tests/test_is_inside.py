from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import TIME

from timefuncs import is_inside

TFUN = Namespace("https://w3id.org/timefuncs/")
INSIDE = Namespace("https://w3id.org/timefuncs/testdata/inside/")

tests_dir = Path(__file__).parent


def test_is_inside():
    g = Graph().parse(str(tests_dir / "data" / "is_inside.ttl"))
    q = """
        SELECT ?a ?b
        WHERE {
            ?a a time:Instant .
            ?b a time:Interval .

            FILTER tfun:isInside(?a, ?b)
        }
        """
    expected = [
        (str(INSIDE.a02), str(INSIDE.b02)),
        (str(INSIDE.a07), str(INSIDE.b07)),
        (str(INSIDE.a08), str(INSIDE.b07)),
        (str(INSIDE.a09), str(INSIDE.b09)),
    ]
    # print()
    # for r in g.query(q, initNs={"time": TIME, "tfun": TFUN}):
    #     print(r)
    actual = sorted([
        (str(r[0]), str(r[1]))
        for r in g.query(
            q,
            initNs={"time": TIME, "tfun": TFUN}
        )
    ])

    assert actual == expected
