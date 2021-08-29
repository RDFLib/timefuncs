from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import TIME

import sys
sys.path.append(str(Path(__file__).parent.parent))
from timefuncs import is_finished_by

TFUN = Namespace("https://w3id.org/timefuncs/")
IFB = Namespace("https://w3id.org/timefuncs/testdata/isfinishedby/")

tests_dir = Path(__file__).parent


def test_is_finished_by():
    g = Graph().parse(str(tests_dir / "data" / "is_finished_by.ttl"))

    q = """
        SELECT ?a ?b
        WHERE {
            VALUES ?a_type { time:Interval time:ProperInterval }
            VALUES ?b_type { time:Interval time:ProperInterval }
            
            ?a a ?a_type .
            ?b a ?b_type .

            FILTER tfun:isFinishedBy(?a, ?b)
        }
        """        
    expected = [
        (str(IFB.a01), str(IFB.b01)),
        # (str(IFB.a02), str(IFB.b02)), false
        (str(IFB.a03), str(IFB.b03)),
        (str(IFB.a04), str(IFB.b04)),
        (str(IFB.a05), str(IFB.b05)),
        (str(IFB.a06), str(IFB.b06)),
        # (str(IFB.a07), str(IFB.b07)), still working on this
        (str(IFB.a08), str(IFB.b08)),
    ]

    actual = sorted([
        (str(r[0]), str(r[1]))
        for r in g.query(
            q,
            initNs={"time": TIME, "tfun": TFUN}
        )
    ])

    assert actual == expected
