from sparql.namespaces import get_namespaces
from rdflib.plugins.stores.sparqlstore import SPARQLStore
from rdflib import Graph, URIRef, Namespace, util, parser, query


class QueryExecutor:
    namespaces = get_namespaces()
    sparql_store = SPARQLStore("http://dbpedia.org/sparql")

    @staticmethod
    def execute(query_string, *args, pretty_print=True, limit=100):
        query_string = QueryExecutor.prepare_query_string(query_string, *args, limit=limit)
        result = QueryExecutor.sparql_store.query(query_string, initNs=QueryExecutor.namespaces)
        if pretty_print:
            for item in list(result):
                print(item)
        return result

    @staticmethod
    def prepare_query_string(query_string: str, *args, limit=100):
        query_string += f"\n LIMIT {limit}"
        for i, arg in enumerate(args):
            query_string = query_string.replace(f'?{i+1}', arg)
        return query_string

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
    def find_property_values(prop):
        q = """
        select distinct ?value
        where {
        ?s rdf:type dbo:Book;
          ?1 ?value.
        }
        """
        return QueryExecutor.execute(q, prop)

    @staticmethod
    def find_by_property(prop, value):
        q = """
        select distinct ?s ?value
        where {
        ?s rdf:type dbo:Book;
          ?1 ?value.
         VALUES ?value { <?2> }        
        }
        """
        return QueryExecutor.execute(q, prop, value)


if __name__ == "__main__":
    # QueryExecutor.find_all_properties(limit=200)
    # print("\n\n\n\n\n")
    # QueryExecutor.find_property_values('dbo:author')
    # print("\n\n\n\n\n")
    # QueryExecutor.find_by_property('dbo:author', 'http://dbpedia.org/resource/Heinz-Otto_Peitgen')
    # print("\n\n\n\n\n")
    QueryExecutor.find_property_values('dbo:lcc')
