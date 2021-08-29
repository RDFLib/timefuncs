from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import TIME

import sys
sys.path.append(str(Path(__file__).parent.parent))
from timefuncs import starts

TFUN = Namespace("https://w3id.org/timefuncs/")
STARTS = Namespace("https://w3id.org/timefuncs/testdata/starts/")

tests_dir = Path(__file__).parent


def test_starts():
    g = Graph().parse(str(tests_dir / "data" / "starts.ttl"))

    q = """
        SELECT ?a ?b
        WHERE {
            VALUES ?a_type { time:Interval time:ProperInterval }
            VALUES ?b_type { time:Interval time:ProperInterval }
            
            ?a a ?a_type .
            ?b a ?b_type .

            FILTER tfun:starts(?a, ?b)
        }
        """        
    expected = [
        (str(STARTS.a01), str(STARTS.b01)),
        # (str(STARTS.a02), str(STARTS.b02)), false
        (str(STARTS.a03), str(STARTS.b03)),
        (str(STARTS.a04), str(STARTS.b04)),
        (str(STARTS.a05), str(STARTS.b05)),
        (str(STARTS.a06), str(STARTS.b06)),
        # (str(STARTS.a07), str(STARTS.b07)), still working on this
        (str(STARTS.a08), str(STARTS.b08)),
    ]

    actual = sorted([
        (str(r[0]), str(r[1]))
        for r in g.query(
            q,
            initNs={"time": TIME, "tfun": TFUN}
        )
    ])

    assert actual == expected
