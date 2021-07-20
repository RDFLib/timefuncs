from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import TIME
from rdflib.plugins.sparql.operators import register_custom_function

from timefuncs import is_after

TFUN = Namespace("https://w3id.org/time-function/")

tests_dir = Path(__file__).parent


def test_is_after():
    register_custom_function(TFUN.isAfter, is_after, raw=True)

    g = Graph().parse(str(tests_dir / "data-after.ttl"))
    q = """
        SELECT ?a ?b
        WHERE {
            ?a a time:TemporalEntity .
            ?b a time:TemporalEntity .

            FILTER tfun:isAfter(?a, ?b)
        }
        """
    expected = [
        ('https://w3id.org/time-function/testdata/after/xA',
        'https://w3id.org/time-function/testdata/after/refA'),
        ('https://w3id.org/time-function/testdata/after/xB',
        'https://w3id.org/time-function/testdata/after/refB'),
        ('https://w3id.org/time-function/testdata/after/xC',
        'https://w3id.org/time-function/testdata/after/refC'),
        ('https://w3id.org/time-function/testdata/after/xD',
        'https://w3id.org/time-function/testdata/after/refD'),
        ('https://w3id.org/time-function/testdata/after/xE',
        'https://w3id.org/time-function/testdata/after/refE'),
        ('https://w3id.org/time-function/testdata/after/xF',
        'https://w3id.org/time-function/testdata/after/refF'),
        ('https://w3id.org/time-function/testdata/after/xG',
        'https://w3id.org/time-function/testdata/after/refG'),
        ('https://w3id.org/time-function/testdata/after/xG',
        'https://w3id.org/time-function/testdata/after/refH'),
        ('https://w3id.org/time-function/testdata/after/xG',
        'https://w3id.org/time-function/testdata/after/refI'),
        ('https://w3id.org/time-function/testdata/after/xG',
        'https://w3id.org/time-function/testdata/after/refJ'),
        ('https://w3id.org/time-function/testdata/after/xH',
        'https://w3id.org/time-function/testdata/after/refG'),
        ('https://w3id.org/time-function/testdata/after/xH',
        'https://w3id.org/time-function/testdata/after/refH'),
        ('https://w3id.org/time-function/testdata/after/xH',
        'https://w3id.org/time-function/testdata/after/refI'),
        ('https://w3id.org/time-function/testdata/after/xH',
        'https://w3id.org/time-function/testdata/after/refJ'),
        ('https://w3id.org/time-function/testdata/after/xI',
        'https://w3id.org/time-function/testdata/after/refG'),
        ('https://w3id.org/time-function/testdata/after/xI',
        'https://w3id.org/time-function/testdata/after/refH'),
        ('https://w3id.org/time-function/testdata/after/xI',
        'https://w3id.org/time-function/testdata/after/refI'),
        ('https://w3id.org/time-function/testdata/after/xI',
        'https://w3id.org/time-function/testdata/after/refJ'),
        ('https://w3id.org/time-function/testdata/after/xJ',
        'https://w3id.org/time-function/testdata/after/refG'),
        ('https://w3id.org/time-function/testdata/after/xJ',
        'https://w3id.org/time-function/testdata/after/refH'),
        ('https://w3id.org/time-function/testdata/after/xJ',
        'https://w3id.org/time-function/testdata/after/refI'),
        ('https://w3id.org/time-function/testdata/after/xJ',
        'https://w3id.org/time-function/testdata/after/refJ')
    ]

    actual = sorted([
        (str(r[0]), str(r[1]))
        for r in g.query(
            q,
            initNs={"time": TIME, "tfun": TFUN}
        )
    ])

    assert actual == expected
