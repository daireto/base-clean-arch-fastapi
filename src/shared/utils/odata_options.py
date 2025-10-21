from odata_v4_query import ODataQueryOptions, ODataQueryParser

from src.core.config import settings


class SafeODataQueryOptions:
    def __init__(self, odata_options: ODataQueryOptions) -> None:
        self._odata_options = odata_options

    @classmethod
    def get_from_query(cls, query_string: str) -> 'SafeODataQueryOptions':
        parser = ODataQueryParser()
        odata_options = parser.parse_query_string(query_string)
        return cls(odata_options)

    def get_sanitized(self) -> ODataQueryOptions:
        top = self._odata_options.top
        max_top = settings.max_records_per_page
        if top and top > max_top:
            self._odata_options.top = max_top
        return self._odata_options
