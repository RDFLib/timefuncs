data = """
    PREFIX time: <http://www.w3.org/2006/time#>
    PREFIX : <https://w3id.org/time-function/testdata/pathExists/>
    
    :a01 time:before :x01 .
    :x01 time:before :y01 .
    :y01 time:before :z01 .
    :z01 time:before :b01 . 
    
    :b02 time:after :x02 .
    :x02 time:after :y02 .
    :y02 time:after :z02 .
    :z02 time:after :a02 . 
    
    :a03 time:before :x03 .
    :y03 time:after :x03 .
    :y03 time:before :z03 .
    :b03 time:after :z03 . 
    """

from rdflib import Graph, Namespace, TIME
from timefuncs.funcs import _path_exists
PE = Namespace("https://w3id.org/time-function/testdata/pathExists/")

g = Graph().parse(data=data)
path = [(TIME.before, "outbound"), (TIME.after, "inbound")]
print(f"a01 b01 {_path_exists(g, PE.a01, PE.b01, path)}")
print(f"a02 b02 {_path_exists(g, PE.a02, PE.b02, path)}")
print(f"a03 b03 {_path_exists(g, PE.a03, PE.b03, path)}")
print(f"a01 b02 {_path_exists(g, PE.a01, PE.b02, path)}")
print(f"a01 b01 {_path_exists(g, PE.b01, PE.a01, path)}")
