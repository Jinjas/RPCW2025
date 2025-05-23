# API de dados sobre a ontologia dos advogados
# Operações CRUD
# 2024-05-07 @jcr
#
# Modelo do Advogado:
#   A1: a :Advogado,                  --> Vamos assumir A1 como o id
#     :Pessoa, owl:NamedIndividual ;
#     :bebida "margarita";
#     :carro "crossover";
#     :cor "verde";
#     :dir :A2;
#     :idade 40;
#     :nome "Otávio";
#     :área "imobiliária" .
#
from flask import Flask, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)

# (R) Listar todos os advogados
#
@app.get('/advogados')
def get_advogados():
    query = """
    PREFIX : <http://www.di.uminho.pt/prc2021/advogados#>

    SELECT ?adv ?n ?i ?a ?b ?c ?cor
    WHERE {{
        ?adv a :Advogado ;
            :nome ?n ;
            :idade ?i ;
            :área ?a ;
            :bebida ?b ;
            :carro ?c ;
            :cor ?cor .
    }}
    """

    result = sparql_get_query(query)

    advogados = []
    for row in result['results']['bindings']:
        advogado = {
            "id": row['adv']['value'].split('#')[1],
            "nome": row['n']['value'],
            "idade": int(row['i']['value']),
            "área": row['a']['value'],
            "bebida": row['b']['value'],
            "carro": row['c']['value'],
            "cor": row['cor']['value']
        }
        advogados.append(advogado)

    return jsonify(advogados), 200

# (R) Consultar um advogado por id
#
@app.get('/advogados/<id>')
def get_advogado(id):
    query = f"""
    PREFIX : <http://www.di.uminho.pt/prc2021/advogados#>
    SELECT * WHERE{{
        :{id} ?p ?o
    }}
    """

    result = sparql_get_query(query)

    if result['results']['bindings']:
        linhas = result['results']['bindings']
        advogado = {}
        for linha in linhas:
            print(linha)
            if linha['p']['type'] == "uri":
                k = linha['p']['value'].split('#')[1]
            else:
                k = linha['p']['value']
            if linha['o']['type'] == "uri":
                v = linha['o']['value'].split('#')[1]
            else:
                v = linha['o']['value']
            advogado[k] = v
        return jsonify(advogado), 200
    else:
        return jsonify({"error": "Advogado inexistente..."}), 404


# (C) Criar um advogado
#
@app.post('/advogados')
def create_advogado():
    data = request.json
    if not data:
        return jsonify({"Erro": "Não foram enviados os dados do advogado a criar..."}), 400
    
    triplos = []
    if "nome" in data:
        triplos.append(f":{data['id']} :nome \"{data['nome']}\" .")
    if "idade" in data:
        triplos.append(f":{data['id']} :idade {data['idade']} .")
    if "área" in data:
        triplos.append(f":{data['id']} :área \"{data['área']}\" .")
    if "cor" in data:
        triplos.append(f":{data['id']} :cor \"{data['cor']}\" .")
    if "carro" in data:
        triplos.append(f":{data['id']} :carro \"{data['carro']}\" .")
    if "bebida" in data:
        triplos.append(f":{data['id']} :bebida \"{data['bebida']}\" .")
    
    query = f"""
    PREFIX : <http://www.di.uminho.pt/prc2021/advogados#>
    INSERT DATA {{
        :{data['id']} a :Advogado, :Pessoa, owl:NamedIndividual .
        {"\n".join(triplos)}
    }}
    """

    print(sparql_query(query))

    return jsonify({"message": f"Advogado criado com sucesso: {data['id']}"}), 201



# (U) Alterar um advogado
#
@app.put('/advogados/<id>')
def update_lawyer(id):
    data = request.json
    if not data:
        return jsonify({"Erro": "Não foram enviados os dados do advogado a alterar..."}), 400
    query = """
    PREFIX : <http://www.di.uminho.pt/prc2021/advogados#>

    DELETE {{
        :{} ?p ?o .
    }}
    INSERT {{
        :{} :idade {} ;
            :área "{}" .
    }}
    WHERE {{
        :{} ?p ?o .
    }}
    """.format(id, id, data['age'], data['area'], id)

    sparql_query(query)

    return jsonify({"message": f"Advogado alterado com sucesso: {id}"})


# (D) Apagar um advogado
#
@app.delete('/advogados/<id>')
def delete_advogado(id):
    query = """
    PREFIX : <http://www.di.uminho.pt/prc2021/advogados#>

    DELETE {{
        :{} ?p ?o .
    }}
    WHERE {{
        :{} ?p ?o .
    }}
    """.format(id, id)

    sparql_query(query)

    return jsonify({"message": f"Advogado removido da base de dados: {id}"})


def sparql_query(query):
    sparql = SPARQLWrapper("http://localhost:7200/repositories/advogados/statements")
    sparql.setMethod('POST')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def sparql_get_query(query):
    sparql = SPARQLWrapper("http://localhost:7200/repositories/advogados")
    sparql.setMethod('GET')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


if __name__ == '__main__':
    app.run(debug=True)
