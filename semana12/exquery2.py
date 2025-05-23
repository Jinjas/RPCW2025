from rdflib import Graph,Namespace, RDF, OWL,RDFS


g = Graph()
g.parse("realeza_populada2.ttl")

q="""
    CONSTRUCT{
        ?b :temProgenitor ?a .
    }
    WHERE {
            {?b :temMae ?a .}
        UNION
            {?b :temPai ?a .}
    }
"""
n = Namespace("http://npcw/ontologies/2025/realeza#")

g.add((n.temProgenitor, RDF.type, OWL.ObjectProperty))
g.add((n.temPai, RDFS.subPropertyOf, n.temProgenitor))
g.add((n.temFilho, RDFS.subPropertyOf, n.temProgenitor))



for r in g.query(q):

    g.add(r)

(g.serialize("realeza_populada3.ttl", format="turtle"))

print(len(g))