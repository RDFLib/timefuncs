from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import TIME
from rdflib.plugins.sparql.operators import register_custom_function

from timefuncs import is_before

TFUN = Namespace("https://w3id.org/time-function/")

tests_dir = Path(__file__).parent


def test_is_before():
    register_custom_function(TFUN.isBefore, is_before, raw=True)

    g = Graph().parse(str(tests_dir / "data-before.ttl"))
    q = """
        SELECT ?a ?b
        WHERE {
            ?a a time:TemporalEntity .
            ?b a time:TemporalEntity .

            FILTER tfun:isBefore(?a, ?b)
        }
        """
    expected = [
        ('https://w3id.org/time-function/testdata/before/xA',
        'https://w3id.org/time-function/testdata/before/refA'),
        ('https://w3id.org/time-function/testdata/before/xB',
        'https://w3id.org/time-function/testdata/before/refB'),
        ('https://w3id.org/time-function/testdata/before/xC',
        'https://w3id.org/time-function/testdata/before/refC'),
        ('https://w3id.org/time-function/testdata/before/xD',
        'https://w3id.org/time-function/testdata/before/refD'),
        ('https://w3id.org/time-function/testdata/before/xE',
        'https://w3id.org/time-function/testdata/before/refE'),
        ('https://w3id.org/time-function/testdata/before/xF',
        'https://w3id.org/time-function/testdata/before/refF'),
        ('https://w3id.org/time-function/testdata/before/xG',
        'https://w3id.org/time-function/testdata/before/refG'),
        ('https://w3id.org/time-function/testdata/before/xG',
        'https://w3id.org/time-function/testdata/before/refH'),
        ('https://w3id.org/time-function/testdata/before/xG',
        'https://w3id.org/time-function/testdata/before/refI'),
        ('https://w3id.org/time-function/testdata/before/xG',
        'https://w3id.org/time-function/testdata/before/refJ'),
        ('https://w3id.org/time-function/testdata/before/xH',
        'https://w3id.org/time-function/testdata/before/refG'),
        ('https://w3id.org/time-function/testdata/before/xH',
        'https://w3id.org/time-function/testdata/before/refH'),
        ('https://w3id.org/time-function/testdata/before/xH',
        'https://w3id.org/time-function/testdata/before/refI'),
        ('https://w3id.org/time-function/testdata/before/xH',
        'https://w3id.org/time-function/testdata/before/refJ'),
        ('https://w3id.org/time-function/testdata/before/xI',
        'https://w3id.org/time-function/testdata/before/refG'),
        ('https://w3id.org/time-function/testdata/before/xI',
        'https://w3id.org/time-function/testdata/before/refH'),
        ('https://w3id.org/time-function/testdata/before/xI',
        'https://w3id.org/time-function/testdata/before/refI'),
        ('https://w3id.org/time-function/testdata/before/xI',
        'https://w3id.org/time-function/testdata/before/refJ'),
        ('https://w3id.org/time-function/testdata/before/xJ',
        'https://w3id.org/time-function/testdata/before/refG'),
        ('https://w3id.org/time-function/testdata/before/xJ',
        'https://w3id.org/time-function/testdata/before/refH'),
        ('https://w3id.org/time-function/testdata/before/xJ',
        'https://w3id.org/time-function/testdata/before/refI'),
        ('https://w3id.org/time-function/testdata/before/xJ',
        'https://w3id.org/time-function/testdata/before/refJ')
    ]

    actual = sorted([
        (str(r[0]), str(r[1]))
        for r in g.query(
            q,
            initNs={"time": TIME, "tfun": TFUN}
        )
    ])

    assert actual == expected
