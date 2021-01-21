from sparql.namespaces import get_namespaces
from rdflib.plugins.stores.sparqlstore import SPARQLStore
from rdflib import Graph, URIRef, Namespace, util, parser, query


class QueryExecutor:
    namespaces = get_namespaces()
    sparql_store = SPARQLStore("http://dbpedia.org/sparql")

    @staticmethod
    def execute(query_string, *args, pretty_print=True, limit=20):
        query_string = QueryExecutor.prepare_query_string(query_string, *args, limit=limit)
        result = QueryExecutor.sparql_store.query(query_string, initNs=QueryExecutor.namespaces)
        if pretty_print:
            for item in list(result):
                print(item)
        return result

    @staticmethod
    def prepare_query_string(query_string: str, *args, limit=20):
        query_string += f"\n LIMIT {limit}"
        for i, arg in enumerate(args):
            query_string = query_string.replace(f'?{i+1}', arg)
        return query_string

    @staticmethod
    def find_all_properties(limit=20):
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
    def find_books_by_property_value(prop, value):
        q = """
        select distinct ?s ?value
        where {
        ?s rdf:type dbo:Book;
          ?1 ?value.
         VALUES ?value { <?2> }        
        }
        """
        return QueryExecutor.execute(q, prop, value)

    @staticmethod
    def find_books_by_property(prop):
        q = """
        select distinct ?s ?value
        where {
        ?s rdf:type dbo:Book;
          ?1 ?value.
        }
        """
        return QueryExecutor.execute(q, prop)

    @staticmethod
    def find_property_values_for_book(prop, book):
        q = """
        select distinct ?value
        where {
        ?s rdf:type dbo:Book;
          ?1 ?value.
         VALUES ?s { <?2> }        
        }
        """
        return QueryExecutor.execute(q, prop, book)

    @staticmethod
    def find_books_by_conditions(genre_list: list, language=None, people=None):
        q = """
        select distinct ?s
        where {
        ?s rdf:type dbo:Book;
          dbo:literaryGenre ?value.
         VALUES ?value { <http://dbpedia.org/resource/?1> }
         ?2
        }
        """
        genre_string = "> <http://dbpedia.org/resource/".join(genre_list)
        language_query = QueryExecutor.generate_language_query_part(language)
        return QueryExecutor.execute(q, genre_string, language_query)

    @staticmethod
    def generate_language_query_part(language: str):
        if language is not None:
            return """
            ?s dbp:language ?language .
              BIND(LCASE(STR(?language)) AS ?lang_lower)
              FILTER(contains(?lang_lower, "*1"))
            """.replace("*1", language.lower())
        else:
            return ""


if __name__ == "__main__":
    pass
    # QueryExecutor.find_all_properties(limit=200)
    # print("\n\n\n\n\n")
    # QueryExecutor.find_property_values('dbo:author')
    # print("\n\n\n\n\n")
    # QueryExecutor.find_books_by_property_value('dbo:author', 'http://dbpedia.org/resource/Heinz-Otto_Peitgen')
    # print("\n\n\n\n\n
    # QueryExecutor.find_property_values('dbo:lcc')
    # QueryExecutor.find_property_values('dbp:genre')
    # QueryExecutor.find_property_values('dbo:literaryGenre')
    # QueryExecutor.find_books_by_property('dbo:literaryGenre')
    # QueryExecutor.find_property_values_for_book('dbo:literaryGenre', 'http://dbpedia.org/resource/77_Shadow_Street')
    # QueryExecutor.find_property_values_for_book('dbp:genre', 'http://dbpedia.org/resource/77_Shadow_Street')
    QueryExecutor.find_property_values('dbo:language')
