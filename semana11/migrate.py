# --------------------------------------------------------------------
# Geração da ontologia para o dataset dos 120 anos dos Jogos Olímpicos
# 2025-04-10 by jcr
# --------------------------------------------------------------------
# Ontologia base (estrutura) criada à mão no Protégé
# --------------------------------------------------------------------
import csv
import re
from rdflib import Graph, Namespace, URIRef, RDF, Literal, XSD, OWL
# --------------------------------------------------------------------
# Carregar a ontologia base para o grafo em memória
# --------------------------------------------------------------------
n = Namespace("http://rpcw.di.uminho.pt/2025/geneologia#")
g = Graph()
g.parse("genoa_base.ttl")

ficheiro = "JCR_Family.csv"
individuos = set()


# Ler o CSV com separador ';'
with open(ficheiro, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=',')

    for linha in reader:
        pessoaURI = URIRef(f"{n}{linha["Indivíduo"].replace(" ", "_")}")
        individuos.add(pessoaURI)
        paiURI = URIRef(f"{n}{linha["Pai"].replace(" ", "_")}")
        individuos.add(paiURI)
        maeURI = URIRef(f"{n}{linha["Mãe"].replace(" ", "_")}")
        individuos.add(maeURI)

        g.add((pessoaURI, n.temPai, paiURI))
        g.add((pessoaURI, n.temMae, maeURI))

    for i in individuos:
        g.add((i, RDF.type, OWL.NamedIndividual))



(g.serialize(destination="geneologia_ramalho_populated.ttl", format="turtle"))