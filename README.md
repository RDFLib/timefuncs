# RDFlib OWL TIME Functions

This Python package implements functions to ascertain the temporal relations of objects in RDF graphs.

This package invents SPARQL functions that are based on logic provided in [OWL TIME](https://www.w3.org/TR/owl-time/) and are named similarly to TIME's Temporal Entity's predicates, for example, the function `isBefore()` correlates to `time:before`, i.e. `isBefore(a, b)` will test to see if `time:before` should be applied between object `a` & `b`.

The functions are made available as functions in [RDFlib](https://pypi.org/project/rdflib/)'s SPARQL implementation where they can be called by IRI, e.g. `isBefore(a, b)` is called `tfun:isBefore(?a, ?b)`. All functions are posed as questions, "is before", and return an RDF literal `true` or `false`.


## Installation 
Normal installation e.g. from PyPI: `pip install timefuncs`.

This package's only dependency is [RDFlib](https://pypi.org/project/rdflib/).


## Use
These functions are implemented in RDFlib Python in the file `timefuncts/funcs.py` and are imported into `timefuncs/__init__.py` and registered there in RDFlib as SPARQL extension functions with their IRIs.

This means they can be used like this (full working script):

```python
from rdflib import Graph
from timefuncs import TFUN

data = """
    PREFIX : <http://example.com/>
    PREFIX time: <http://www.w3.org/2006/time#>    
    
    :a01 time:before :b01 . 
    
    :a02 time:after :b02 .
    """

g = Graph().parse(data=data)

q = """
    SELECT *
    WHERE {
        ?x ?p ?y .
        FILTER tfun:isBefore(?x, ?y)
    }
    """
for r in g.query(q, initNs={"tfun": TFUN}):
    print(f"{r['x']} is before {r['y']}")

# prints: http://example.com/a01 is before http://example.com/b0
```

## Functions
These functions are implemented as SPARQL extension functions with the namespace `https://w3id.org/timefuncs/`, e.g. `isBefore()`'s full IRI is `https://w3id.org/timefuncs/isBefore`.

Functions implemented so far, and their corresponding TIME relations:

* `tfun:contains()`
    * `time:intervalBefore`
* `tfun:hasDuring()`
    * alias for `contains()`
* `tfun:hasInside()`
    * `time:intervalBefore`
* `tfun:isAfter()`
    * `time:after`
* `tfun:isBefore()`
    * `time:before`
* `tfun:isContainedBy()`
    * `time:intervalBefore`
* `tfun:isDuring()`
    * alias for `isContainedBy()`
* `tfun:isInside()`
    * `time:inside`
    
These functions are yet to be implemented:

* `tfun:isDisjoint()`
    * `time:intervalDisjoint`
* `tfun:isIn()`
    * `time:intervalIn`
    

### Implementation logic
Functions are implemented to test for every conceivable way that they may be found to be true in data. For example, `isBefore(a, b)` will return true if:

* the predicate `time:before` is given between `a` & `b`, or any chain of objects `a` ... `n` ... `b`
* the predicate `time:after` is given between `b` & `a`, or any chain of objects `b` ... `n` ... `a`
* any chain of `time:before` & `time:after` links `a` & `b`, all pointing in the right directions
* the end of `a` is declared as being before `b` or the start of `b`
    * i.e.  for `<a> time:hasEnd <a_end> .` and `<b> time:hasBeginning <b_beginning> .`, `isBefore(a, b)` is `true` if `<a_end> time:before <b_beginning>`
* the start of `b` is declared as being after `a` or the end of `a`
* `a` can be calculated as being before `b`, based on their instantaneous times or start and end times
    * i.e. for `<a> time:inXSDDateTimeStamp <a_xsd> .` and `<b> time:inXSDDateTimeStamp <b_xsd> .` or  `<a> time:hasEnd/time:inXSDDateTimeStamp <a_xsd> .` and `<b> time:hasEnd/time:inXSDDateTimeStamp <b_xsd> .`, `isBefore(a, b)` is `true` if `<a_xsd> <b_xsd>`


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