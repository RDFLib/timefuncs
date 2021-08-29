from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import TIME

import sys
sys.path.append(str(Path(__file__).parent.parent))
from timefuncs import finishes

TFUN = Namespace("https://w3id.org/timefuncs/")
FINISHES = Namespace("https://w3id.org/timefuncs/testdata/finishes/")

tests_dir = Path(__file__).parent


def test_finishes():
    g = Graph().parse(str(tests_dir / "data" / "finishes.ttl"))

    q = """
        SELECT ?a ?b
        WHERE {
            VALUES ?a_type { time:Interval time:ProperInterval }
            VALUES ?b_type { time:Interval time:ProperInterval }
            
            ?a a ?a_type .
            ?b a ?b_type .

            FILTER tfun:finishes(?a, ?b)
        }
        """        
    expected = [
        (str(FINISHES.a01), str(FINISHES.b01)),
        # (str(FINISHES.a02), str(FINISHES.b02)), false
        (str(FINISHES.a03), str(FINISHES.b03)),
        (str(FINISHES.a04), str(FINISHES.b04)),
        (str(FINISHES.a05), str(FINISHES.b05)),
        (str(FINISHES.a06), str(FINISHES.b06)),
        # (str(FINISHES.a07), str(FINISHES.b07)), still working on this
        (str(FINISHES.a08), str(FINISHES.b08)),
    ]

    actual = sorted([
        (str(r[0]), str(r[1]))
        for r in g.query(
            q,
            initNs={"time": TIME, "tfun": TFUN}
        )
    ])

    assert actual == expected
