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
    def find_property_values(prop, limit=20):
        q = """
        select distinct ?value
        where {
        ?s rdf:type dbo:Book;
          ?1 ?value.
        }
        """
        return QueryExecutor.execute(q, prop, limit=limit)

    @staticmethod
    def find_books_by_property_value(prop, value, limit=20):
        q = """
        select distinct ?s ?value
        where {
        ?s rdf:type dbo:Book;
          ?1 ?value.
         VALUES ?value { <?2> }        
        }
        """
        return QueryExecutor.execute(q, prop, value, limit=limit)

    @staticmethod
    def find_books_with_property(prop, limit=20):
        q = """
        select distinct ?s ?value
        where {
        ?s rdf:type dbo:Book;
          ?1 ?value.
        }
        """
        return QueryExecutor.execute(q, prop, limit=limit)

    @staticmethod
    def find_property_values_for_book(prop, book, limit=20):
        q = """
        select distinct ?value
        where {
        ?s rdf:type dbo:Book;
          ?1 ?value.
         VALUES ?s { <?2> }        
        }
        """
        return QueryExecutor.execute(q, prop, book, limit=limit)

    @staticmethod
    def find_books_by_conditions(genre_list: list = None, language: str = None,
                                 people: set = None, book_name: str = None, limit=20):
        q = """
        select distinct ?book SAMPLE(?bookName AS ?bookNameSampled) SAMPLE(?bookAbstract AS ?bookAbstractSampled)
        where {
        ?book rdf:type dbo:Book;
          dbo:literaryGenre ?value.
        OPTIONAL { ?book foaf:name ?bookNameFoaf. 
                FILTER(lang(?bookNameFoaf) = "en")}
        OPTIONAL { ?book rdfs:label ?bookLabel. 
                FILTER(lang(?bookLabel) = "en")}
        OPTIONAL { ?book dbp:name ?bookNameDbp. 
                FILTER(lang(?bookNameDbp) = "en")}
        BIND(if(bound(?bookNameFoaf), ?bookNameFoaf, 
                if(bound(?bookLabel), ?bookLabel, 
                if(bound(?bookNameDbp), ?bookNameDbp, substr(str(?book), 29))
                )) as ?bookName)
        OPTIONAL { ?book  dbo:abstract  ?bookAbstract. 
                FILTER(lang(?bookAbstract) = "en")}
         ?1
         ?2
         ?3
         ?4
        }
        GROUP BY ?book
        """
        genre_query = QueryExecutor.generate_genre_query_part(genre_list)
        language_query = QueryExecutor.generate_language_query_part(language)
        people_query = QueryExecutor.generate_people_query_part(people)
        book_name_query = QueryExecutor.generate_book_name_query_part(book_name)
        return QueryExecutor.execute(q, genre_query, language_query, people_query,
                                     book_name_query, limit=limit)

    @staticmethod
    def generate_genre_query_part(genre_list: list):
        if genre_list is not None:
            genre_string = "> <http://dbpedia.org/resource/".join(genre_list)
            return """
             VALUES ?value { <http://dbpedia.org/resource/*1> }
             """.replace("*1", genre_string)
        else:
            return ""

    @staticmethod
    def generate_language_query_part(language: str):
        if language is not None:
            return """
            ?book dbp:language ?language .
              BIND(LCASE(STR(?language)) AS ?lang_lower)
              FILTER(contains(?lang_lower, "*1"))
            """.replace("*1", language.lower())
        else:
            return ""

    @staticmethod
    def generate_people_query_part(people: set):
        if people is not None:
            return """
            ?book ?prop ?persona .
            ?persona rdfs:label ?name
              BIND(LCASE(STR(?name)) AS ?name_lower)
              FILTER(?name_lower IN ("*1"))
            """.replace("*1", '", "'.join(people).lower())
        else:
            return ""

    @staticmethod
    def generate_book_name_query_part(book_name: str):
        if book_name is not None:
            return """
            BIND(LCASE(?bookName) AS ?bookNameLower)
              FILTER(contains(?bookNameLower, "*1"))
            """.replace("*1", book_name.lower())
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
    # QueryExecutor.find_property_values('dbo:language')
    # QueryExecutor.find_books_with_property('dbo:country', limit=50)
