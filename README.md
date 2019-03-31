# RDF_repo
Scripts to convert to RDF the result of GitHub repo queries.

## Requirements
You need two python libraries: [PyGithub](https://pygithub.readthedocs.io/en/latest/introduction.html) and [RDFlib](https://rdflib.readthedocs.io/en/stable/). If you have `pip` installed, then run in the terminal
```
pip install PyGithub
pip install RDFlib
pip install requests
```

## Quick start
Clone the repository. Open script.py file, edit the fields user and password with your GitHub username and password in the following line:

```g = Github("user", "password")```

or comment the line above and uncomment 

```#g = Github("access_token") ```

to access it with a token, and replace `"access_token"` with your token.

Then, replace `machine+learning&page=1` in the following line: 

```TOPIC_QUERY = 'machine+learning&page=1'```

with the topic you want to search repository about e.g. if you want to search repositories about _"Boltzmann Machine"_ write `'boltzmann+machine'`. For more details to use GitHub API [go here](https://developer.github.com/v3/search/#search-repositories).

In the terminal, move to the folder where your files are, and run:

```python ./script.py```

You will get RDF triples in *n-triples* format (`.nt` extension). 

## Functions

Given a graph and a GitHub user, the function add the triples about the organizations the user belongs to:
```exploreOrganisations(graph, user)```

Given a graph and a GitHub repository, the function add the triples about the StarGazers of that repository:
```exploreStargazers(graph, repo, repository_url)```

Given a graph and a GitHub repository, the function add the triples about the Contributors of that repository:
```exploreContributors(graph, repo, repository_url)```

Given a graph and a GitHub repository, the function add the triples about the repository and the author of the repository:
```addRepos(graph, repo)```
    
Given a graph and a GitHub user, the function add the triples about the repositories created by the user, using addRepos(...) function:
```exploreRepos(graph, author)```

Given the name of a Programming Language as string, it search the entity in Wikidata:
```searchProgrammingLanguage(query)```

## GitHub entities already mapped in a Shared Vocabulary

Organizations: The url of the organization is used as IRI, type: https://schema.org/Organization and https://wikidata.org/wiki/Q43229 .

To be a member of the organization: https://schema.org/memberOf and https://wikidata.org/wiki/Property:P463 .

Repositories: The url of the repository is used as IRI, type: https://wikidata.org/wiki/Property:P1324 and https://schema.org/SoftwareSourceCode .

The url of a repository, is also the object of the following predicate: https://schema.org/codeRepository .

Authors: The url of the author/owner of a repository is used as IRI, type: https://schema.org/author .

ID for organizations, users, repositories: https://schema.org/identifier .

Name of organizations, users, repositories: https://schema.org/name .

Avatar of users or organizations: https://schema.org/image .

Description of users, organizations, repositories: https://schema.org/description .

GitHub user: the url of the user is used as IRI, type: https://wikidata.org/wiki/Q20374321 .

GitHub contributor: the url of the user is used as IRI, type: https://wikidata.org/wiki/Q20204892 .

The property of *contributing* is mapped to: https://wikidata.org/wiki/Property:P3919 .

The action of *stargazing* is mapped to: https://schema.org/BookmarkAction .

The date when repositories or organizations have been created: https://schema.org/dateCreated .

The date when repositories or organizations have been updated on GitHub: https://schema.org/dateModified .

The datatype of the two dates above is XML Schema Definition (XSD) 'dateTime'.

If an organization is a company, then it is mapped to: https://schema.org/Corporation .

The property of being a programming languages is mapped to: https://schema.org/programmingLanguage .

The different kinds of programming languages, are mapped to the corrisponding Wikidata page, if available. For few of them, since the Wikidate is not available, the url of the corresponding programming language is provided. Otherwise, only the string with the name is provided.
