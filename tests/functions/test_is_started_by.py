from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import TIME

import sys
sys.path.append(str(Path(__file__).parent.parent))
from timefuncs import is_started_by

TFUN = Namespace("https://w3id.org/timefuncs/")
ISB = Namespace("https://w3id.org/timefuncs/testdata/isstartedby/")

tests_dir = Path(__file__).parent


def test_is_started_by():
    g = Graph().parse(str(tests_dir / "data" / "is_started_by.ttl"))

    q = """
        SELECT ?a ?b
        WHERE {
            VALUES ?a_type { time:Interval time:ProperInterval }
            VALUES ?b_type { time:Interval time:ProperInterval }
            
            ?a a ?a_type .
            ?b a ?b_type .

            FILTER tfun:isStartedBy(?a, ?b)
        }
        """        
    expected = [
        (str(ISB.a01), str(ISB.b01)),
        # (str(ISB.a02), str(ISB.b02)), false
        (str(ISB.a03), str(ISB.b03)),
        (str(ISB.a04), str(ISB.b04)),
        (str(ISB.a05), str(ISB.b05)),
        (str(ISB.a06), str(ISB.b06)),
        # (str(ISB.a07), str(ISB.b07)), still working on this
        (str(ISB.a08), str(ISB.b08)),
    ]

    actual = sorted([
        (str(r[0]), str(r[1]))
        for r in g.query(
            q,
            initNs={"time": TIME, "tfun": TFUN}
        )
    ])

    assert actual == expected
