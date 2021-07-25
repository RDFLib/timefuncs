Markdown documentation created by [pyLODE](http://github.com/rdflib/pyLODE) 

# OWL TIME Functions
### A taxonomy

## Metadata
* **URI**
  * `https://w3id.org/timefuncs/voc`
* **Publisher(s)**
  * [Nicholas J. Car](https://orcid.org/0000-0002-8742-7730)
    [[0000-0002-8742-7730](https://orcid.org/0000-0002-8742-7730)]
    [nicholas.car@anu.edu.au](nicholas.car@anu.edu.au) of [SURROUND Australia Pty Ltd](https://surroundaustralia.com)
* **Creators(s)**
  * [Nicholas J. Car](https://orcid.org/0000-0002-8742-7730)
    [[0000-0002-8742-7730](https://orcid.org/0000-0002-8742-7730)]
    [nicholas.car@anu.edu.au](nicholas.car@anu.edu.au) of [SURROUND Australia Pty Ltd](https://surroundaustralia.com)
* **Created**
  * 2021-07-25
* **Modified**
  * 2021-07-25
* **Version Information**
  * 0.1.0

* **Taxonomy RDF**
  * RDF ([timefuncs.ttl](turtle))
### Description
SPARQL functions for testing relations between Temporal Entities as defined by the Time Ontology in OWL.


## Table of Contents
1. [Object Concepts](#concepts)
1. [Namespaces](#namespaces)
1. [Legend](#legend)


## Overview

**Figure 1:** Ontology overview
## Concepts
* [contains](https://w3id.org/timefuncs/contains) (con)
* [hasDuring](https://w3id.org/timefuncs/hasDuring) (con)
* [hasInside](https://w3id.org/timefuncs/hasInside) (con)
* [isAfter](https://w3id.org/timefuncs/isAfter) (con)
* [isBefore](https://w3id.org/timefuncs/isBefore) (con)
* [isContainedBy](https://w3id.org/timefuncs/isContainedBy) (con)
* [isDuring](https://w3id.org/timefuncs/isDuring) (con)
* [isInside](https://w3id.org/timefuncs/isInside) (con)

### Contains
Property | Value
--- | ---
URI | `https://w3id.org/timefuncs/contains`
Preferred Labels |Contains (en)<br />
Definitions |A function accepting two Proper Interval parameters, a & b, testing testing whether a contains b with 'contains' defined as per time:intervalContains. Returns a boolean, true if a contains b.<br />
### Has During
Property | Value
--- | ---
URI | `https://w3id.org/timefuncs/hasDuring`
Preferred Labels |Has During (en)<br />
Definitions |A synonym for `contains`.<br />
### Has Inside
Property | Value
--- | ---
URI | `https://w3id.org/timefuncs/hasInside`
Preferred Labels |Has Inside (en)<br />
Definitions |A function accepting an Interval a and an Instant b, testing testing whether the Interval contains the Instant, as per time:inside. Returns a boolean, true if a contains b.<br />
### Is After
Property | Value
--- | ---
URI | `https://w3id.org/timefuncs/isAfter`
Preferred Labels |Is After (en)<br />
Definitions |A function accepting two Temporal Entity parameters, a & b, testing testing whether a is after b with 'after' defined as per time:after. Returns a boolean, true if a is after b.<br />
### Is Before
Property | Value
--- | ---
URI | `https://w3id.org/timefuncs/isBefore`
Preferred Labels |Is Before (en)<br />
Definitions |A function accepting two Temporal Entity parameters, a & b, testing testing whether a is before b with 'before' defined as per time:after. Returns a boolean, true if a is before b.<br />
### Is Contained By
Property | Value
--- | ---
URI | `https://w3id.org/timefuncs/isContainedBy`
Preferred Labels |Is Contained By (en)<br />
Definitions |A function accepting two Proper Interval parameters, a & b, testing testing whether a is contained by b with 'is contained by' defined as per 'intervalDuring' by time:intervalDuring. Returns a boolean, true if a is contained by b.<br />
### Is During
Property | Value
--- | ---
URI | `https://w3id.org/timefuncs/isDuring`
Preferred Labels |Is During (en)<br />
Definitions |A synonym for `isContainedBy`.<br />
### Is Inside
Property | Value
--- | ---
URI | `https://w3id.org/timefuncs/isInside`
Preferred Labels |Is Inside (en)<br />
Definitions |A function accepting an Instant a and an Interval b, testing testing whether the Instant is contained by the Interval, as per the inverse of time:inside. Returns a boolean, true if a is contained by b.<br />

## Namespaces
* **default (:)**
  * `https://w3id.org/timefuncs/voc`
* **:**
  * `https://w3id.org/timefuncs/`
* **dcterms**
  * `http://purl.org/dc/terms/`
* **owl**
  * `http://www.w3.org/2002/07/owl#`
* **rdf**
  * `http://www.w3.org/1999/02/22-rdf-syntax-ns#`
* **rdfs**
  * `http://www.w3.org/2000/01/rdf-schema#`
* **sdo**
  * `https://schema.org/`
* **skos**
  * `http://www.w3.org/2004/02/skos/core#`
* **xsd**
  * `http://www.w3.org/2001/XMLSchema#`

## Legend
* Collections: col
* Concepts: con