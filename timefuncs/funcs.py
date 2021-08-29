"""
This file contains a list of Python functions designed to bd wrapped as SPARQL functions within
[rdflib](https://pypi.org/project/rdflib/).

These functions somewhat match predicates given in the [Time Ontology in OWL](https://www.w3.org/TR/owl-time/) which is
a [World Wide Web Consortium (W3C)](https://www.w3.org/)-recommended ontology for temporal relations in RDF/SPARQL.

The SPARQL definitions of these functions will likely be submitted to the W3C's
[Spatial Data on the Web Interest Group](https://www.w3.org/2017/sdwig/) for some form of ratification/recommendation.
This Python implementation will then serve as one of the necessary implementations for such a submission.

Nicholas J. Car, 2021-07-24
nicholas.car@anu.edu.au

Functions index
---------------

"""

from typing import List, Union, Tuple
from typing import Literal as TLiteral

from rdflib import Graph, BNode, Literal, URIRef
from rdflib.namespace import RDF, TIME
from rdflib.paths import ZeroOrMore, OneOrMore


# 1
def contains(e, ctx) -> Literal:
    """SPARQL tfun:contains(a, b)

    Returns Literal(true) if a is inside b where 'inside' is determined by all
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
            "a is tested to be inside b"
        )

    g = ctx.ctx.graph

    if (a, TIME.intervalContains * OneOrMore, b) in g:
        return Literal(True)

    if (b, TIME.intervalDuring * OneOrMore, a) in g:
        return Literal(True)

    for a_beginning in g.objects(a, TIME.hasBeginning):
        for a_end in g.objects(a, TIME.hasEnd):
            for b_beginning in g.objects(b, TIME.hasBeginning):
                for b_end in g.objects(b, TIME.hasEnd):
                    # declared
                    if (a_beginning, TIME.before, b_beginning) in g and (
                        a_end,
                        TIME.after,
                        b_end,
                    ) in g:
                        return Literal(True)
                    if (b_beginning, TIME.after, a_beginning) in g and (
                        a_end,
                        TIME.after,
                        b_end,
                    ) in g:
                        return Literal(True)
                    if (b_beginning, TIME.after, a_beginning) in g and (
                        b_end,
                        TIME.before,
                        a_end,
                    ) in g:
                        return Literal(True)
                    if (a_beginning, TIME.before, b_beginning) in g and (
                        b_end,
                        TIME.before,
                        a_end,
                    ) in g:
                        return Literal(True)

                    # calculated
                    for a_beginning_time in g.objects(
                        a_beginning,
                        TIME.inXSDDateTimeStamp | TIME.inXSDDateTime | TIME.inXSDDate,
                    ):
                        for a_end_time in g.objects(
                            a_end,
                            TIME.inXSDDateTimeStamp
                            | TIME.inXSDDateTime
                            | TIME.inXSDDate,
                        ):
                            for b_beginning_time in g.objects(
                                b_beginning,
                                TIME.inXSDDateTimeStamp
                                | TIME.inXSDDateTime
                                | TIME.inXSDDate,
                            ):
                                for b_end_time in g.objects(
                                    b_end,
                                    TIME.inXSDDateTimeStamp
                                    | TIME.inXSDDateTime
                                    | TIME.inXSDDate,
                                ):
                                    if (
                                        b_beginning_time > a_beginning_time
                                        and a_end_time > b_end_time
                                    ):
                                        return Literal(True)

    if _path_exists(
        g, a, b, [(TIME.intervalContains, "outbound"), (TIME.intervalDuring, "inbound")]
    ):
        return Literal(True)

    return Literal(False)


# 2
def finishes(e, ctx) -> Literal:
    """SPARQL tfun:finishes(a, b)

    From https://www.w3.org/TR/owl-time/#time:intervalFinishes:
    "If a proper interval T1 is intervalFinishes another proper interval T2, then the beginning of T1 is after the
    beginning of T2, and the end of T1 is coincident with the end of T2."

    Returns Literal(true) if a and be are ProperIntervals and the beginning of a is after the beginning of b,
    and the end of a is coincident with the end of b. Else returns False.

    Example:

    SELECT ?a ?b
    WHERE {
        ?a a time:ProperInterval .
        ?b a time:ProperInterval .

        FILTER tfun:finishes(?a, ?b)
    }

    tfun:finishes(a, b) is equivalent to tfun:isFinishedBy(b, a)
    """
    try:
        a = e.expr[0]
        b = e.expr[1]
    except Exception as err:
        raise ValueError(
            "This function, isInside(a, b), requires two IRI parameters, "
            "where a & b are Time Ontology Instant and Interval instances, respectively. "
            "a is tested to be inside b"
        )

    g = ctx.ctx.graph

    # a must be some form of Interval
    if (a, RDF.type, TIME.Interval) not in g and (a, RDF.type, TIME.ProperInterval) not in g:
        return Literal(False)

    # b must be some form of Interval
    if (b, RDF.type, TIME.Interval) not in g and (b, RDF.type, TIME.ProperInterval) not in g:
        return Literal(False)

    # direct or transitive declared relations
    if _path_exists(
        g, a, b, [
                (TIME.intervalFinishes, "outbound"), (TIME.intervalFinishedBy, "inbound"),
                (TIME.intervalEquals, "outbound"), (TIME.intervalEquals, "inbound")
            ]
    ):
        return Literal(True)

    # the beginning of T1 is after the beginning of T2, and the end of T1 is coincident with the end of T2
    for o in g.objects(a, TIME.hasBeginning):
        for a_beg in g.objects(o, TIME.inXSDDateTimeStamp):
            for o2 in g.objects(b, TIME.hasBeginning):
                for b_beg in g.objects(o2, TIME.inXSDDateTimeStamp):
                    for o3 in g.objects(a, TIME.hasEnd):
                        for a_end in g.objects(o3, TIME.inXSDDateTimeStamp):
                            for o4 in g.objects(b, TIME.hasEnd):
                                for b_end in g.objects(o4, TIME.inXSDDateTimeStamp):
                                    if a_beg > b_beg and a_end == b_end and a_beg < a_end and b_beg < b_end:
                                        return Literal(True)

    return Literal(False)


# 3
def has_beginning(e, ctx) -> Literal:
    """SPARQL tfun:hasBeginning(a, b)

    Returns True if a is a time:TemporalEntity and b is a time:Instant and b is the same Instant as the beginning of a.

    """
    raise NotImplementedError()


# 4
def has_during(e, ctx) -> Literal:
    """SPARQL tfun:hasDuring(a, b)

    Alias for contains"""
    return contains(e, ctx)


# 5
def has_end(e, ctx) -> Literal:
    """SPARQL tfun:hasEnd(a, b)

    """
    raise NotImplementedError()


# 6
def has_inside(e, ctx) -> Literal:
    """SPARQL tfun:hasInside(a, b)

    Returns Literal(true) if a has b inside it where 'inside' is determined by all
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
            "a is tested to have b inside it"
        )

    g = ctx.ctx.graph

    if (a, TIME.before | TIME.after, b) in g:
        return Literal(False)

    if (a, TIME.inside, b) in g:
        return Literal(True)

    for a_beginning in g.objects(a, TIME.hasBeginning * OneOrMore):
        for a_end in g.objects(a, TIME.hasEnd * OneOrMore):
            # declared
            if (b, TIME.after, a_beginning) in g and (b, TIME.before, a_end) in g:
                return Literal(True)

            # calculated
            for a_beginning_time in g.objects(
                a_beginning,
                TIME.inXSDDateTimeStamp | TIME.inXSDDateTime | TIME.inXSDDate,
            ):
                for a_end_time in g.objects(
                    a_end, TIME.inXSDDateTimeStamp | TIME.inXSDDateTime | TIME.inXSDDate
                ):
                    for b_time in g.objects(
                        b, TIME.inXSDDateTimeStamp | TIME.inXSDDateTime | TIME.inXSDDate
                    ):
                        if a_beginning_time < b_time < a_end_time:
                            return Literal(True)

    return Literal(False)


