from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import TIME

import sys
sys.path.append(str(Path(__file__).parent.parent))
from timefuncs import contains

TFUN = Namespace("https://w3id.org/timefuncs/")
CON = Namespace("https://w3id.org/timefuncs/testdata/contains/")

tests_dir = Path(__file__).parent


def test_contained():
    g = Graph().parse(str(tests_dir / "data" / "contains.ttl"))
    q = """
        SELECT ?a ?b
        WHERE {
            ?a a time:Interval .
            ?b a time:Interval .

            FILTER tfun:contains(?a, ?b)
        }
        """
    expected = [
        (str(CON.a01), str(CON.b01)),
        (str(CON.a02), str(CON.b02)),
        (str(CON.a03), str(CON.b03)),
        (str(CON.a04), str(CON.b04)),
        (str(CON.a05), str(CON.b05)),
        (str(CON.a06), str(CON.b06)),
        (str(CON.a07), str(CON.b07)),
        (str(CON.a08), str(CON.b08)),
        (str(CON.a09), str(CON.b09)),
    ]

    actual = sorted([
        (str(r[0]), str(r[1]))
        for r in g.query(
            q,
            initNs={"time": TIME, "tfun": TFUN}
        )
    ])

    assert actual == expected
