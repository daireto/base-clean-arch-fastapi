from odata_v4_query import ODataQueryOptions, ODataQueryParser


class ODataHelper:
    def __init__(self, odata_options: ODataQueryOptions, max_top: int) -> None:
        self._odata_options = odata_options
        self._max_top = max_top
        self._sanitize()

    @classmethod
    def get_from_query(cls, query_string: str, max_top: int) -> 'ODataHelper':
        parser = ODataQueryParser()
        odata_options = parser.parse_query_string(query_string)
        return cls(odata_options, max_top)

    def get(self) -> ODataQueryOptions:
        return self._odata_options

    def get_for_counting(self) -> ODataQueryOptions:
        return ODataQueryOptions(
            count=True,
            filter_=self._odata_options.filter_,
            search=self._odata_options.search,
        )

    def get_skip(self) -> int:
        if self._odata_options.page:
            return (self._odata_options.page - 1) * self.get_top()
        return self._odata_options.skip or 0

    def get_top(self) -> int:
        return self._odata_options.top or self._max_top

    def get_page(self) -> int:
        return self._odata_options.page or 1

    def _sanitize(self) -> None:
        top = self._odata_options.top
        if top and top > self._max_top:
            self._odata_options.top = self._max_top
