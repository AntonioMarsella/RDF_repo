from github import Github
import requests
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, Literal, XSD, OWL
from rdflib.namespace import DC, FOAF

# using username and password
g = Github("user", "password")

# or using an access token
#g = Github("71467ab28842fc6839a069a8f32700e0c6c8fb8a")

#Namespaces definition
SCHEMA = Namespace("https://schema.org/")
WD = Namespace("https://www.wikidata.org/wiki/")
WDPROPERTY = Namespace("https://www.wikidata.org/wiki/Property:")

#Open the files where the triples will be saved
file = open("example.nt","w")
#Dictionary with some Programming Language name as keys and the IRI as values
dict = {'Python' : 'WD.Q28865', 'C++' : 'Q28865', 'Go' : 'WD.Q37227', 'Jupyter Notebook' : 'WD.Q55630549', 'Jsonnet' :  'https://jsonnet.org/', 'Java' :  'WD.Q251', 'Swift' : 'WD.Q17118377', 'PHP' : 'WD.Q59', 'HTML' : 'WD.Q8811','HTML5' : 'WD.Q2053', 'Scala':'WD.Q460584', 'JavaScript':'WD.Q2005', 'TeX': 'WD.Q5301', 'R':'WD.Q206904', 'Matlab':'WD.Q37805571', 'MATLAB':'WD.Q37805571', 'Haskell':'WD.Q34010','Clojure':'WD.Q51798', 'Rust':'WD.Q575650','CSS':'WD.Q11707176','C':'WD.Q15777','Objective-C':'WD.Q188531','Ruby':'WD.Q161053','ECL':'WD.Q5322691','Common Lisp':'WD.Q849146','Lisp':'WD.Q132874','PowerShell':'WD.Q840410','Julia':'WD.Q2613697','Lua':'WD.Q207316','ShaderLab':'https://docs.unity3d.com/Manual/SL-Shader.html','OpenEdge ABL':'WD.Q1963461','Shell':'WD.Q14663','TypeScript':'WD.Q978185','Pascal':'WD.Q81571','Lean':'https://leanprover.github.io/programming_in_lean/','MoonScript':'https://moonscript.org/','Groff':'https://www.gnu.org/software/groff/','Vue':'WD.Q24589705','Max':'WD.Q1707206','Elixir':'WD.Q5362035','Crystal':'WD.Q21921428','Mathematica':'WD.Q81294','SAS':'WD.Q2003932','Makefile':'WD.Q20748783','Perl':'WD.Q42478'}

#_________________________START functions definition________________________#
#Given a graph and a GitHub user, the function add the triples about the organizations the user belongs to.
def exploreOrganisations(graph, user):
    for org in user.get_orgs():
        if org.html_url != None:
            print(org.html_url)
            org_html_url = URIRef(org.html_url)
            user_IRI = URIRef(user.html_url)
            graph.add( (org_html_url, RDF.type, SCHEMA.Organization) )
            graph.add( (user_IRI, SCHEMA.memberOf, org_html_url) )
            graph.add( (user_IRI, WDPROPERTY.P463, org_html_url) ) #wikidata Member of
            graph.add( (org_html_url, RDF.type, WD.Q43229) ) #Wikidata organization

            if org.name != None:
                schema_name = Literal(repo.full_name, datatype=XSD.string)
                graph.add( (org_html_url, SCHEMA.name, schema_name) )
            #if org.description != None:
                #description = Literal(org.description, datatype=XSD.string)
                #graph.add((org_html_url, SCHEMA.description, description) )
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

                
#Given a graph and a GitHub repository, the function add the triples about the StarGazers of that repository.
def exploreStargazers(graph, repo, repository_url):
    for stargazer in repo.get_stargazers_with_dates():
        user = stargazer.user
        user_IRI = URIRef(user.html_url)
        if user.name != None:
            user_name = Literal(user.name, datatype=XSD.string)
            graph.add( (user_IRI, SCHEMA.name, user_name) )
        if user.id != None:
            user_identifier = Literal(user.id, datatype=XSD.int)
            graph.add((user_IRI, SCHEMA.identifier, user_identifier))
        if user.avatar_url != None:
            user_avatar = URIRef(user.avatar_url)
            graph.add((user_IRI, SCHEMA.image, user_avatar))

        graph.add( (user_IRI, RDF.type, WD.Q20374321))  # the stargazer is GitHub user
        graph.add( (user_IRI, SCHEMA.BookmarkAction, repository_url) )
        #exploreRepos(graph, user) #If uncommented, it could takes too long to run.

        
