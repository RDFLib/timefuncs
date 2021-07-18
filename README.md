# RDFlib OWL TIME Functions

This Python package implements functions to ascertain the temporal relations of objects in RDF graphs.

This package invents SPARQL functions that are based on logic provided in [OWL TIME](https://www.w3.org/TR/owl-time/) and are named similarly to TIME's relations, for example:

* **`isBefore(x, y)`** 
    * determines if the `Temporal Entity` `x` is before `Temporal Entity` `y` by determining if: 
        * the predicate `time:before` is given between `x` & `y` or
        * the predicate `time:after` is given between `y` & `x` or
        * the end of `x` is declared as being before `y` or the start of `y`
            * i.e.  for `<x> time:hasEnd <x_end> .` and `<y> time:hasBeginning <y_beginning> .`, `isBefore(x, y)` is `true` if `<x_end> time:before <y_beginning>`
        * the start of `y` is declared as being after `x` or the end of `x`
        * `x` can be calculated as being before `y`, based on their instantaneous times or start and end times
            * i.e. for `<x> time:inXSDDateTimeStamp <x_xsd> .` and `<y> time:inXSDDateTimeStamp <y_xsd> .` or  `<x> time:hasEnd/time:inXSDDateTimeStamp <x_xsd> .` and `<y> time:hasEnd/time:inXSDDateTimeStamp <y_xsd> .`, `isBefore(x, y)` is `true` if `<x_xsd> < <y_xsd>`
    
A pure SPARQL and an rdflib Python implementation of `isBefore()` are given in `test_isBefore_SPARQL.py` & `test_isBefore_rdflib.py` respectively.
