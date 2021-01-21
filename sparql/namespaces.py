from rdflib import Namespace
from rdflib.namespace import FOAF, RDF, RDFS, XSD


def get_namespaces():
    schema = Namespace("http://schema.org/")
    ontology = Namespace("http://dbpedia.org/ontology/")
    dbo = Namespace("http://dbpedia.org/ontology/")
    dbp = Namespace("http://dbpedia.org/property/")
    dbr = Namespace("http://dbpedia.org/resource/")
    ns = dict(rdf=RDF, foaf=FOAF, rdfs=RDFS, xsd=XSD, schema=schema,
              dbo=dbo, dbp=dbp, dbr=dbr,
              ontology=ontology)
    return ns
