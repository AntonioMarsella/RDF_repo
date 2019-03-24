from github import Github
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, Literal, XSD, OWL
from rdflib.namespace import DC, FOAF

# using username and password
g = Github("user", "password")

# or using an access token
#g = Github("access_token")

#Namespaces definition
SCHEMA = Namespace("https://schema.org/")
WD = Namespace("https://www.wikidata.org/wiki/")
WDPROPERTY = Namespace("https://www.wikidata.org/wiki/Property:")
file = open("example.nt","w")

def exploreOrganisations(graph, user):
    for org in user.get_orgs():

        if org.html_url != None
            org_html_url = URIRef(org.html_url)
            user_IRI = URIRef(user.html_url)
            graph.add( (org_html_url, RDF.type, SCHEMA.Organization) )
            graph.add( (user_IRI, SCHEMA.memberOf, org_html_url) )
            graph.add( (user_IRI, WDPROPERTY.P463, org_html_url) ) #wikidata Member of
            graph.add( (org_html_url, RDF.type, WD.Q43229) ) #Wikidata organization

            if org.name != None:
                schema_name = Literal(repo.full_name, datatype=XSD.string)
                graph.add( (org_html_url, SCHEMA.name, schema_name) 
            if org.id != None:
                org_id = Literal(repo.id, datatype=XSD.int)  # id as integer
                graph.add((org_html_url, SCHEMA.identifier, org_id) )  # id of the organization as an integer
            if org.created_at != None:
                dateCreated = Literal(org.created_at, datatype=XSD.dateTime)
                graph.add((org_html_url, SCHEMA.dateCreated, dateCreated) )
            if org.updated_at != None:
                dateModified = Literal(org.updated_at, datatype=XSD.dateTime)
                graph.add((org_html_url, SCHEMA.dateModified, dateModified) )
            if org.company != None:
                company = Literal(org.company, datatype=XSD.string)
                graph.add ( (org_html_url, SCHEMA.Corporation, company) )


def exploreStargazers(graph, repo, repository_url):
    for stargazer in repo.get_stargazers_with_dates():
        user = stargazer.user
        user_IRI = URIRef(user.html_url)
        if user.name != None:
            user_name = Literal(user.name, datatype=XSD.string)
            graph.add( (user_IRI, SCHEMA.name, user_name) )
        user_identifier = Literal(user.id, datatype=XSD.int)
        user_avatar = URIRef(user.avatar_url)
        graph.add( (user_IRI, SCHEMA.identifier, user_identifier) )
        graph.add( (user_IRI, RDF.type, WD.Q20374321))  # the stargazer is GitHub user
        graph.add( (user_IRI, SCHEMA.image, user_avatar) )
        graph.add( (user_IRI, SCHEMA.BookmarkAction, repository_url) )
        #exploreRepos(graph, user)



def exploreContributors(graph, repo, repository_url):
    for contributor in repo.get_contributors():
        user = contributor
        user_IRI = URIRef(user.html_url)
        if user.name != None:
            user_name = Literal(user.name, datatype=XSD.string)
            graph.add((user_IRI, SCHEMA.name, user_name))
        user_identifier = Literal(user.id, datatype=XSD.int)
        user_avatar = URIRef(user.avatar_url)
        graph.add( (user_IRI, SCHEMA.identifier, user_identifier) )
        graph.add( (user_IRI, RDF.type, WD.Q20374321) )  # the contributor is GitHub user
        graph.add( (user_IRI, SCHEMA.image, user_avatar) )
        graph.add( (user_IRI, RDF.type, WD.Q20204892) )
        graph.add( (user_IRI, SCHEMA.contributor, repository_url) )
        graph.add( (user_IRI, WDPROPERTY.P3919, repository_url) ) #contributed to (wikidata property)
        exploreRepos(graph, user)


def exploreRepos(graph, author): #Repositories of an owner
    for repo in author.get_repos():
        repository_url = URIRef(repo.html_url)
        schema_name = Literal(repo.full_name, datatype=XSD.string)
        repo_id = Literal(repo.id, datatype=XSD.int)  # id as integer
        description = Literal(repo.description, datatype=XSD.string)
        dateCreated = Literal(repo.created_at, datatype=XSD.dateTime)
        dateModified = Literal(repo.updated_at, datatype=XSD.dateTime)
        if repo.language != None:
            ProgrammingLanguage = Literal(repo.language, datatype=XSD.string)
            graph.add((repository_url, SCHEMA.programmingLanguage, ProgrammingLanguage))

        graph.add(
            (repository_url, RDF.type, WDPROPERTY.P1324))  # The repository is a (wikidata) source code repository type
        graph.add((repository_url, RDF.type,
                   SCHEMA.SoftwareSourceCode))  # The repository is a (schema.org) SoftwareSourceCode type
        graph.add((repository_url, SCHEMA.identifier, repo_id))  # id of the repository as an integer
        graph.add((repository_url, SCHEMA.codeRepository, repository_url))
        graph.add((repository_url, SCHEMA.dateCreated, dateCreated))
        graph.add((repository_url, SCHEMA.dateModified, dateModified))
        graph.add((repository_url, SCHEMA.name, schema_name))
        graph.add((repository_url, SCHEMA.description, description))

        # author section
        owner_name = Literal(author.name, datatype=XSD.string)
        owner_identifier = Literal(author.id, datatype=XSD.int)
        owner = URIRef(author.html_url)
        owner_avatar = URIRef(author.avatar_url)

        graph.add((owner, SCHEMA.author, repository_url))
        graph.add((owner, SCHEMA.identifier, owner_identifier))
        graph.add((owner, RDF.type, WD.Q20374321))  # the owner is GitHub user
        graph.add((owner, SCHEMA.name, owner_name))
        graph.add((owner, SCHEMA.image, owner_avatar))
        exploreOrganisations(graph,author)
        #exploreCommits(graph,repo)

#This function takes too much time to process.
#def exploreCommits(graph, repo):
#  repo_IRI = URIRef(repo.html_url)
#  if repo.get_commits() != None:
#    for commit in repo.get_commits():
#      commit_IRI = URIRef(commit.html_url)
#      graph.add( (commit_IRI, RDF.type, WD.Q20058545))
#      graph.add( (commit_IRI, WD.Q20058545, repo_IRI ))

#Create the graph (where we will insert the triples
graph = Graph()

graph.add( (WDPROPERTY.P1324,OWL.sameAs,SCHEMA.SoftwareSourceCode) ) #Wikidata GitHub repository and Schema SoftwareSourceCode are the same thing

#write the topic you want to query with '+' between two words
TOPIC_QUERY = 'AntonioMarsella/rdf_repo'
repositories = g.search_repositories(query=TOPIC_QUERY)

for repo in repositories:
    repository_url = URIRef(repo.html_url)
    schema_name = Literal(repo.full_name, datatype=XSD.string)
    repo_id = Literal(repo.id, datatype=XSD.int) #id as integer
    description = Literal(repo.description, datatype=XSD.string)
    dateCreated = Literal(repo.created_at, datatype=XSD.dateTime)
    dateModified = Literal(repo.updated_at, datatype=XSD.dateTime)
    if repo.language != None:
        ProgrammingLanguage = Literal(repo.language, datatype=XSD.string)
        graph.add((repository_url, SCHEMA.programmingLanguage, ProgrammingLanguage))

    graph.add( (repository_url, RDF.type, WDPROPERTY.P1324  ) ) #The repository is a (wikidata) source code repository type
    graph.add( (repository_url, RDF.type, SCHEMA.SoftwareSourceCode) ) #The repository is a (schema.org) SoftwareSourceCode type
    graph.add( (repository_url, SCHEMA.identifier, repo_id) ) #id of the repository as an integer
    graph.add( (repository_url, SCHEMA.codeRepository, repository_url) )
    graph.add( (repository_url, SCHEMA.dateCreated, dateCreated) )
    graph.add( (repository_url, SCHEMA.dateModified, dateModified) )
    graph.add( (repository_url, SCHEMA.name, schema_name) )
    graph.add( (repository_url, SCHEMA.description, description) )

    exploreStargazers(graph, repo, repository_url)  # Add triples about stargazers
    exploreContributors(graph, repo, repository_url)  # Add triples about contributors

    #author section
    owner_name = Literal(repo.owner.name, datatype=XSD.string)
    owner_identifier = Literal(repo.owner.id, datatype=XSD.int)
    owner = URIRef(repo.owner.html_url)
    owner_avatar = URIRef(repo.owner.avatar_url)

    graph.add( (owner, SCHEMA.author, repository_url) )
    graph.add( (owner, SCHEMA.identifier, owner_identifier) )
    graph.add( (owner, RDF.type, WD.Q20374321) ) #the owner is GitHub user
    graph.add( (owner, SCHEMA.name, owner_name) )
    graph.add( (owner, SCHEMA.image, owner_avatar) )
    exploreOrganisations(graph, repo.owner)
    exploreCommits(graph,repo)

result = graph.serialize(format='nt')
triples = result.decode("UTF-8") #otherwise it prints b' at the beginning of everyline and \n for return
file.write(triples)
file.close()
print(triples)