# 7
def is_after(e, ctx) -> Literal:
    """SPARQL tfun:isAfter(a, b)

    Returns Literal(true) if a is after b where 'after' is determined by all
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
            "a is tested to be before b"
        )

    g = ctx.ctx.graph

    if (a, TIME.hasBeginning * ZeroOrMore / TIME.after, b) in g:
        return Literal(True)

    if (b, TIME.hasEnd * ZeroOrMore / TIME.before, a) in g:
        return Literal(True)

    for z in g.objects(b, TIME.hasEnd * ZeroOrMore / TIME.before):
        if (a, TIME.hasBeginning, z) in g:
            return Literal(True)

    for z in g.objects(a, TIME.hasBeginning * ZeroOrMore / TIME.after):
        if (b, TIME.hasEnd, z) in g:
            return Literal(True)

    ref_xsds = list(
        g.objects(b, TIME.hasBeginning * ZeroOrMore / TIME.inXSDDateTimeStamp)
    )
    x_xsds = list(g.objects(a, TIME.hasEnd * ZeroOrMore / TIME.inXSDDateTimeStamp))
    if len(ref_xsds) > 0 and len(x_xsds) > 0:
        if sorted(x_xsds)[0] > sorted(ref_xsds)[-1]:
            return Literal(True)

    ref_xsds = list(
        g.objects(b, TIME.hasBeginning * ZeroOrMore / TIME.inXSDDate)
    )
    x_xsds = list(g.objects(a, TIME.hasEnd * ZeroOrMore / TIME.inXSDDate))
    if len(ref_xsds) > 0 and len(x_xsds) > 0:
        if sorted(x_xsds)[0] > sorted(ref_xsds)[-1]:
            return Literal(True)

    if _path_exists(g, a, b, [(TIME.after, "outbound"), (TIME.before, "inbound")]):
        return Literal(True)

    return Literal(False)


# 8
def is_before(e, ctx) -> Literal:
    """SPARQL tfun:isBefore(a, b)

    Returns Literal(true) if a is before b where 'before' is determined by all
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
            "a is tested to be before b"
        )

    g = ctx.ctx.graph

    if (a, TIME.hasEnd * ZeroOrMore / TIME.before, b) in g:
        return Literal(True)

    if (b, TIME.hasBeginning * ZeroOrMore / TIME.after, a) in g:
        return Literal(True)

    for z in g.objects(b, TIME.hasBeginning * ZeroOrMore / TIME.after):
        if (a, TIME.hasEnd, z) in g:
            return Literal(True)

    for z in g.objects(a, TIME.hasEnd * ZeroOrMore / TIME.before):
        if (b, TIME.hasBeginning, z) in g:
            return Literal(True)

    ref_xsds = list(
        g.objects(b, TIME.hasBeginning * ZeroOrMore / TIME.inXSDDateTimeStamp)
    )
    x_xsds = list(g.objects(a, TIME.hasEnd * ZeroOrMore / TIME.inXSDDateTimeStamp))
    if len(ref_xsds) > 0 and len(x_xsds) > 0:
        if sorted(x_xsds)[-1] < sorted(ref_xsds)[0]:
            return Literal(True)

    ref_xsds = list(
        g.objects(b, TIME.hasBeginning * ZeroOrMore / TIME.inXSDDate)
    )
    x_xsds = list(g.objects(a, TIME.hasEnd * ZeroOrMore / TIME.inXSDDate))
    if len(ref_xsds) > 0 and len(x_xsds) > 0:
        if sorted(x_xsds)[-1] < sorted(ref_xsds)[0]:
            return Literal(True)

    if _path_exists(g, a, b, [(TIME.before, "outbound"), (TIME.after, "inbound")]):
        return Literal(True)

    return Literal(False)


