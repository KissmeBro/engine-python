
import re
import json
from typing import (
    Optional,
    Literal,
    Union,
    Dict,
    List,
    Any
)
from ...network import Network
from ...exceptions import (
    EngineError,
    InvalidAPIKeyError,
    APILimitExceededError,
    NetworkError,
    UnexpectedResponseError,
)


class SearchResult:
    """
    Represents a single search result item from Google Custom Search API.

    This class allows both dot-notation (obj.key) and dict-style (obj["key"]) access,
    while normalizing invalid Python attribute characters like ':' and '-'.
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """
        Initialize the SearchResult object.

        Args:
            data (Dict[str, Any]): Raw search result data from the API.
        """
        # Normalize keys to make them valid Python attributes
        self._data = self._replace_keys(data)

        # Set attributes for dot-access
        for key, value in self._data.items():
            setattr(self, key, self._convert_recursive(value))

    def _replace_keys(self, obj: Any) -> Any:
        """
        Recursively replace ':' and '-' in keys with '_'.

        Args:
            obj (Any): The input data (dict, list, or primitive).

        Returns:
            Any: The normalized data.
        """
        if isinstance(obj, dict):
            return {
                re.sub(r"[:\-]", "_", k): self._replace_keys(v)
                for k, v in obj.items()
            }
        if isinstance(obj, list):
            return [self._replace_keys(item) for item in obj]
        return obj

    def __getattr__(self, name: str) -> Any:
        """
        Handle missing attributes for dot-notation access.

        Args:
            name (str): The attribute name.

        Returns:
            Any: Default value ("N/A") if attribute not found.
        """
        return None

    def __getitem__(self, key: str) -> Any:
        """
        Allow dictionary-style access (obj["key"]).

        Args:
            key (str): The key name.

        Returns:
            Any: The value for the given key, or "N/A" if not found.
        """
        value = self._data.get(key, None)
        # Ensure nested dicts are also SearchResult objects
        if isinstance(value, dict):
            return SearchResult(value)
        if isinstance(value, list):
            return [self._convert_recursive(v) for v in value]
        return value

    def __contains__(self, key: str) -> bool:
        """
        Check if a key exists in the data.

        Args:
            key (str): The key name.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        return key in self._data

    def __iter__(self):
        """
        Allow iteration over keys like a dictionary.
        """
        return iter(self._data)

    def keys(self):
        """
        Return the keys of the search result.
        """
        return self._data.keys()

    def items(self):
        """
        Return the (key, value) pairs.
        """
        return self._data.items()

    def values(self):
        """
        Return the values.
        """
        return self._data.values()

    def __repr__(self) -> str:
        """
        Pretty-print the stored data in JSON format.
        """
        return json.dumps(self._data, ensure_ascii=False, indent=4)

    @classmethod
    def _convert_recursive(cls, value: Any) -> Any:
        """
        Recursively convert dictionaries and lists to SearchResult objects.

        Args:
            value (Any): The input value.

        Returns:
            Any: Converted object.
        """
        if isinstance(value, dict):
            return cls(value)
        if isinstance(value, list):
            return [cls._convert_recursive(item) for item in value]
        return value


