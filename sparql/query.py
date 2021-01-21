from sparql.namespaces import get_namespaces
from rdflib.plugins.stores.sparqlstore import SPARQLStore
from rdflib import Graph, URIRef, Namespace, util, parser, query


class QueryExecutor:
    namespaces = get_namespaces()
    sparql_store = SPARQLStore("http://dbpedia.org/sparql")

    @staticmethod
    def execute(query_string, pretty_print=True, limit=100):
        query_string += f"\n LIMIT {limit}"
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
        """.replace("?1", author)
        return QueryExecutor.execute(q)

    @staticmethod
    def find_all_properties(limit=100):
        q = """
        select distinct ?prop
        where {
        ?s rdf:type dbo:Book;
          ?prop ?value.
        }        
        """
        return QueryExecutor.execute(q, limit=limit)

    @staticmethod
    def show_property_values(property):
        q = """
        select distinct ?prop
        where {
        ?s rdf:type dbo:Book;
          ?1 ?value.
        }        
        """.replace("?1", property)
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
        """
        return QueryExecutor.execute(q)


if __name__ == "__main__":
    QueryExecutor.find_all_properties(limit=200)
    # QueryExecutor.find_something()
    # QueryExecutor.find_by_author('http://dbpedia.org/resource/Heinz-Otto_Peitgen')
