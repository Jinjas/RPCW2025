# Ficha sobre os Jogos Olímpicos

## 2025-04-15 by jcr

---

## Dataset

[Dataset](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results) contendo os dados históricos sobre os jogos olímpicos de Atenas em 1896 até ao Rio
de Janeiro em 2016.

Como o dataset tem várias dezenas de MB foram preparados [datasets mais pequenos](https://epl.di.uminho.pt/~jcr/AULAS/RPCW2025/semana10/) para poderem ser trabalhados na sala de aula. Nomeadamente com 100, 1000 e 10000 registos.

---

## Plano de trabalho

Tenta resolver as questões que se colocam nas secções seguintes.

### 1. Modelo ontológico

Como podes ver facilmente analisando as primeiras linhas, a folha de cálculo não é modelo ideal para armazenar esta informação. Há várias dimensões que não cabem no limite de 2 dimensões.

Analisa o dataset e tenta modelar, com a ajuda de um diagrama, o modelo ontológico ideal para conter a informação do dataset.

Será promovida uma discussão na aula para se chegar a um modelo final mas é importante que consigas avançar com uma proposta tua.

### 2. Migração de Dados

Tendo o modelo estabilizado e especificado no Protégé, é preciso migrar a informação do dataset para o nosso modelo ontológico.

Depois de uma breve discussão com o docente sobre a abordagem a seguir, tenta criar a script de migração.

Após a migração, carrega a ontologia resultante no GraphDB, que deverás ter a correr num docker.

### 3. Queries

Vais agora tentar especificar várias queries e ser crítico em relação ao resultado obtido.
Regista as queries que vais especificando num ficheiro de texto.

Testa todas as queries que vais fazendo no GraphDB.

1. Especifica uma query que produz a lista dos nomes de atletas que ganharam a medalha de ouro;

```
PREFIX : <http://www.di.uminho.pt/rpcw2025/jogos_olímpicos#>
select ?name where {
    ?atleta a :Atleta ;
            :nome ?name .
    ?partic :temParticipante ?atleta ;
            :medalha "Gold" .
}
order by ?name
```

2. Especifica uma query que lista o nome dos atletas que ganharam medalhas e o respetivo número de medalhas (distribuição de medalhas por atletas), tem atenção à informação incompleta;

```
PREFIX : <http://www.di.uminho.pt/rpcw2025/jogos_olímpicos#>
select ?name (count (?medalha) as ?nmedalha) where {
    ?atleta a :Atleta ;
            :nome ?name .
    ?partic :temParticipante ?atleta ;
            :medalha ?medalha .
    filter (?medalha != 'NA') .
}
group by ?name
order by desc(?nmedalha)
```

3. Especifica uma query que calcula a distribuição de atletas por equipa;

```
PREFIX : <http://www.di.uminho.pt/rpcw2025/jogos_olímpicos#>
select ?nequipa (count (?atleta) as ?natletas) where {
    ?atleta a :Atleta ;
            :pertenceEquipa ?equipa .
    ?equipa :nome ?nequipa .
}
group by ?nequipa
order by desc(?natletas)
```

4. Especifica uma query que lista as equipas com a média do peso e da altura dos seus atletas;

```
PREFIX : <http://www.di.uminho.pt/rpcw2025/jogos_olímpicos#>
select ?nequipa
        (avg (?peso) as ?pesomedio)
        (avg (?altura) as ?alturamedio)
 where {
    ?atleta a :Atleta ;
            :peso ?peso ;
            :altura ?altura ;
            :pertenceEquipa ?equipa .
    ?equipa :nome ?nequipa .

    filter(datatype(?altura) = xsd:integer) .
    filter(datatype(?peso) = xsd:integer) .

}
group by ?nequipa
order by desc(?pesomedio)

```

5. Especifica uma query que indica qual o atleta mais idoso que participou no `Judo` e em que ano;

```
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX : <http://www.di.uminho.pt/rpcw2025/jogos_olímpicos#>
select ?name ?idade ?ano where {
?atleta a :Atleta ;
:nome ?name ;
:idade ?idade .

    ?partic :temParticipante ?atleta ;
            :éParticipaçãoDe ?evento.

    ?evento :temModalidade/:nome "Snowboarding" .

    ?jogo :temEvento ?evento;
            :ano ?ano .

    filter(datatype(?idade) = xsd:integer) .

}
order by desc(?idade)
limit 1
```

6. Especifica uma query que lista os nomes das modalidades por ordem alfabética;

```
PREFIX : <http://www.di.uminho.pt/rpcw2025/jogos_olímpicos#>
select ?nome  where {
?modalidade a :Desporto ;
    :nome ?nome .
}
order by ?nome
```

7. Especifica uma query que calcula a distribuição de atletas por modalidade;

```

PREFIX : <http://www.di.uminho.pt/rpcw2025/jogos_olímpicos#>

select ?modalidade (count(?a) as ?natletas) where{
    ?a a :Atleta .
    ?partic :temParticipante ?a ;
            :éParticipaçãoDe/:temModalidade/:nome ?modalidade .
}
group by ?modalidade
order by desc(?natletas)

```

---

### 4. Queries++

8. Especifica uma query que lista os atletas e respetivas alturas;

```
PREFIX : <http://www.di.uminho.pt/rpcw2025/jogos_olímpicos#>

select * where{
    ?a a :Atleta ;
        :nome ?anome ;
        :altura ?altura .
}

```

9. Especifica a mesma query que em vez de devolver valores, devolve triplos, usa a cláusula `CONSTRUCT`. Testa no GraphDB e analisa a forma do resultado comparando com a query anterior.

```
PREFIX : <http://www.di.uminho.pt/rpcw2025/jogos_olímpicos#>

construct {
    ?a :altura ?altura .
} where{
    ?a a :Atleta ;
        :nome ?anome ;
        :altura ?altura .

    filter(str(?altura) != 'NA')
}

```

- **Todas as variáveis** na cláusula CONSTRUCT têm de estar na cláusula WHERE.

10. Especifica uma query que produz uma lista dos eventos;

```
PREFIX : <http://www.di.uminho.pt/rpcw2025/jogos_olímpicos#>

select ?eventos ?nome where{
    ?eventos a :Evento ;
        :nome ?nome .
}

```

11. Especifica uma query que produz uma lista de eventos em que cada evento tem associada uma lista de atletas (é preciso utiliar a função de agregação `GROUP_CONCAT`);

```
PREFIX : <http://www.di.uminho.pt/rpcw2025/jogos_olímpicos#>

select ?nome (GROUP_CONCAT(?anome; separator=", ") as ?atletas) where{
    ?evento a :Evento ;
        :nome ?nome .

    ?particip :éParticipaçãoDe ?evento;
              :temParticipante/:nome ?anome.
}
group by ?nome
order by ?nome

```

12. Especifica uma query que calcula os triplos necessários para completar a ontologia com a simetria da relação `éParticipaçãoDe` (`temParticipação`), usa a cláusula `CONSTRUCT`;

```
PREFIX : <http://www.di.uminho.pt/rpcw2025/jogos_olímpicos#>

construct {
    ?e :temParticipação ?particip .
}
where{
    ?particip :éParticipaçãoDe ?e .
}

```

- Vamos **inserir** esta informação na BD:

13. Cria uma nova query, baseada na anterior, onde substituis a cláusula `CONSTRUCT` pela cláusula `INSERT`. Testa e observa o que acontece no GraphDB;

```
PREFIX : <http://www.di.uminho.pt/rpcw2025/jogos_olímpicos#>

insert {
    ?e :temParticipação ?particip .
}
where{
    ?particip :éParticipaçãoDe ?e .
}
```

14. Com os novos triplos inseridos na BD, cria uma nova query para a distribuição de atletas por evento, onde usas **property chains** para simplificar;

```
PREFIX : <http://www.di.uminho.pt/rpcw2025/jogos_olímpicos#>

select ?nome (count(?a) as ?natletas) where{
    ?evento a :Evento ;
        :nome ?nome ;
        :temParticipação/:temParticipante ?a.
}
group by ?nome
order by desc(?natletas)

```

#### Revisitando as medalhas

- Uma participação relaciona-se com os atletas pela relação `temParticipante`;
- Vamos completar a simetria desta relação:
  1. Testando com uma query CONSTRUCT;
  2. Acrescentando os triplos em falta com INSERT.

15. Vamos voltar a especificar agora a distribuição de medalhas por atleta, tirando partido da nova relação e usando novamente **property chains**;

- Desafio: **Lista as medalhas do atleta mais medalhado**

---

### App Web de exploração

- Pensa na interface de uma Aplicação Web para explorar este dataset e as queries desenvolvidas;
- Cria o dashboard principal.
