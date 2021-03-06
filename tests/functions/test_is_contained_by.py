from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import TIME

import sys
sys.path.append(str(Path(__file__).parent.parent))
from timefuncs import is_contained_by

TFUN = Namespace("https://w3id.org/timefuncs/")
ICB = Namespace("https://w3id.org/timefuncs/testdata/iscontainedby/")

tests_dir = Path(__file__).parent


def test_is_contained_by():
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
        (str(ICB.a06), str(ICB.b06)),
        (str(ICB.a07), str(ICB.b07)),
        (str(ICB.a08), str(ICB.b08)),
        (str(ICB.a09), str(ICB.b09)),
    ]

    actual = sorted([
        (str(r[0]), str(r[1]))
        for r in g.query(
            q,
            initNs={"time": TIME, "tfun": TFUN}
        )
    ])

    assert actual == expected
