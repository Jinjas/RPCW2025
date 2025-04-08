from rdflib import Graph, Namespace, Literal, RDF, OWL


g = Graph()
g.parse("genoa4.ttl")


q="""
Construct{
    ?a :temSogro ?p .
    ?a :temSogra ?m .
}
WHERE {
     ?a :temFilho ?x . 
     ?b :temFilho ?x . 
     ?b :temPai ?p .
     ?b :temMae ?m .
     FILTER(?a != ?b)
}
"""
n = Namespace("http://npcw/ontologies/2025/genoa#")

g.add((n.temSogra, RDF.type, OWL.ObjectProperty))
g.add((n.temSogro, RDF.type, OWL.ObjectProperty))

for r in g.query(q):
    #print (r[0].split("#")[1], r[1], r[2].split("#")[1])
    g.add((r))
    #g.add((r[0], n.tem, r[2]))

(g.serialize("genoa5.ttl", format="turtle"))