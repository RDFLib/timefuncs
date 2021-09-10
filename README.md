# RDFlib OWL TIME Functions

This Python package implements functions to ascertain the temporal relations of objects in RDF graphs.

This package invents SPARQL functions that are based on logic provided in [OWL TIME](https://www.w3.org/TR/owl-time/) and are named similarly to TIME's Temporal Entity's predicates, for example, the function `isBefore()` correlates to `time:before`, i.e. `isBefore(a, b)` will test to see if `time:before` should be applied between object `a` & `b`.

The functions are made available as functions in [RDFlib](https://pypi.org/project/rdflib/)'s SPARQL implementation where they can be called by IRI, e.g. `isBefore(a, b)` is called `tfun:isBefore(?a, ?b)`. All functions are posed as questions, "is before", and return an RDF literal `true` or `false`.

This repository also contains a formal declaration of the functions that this package implements as a [SKOS](https://www.w3.org/TR/skos-reference/) vocabulary. See the [Vocabulary](#vocabulary) section below.


## Installation 
Normal Python package installation e.g. from PyPI: `pip install timefuncs`.

This package's only non-standard dependency is [RDFlib](https://pypi.org/project/rdflib/).


## Use
These functions are implemented in RDFlib Python in the file `timefuncts/funcs.py` and are imported into `timefuncs/__init__.py` and registered there in RDFlib as SPARQL extension functions with their IRIs.

This means they can be used like this (full working script):

```python
from rdflib import Graph
from timefuncs import TFUN


data = """
    PREFIX : <http://example.com/>
    PREFIX time: <http://www.w3.org/2006/time#>    
    
    :a01 a time:TemporalEntity .    
    :b01 a time:TemporalEntity .
    :c01 a time:TemporalEntity .
    :d01 a time:TemporalEntity .
    
    :a01 time:before :c01 .

    :b01 time:after :c01 .
    """

g = Graph().parse(data=data)

q = """
    PREFIX tfun: <https://w3id.org/timefuncs/>

    SELECT *
    WHERE {
        ?x a time:TemporalEntity .
        ?y a time:TemporalEntity .
        
        FILTER tfun:isBefore(?x, ?y)
    }
    """
for r in g.query(q):
    print(f"{r['x']} is before {r['y']}")
```
The above stript outputs:

```bash
http://example.com/a01 is before http://example.com/b01
http://example.com/a01 is before http://example.com/c01
http://example.com/b01 is before http://example.com/c01
```

The above script is run using an environment that has had the time functions registered with its copy of rdflib (perhaps by running `pip install timefuncs`) so that there is no need to import anything other than rdfib and the time functions namespace (`from timefuncs import TFUN`). It may appear that the namespace is not used but it is, internally! No need to re-declare `tfun:` as a `PREFIX` in the SPARQL query...

The time function used here, `tfun:isBefore`, is called as a filter function to return `true` when the first given object, here `?x` is _before_ the second given object, `?y`.

This example uses a pretty open-ended graph pattern match (`?x ?p ?y).

### Working with Reasoning / Inferencing
These functions don't assume that any reasoning has been carried out on data and will correctly interpret `time:before` / `time:after` and similar inverses, transitive relations (chains of properties) and so on. But there are limits: you will always be able to invent highly complex relations between `time:TemporalEntity` instances that these functions won't correctly work with. 

To work with highly complex data, try reasoning over your data first with OWL TIME's axioms before running these functions. To do this, you need a tool that can calculate OWL "RL" inferences, such as [rdflib's OWL-RL](https://github.com/RDFLib/OWL-RL). Many triplestores have OWL-RL reasoning capability built-in or as add ons.

## Functions
Functions in this package are implemented as SPARQL extension functions with the namespace `https://w3id.org/timefuncs/`, e.g. `isBefore()`'s full IRI is `https://w3id.org/timefuncs/isBefore`.

Python implementations are named the same as the SPARQL functions, but in snake_case, not camelCase, e.g. SPARQL's `isBefore()` is implemented in Python's `is_before()`.

Functions implemented so far, and their corresponding TIME relations:

**SPARQL** | **Parameters** | **TIME predicates** | **Notes**
--- | --- | --- | ---
`tfun:contains(a, b)` | `time:Interval`<br />`time:Interval` | `time:intervalContains`<br />inv. `time:intervalDuring` | equivalent to `tfun:isContainedBy(b, a)`
`tfun:finishes(a, b)` | `time:Interval`<br />`time:Interval` | `time:intervalFinishes`<br />inv. `time:intervalFinishedBy`<br />not `time:disjoint` | equivalent to `tfun:isFinishedBy(b, a)`
`tfun:hasDuring(a, b)` | `time:Interval`<br />`time:Interval` | | alias for `contains(a, b)`
`tfun:hasInside(a, b)` | `time:Interval`<br />`time:Instant` | `time:inside`<br />not `time:before`<br />not `time:after` | equivalent to `tfun:isInside(b, a)`
`tfun:isAfter(a, b)` | `time:TemporalEntity`<br />`time:TemporalEntity` | `time:after`<br />inv. `time:before` | equivalent to `tfun:isBefore(b, a)`
`tfun:isBefore(a, b)` | `time:TemporalEntity`<br />`time:TemporalEntity` | `time:before`<br />inv. `time:after` | equivalent to `tfun:isAfter(b, a)`
`tfun:isContainedBy(a, b)` | `time:Interval`<br />`time:Interval` | `time:intervalDuring`<br />inv. `time:intervalContains` | equivalent to `tfun:contains(b, a)`
`tfun:isDuring(a, b)` | `time:Interval`<br />`time:Interval` | | alias for `isContainedBy(a, b)`
`tfun:isFinishedBy(a, b)` | `time:Interval`<br />`time:Interval` | `time:intervalFinishedBy`<br />inv. `time:intervalFinishes`<br />not `time:disjoint` | equivalent to `tfun:finishes(b, a)`
`tfun:isInside(a, b)` | `time:Instant`<br />`time:Interval` | inv. `time:inside`<br />not `time:after`<br />not `time:before` | equivalent to `tfun:hasInside(b, a)`
`tfun:isStartedBy(a, b)` | `time:Interval`<br />`time:Interval` | `time:isStartedBy`<br />inv. `time:starts` | `tfun:starts(b, a)` 
`tfun:starts(a, b)` | `time:Interval`<br />`time:Interval` | `time:starts`<br />inv. `time:isStartedBy` | `tfun:isStartedBy(b, a)` 
    
These functions are yet to be implemented:

**SPARQL** | **Notes**
--- | ---
`tfun:hasBeginning(a, b)` | 
`tfun:hasEnd(a, b)` | 
`tfun:isFinishedBy(a, b)` | 
`tfun:isBeginningOf(a, b)` | 
`tfun:isDisjoint(a, b)` | 
`tfun:isEndOf(a, b)` | 
`tfun:isEquals(a, b)` | 
`tfun:isIn(a, b)` | 
`tfun:isMetBy(a, b)` | 
`tfun:isNotDisjoint(a, b)` | 
`tfun:isOverlappedBy(a, b)` | 
`tfun:isStartedBy(a, b)` | 
`tfun:meets(a, b)` | 
`tfun:overlaps(a, b)` |

### Non-TIME functions
The following _proposed_ functions are inspired by OWL TIME but not directly related to its predicates or classes:

**SPARQL** | **Notes**
--- | ---
`tfun:hasTemporalRelation(a, b)` | Returns the temporal relation between `a` & `b`<br />May have to run sequences of the other `isDisjoint(a, b)` functions to determine
`tfun:toUNIXTime(a)` | Returns a UNIX Time representation of a `xsd:dateTime` or `xsd:dateTimeStamp`<br />May be extended for other TRS inputs
`tfun:toXSDDateTimeStamp(a)` | Returns an XSD `xsd:dateTimeStamp` (UTC) representation of a UNIX time<br />May be extended for other TRS inputs

  
### Implementation logic
Functions implemented test for every conceivable way that a temporal relation may be found to be true in given data. For example, `isBefore(a, b)` will return true if:

* the predicate `time:before` is given between `a` & `b`, or any chain of objects `a` ... `n` ... `b`
* the predicate `time:after` is given between `b` & `a`, or any chain of objects `b` ... `n` ... `a`
* any chain of `time:before` & `time:after` links `a` & `b`, all pointing in the right directions
* the end of `a` is declared as being before `b` or the start of `b`
    * i.e.  for `<a> time:hasEnd <a_end> .` and `<b> time:hasBeginning <b_beginning> .`, `isBefore(a, b)` is `true` if `<a_end> time:before <b_beginning>`
* the start of `b` is declared as being after `a` or the end of `a`
* `a` can be calculated as being before `b`, based on their instantaneous times or start and end times
    * i.e. for `<a> time:inXSDDateTimeStamp <a_xsd> .` and `<b> time:inXSDDateTimeStamp <b_xsd> .` or  `<a> time:hasEnd/time:inXSDDateTimeStamp <a_xsd> .` and `<b> time:hasEnd/time:inXSDDateTimeStamp <b_xsd> .`, `isBefore(a, b)` is `true` if `<a_xsd> <b_xsd>`


## Vocabulary
The time functions, both implemented and to-be implemented, are listed in a SKOS vocabulary, the source files for which are given in the [voc/](voc/) folder within this repository. The vocabulary is presented online in both RDF (turtle) and HTML (Markdown) formats from these source files, accessible via the namespace IRI:

* <https://w3id.org/timefuncs/voc> - HTML
* <https://w3id.org/timefuncs/voc.ttl> - RDF

Each function's IRI resolves to its Concept entry in the vocbaulary, for example, <https://w3id.org/timefuncs/isContainedBy> --> <https://github.com/RDFLib/timefuncs/blob/master/voc/timefuncs.md#is-contained-by>.

_(The Markdown is auto-generated from the RDF using [pyLODE](https://github.com/rdflib/pyLODE/))_

## Testing
All tests are in `tests/` and implemented using [pytest](https://pypi.org/project/pytest/).

There are individual tests for each function, e.g. `tests/test_is_before.py` for `isBefore()` as well as a test file to rn all tests againts OWL TIME's [test suite](https://github.com/w3c/sdw/tree/gh-pages/time/test-suite)): `tests/test_test_suite.py`.


## Contributing
Via GitHub, Issues & Pull Requests: 

* <https://github.com/rdflib/timefuncs>


## License
This code is licensed with the BSD 3-clause license as per [LICENSE](LICENSE) which is the same license as used for [rdflib](https://pypi.org/project/rdflib/).


## Citation
```bibtex
@software{https://github.com/rdflib/timefuncs,
  author = {{Nicholas J. Car}},
  title = {RDFlib OWL TIME Functions},
  version = {0.0.2},
  date = {2021},
  url = {https://github.com/rdflib/timefuncs}
}
```

## Contact
_Creator & maintainer:_  
**Nicholas J. Car**  
_Data System Architect_  
[SURROUND Australia Pty Ltd](https://surroundaustralia.com)  
<nicholas.car@surroundaustrlaia.com>  
and  
_Adjunct Senior Lecturer_  
College of Engineering & Computer Science  
Australian National University  
<nicholas.car@anu.edu.au>  

https://orcid.org/0000-0002-8742-7730