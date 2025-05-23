# --------------------------------------------------------------------
# Geração da ontologia para o dataset dos 120 anos dos Jogos Olímpicos
# 2025-04-10 by jcr
# --------------------------------------------------------------------
# Ontologia base (estrutura) criada à mão no Protégé
# --------------------------------------------------------------------
import json
import re
from rdflib import Graph, Namespace, URIRef, RDF, Literal, XSD, OWL
# --------------------------------------------------------------------
# Carregar a ontologia base para o grafo em memória
# --------------------------------------------------------------------
n = Namespace("http://npcw/ontologies/2025/realeza#")
g = Graph()
g.parse("realeza.ttl")

ficheiro = "realeza_pt.json"
individuos = set()


# Ler o CSV com separador ';'
with open(ficheiro, newline='', encoding='utf-8') as f:
    data = json.load(f)

    for i, dinastia in enumerate(data):
        #add dinastia

        dinastiaURI = URIRef(f"{n}Dinastia_{i+1}")
        g.add((dinastiaURI, RDF.type, OWL.NamedIndividual))
        g.add((dinastiaURI, RDF.type, n.Dinastia))
        g.add((dinastiaURI,n.nome,Literal(dinastia)))

        for rei in data[dinastia]:
            reiURI = URIRef(f"{n}{rei['nome'].replace(' ', '_')}")
            maeURI = URIRef(f"{n}{rei['pai'].replace(' ', '_')}")
            paiURI = URIRef(f"{n}{rei['mãe'].replace(' ', '_')}")
            if reiURI not in individuos:
                individuos.add(reiURI)
                g.add((reiURI,RDF.type, OWL.NamedIndividual))
                g.add((reiURI,RDF.type, n.Pessoa))
                g.add((reiURI,n.nome, Literal(rei['nome'])))

            g.add((reiURI,n.dataNasc, Literal(rei['nascimento'])))
            g.add((reiURI,n.dataObito, Literal(rei['morte'])))
            g.add((reiURI,n.temPai, paiURI))
            g.add((reiURI,n.temMae, maeURI))
            g.add((reiURI,n.pertenceDinastia, dinastiaURI))
            if maeURI not in individuos:
                individuos.add(maeURI)
                g.add((maeURI,RDF.type, OWL.NamedIndividual))
                g.add((maeURI,RDF.type, n.Pessoa))
                g.add((maeURI,n.nome, Literal(rei['mãe'])))

            if paiURI not in individuos:
                individuos.add(paiURI)
                g.add((paiURI,RDF.type, OWL.NamedIndividual))
                g.add((paiURI,RDF.type, n.Pessoa))
                g.add((paiURI,n.nome, Literal(rei['mãe'])))


    
(g.serialize(destination="realeza_populada.ttl", format="turtle"))

print(len(g))