class GoogleEngine:
    """
    Asynchronous engine for Google Custom Search API integration.

    Supports searching with extensive filtering and image search options.
    """

    def __init__(self, api_key: str, cse_id: str) -> None:
        """
        Initialize the engine with API credentials.

        Args:
            api_key (str): Google API key.
            cse_id (str): Programmable Search Engine ID (CSE ID).
        """
        self.api_key = api_key
        self.cse_id = cse_id
        self._endpoint = "https://www.googleapis.com/customsearch/v1"
        self._network: Optional[Network] = None

    async def __aenter__(self) -> "GoogleEngine":
        """
        Async context manager entrypoint.

        Returns:
            GoogleEngine: Instance of the initialized engine.
        """
        self._network = Network(self._endpoint)
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[object],
    ) -> None:
        """
        Async context manager cleanup.

        Args:
            exc_type (Optional[type]): Exception type if raised.
            exc_val (Optional[BaseException]): The exception instance.
            exc_tb (Optional[object]): The traceback object.
        """
        self._network = None

    async def connect(self) -> None:
        """
        Explicitly initialize the internal network client.

        Use this if not using the context manager.
        """
        self._network = Network(self._endpoint)

    async def close(self) -> None:
        """
        Explicitly close the network client session.

        Use this if not using the context manager.
        """
        self._network = None

    async def search(
        self,
        q: str,
        num: Optional[Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]] = None,
        start: Optional[int] = None,  # 1-100
        sort: Optional[str] = None,
        filter: Optional[Literal["0", "1"]] = None,
        dateRestrict: Optional[str] = None,
        fileType: Optional[str] = None,
        rights: Optional[str] = None,
        fields: Optional[str] = None,
        orTerms: Optional[str] = None,
        exactTerms: Optional[str] = None,
        excludeTerms: Optional[str] = None,
        hq: Optional[str] = None,
        lowRange: Optional[str] = None,
        highRange: Optional[str] = None,
        linkSite: Optional[str] = None,
        siteSearch: Optional[str] = None,
        siteSearchFilter: Optional[Literal["e", "i"]] = None,
        cr: Optional[str] = None,
        gl: Optional[str] = None,
        lr: Optional[Literal[
            "lang_ar", "lang_bg", "lang_ca", "lang_cs", "lang_da", "lang_de",
            "lang_el", "lang_en", "lang_es", "lang_et", "lang_fi", "lang_fr",
            "lang_hr", "lang_hu", "lang_id", "lang_is", "lang_it", "lang_iw",
            "lang_ja", "lang_ko", "lang_lt", "lang_lv", "lang_nl", "lang_no",
            "lang_pl", "lang_pt", "lang_ro", "lang_ru", "lang_sk", "lang_sl",
            "lang_sr", "lang_sv", "lang_tr", "lang_zh-CN", "lang_zh-TW"
        ]] = None,
        hl: Optional[str] = None,
        safe: Optional[Literal["safeUndefined", "active", "off"]] = None,
        c2coff: Optional[Literal[0, 1]] = None,
        searchType: Optional[Literal[
            "searchTypeUndefined", "image"
        ]] = None,
        imgSize: Optional[Literal[
            "imgSizeUndefined", "HUGE", "ICON", "LARGE", "MEDIUM", "SMALL",
            "XLARGE", "XXLARGE"
        ]] = None,
        imgType: Optional[Literal[
            "imgTypeUndefined", "clipart", "face", "lineart", "stock", "photo",
            "animated"
        ]] = None,
        imgColorType: Optional[Literal[
            "imgColorTypeUndefined", "mono", "gray", "color", "trans"
        ]] = None,
        imgDominantColor: Optional[Literal[
            "imgDominantColorUndefined", "black", "blue", "brown", "gray",
            "green", "orange", "pink", "purple", "red", "teal", "white", "yellow"
        ]] = None,
        imgFilter: Optional[str] = None,
    ) -> Union[List[SearchResult], List[None]]:
        """
        Perform an asynchronous search using Google Custom Search API.

        Args:
            q: Search query string.
            num: Number of results to return (1-10).
            start: Index of the first result (1-100).
            sort: Sorting expression (e.g., 'date').
            filter: Duplicate filter ('0'=off, '1'=on).
            dateRestrict: Date filter (d[number], w[number], m[number], y[number]).
            fileType: Restrict to file type (e.g., 'pdf').
            rights: Usage rights (e.g., 'cc_publicdomain').
            fields: Fields to include in the response.
            orTerms: Additional terms (OR logic).
            exactTerms: Exact phrase to include.
            excludeTerms: Terms to exclude.
            hq: Helper/boost query.
            lowRange: Lower numeric bound.
            highRange: Upper numeric bound.
            linkSite: Pages linking to a site.
            siteSearch: Restrict to a site.
            siteSearchFilter: 'i' include / 'e' exclude.
            cr: Country restrict.
            gl: Geolocation country.
            lr: Language restrict.
            hl: Interface language.
            safe: SafeSearch filter.
            c2coff: Chinese search option (0/1).
            searchType: Search type ('image' or undefined).
            imgSize: Image size filter.
            imgType: Image type filter.
            imgColorType: Image color type filter.
            imgDominantColor: Dominant image color filter.
            imgFilter: Image SafeSearch filter.

        Returns:
            A list of SearchResult objects if found, else an empty list.

        Raises:
            EngineError: If network is uninitialized.
            InvalidAPIKeyError: If API key is invalid.
            APILimitExceededError: If quota is exceeded.
            NetworkError: For network issues.
            UnexpectedResponseError: For unexpected HTTP responses.
        """
        if self._network is None:
            raise EngineError(
                "Network session is not initialized. Use async context manager."
            )

        params = {
            "key": self.api_key,
            "cx": self.cse_id,
            "q": q,
            "num": num,
            "start": start,
            "sort": sort,
            "filter": filter,
            "dateRestrict": dateRestrict,
            "fileType": fileType,
            "rights": rights,
            "fields": fields,
            "orTerms": orTerms,
            "exactTerms": exactTerms,
            "excludeTerms": excludeTerms,
            "hq": hq,
            "lowRange": lowRange,
            "highRange": highRange,
            "linkSite": linkSite,
            "siteSearch": siteSearch,
            "siteSearchFilter": siteSearchFilter,
            "cr": cr,
            "gl": gl,
            "lr": lr,
            "hl": hl,
            "safe": safe,
            "c2coff": c2coff,
            "searchType": searchType,
            "imgSize": imgSize,
            "imgType": imgType,
            "imgColorType": imgColorType,
            "imgDominantColor": imgDominantColor,
            "imgFilter": imgFilter
        }
        params = {k: v for k, v in params.items() if v is not None}

        try:
            data = await self._network.request(params)
        except (
            InvalidAPIKeyError,
            APILimitExceededError,
            NetworkError,
            UnexpectedResponseError,
            EngineError,
        ) as exc:
            raise exc

        items = data.get("items", [])
        return [
            SearchResult(item)
            for item in items
        ]
