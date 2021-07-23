from typing import List, Union, Tuple
from typing import Literal as TLiteral
from rdflib import Graph, BNode, Literal, TIME, URIRef
from rdflib.paths import ZeroOrMore, OneOrMore


def is_before(e, ctx) -> Literal:
    """Returns Literal(true) if a is before b where 'before' is determined by all
    of the possibilities for its expression within the Time Ontology in OWL, see
    https://www.w3.org/TR/owl-time/#time:before. Returns Literal(false) otherwise.

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
        a = e.expr[0]
        b = e.expr[1]
    except Exception as err:
        raise ValueError(
            "This function, isBefore(a, b), requires two IRI parameters, "
            "where a & b are Time Ontology TemporalEntity instances. "
            "a is tested to be before b")

    g = ctx.ctx.graph

    if (a, TIME.hasEnd*ZeroOrMore/TIME.before, b) in g:
        return Literal(True)

    if (b, TIME.hasBeginning*ZeroOrMore/TIME.after, a) in g:
        return Literal(True)

    for z in g.objects(b, TIME.hasBeginning*ZeroOrMore/TIME.after):
        if (a, TIME.hasEnd, z) in g:
            return Literal(True)

    for z in g.objects(a, TIME.hasEnd*ZeroOrMore/TIME.before):
        if (b, TIME.hasBeginning, z) in g:
            return Literal(True)

    ref_xsds = list(g.objects(b, TIME.hasBeginning*ZeroOrMore/TIME.inXSDDateTimeStamp))
    x_xsds = list(g.objects(a, TIME.hasEnd*ZeroOrMore/TIME.inXSDDateTimeStamp))
    if len(ref_xsds) > 0 and len(x_xsds) > 0:
        if sorted(x_xsds)[-1] < sorted(ref_xsds)[0]:
            return Literal(True)

    if _path_exists(g, a, b, [(TIME.before, "outbound"), (TIME.after, "inbound")]):
        return Literal(True)

    return Literal(False)


def is_after(e, ctx) -> Literal:
    """Returns Literal(true) if a is after b where 'after' is determined by all
    of the possibilities for its expression within the Time Ontology in OWL, see
    https://www.w3.org/TR/owl-time/#time:after. Returns Literal(false) otherwise.

    Use: isAfter(a, b) in a SPARQL query, where a & b are time:TemporalEntity
    instance.

    Example:

    SELECT ?a ?b
    WHERE {
        ?a a time:TemporalEntity .
        ?b a time:TemporalEntity .

        FILTER tfun:isAfter(?a, ?b)
    }

    """
    try:
        a = e.expr[0]
        b = e.expr[1]
    except Exception as err:
        raise ValueError(
            "This function, isAfter(a, b), requires two IRI parameters, "
            "where a & b are Time Ontology TemporalEntity instances. "
            "a is tested to be before b")

    g = ctx.ctx.graph

    if (a, TIME.hasBeginning*ZeroOrMore/TIME.after, b) in g:
        return Literal(True)

    if (b, TIME.hasEnd*ZeroOrMore/TIME.before, a) in g:
        return Literal(True)

    for z in g.objects(b, TIME.hasEnd*ZeroOrMore/TIME.before):
        if (a, TIME.hasBeginning, z) in g:
            return Literal(True)

    for z in g.objects(a, TIME.hasBeginning*ZeroOrMore/TIME.after):
        if (b, TIME.hasEnd, z) in g:
            return Literal(True)

    ref_xsds = list(g.objects(b, TIME.hasBeginning*ZeroOrMore/TIME.inXSDDateTimeStamp))
    x_xsds = list(g.objects(a, TIME.hasEnd*ZeroOrMore/TIME.inXSDDateTimeStamp))
    if len(ref_xsds) > 0 and len(x_xsds) > 0:
        if sorted(x_xsds)[0] > sorted(ref_xsds)[-1]:
            return Literal(True)

    if _path_exists(g, a, b, [(TIME.after, "outbound"), (TIME.before, "inbound")]):
        return Literal(True)

    return Literal(False)


def has_inside(e, ctx) -> Literal:
    """Returns Literal(true) if a has b inside it where 'inside' is determined by all
    of the possibilities for its expression within the Time Ontology in OWL, see
    https://www.w3.org/TR/owl-time/#time:inside. Returns Literal(false) otherwise.

    Note that this function is couched in reverse terms to is_inside() and that is_inside() has no correlating
    predicate in OWL TIME

    Use: hasInside(a, b) in a SPARQL query, where a is a time:Interval and b is a time:Instant instance.

    Example:

    SELECT ?a ?b
    WHERE {
        ?a a time:Interval .
        ?b a time:Instant .

        FILTER tfun:hasInside(?a, ?b)
    }

    """
    try:
        a = e.expr[0]
        b = e.expr[1]
    except Exception as err:
        raise ValueError(
            "This function, hasInside(a, b), requires two IRI parameters, "
            "where a & b are Time Ontology Interval and Instant instances, respectively. "
            "a is tested to have b inside it")

    g = ctx.ctx.graph

    if (a, TIME.before | TIME.after, b) in g:
        return Literal(False)

    if (a, TIME.inside, b) in g:
        return Literal(True)

    for a_beginning in g.objects(a, TIME.hasBeginning*OneOrMore):
        for a_end in g.objects(a, TIME.hasEnd*OneOrMore):
            # declared
            if (b, TIME.after, a_beginning) in g and (b, TIME.before, a_end) in g:
                return Literal(True)

            # calculated
            for a_beginning_time in g.objects(a_beginning, TIME.inXSDDateTimeStamp | TIME.inXSDDateTime | TIME.inXSDDate):
                for a_end_time in g.objects(a_end, TIME.inXSDDateTimeStamp | TIME.inXSDDateTime | TIME.inXSDDate):
                    for b_time in g.objects(b, TIME.inXSDDateTimeStamp | TIME.inXSDDateTime | TIME.inXSDDate):
                        if a_beginning_time < b_time < a_end_time:
                            return Literal(True)

    return Literal(False)


def is_inside(e, ctx) -> Literal:
    """Returns Literal(true) if a is inside b where 'inside' is determined by all
    of the possibilities for its expression within the Time Ontology in OWL, see
    https://www.w3.org/TR/owl-time/#time:inside. Returns Literal(false) otherwise.

    Note that this function is couched in reverse terms to has_inside() and that this function has no correlating
    predicate in OWL TIME

    Use: isInside(a, b) in a SPARQL query, where a is a time:Instant and b is a time:Interval instance.

    Example:

    SELECT ?a ?b
    WHERE {
        ?a a time:Interval .
        ?b a time:Instant .

        FILTER tfun:isInside(?a, ?b)
    }

    """
    try:
        a = e.expr[0]
        b = e.expr[1]
    except Exception as err:
        raise ValueError(
            "This function, isInside(a, b), requires two IRI parameters, "
            "where a & b are Time Ontology Instant and Interval instances, respectively. "
            "a is tested to be inside b")

    g = ctx.ctx.graph

    if (a, TIME.before | TIME.after, b) in g:
        return Literal(False)

    if (b, TIME.inside, a) in g:
        return Literal(True)

    for b_beginning in g.objects(b, TIME.hasBeginning*OneOrMore):
        for b_end in g.objects(b, TIME.hasEnd*OneOrMore):
            # declared
            if (a, TIME.after, b_beginning) in g and (a, TIME.before, b_end) in g:
                return Literal(True)

            # calculated
            for b_beginning_time in g.objects(b_beginning, TIME.inXSDDateTimeStamp | TIME.inXSDDateTime | TIME.inXSDDate):
                for b_end_time in g.objects(b_end, TIME.inXSDDateTimeStamp | TIME.inXSDDateTime | TIME.inXSDDate):
                    for a_time in g.objects(a, TIME.inXSDDateTimeStamp | TIME.inXSDDateTime | TIME.inXSDDate):
                        if b_beginning_time < a_time < b_end_time:
                            return Literal(True)

    return Literal(False)


def is_contained_by(e, ctx) -> Literal:
    """Returns Literal(true) if a is contained by b where 'is contained by' is determined by all
    of the possibilities for calculating the predicate `time:intervalDuring` in the Time Ontology in
    OWL, see https://www.w3.org/TR/owl-time/#time:intervalDuring. Returns Literal(false) otherwise.

    Note that this function calculates the inverse to the function contains().

    Use: isContainedBy(a, b) in a SPARQL query, where a and b are time:ProperInterval instances.

    Example:

    SELECT ?a ?b
    WHERE {
        ?a a time:ProperInterval .
        ?b a time:ProperInterval .

        FILTER tfun:isContainedBy(?a, ?b)
    }

    """
    try:
        a = e.expr[0]
        b = e.expr[1]
    except Exception as err:
        raise ValueError(
            "This function, isInside(a, b), requires two IRI parameters, "
            "where a & b are Time Ontology Instant and Interval instances, respectively. "
            "a is tested to be inside b")

    g = ctx.ctx.graph

    # for a, b in g.subject_objects(TIME.intervalDuring):
    #     print(a, b)
    #     g.add((b, TIME.intervalContains, a))
    #
    # print("------")
    # for a, b in g.subject_objects(TIME.intervalContains):
    #     print(a, b)
    #     g.add((b, TIME.intervalDuring, a))

    if (a, TIME.intervalDuring*OneOrMore, b) in g:
        return Literal(True)

    if (b, TIME.intervalContains*OneOrMore, a) in g:
        return Literal(True)

    if (a, TIME.intervalDuring*OneOrMore, b) in g:
        return Literal(True)

    if (b, TIME.intervalContains*OneOrMore, a) in g:
        return Literal(True)

    for a_beginning in g.objects(a, TIME.hasBeginning):
        for a_end in g.objects(a, TIME.hasEnd):
            for b_beginning in g.objects(b, TIME.hasBeginning):
                for b_end in g.objects(b, TIME.hasEnd):
                    # declared
                    if (a_beginning, TIME.after, b_beginning) in g and (a_end, TIME.before, b_end) in g:
                        return Literal(True)
                    if (b_beginning, TIME.before, a_beginning) in g and (a_end, TIME.before, b_end) in g:
                        return Literal(True)
                    if (b_beginning, TIME.before, a_beginning) in g and (b_end, TIME.after, a_end) in g:
                        return Literal(True)
                    if (a_beginning, TIME.after, b_beginning) in g and (b_end, TIME.after, a_end) in g:
                        return Literal(True)

                    # calculated
                    for a_beginning_time in g.objects(
                            a_beginning,
                            TIME.inXSDDateTimeStamp | TIME.inXSDDateTime | TIME.inXSDDate):
                        for a_end_time in g.objects(
                                a_end,
                                TIME.inXSDDateTimeStamp | TIME.inXSDDateTime | TIME.inXSDDate):
                            for b_beginning_time in g.objects(
                                    b_beginning,
                                    TIME.inXSDDateTimeStamp | TIME.inXSDDateTime | TIME.inXSDDate):
                                for b_end_time in g.objects(
                                        b_end,
                                        TIME.inXSDDateTimeStamp | TIME.inXSDDateTime | TIME.inXSDDate):
                                    if b_beginning_time < a_beginning_time and a_end_time < b_end_time:
                                        return Literal(True)

    if _path_exists(g, a, b, [(TIME.intervalDuring, "outbound"), (TIME.intervalContains, "inbound")]):
        return Literal(True)

    return Literal(False)


def contains(e, ctx) -> Literal:
    """Returns Literal(true) if a is inside b where 'inside' is determined by all
    of the possibilities for its expression within the Time Ontology in OWL, see
    https://www.w3.org/TR/owl-time/#time:inside. Returns Literal(false) otherwise.

    Note that this function is couched in reverse terms to has_inside() and that this function has no correlating
    predicate in OWL TIME

    Use: isInside(a, b) in a SPARQL query, where a is a time:Instant and b is a time:Interval instance.

    Example:

    SELECT ?a ?b
    WHERE {
        ?a a time:Interval .
        ?b a time:Instant .

        FILTER tfun:isInside(?a, ?b)
    }

    """
    try:
        a = e.expr[0]
        b = e.expr[1]
    except Exception as err:
        raise ValueError(
            "This function, isInside(a, b), requires two IRI parameters, "
            "where a & b are Time Ontology Instant and Interval instances, respectively. "
            "a is tested to be inside b")

    g = ctx.ctx.graph


def is_during(e, ctx) -> Literal:
    """Returns Literal(true) if a is inside b where 'inside' is determined by all
    of the possibilities for its expression within the Time Ontology in OWL, see
    https://www.w3.org/TR/owl-time/#time:inside. Returns Literal(false) otherwise.

    Note that this function is couched in reverse terms to has_inside() and that this function has no correlating
    predicate in OWL TIME

    Use: isInside(a, b) in a SPARQL query, where a is a time:Instant and b is a time:Interval instance.

    Example:

    SELECT ?a ?b
    WHERE {
        ?a a time:Interval .
        ?b a time:Instant .

        FILTER tfun:isInside(?a, ?b)
    }

    """
    try:
        a = e.expr[0]
        b = e.expr[1]
    except Exception as err:
        raise ValueError(
            "This function, isInside(a, b), requires two IRI parameters, "
            "where a & b are Time Ontology Instant and Interval instances, respectively. "
            "a is tested to be inside b")

    g = ctx.ctx.graph


def has_during(e, ctx) -> Literal:
    """Returns Literal(true) if a is inside b where 'inside' is determined by all
    of the possibilities for its expression within the Time Ontology in OWL, see
    https://www.w3.org/TR/owl-time/#time:inside. Returns Literal(false) otherwise.

    Note that this function is couched in reverse terms to has_inside() and that this function has no correlating
    predicate in OWL TIME

    Use: isInside(a, b) in a SPARQL query, where a is a time:Instant and b is a time:Interval instance.

    Example:

    SELECT ?a ?b
    WHERE {
        ?a a time:Interval .
        ?b a time:Instant .

        FILTER tfun:isInside(?a, ?b)
    }

    """
    try:
        a = e.expr[0]
        b = e.expr[1]
    except Exception as err:
        raise ValueError(
            "This function, isInside(a, b), requires two IRI parameters, "
            "where a & b are Time Ontology Instant and Interval instances, respectively. "
            "a is tested to be inside b")

    g = ctx.ctx.graph


def _path_exists(
        g: Graph,
        a: Union[URIRef, BNode],
        b: Union[URIRef, BNode],
        predicates: List[Tuple[URIRef, TLiteral["outbound", "inbound"]]]) -> bool:
    """Finds if any path between RDF nodes a and b in graph g exists,
    following any of the predicates supplied, in any order"""

    if a == b:
        return False

    def _get_next_nodes(node, preds):
        """Finds any nodes linked to a given node, 'node' via any of the given predicates 'pred'.

        Looks for both s pred o and o pred s (inverse)"""
        next_nodes = []

        for p in preds:
            print(p)
            if p[1] == "outbound":
                for o in g.objects(subject=node, predicate=p[0]):
                    next_nodes.append(o)
            elif p[1] == "inbound":
                for s in g.subjects(predicate=p[0], object=node):
                    next_nodes.append(s)

        return next_nodes

    # standard breadth-first search
    def bfs(node):
        visited = []
        queue = []
        visited.append(node)
        queue.append(node)

        while queue:
            s = queue.pop(0)
            for x in _get_next_nodes(s, predicates):
                if x == b:
                    return True
                if x not in visited:
                    visited.append(x)
                    queue.append(x)
        return False

    return bfs(a)
