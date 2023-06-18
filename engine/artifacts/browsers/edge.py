import json

from artifacts.browsers.browser import ChromiumBrowser


class Edge(ChromiumBrowser):

    def __init__(self, artifact: str):
        super().__init__(artifact=artifact)
        
    @property
    def browser_type(self) -> str:
        return "edge"
        
    def parse(self, descending: bool = False) -> None:
        history = sorted([
                json.dumps(record._packdict(), indent=2, default=str, ensure_ascii=False)
                for record in self.history()], reverse=descending)

        downloads = sorted([
                json.dumps(record._packdict(), indent=2, default=str, ensure_ascii=False)
                for record in self.downloads()], reverse=descending)
        
        keyword_search_terms = sorted([
                json.dumps(record._packdict(), indent=2, default=str, ensure_ascii=False)
                for record in self.keyword_search_terms()], reverse=descending)

        self.result = {
            "edge_history": history,
            "edge_downloads": downloads,
            "edge_keyword_search_terms": keyword_search_terms,
        }