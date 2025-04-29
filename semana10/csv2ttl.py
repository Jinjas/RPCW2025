# --------------------------------------------------------------------
# Geração da ontologia para o dataset dos 120 anos dos Jogos Olímpicos
# 2025-04-10 by jcr
# --------------------------------------------------------------------
# Ontologia base (estrutura) criada à mão no Protégé
# --------------------------------------------------------------------
import csv
import re
from rdflib import Graph, Namespace, URIRef, RDF, Literal, XSD
# --------------------------------------------------------------------
# Carregar a ontologia base para o grafo em memória
# --------------------------------------------------------------------
n = Namespace("http://www.di.uminho.pt/rpcw2025/jogos_olímpicos#")
g = Graph()
g.parse("olimpicos_base.ttl")

ficheiro = "slice_10000.csv"
equipas = []
atletas = []
jogos =[]
eventos = []
modalidades = []
participacoes = []
# Ler o CSV com separador ';'
with open(ficheiro, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    for linha in reader:

        # Cálculo dos URI de cada entidade
        atletaURI = URIRef(f"{n}atleta_{linha['ID']}")
        eventoURI = URIRef(f"{n}evento_{len(eventos)}")
        equipaURI = URIRef(f"{n}equipa_{len(equipas)}")
        jogosURI = URIRef(f"{n}jogos_{len(jogos)}")
        modalidadeURI = URIRef(f"{n}modalidade_{len(modalidades)}")
        participacaoURI = URIRef(f"{n}particip_a{linha['ID']}_e{len(eventos)}")

        # Tratamento do Atleta -----------------------    
        if linha['ID'] not in atletas:
            g.add((atletaURI, RDF.type, n.Atleta))
            g.add((atletaURI, n.nome, Literal(linha['Name'])))
            g.add((atletaURI, n.sexo, Literal(linha['Sex'])))
            if linha['Age'].isdigit():
                g.add((atletaURI, n.idade, Literal(int(linha['Age']), datatype=XSD.integer)))
            else:
                g.add((atletaURI, n.peso, Literal(linha['Age'], datatype=XSD.string)))
            if linha['Height'].isdigit():
                g.add((atletaURI, n.altura, Literal(int(linha['Height']), datatype=XSD.integer)))
            else:
                g.add((atletaURI, n.altura, Literal(linha['Height'], datatype=XSD.string)))
            if linha['Weight'].isdigit():
                g.add((atletaURI, n.peso, Literal(int(linha['Weight']), datatype=XSD.integer)))
            else:
                g.add((atletaURI, n.peso, Literal(linha['Weight'], datatype=XSD.string)))
            atletas.append(linha['ID'])
        # Tratamento da Equipa -----------------------    
        if linha['Team'] not in equipas:
            g.add((equipaURI, RDF.type, n.Equipa))
            g.add((equipaURI, n.nome, Literal(linha['Team'])))
            g.add((equipaURI, n.noc, Literal(linha['NOC'])))
            equipas.append(linha['Team'])
        g.add((atletaURI, n.pertenceEquipa, equipaURI))
        # Não vou contruir o triplo inverso: Equipa :temAtleta Atleta

        # Tratamento dos Jogos -----------------------    
        if linha['Games'] not in jogos:
            g.add((jogosURI, RDF.type, n.Jogos))
            g.add((jogosURI, n.nome, Literal(linha['Games'])))
            g.add((jogosURI, n.cidade, Literal(linha['City'])))
            g.add((jogosURI, n.época, Literal(linha['Season'])))
            g.add((jogosURI, n.ano, Literal(linha['Year'])))
            jogos.append(linha['Games'])

        # Tratamento da Modalidade -----------------------
        if linha['Sport'] not in modalidades:
            g.add((modalidadeURI, RDF.type, n.Desporto))
            g.add((modalidadeURI, n.nome, Literal(linha['Sport'])))
            modalidades.append(linha['Sport'])

        # Tratamento do Evento -----------------------
        if linha['Event'] not in eventos:
            g.add((eventoURI, RDF.type, n.Evento))
            g.add((eventoURI, n.nome, Literal(linha['Event'])))
            g.add((eventoURI, n.temModalidade, modalidadeURI))
            g.add((jogosURI, n.temEvento, eventoURI))
            eventos.append(linha['Event'])

        # Tratamento da Participação -----------------------
        if participacaoURI not in participacoes:
            g.add((participacaoURI, RDF.type, n.Participação))
            g.add((participacaoURI, n.medalha, Literal(linha['Medal'])))
            g.add((participacaoURI, n.temParticipante, atletaURI))
            g.add((participacaoURI, n.éParticipaçãoDe, eventoURI))
            participacoes.append(participacaoURI)

(g.serialize("genoa5.ttl", format="turtle"))


