from rdflib import Graph, Namespace, Literal, RDF, OWL


g = Graph()
g.parse("genoa3.ttl")


q="""
Construct{
    ?a :temAvo ?b .
    ?b :temNeto ?a .
}
WHERE {
     ?b :temFilho ?c . 
     ?c :temFilho ?a .
}
"""
n = Namespace("http://npcw/ontologies/2025/genoa#")

g.add((n.temAvo, RDF.type, OWL.ObjectProperty))
g.add((n.temNeto, RDF.type, OWL.ObjectProperty))

for r in g.query(q):
    #print (r[0].split("#")[1], r[1], r[2].split("#")[1])
    g.add((r))
    #g.add((r[0], n.tem, r[2]))

(g.serialize("genoa4.ttl", format="turtle"))