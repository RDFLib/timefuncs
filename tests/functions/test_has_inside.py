from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import TIME

import sys
sys.path.append(str(Path(__file__).parent.parent))
from timefuncs import has_inside

TFUN = Namespace("https://w3id.org/timefuncs/")
INSIDE = Namespace("https://w3id.org/timefuncs/testdata/inside/")

tests_dir = Path(__file__).parent


def test_has_inside():
    g = Graph().parse(str(tests_dir / "data" / "has_inside.ttl"))
    q = """
        SELECT ?a ?b
        WHERE {
            ?a a time:Interval .
            ?b a time:Instant .

            FILTER tfun:hasInside(?a, ?b)
        }
        """
    expected = [
        (str(INSIDE.a01), str(INSIDE.b01)),
        (str(INSIDE.a07), str(INSIDE.b07)),
        (str(INSIDE.a07), str(INSIDE.b08)),
        (str(INSIDE.a09), str(INSIDE.b09)),
    ]

    actual = sorted([
        (str(r[0]), str(r[1]))
        for r in g.query(
            q,
            initNs={"time": TIME, "tfun": TFUN}
        )
    ])

    assert actual == expected
