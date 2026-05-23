import os
from langchain.tools import tool
from langchain_tavily import TavilySearch
from pydantic_models.web_search_model import WebSearch
from dotenv import load_dotenv

load_dotenv()
path = os.getenv("tavily_api_key")
if not path or path == "":
    raise ValueError("Tavily key not found")
else:
    os.environ["TAVILY_API_KEY"] = path


@tool(description="web_search", args_schema=WebSearch)
def web_search(query: str, limit: int = 3):
    """
    Takes the query and return result by searching from web.

    args:
    query: string to search on web.
    max: max number of result you want to see. default to 3

    return:
    string of responses with content and url from where it get extracted.
    """

    tool = TavilySearch(
        max_results = limit,
        search_depth = 'basic'
    )

    result = tool.invoke({"query" : query})

    li = []
    for i, re in enumerate(result["results"]):
        url = re.get('url',None)
        content = re.get('content')
        li.append(f"result {i+1}: \n\tconten: {content}\n\t url : {url}")
    
    response = "\n".join(li)
    return response