# 9
def is_finished_by(e, ctx) -> Literal:
    """SPARQL tfun:isFinishedBy(a, b)

    From https://www.w3.org/TR/owl-time/#time:intervalFinishedBy:
    "If a proper interval T1 is intervalFinishedBy another proper interval T2, then the beginning of T1 is before
    the beginning of T2, and the end of T1 is coincident with the end of T2."

    Returns Literal(true) if a and be are ProperIntervals and the beginning of b is after the beginning of a,
    and the end of b is coincident with the end of a. Else returns False.

    Example:

    SELECT ?a ?b
    WHERE {
        ?a a time:ProperInterval .
        ?b a time:ProperInterval .

        FILTER tfun:isFinishedBy(?a, ?b)
    }

    tfun:isFinishedBy(a, b) is equivalent to tfun:finishes(b, a)
    """
    try:
        a = e.expr[0]
        b = e.expr[1]
    except Exception as err:
        raise ValueError(
            "This function, isInside(a, b), requires two IRI parameters, "
            "where a & b are Time Ontology Instant and Interval instances, respectively. "
            "a is tested to be inside b"
        )

    g = ctx.ctx.graph

    # a must be some form of Interval
    if (a, RDF.type, TIME.Interval) not in g and (a, RDF.type, TIME.ProperInterval) not in g:
        return Literal(False)

    # b must be some form of Interval
    if (b, RDF.type, TIME.Interval) not in g and (b, RDF.type, TIME.ProperInterval) not in g:
        return Literal(False)

    # direct or transitive declared relations
    if _path_exists(
        g, a, b, [
                (TIME.intervalFinishedBy, "outbound"), (TIME.intervalFinishes, "inbound"),
                (TIME.intervalEquals, "outbound"), (TIME.intervalEquals, "inbound")
            ]
    ):
        return Literal(True)

    # the beginning of b is after the beginning of a, and the end of b is coincident with the end of a
    for o in g.objects(a, TIME.hasBeginning):
        for a_beg in g.objects(o, TIME.inXSDDateTimeStamp):
            for o2 in g.objects(b, TIME.hasBeginning):
                for b_beg in g.objects(o2, TIME.inXSDDateTimeStamp):
                    for o3 in g.objects(a, TIME.hasEnd):
                        for a_end in g.objects(o3, TIME.inXSDDateTimeStamp):
                            for o4 in g.objects(b, TIME.hasEnd):
                                for b_end in g.objects(o4, TIME.inXSDDateTimeStamp):
                                    if a_beg < b_beg and a_end == b_end and a_beg < a_end and b_beg < b_end:
                                        return Literal(True)

    return Literal(False)


