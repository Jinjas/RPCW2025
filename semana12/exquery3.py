from rdflib import Graph,Namespace, RDF, OWL,RDFS


g = Graph()
g.parse("realeza_populada3.ttl")

q="""
    CONSTRUCT{
        ?b :temAntepassado ?a .
    }
    WHERE {
        ?b :temProgenitor+ ?a .
    }
"""
q2="""
    CONSTRUCT{
        ?b :temDescendente ?a .
    }
    WHERE {
        ?b :temFilho+ ?a .
    }
"""

n = Namespace("http://npcw/ontologies/2025/realeza#")

g.add((n.temRelaçao, RDF.type, OWL.ObjectProperty))
g.add((n.temAntepassado, RDF.type, OWL.ObjectProperty))
g.add((n.temDescendente, RDF.type, OWL.ObjectProperty))
g.add((n.temDescendente, RDFS.subPropertyOf, n.temRelaçao))
g.add((n.temFilho, RDFS.subPropertyOf, n.temDescendente))
g.add((n.temAntepassado, RDFS.subPropertyOf, n.temRelaçao))
g.add((n.temProgenitor, RDFS.subPropertyOf, n.temAntepassado))



for r in g.query(q):

    g.add(r)
for r in g.query(q2):

    g.add(r)

(g.serialize("realeza_populada4.ttl", format="turtle"))

print(len(g))