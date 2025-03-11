select \* where {
{
?s a :Rei.
?s :tem filho ?filho .
}
OPTIONAL {
?filho : temNome ?nome .
Filter (lang(?nome) = "en")
}
}

## query 1

from: http://dbpedia.org

select distinct ?nome ?abs where {
?desporto a dbo:Sport .
?desporto dbo:abstract ?abs .
filter(lang(?abs)="en").
?desporto rdfs:label ?nome.
filter(lang(?nome)="en").
} LIMIT 100

## query 2

from: <http://schema.org/>

select distinct ?person ?desporto ?nome ?origem where {
?person a schema:Person.
?person dbp:sport ?desporto .
?atleta dbp:name ?nome .
?atleta dbp:nationality ?origem .
} LIMIT 1000
