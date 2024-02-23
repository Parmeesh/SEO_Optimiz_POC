from newspaper import Article


url=input('Enter the url of the article:')
article=Article(url)
article_title= article.title


from langchain.tools import Tool
from langchain_community.utilities import GoogleSearchAPIWrapper

search=GoogleSearchAPIWrapper(google_api_key=' AIzaSyAQvX77pPkOpeqgiHI_-IIclgBkijdhjUc')

tool=Tool(
    name="google_search",
    description="Search Google for the articles related to this topic",
    func= search.run,
)

tool.run(article_title)



