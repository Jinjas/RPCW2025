from rdflib import Graph,Namespace,Literal


g = Graph()
g.parse("genoa.ttl")


q="""
Select ?s
where {
    ?s a :Pessoa .
}
"""
n = Namespace("http://npcw/ontologies/2025/untitled-ontology-8#")

for r in g.query(q):

    #print(r[0].split("/")[-1])
    g.add((r[0],n.nome,Literal(r[0].split('#')[1],lang="pt")))

print(g.serialize())