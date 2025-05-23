from rdflib import Graph,Namespace, RDF, OWL


g = Graph()
g.parse("realeza_populada.ttl")

q="""
    CONSTRUCT{
        ?a :temFilho ?b .
    }
    WHERE {
            {?b :temMae ?a .}
        UNION
            {?b :temPai ?a .}
    }
"""
n = Namespace("http://npcw/ontologies/2025/realeza#")

g.add((n.temFilho, RDF.type, OWL.ObjectProperty))

for r in g.query(q):

    g.add(r)

(g.serialize("realeza_populada2.ttl", format="turtle"))

print(len(g))