# 10
def is_beginning_of(e, ctx) -> Literal:
    """SPARQL tfun:isBeginningOf(a, b)

    """
    raise NotImplementedError()


# 11
def is_contained_by(e, ctx) -> Literal:
    """SPARQL tfun:isContainedBy(a, b)

    Returns Literal(true) if a is contained by b where 'is contained by' is determined by all
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
            "a is tested to be inside b"
        )

    g = ctx.ctx.graph

    if (a, TIME.intervalDuring * OneOrMore, b) in g:
        return Literal(True)

    if (b, TIME.intervalContains * OneOrMore, a) in g:
        return Literal(True)

    for a_beginning in g.objects(a, TIME.hasBeginning):
        for a_end in g.objects(a, TIME.hasEnd):
            for b_beginning in g.objects(b, TIME.hasBeginning):
                for b_end in g.objects(b, TIME.hasEnd):
                    # declared
                    if (a_beginning, TIME.after, b_beginning) in g and (
                        a_end,
                        TIME.before,
                        b_end,
                    ) in g:
                        return Literal(True)
                    if (b_beginning, TIME.before, a_beginning) in g and (
                        a_end,
                        TIME.before,
                        b_end,
                    ) in g:
                        return Literal(True)
                    if (b_beginning, TIME.before, a_beginning) in g and (
                        b_end,
                        TIME.after,
                        a_end,
                    ) in g:
                        return Literal(True)
                    if (a_beginning, TIME.after, b_beginning) in g and (
                        b_end,
                        TIME.after,
                        a_end,
                    ) in g:
                        return Literal(True)

                    # calculated
                    for a_beginning_time in g.objects(
                        a_beginning,
                        TIME.inXSDDateTimeStamp | TIME.inXSDDateTime | TIME.inXSDDate,
                    ):
                        for a_end_time in g.objects(
                            a_end,
                            TIME.inXSDDateTimeStamp
                            | TIME.inXSDDateTime
                            | TIME.inXSDDate,
                        ):
                            for b_beginning_time in g.objects(
                                b_beginning,
                                TIME.inXSDDateTimeStamp
                                | TIME.inXSDDateTime
                                | TIME.inXSDDate,
                            ):
                                for b_end_time in g.objects(
                                    b_end,
                                    TIME.inXSDDateTimeStamp
                                    | TIME.inXSDDateTime
                                    | TIME.inXSDDate,
                                ):
                                    if (
                                        b_beginning_time < a_beginning_time
                                        and a_end_time < b_end_time
                                    ):
                                        return Literal(True)

    if _path_exists(
        g, a, b, [(TIME.intervalDuring, "outbound"), (TIME.intervalContains, "inbound")]
    ):
        return Literal(True)

    return Literal(False)


# 12
def is_disjoint(e, ctx) -> Literal:
    """SPARQL tfun:isDisjoint(a, b)

    """
    raise NotImplementedError()


# 13
def is_during(e, ctx) -> Literal:
    """SPARQL tfun:isDuring(a, b)

    Alias for is_contained_by"""
    return is_contained_by(e, ctx)


# 14
def is_end_of(e, ctx) -> Literal:
    """SPARQL tfun:isEndOf(a, b)

    """
    raise NotImplementedError()


# 15
def is_equals(e, ctx) -> Literal:
    """SPARQL tfun:isEquals(a, b)

    """
    raise NotImplementedError()


# 16
def is_in(e, ctx) -> Literal:
    """SPARQL tfun:isIn(a, b)

    """
    raise NotImplementedError()


# 17
def is_inside(e, ctx) -> Literal:
    """SPARQL tfun:isInside(a, b)

    Returns Literal(true) if a is inside b where 'inside' is determined by all
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
            "a is tested to be inside b"
        )

    g = ctx.ctx.graph

    if (a, TIME.before | TIME.after, b) in g:
        return Literal(False)

    if (b, TIME.inside, a) in g:
        return Literal(True)

    for b_beginning in g.objects(b, TIME.hasBeginning * OneOrMore):
        for b_end in g.objects(b, TIME.hasEnd * OneOrMore):
            # declared
            if (a, TIME.after, b_beginning) in g and (a, TIME.before, b_end) in g:
                return Literal(True)

            # calculated
            for b_beginning_time in g.objects(
                b_beginning,
                TIME.inXSDDateTimeStamp | TIME.inXSDDateTime | TIME.inXSDDate,
            ):
                for b_end_time in g.objects(
                    b_end, TIME.inXSDDateTimeStamp | TIME.inXSDDateTime | TIME.inXSDDate
                ):
                    for a_time in g.objects(
                        a, TIME.inXSDDateTimeStamp | TIME.inXSDDateTime | TIME.inXSDDate
                    ):
                        if b_beginning_time < a_time < b_end_time:
                            return Literal(True)

    return Literal(False)


