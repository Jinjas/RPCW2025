from rdflib import Graph,Namespace, RDF, OWL,RDFS


g = Graph()
g.parse("realeza_populada4.ttl")

q="""
    CONSTRUCT{
        ?a :temIrmao ?b .
    }
    WHERE {
        ?a :temProgenitor/:temFilho ?b .
        filter(?a != ?b)
    }
"""

n = Namespace("http://npcw/ontologies/2025/realeza#")

g.add((n.temIrmao, RDF.type, OWL.ObjectProperty))
g.add((n.temIrmao, RDFS.subPropertyOf, n.temRelaçao))



for r in g.query(q):

    g.add(r)

(g.serialize("realeza_populada5.ttl", format="turtle"))

print(len(g))