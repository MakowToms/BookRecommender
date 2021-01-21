from sparql.namespaces import get_namespaces
from rdflib.plugins.stores.sparqlstore import SPARQLStore
from rdflib import Graph, URIRef, Namespace, util, parser, query


class QueryExecutor:
    namespaces = get_namespaces()
    sparql_store = SPARQLStore("http://dbpedia.org/sparql")

    @staticmethod
    def execute(query_string, pretty_print=True):
        result = QueryExecutor.sparql_store.query(query_string, initNs=QueryExecutor.namespaces)
        if pretty_print:
            for item in list(result):
                print(item)
        return result

    @staticmethod
    def find_by_author(author):
        q = """
        select distinct ?s  ?author 
        where {
        ?s rdf:type dbo:Book;
          dbo:author ?author .
         VALUES ?author { <?1> }
        }        
        LIMIT 100
        """.replace("?1", author)
        return QueryExecutor.execute(q)

    @staticmethod
    def find_something():
        q = """
        select distinct ?s  ?author 
        where {
        ?s rdf:type ontology:Book;
          dbo:author ?author .
        ?s dbo:lcc ?lcc .
        }
        LIMIT 100
        """
        return QueryExecutor.execute(q)


if __name__ == "__main__":
    QueryExecutor.find_something()
    # QueryExecutor.find_by_author('http://dbpedia.org/resource/Heinz-Otto_Peitgen')