# 18
def is_met_by(e, ctx) -> Literal:
    """SPARQL tfun:isMetBy(a, b)

    """
    raise NotImplementedError()


# 19
def is_not_disjoint(e, ctx) -> Literal:
    """SPARQL tfun:isNotDisjoint(a, b)

    """
    raise NotImplementedError()


# 20
def is_overlapped_by(e, ctx) -> Literal:
    """SPARQL tfun:isOverlappedBy(a, b)

    """
    raise NotImplementedError()


# 21
def is_started_by(e, ctx) -> Literal:
    """SPARQL tfun:isStartedBy(a, b)

    From https://www.w3.org/TR/owl-time/#time:intervalStarts:
    "If a proper interval T1 is intervalStartedBy another proper interval T2, then the beginning of T1 is coincident
    with the beginning of T2, and the end of T1 is after the end of T2. "

    Returns Literal(true) if a and be are ProperIntervals and the beginning of b is coincident with the beginning
    of a, and the end of b is before the end of a. Else returns False.

    Example:

    SELECT ?a ?b
    WHERE {
        ?a a time:ProperInterval .
        ?b a time:ProperInterval .

        FILTER tfun:isStartedBy(?a, ?b)
    }

    tfun:isStartedBy(a, b) is equivalent to tfun:starts(b, a)
    """
    try:
        a = e.expr[0]
        b = e.expr[1]
    except Exception as err:
        raise ValueError(
            "This function, isInside(a, b), requires two IRI parameters, "
            "where a & b are Time Ontology Instant and Interval instances, respectively. "
            "a is tested to be inside b"
        )

    g = ctx.ctx.graph

    # a must be some form of Interval
    if (a, RDF.type, TIME.Interval) not in g and (a, RDF.type, TIME.ProperInterval) not in g:
        return Literal(False)

    # b must be some form of Interval
    if (b, RDF.type, TIME.Interval) not in g and (b, RDF.type, TIME.ProperInterval) not in g:
        return Literal(False)

    # direct or transitive declared relations
    if _path_exists(
        g, a, b, [
                (TIME.intervalStartedBy, "outbound"), (TIME.intervalStarts, "inbound"),
                (TIME.intervalEquals, "outbound"), (TIME.intervalEquals, "inbound")
            ]
    ):
        return Literal(True)

    # the beginning of a is coincident with the beginning of b, and the end of a is before the end of b
    for o in g.objects(a, TIME.hasBeginning):
        for a_beg in g.objects(o, TIME.inXSDDateTimeStamp):
            for o2 in g.objects(b, TIME.hasBeginning):
                for b_beg in g.objects(o2, TIME.inXSDDateTimeStamp):
                    for o3 in g.objects(a, TIME.hasEnd):
                        for a_end in g.objects(o3, TIME.inXSDDateTimeStamp):
                            for o4 in g.objects(b, TIME.hasEnd):
                                for b_end in g.objects(o4, TIME.inXSDDateTimeStamp):
                                    if a_beg == b_beg and a_end < b_end and a_beg < a_end and b_beg < b_end:
                                        return Literal(True)

    return Literal(False)


