# Freebase Setup

## Requirements

- OpenLink Virtuoso 7.2.5 
- Python 3
- Freebase dump

### Data Availability Issue
`Reimplementation/issues.md`

The original Freebase setup instruction points to the Google Freebase data dump page. However, the link does not provide a simple one-click dataset download workflow for this reimplementation. The Freebase API has been shut down, and the available dump is a historical archive.

The original GoG implementation assumes a local Virtuoso endpoint over the full Freebase dump. However, deploying the full Freebase dump is resource-intensive. The official Freebase triples contain around 1.9 billion triples, about 22 GB compressed and 250 GB uncompressed.

Due to local resource limitations, this reimplementation uses a partial Freebase dump instead of the full dump.

### Updated Reimplementation Decision

Following the tutor's suggestion, Freebase should be deployed locally via Virtuoso. If the full dump cannot be deployed due to resource limitations, a partial dump can be used. In that case, the benchmark must be filtered so that only questions answerable by the partial KG are evaluated.

## Partial Dump Alternative

Because Freebase deployment is infeasible, the following partial-KG procedure should be used:

1. Select the target benchmark, e.g. WebQSP or CWQ.
2. Extract seed entities from the questions, including topic entities and gold answer MIDs.
3. Construct a partial Freebase dump around these entities, for example by keeping 1-hop or 2-hop neighboring triples and required CVT nodes.
4. Import the partial dump into Virtuoso.
5. Test each benchmark question against the local SPARQL endpoint.
6. Keep only questions whose answers can be found in the partial KG.
7. Report the number of retained questions and mark the results as partial-KG results.

Results from this setting should not be directly compared with the original full-Freebase results.

## Setup

### Data Preprocessing

We use this py script (public link), to clean the data and remove non-English or non-digital triplets:

`gunzip -c freebase-rdf-latest.gz > freebase # data size: 400G
nohup python -u FilterEnglishTriplets.py 0<freebase 1>FilterFreebase 2>log_err & # data size: 125G`

### Import data

we import the cleaned data to virtuoso,
`
tar xvpfz virtuoso-opensource.x86_64-generic_glibc25-linux-gnu.tar.gz
cd virtuoso-opensource/database/
mv virtuoso.ini.sample virtuoso.ini

\# ../bin/virtuoso-t -df # start the service in the shell
../bin/virtuoso-t  # start the service in the backend.
../bin/isql 1111 dba dba # run the database

\# 1、unzip the data and use rdf_loader to import
SQL>
ld_dir('.', 'FilterFreebase', 'http://freebase.com'); 
rdf_loader_run(); 
`

Wait for a long time and then ready to use.

## Mapping data to Wikidata

Due to the partial incompleteness of the data present in the freebase dump, we need to map some of the entities with missing partial relationships to wikidata. We download these rdf data via this public link

we can use the above method to add it into virtuoso.

## Test example

import json
from SPARQLWrapper import SPARQLWrapper, JSON

SPARQLPATH = "http://localhost:8890/sparql"

def test():
    try:
        sparql = SPARQLWrapper(SPARQLPATH)
        sparql_txt = """PREFIX ns: <http://rdf.freebase.com/ns/>
            SELECT distinct ?name3
            WHERE {
            ns:m.0k2kfpc ns:award.award_nominated_work.award_nominations ?e1.
            ?e1 ns:award.award_nomination.award_nominee ns:m.02pbp9.
            ns:m.02pbp9 ns:people.person.spouse_s ?e2.
            ?e2 ns:people.marriage.spouse ?e3.
            ?e2 ns:people.marriage.from ?e4.
            ?e3 ns:type.object.name ?name3
            MINUS{?e2 ns:type.object.name ?name2}
            }
        """
        #print(sparql_txt)
        sparql.setQuery(sparql_txt)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print(results)
    except:
        print('Your database is not installed properly !!!')

test()
