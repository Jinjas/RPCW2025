import requests
from tabulate import tabulate

def query_graphdb(endpoint_url, sparql_query):
    # Set up the headers
    headers = {
        'Accept': 'application/json',  # You can change this based on the response format you need
    }
    
    # Make the GET request to the GraphDB endpoint
    response = requests.get(endpoint_url, params={'query': sparql_query}, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Return the JSON response from the GraphDB endpoint
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# Example usage:
endpoint = "http://localhost:7200/repositories/HistoriaPT"
sparql_query = """
    SELECT ?subject ?predicate ?object
    WHERE {
        ?subject ?predicate ?object
    }
"""



result = query_graphdb(endpoint, sparql_query)
triplos =[]
for res in result["results"]["bindings"]:
    triplos.append((res['subject']['value'].split('#')[-1],
                    res['predicate']['value'].split('#')[-1],
                    res['object']['value'].split('#')[-1]
                    ))
print(tabulate(triplos))