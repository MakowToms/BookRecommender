from rdflib import Namespace
from rdflib.namespace import FOAF, RDF, RDFS, XSD, OWL


def get_namespaces():
    schema = Namespace("http://schema.org/")
    ontology = Namespace("http://dbpedia.org/ontology/")
    dbo = Namespace("http://dbpedia.org/ontology/")
    dbp = Namespace("http://dbpedia.org/property/")
    dbr = Namespace("http://dbpedia.org/resource/")
    wdt = Namespace("http://www.wikidata.org/prop/direct/")
    wd = Namespace("http://www.wikidata.org/entity/")
    ns = dict(rdf=RDF, foaf=FOAF, rdfs=RDFS, xsd=XSD, schema=schema, owl=OWL,
              dbo=dbo, dbp=dbp, dbr=dbr, wd=wd, wdt=wdt,
              ontology=ontology)
    return ns