# 22
def meets(e, ctx) -> Literal:
    """SPARQL tfun:meets(a, b)

    """
    raise NotImplementedError()


# 23
def overlaps(e, ctx) -> Literal:
    """SPARQL tfun:overlaps(a, b)

    """
    raise NotImplementedError()


# 24
def starts(e, ctx) -> Literal:
    """SPARQL tfun:starts(a, b)

    From https://www.w3.org/TR/owl-time/#time:intervalStarts:
    "If a proper interval T1 is intervalStarts another proper interval T2, then the beginning of T1 is coincident
    with the beginning of T2, and the end of T1 is before the end of T2. "

    Returns Literal(true) if a and be are ProperIntervals and the beginning of a is coincident with the beginning
    of b, and the end of a is before the end of b. Else returns False.

    Example:

    SELECT ?a ?b
    WHERE {
        ?a a time:ProperInterval .
        ?b a time:ProperInterval .

        FILTER tfun:starts(?a, ?b)
    }

    tfun:starts(a, b) is equivalent to tfun:isStartedBy(b, a)
    """
    try:
        a = e.expr[0]
        b = e.expr[1]
    except Exception as err:
        raise ValueError(
            "This function, isInside(a, b), requires two IRI parameters, "
            "where a & b are Time Ontology Instant and Interval instances, respectively. "
            "a is tested to be inside b"
        )

    g = ctx.ctx.graph

    # a must be some form of Interval
    if (a, RDF.type, TIME.Interval) not in g and (a, RDF.type, TIME.ProperInterval) not in g:
        return Literal(False)

    # b must be some form of Interval
    if (b, RDF.type, TIME.Interval) not in g and (b, RDF.type, TIME.ProperInterval) not in g:
        return Literal(False)

    # direct or transitive declared relations
    if _path_exists(
        g, a, b, [
                (TIME.intervalStarts, "outbound"), (TIME.intervalStartedBy, "inbound"),
                (TIME.intervalEquals, "outbound"), (TIME.intervalEquals, "inbound")
            ]
    ):
        return Literal(True)

    # the beginning of a is coincident with the beginning of b, and the end of a is before the end of b
    for o in g.objects(a, TIME.hasBeginning):
        for a_beg in g.objects(o, TIME.inXSDDateTimeStamp):
            for o2 in g.objects(b, TIME.hasBeginning):
                for b_beg in g.objects(o2, TIME.inXSDDateTimeStamp):
                    for o3 in g.objects(a, TIME.hasEnd):
                        for a_end in g.objects(o3, TIME.inXSDDateTimeStamp):
                            for o4 in g.objects(b, TIME.hasEnd):
                                for b_end in g.objects(o4, TIME.inXSDDateTimeStamp):
                                    if a_beg == b_beg and a_end < b_end and a_beg < a_end and b_beg < b_end:
                                        return Literal(True)

    return Literal(False)


def _path_exists(
    g: Graph,
    a: Union[URIRef, BNode],
    b: Union[URIRef, BNode],
    predicates: List[Tuple[URIRef, TLiteral["outbound", "inbound"]]],
) -> bool:
    """Finds if any path between RDF nodes a and b in graph g exists,
    following any of the predicates supplied, in any order.

    This function is a support function for the named TIME functions such as is_before."""

    if a == b:
        return False

    def _get_next_nodes(node, preds):
        """Finds any nodes linked to a given node, 'node' via any of the given predicates 'pred'.

        Looks for both s pred o and o pred s (inverse)"""
        next_nodes = []

        for p in preds:
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
