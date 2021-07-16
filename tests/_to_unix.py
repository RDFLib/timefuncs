import time
from dateutil.parser import parse
from rdflib import Graph, Literal, BNode, URIRef
from rdflib.namespace import RDF, TIME, XSD

g = Graph().parse("time-test-individuals.ttl")
UNIX = URIRef("http://dbpedia.org/resource/Unix_time")


for s, p, o in g.triples((None, TIME.inXSDDateTimeStamp, None)):
    greg = parse(str(o))
    unix = time.mktime(greg.timetuple())
    bn = BNode()
    g.add((s, TIME.inTimePosition, bn))
    g.add((bn, TIME.hasTRS, UNIX))
    g.add((bn, TIME.numericPosition, Literal(round(unix), datatype=XSD.integer)))

# find all datatype objects of type xsd:dateTimeStamp, xsd:dateTime, xsd:date
# convert them to UNIX time

g.serialize(destination="time-test-individuals-unix2.ttl")
