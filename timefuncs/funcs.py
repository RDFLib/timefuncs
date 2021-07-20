from rdflib import Literal, TIME
from rdflib.paths import ZeroOrMore


def is_before(e, ctx) -> Literal:
    """Returns Literal(true) if a is before b where 'before' is determined by all
    of the possibilities for its expression within the Time Ontology in OWL, see
    https://www.w3.org/TR/owl-time/#time:before. Returnes Literal(false) otherwise.

    Use: isBefore(a, b) in a SPARQL query, where a & b are time:TemporalEntity
    instance.

    Example:

    SELECT ?a ?b
    WHERE {
        ?a a time:TemporalEntity .
        ?b a time:TemporalEntity .

        FILTER tfun:isBefore(?a, ?b)
    }

    """
    try:
        ref = e.expr[0]
        x = e.expr[1]
    except Exception as err:
        raise ValueError(
            "This function, isBefore(a, b), requires two IRI parameters, "
            "where a & b are Time Ontology TemporalEntity instances. "
            "a is tested to be before b")

    g = ctx.ctx.graph

    if (x, TIME.hasEnd*ZeroOrMore/TIME.before, ref) in g:
        return Literal(True)

    if (ref, TIME.hasBeginning*ZeroOrMore/TIME.after, x) in g:
        return Literal(True)

    for z in g.objects(ref, TIME.hasBeginning*ZeroOrMore/TIME.after):
        if (x, TIME.hasEnd, z) in g:
            return Literal(True)

    for z in g.objects(ref, TIME.hasBeginning):
        if (x, TIME.hasEnd*ZeroOrMore/TIME.before, z) in g:
            return Literal(True)

    ref_xsds = list(g.objects(ref, TIME.hasBeginning*ZeroOrMore/TIME.inXSDDateTimeStamp))
    x_xsds = list(g.objects(x, TIME.hasEnd*ZeroOrMore/TIME.inXSDDateTimeStamp))
    if len(ref_xsds) > 0 and len(x_xsds) > 0:
        if sorted(x_xsds)[-1] < sorted(ref_xsds)[0]:
            return Literal(True)

    return Literal(False)
