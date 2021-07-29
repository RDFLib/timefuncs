from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import TIME

import sys
sys.path.append(str(Path(__file__).parent.parent))
from timefuncs import is_after

TFUN = Namespace("https://w3id.org/timefuncs/")
AFTER = Namespace("https://w3id.org/timefuncs/testdata/after/")

tests_dir = Path(__file__).parent


def test_is_after():
    g = Graph().parse(str(tests_dir / "data" / "after.ttl"))
    q = """
        SELECT ?a ?b
        WHERE {
            ?a a time:TemporalEntity .
            ?b a time:TemporalEntity .

            FILTER tfun:isAfter(?a, ?b)
        }
        """        
    expected = [
        (str(AFTER.a01), str(AFTER.b01)),
        (str(AFTER.a02), str(AFTER.b02)),
        (str(AFTER.a03), str(AFTER.b03)),
        (str(AFTER.a04), str(AFTER.b04)),
        (str(AFTER.a05), str(AFTER.b05)),
        (str(AFTER.a06), str(AFTER.b06)),
        (str(AFTER.a07), str(AFTER.b07)),
        (str(AFTER.a07), str(AFTER.b08)),
        (str(AFTER.a07), str(AFTER.b09)),
        (str(AFTER.a07), str(AFTER.b10)),
        (str(AFTER.a08), str(AFTER.b07)),
        (str(AFTER.a08), str(AFTER.b08)),
        (str(AFTER.a08), str(AFTER.b09)),
        (str(AFTER.a08), str(AFTER.b10)),
        (str(AFTER.a09), str(AFTER.b07)),
        (str(AFTER.a09), str(AFTER.b08)),
        (str(AFTER.a09), str(AFTER.b09)),
        (str(AFTER.a09), str(AFTER.b10)),
        (str(AFTER.a10), str(AFTER.b07)),
        (str(AFTER.a10), str(AFTER.b08)),
        (str(AFTER.a10), str(AFTER.b09)),
        (str(AFTER.a10), str(AFTER.b10))
    ]

    actual = sorted([
        (str(r[0]), str(r[1]))
        for r in g.query(
            q,
            initNs={"time": TIME, "tfun": TFUN}
        )
    ])

    assert actual == expected
