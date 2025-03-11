# Harvester.py
# 2025-03-11 by Jinji
# -------------------
import json
import requests
from query import query_graphdb


desportos = []
endpoint = "https://dbpedia.org/sparql"
dataset = []
with open("desportos.json") as f:
    desportos = json.load(f)


for d in desportos:
    sparql_query=f"""
    select distinct ?label ?abstract where {{
   
   <{d}> rdfs:label ?label .
   <{d}> dbo:abstract ?abstract.
FILTER(LANG(?label) = 'en') .
FILTER(LANG(?abstract) = 'en')
}}
"""
    sparql_query2=f"""
    select distinct ?atleta ?nome ?origem ?data where {{
   
   ?atleta a schema:Person. 
    ?atleta dbp:sport <{d}>.
    ?atleta foaf:name ?nome .
    ?atleta dbo:nationality ?origem .
    ?atleta dbo:birthDate ?data .

}}
"""
    result = query_graphdb(endpoint, sparql_query)
    result2 = query_graphdb(endpoint, sparql_query2)
    
    atletas = []
    for x in result2['results']['bindings']:
        atletas.append(
            {
                "id": x['atleta']['value'],
                "nome": x['nome']['value'],
                "origem": x['origem']['value'],
                "dataNasc": x['data']['value']
            }
        )
    dataset.append(
        {
            "id" : d,
            "designacao": result['results']['bindings'][0]['label']['value'],
            "abs":result['results']['bindings'][0]['abstract']['value'],
            "atletas": atletas
        }
    )
    
with open("dataset.json","w") as fout:
    json.dump(dataset,fout,indent=4)
