import time
from rdflib import Graph, Literal, BNode, URIRef
from rdflib.namespace import TIME, XSD
from datetime import datetime
import re

g = Graph().parse("test-cases/time-test-individuals.ttl")
UNIX = URIRef("http://dbpedia.org/resource/Unix_time")


def _parse_inXSDDateTimeStamp(dt: str):
    # 2020-12-01T09:00:00
    try:
        return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    except:
        pass

    # 2020-12-01T09:00:00Z
    try:
        return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")
    except:
        pass

    # 2021-12-11T10:31:31+10:00
    try:
        return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S%z")
    except:
        pass

    # 2021-12-11T11:31:32.01+11:00
    try:
        return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%f%z")
    except:
        pass

    # 2021-12-11T11:31:32.01Z
    try:
        return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        pass

    return None


for s, p, o in g.triples((None, TIME.inXSDDateTimeStamp, None)):
    greg = _parse_inXSDDateTimeStamp(str(o))
    unix = time.mktime(greg.timetuple())
    bn = BNode()
    g.add((s, TIME.inTimePosition, bn))
    g.add((bn, TIME.hasTRS, UNIX))
    g.add((bn, TIME.numericPosition, Literal(round(unix), datatype=XSD.integer)))

# find all datatype objects of type xsd:dateTimeStamp, xsd:dateTime, xsd:date
# convert them to UNIX time

g.serialize(destination="time-test-individuals-unix2.ttl")
