# RDFlib OWL TIME Functions

This Python package implements functions to ascertain the temporal relations of objects in RDF graphs.

This package invents SPARQL functions that are based on logic provided in [OWL TIME](https://www.w3.org/TR/owl-time/) and are named similarly to TIME's relations, for example:

* **`isBefore(x, y)`** 
    * determines if the predicate `time:before` is given between `x` & `y`
    * or if the end of `x`is declared as being before the start of `y`
        * i.e.  for `<x> time:hasEnd <x_end> .` and `<y> time:hasBeginning <y_beginning> .`, `isBefore(x, y)` is `true` if `<x_end> time:before <y_beginning>`
    * or if `x` can be calculated as being before `y`, based on their instantaneous times or start and end times
        * i.e. for `<x> time:inXSDDateTimeStamp <x_xsd> .` and `<y> time:inXSDDateTimeStamp <y_xsd> .` or  `<x> time:hasEnd/time:inXSDDateTimeStamp <x_xsd> .` and `<y> time:hasEnd/time:inXSDDateTimeStamp <y_xsd> .`, `isBefore(x, y)` is `true` if `<x_xsd> < <y_xsd>`    