import json

from app.engine.artifacts.browsers.browser import ChromiumBrowser


class Chrome(ChromiumBrowser):
    
    def __init__(self, artifact: str):
        super().__init__(artifact=artifact)
        
    @property
    def browser_type(self) -> str:
        return "chrome"

    def parse(self, descending: bool = True) -> None:
        history = sorted([
                json.dumps(record, indent=2, default=str, ensure_ascii=False)
                for record in self.history()], reverse=descending)

        downloads = sorted([
                json.dumps(record, indent=2, default=str, ensure_ascii=False)
                for record in self.downloads()], reverse=descending)
        
        keyword_search_terms = sorted([
                json.dumps(record, indent=2, default=str, ensure_ascii=False)
                for record in self.keyword_search_terms()], reverse=descending)

        self.result = {
            "chrome_history": history,
            "chrome_downloads": downloads,
            "chrome_keyword_search_terms": keyword_search_terms,
        }