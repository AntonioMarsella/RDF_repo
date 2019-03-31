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

