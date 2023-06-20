from collections import defaultdict
from typing import Generator

from dissect.sql.sqlite3 import SQLite3
from dissect.sql.exceptions import Error as SQLError

from app.engine.util.extractor import extract_basename, extract_fileext
from app.engine.forensic_artifact import ForensicArtifact


class ChromiumBrowser(ForensicArtifact):
    
    def __init__(self, artifact: str):
        super().__init__(artifact=artifact)
    
    @property
    def browser_type(self) -> str:
        raise NotImplementedError   
    
    def parse(self, descending: bool = False) -> None:
        raise NotImplementedError
    
    def history(self) -> Generator[dict, None, None]:
        for db_file in self._iter_entry(name="History*"):
            try:
                db = SQLite3(db_file.open("rb"))
                try:
                    urls = {row.id: row for row in db.table("urls").rows()}
                    visits = {}

                    for row in db.table("visits").rows():
                        visits[row.id] = row
                        url_record = urls[row.url]
                        
                        if row.from_visit and row.from_visit in visits:
                            from_visit = visits[row.from_visit]
                            from_url = urls[from_visit.url]
                        else:
                            from_visit, from_url = None, None

                        if (url := url_record.url).startswith("http"):
                            yield {
                                "ts": self.ts.webkittimestamp(row.visit_time),
                                "id": row.id,
                                "url": url,
                                "title": url_record.title,
                                "visit_type": None,
                                "visit_count": url_record.visit_count,
                                "hidden": url_record.hidden,
                                "from_visit": row.from_visit or None,
                                "from_url": from_url.url if from_url else None,
                                "source": str(db_file),
                                "browser_type": self.browser_type,
                            }
                except SQLError as e:
                    print(f"Error processing history file: {db_file} / exc_info={e}")
                except:
                    pass
            except:
                pass


    def downloads(self) -> Generator[dict, None, None]:
        for db_file in self._iter_entry(name="History*"):
            try:
                db = SQLite3(db_file.open("rb"))
                try:
                    download_chains = defaultdict(list)
                    for row in db.table("downloads_url_chains"):
                        download_chains[row.id].append(row)

                    for chain in download_chains.values():
                        chain.sort(key=lambda row: row.chain_index)

                    for row in db.table("downloads").rows():
                        download_path = row.target_path
                        file_name = extract_basename(download_path)
                        file_extension = extract_fileext(download_path)

                        if (download_chain := download_chains.get(row.id)):
                            download_chain_url = download_chain[-1].url
                        else:
                            download_chain_url = None

                        if (state := row.get("state")) == 0:
                            state = "Incomplete"
                        else:
                            state = "Complete"

                        yield {
                            "ts_start": self.ts.webkittimestamp(row.start_time),
                            "ts_end": self.ts.webkittimestamp(row.end_time) if row.end_time else None,
                            "file_name": file_name,
                            "file_extension": file_extension,
                            "received_bytes": row.get("total_bytes"),
                            "download_path": download_path,
                            "download_url": row.get("tab_url"),
                            "download_chain_url": download_chain_url,
                            "reference_url": row.referrer,
                            "id": row.get("id"),
                            "mime_type": row.get("mime_type"),
                            "state": state,
                            "browser_type": self.browser_type,
                            "source": str(db_file),
                        }
                except SQLError as e:
                    print(f"Error processing history file: {db_file} / exc_info={e}")
                except:
                    pass
            except:
                pass
                
    def keyword_search_terms(self):
        for db_file in self._iter_entry(name="History*"):
            try:
                db = SQLite3(db_file.open("rb"))
                try:
                    urls = {row.id: row for row in db.table("urls").rows()}

                    for row in db.table("keyword_search_terms").rows():
                        keyword_search_terms = {}
                        url_row = urls.get(row.url_id)
                        keyword_search_terms.update(row._values)
                        keyword_search_terms.update(url_row._values)
                        
                        last_visit_time = keyword_search_terms.get("last_visit_time")
                        term = keyword_search_terms.get("term")
                        title = keyword_search_terms.get("title")
                        url = keyword_search_terms.get("url")
                        id = keyword_search_terms.get("id")
                        visit_count = keyword_search_terms.get("visit_count")
                        hidden = keyword_search_terms.get("hidden")
                        
                        engines = {
                            "Google": "://www.google.com",
                            "Amazon": "://www.amazon.com",
                            "Yahoo": "://search.yahoo.com",
                            "Bing": "://www.bing.com",
                            "Naver": "://search.naver.com",
                            "Naver Map": "//map.naver.com",
                            "Daum": "://search.daum.net",
                            "Youtube": "://www.youtube.com",
                            "Github": "://github.com",
                        }
                        
                        search_engine = "Unknown"
                        for engine_name, site_url in engines.items():
                            if site_url in url:
                                search_engine = engine_name

                        yield {
                            "ts": self.ts.webkittimestamp(last_visit_time),
                            "term": term,
                            "title": title,
                            "search_engine": search_engine,
                            "url": url,
                            "id": id,
                            "visit_count": visit_count,
                            "hidden": hidden,
                            "browser_type": self.browser_type,
                        }
                except SQLError as e:
                    print(f"Error processing history file: {db_file} / exc_info={e}")
            except:
                pass
    