#Given a graph and a GitHub repository, the function add the triples about the Contributors of that repository.
def exploreContributors(graph, repo, repository_url):
    for contributor in repo.get_contributors():
        user = contributor
        user_IRI = URIRef(user.html_url)
        if user.name != None:
            user_name = Literal(user.name, datatype=XSD.string)
            graph.add((user_IRI, SCHEMA.name, user_name))
        if user.id != None:
            user_identifier = Literal(user.id, datatype=XSD.int)
            graph.add( (user_IRI, SCHEMA.identifier, user_identifier) )
        if user.avatar_url != None:
            user_avatar = URIRef(user.avatar_url)
            graph.add((user_IRI, SCHEMA.image, user_avatar))
        graph.add( (user_IRI, RDF.type, WD.Q20374321) )  # the contributor is GitHub user
        graph.add( (user_IRI, RDF.type, WD.Q20204892) )
        graph.add( (user_IRI, SCHEMA.contributor, repository_url) )
        graph.add( (user_IRI, WDPROPERTY.P3919, repository_url) ) #contributed to (wikidata property)
        #exploreRepos(graph, user)  #If uncommented, it could takes too long to run.
    
    
#Given a graph and a GitHub repository, the function add the triples about the repository and the author of the repository
def addRepos(graph, repo):
        author = repo.owner
        repository_url = URIRef(repo.html_url)
        schema_name = Literal(repo.full_name, datatype=XSD.string)
        repo_id = Literal(repo.id, datatype=XSD.int)  # id as integer
        description = Literal(repo.description, datatype=XSD.string)
        dateCreated = Literal(repo.created_at, datatype=XSD.dateTime)
        dateModified = Literal(repo.updated_at, datatype=XSD.dateTime)
        
        if repo.language != None:
            ProgrammingLanguage = searchProgrammingLanguage(repo.language)
            if repo.language in dict:
                ProgrammingLanguage = eval(dict[repo.language])
                graph.add((repository_url, SCHEMA.programmingLanguage, ProgrammingLanguage))
            elif ProgrammingLanguage != None:
                graph.add((repository_url, SCHEMA.programmingLanguage, ProgrammingLanguage))
            else:
                ProgrammingLanguage = Literal(repo.language, datatype=XSD.string)
                graph.add((repository_url, SCHEMA.programmingLanguage, ProgrammingLanguage))

        graph.add( (repository_url, RDF.type, WDPROPERTY.P1324) )  # The repository is a (wikidata) source code repository type
        graph.add( (repository_url, RDF.type,
                   SCHEMA.SoftwareSourceCode) )  # The repository is a (schema.org) SoftwareSourceCode type
        graph.add( (repository_url, SCHEMA.identifier, repo_id) )  # id of the repository as an integer
        graph.add( (repository_url, SCHEMA.codeRepository, repository_url) )
        graph.add( (repository_url, SCHEMA.dateCreated, dateCreated) )
        graph.add( (repository_url, SCHEMA.dateModified, dateModified) )
        graph.add( (repository_url, SCHEMA.name, schema_name) )
        graph.add( (repository_url, SCHEMA.description, description) )

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
        
#Given a graph and a GitHub user, the function add the triples about the repositories created by the user, using addRepos(...) function.
def exploreRepos(graph, author): #Repositories of an owner
    for repo in author.get_repos():
        addRepos(graph,repo)

        
#Given the name of a Programming Language as string, it search the entity in Wikidata
def searchProgrammingLanguage(query):
    API_ENDPOINT = "https://www.wikidata.org/w/api.php"
    params = {
        'action' : 'wbsearchentities',
        'format' : 'json',
        'language' : 'en',
        'search' : query
    }
    r = requests.get(API_ENDPOINT, params = params)
    return(URIRef(r.json()['search'][0]['concepturi']))

#_________________________END functions definition__________________________#

#Create the knowledge graph where the triples will be inserted
graph = Graph()

#Wikidata GitHub repository and Schema SoftwareSourceCode are the same thing
graph.add( (WDPROPERTY.P1324,OWL.sameAs,SCHEMA.SoftwareSourceCode) ) 

#Write the topic you want to query with '+' between two words. For more details go to https://developer.github.com/v3/search/
TOPIC_QUERY = 'machine+learning&page=2'
#Query the topic in GitHub
repositories = g.search_repositories(query=TOPIC_QUERY)

#For loop over all the found repositories
for repo in repositories:
    addRepos(graph, repo)
    repository_url = URIRef(repo.html_url)
    exploreStargazers(graph, repo, repository_url)  # Add triples about stargazers
    exploreContributors(graph, repo, repository_url)  # Add triples about contributors

#Write the triples in n-triples format. Format support can be extended with plugins,
#but ‘xml’, ‘n3’, ‘turtle’, ‘nt’, ‘pretty-xml’, ‘trix’, ‘trig’ and ‘nquads’ are built in.

result = graph.serialize(format='nt')
triples = result.decode("UTF-8") #Otherwise b' is printed at the beginning and \n at the end of everyline
file.write(triples)
file.close()
#print(triples)

