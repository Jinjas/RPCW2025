from rdflib import Graph,Namespace,Literal


g = Graph()
g.parse("genoa2.ttl")


q="""
    CONSTRUCT{
        ?prog :temFilho ?filho .
    }
    WHERE {
            {?filho :temMae ?prog .}
        UNION
            {?filho :temPai ?prog .}
    }
"""
n = Namespace("http://npcw/ontologies/2025/genoa#")

for r in g.query(q):

    g.add((r[0],n.temFilho,r[2]))

(g.serialize("genoa3.ttl", format="turtle"))