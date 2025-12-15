from __future__ import annotations
import re
from datetime import date
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Union, Callable
from collections import Counter
from collections import defaultdict



from library_functions import (
    ValidationError,
    DataParseError,
    validate_url_format,
    parse_csv_data,
    extract_keywords,
)


class ContentRecord:
    """
    Represents a single piece of content in a digital collection, including its
    source URL, body text, and any attached CSV-style data. Provides methods
    for URL validation, CSV parsing, and keyword extraction.

    A ContentRecord bundles data (url, text, csv blob) with behavior
    (validate_url_format, parse_csv_data, extract_keywords). This shows how
    related operations can live together on one object instead of being loose
    functions.
"""

    def __init__(
        self,
        record_id: str,
        source_url: str,
        text: str,
        csv_blob: Optional[str] = None,
        date_added: Optional[date] = None,
    ) -> None:
        """
        Initialize a ContentRecord.

        Args:
            record_id: Unique ID for this content inside your system.
            source_url: URL where the content was obtained.
            text: Full text body for keyword analysis.
            csv_blob: Optional CSV data as a string.
            date_added: Optional date object. If not provided, uses today's date.

        Raises:
            ValueError: If record_id or text are empty strings.
            TypeError: If types are incorrect.
        """
        if not isinstance(record_id, str):
            raise TypeError("record_id must be a string")
        if not record_id.strip():
            raise ValueError("record_id cannot be empty")

        if not isinstance(source_url, str):
            raise TypeError("source_url must be a string")

        if not isinstance(text, str):
            raise TypeError("text must be a string")
        if not text.strip():
            raise ValueError("text cannot be empty")

        if csv_blob is not None and not isinstance(csv_blob, str):
            raise TypeError("csv_blob must be a string or None")

        if date_added is not None and not isinstance(date_added, date):
            raise TypeError("date_added must be a datetime.date or None")

        # Store private
        self._record_id = record_id.strip()
        self._source_url = source_url.strip()
        self._text = text
        self._csv_blob = csv_blob
        self._date_added = date_added if date_added is not None else date.today()

        # Will hold parsed CSV rows once parse_csv() is called
        self._parsed_rows: Optional[
            Union[List[Dict[str, object]], List[List[str]]]
        ] = None

    # ------------------------------------------------------------------
    # Properties (encapsulation / controlled access)
    # ------------------------------------------------------------------

    @property
    def record_id(self) -> str:
        """str: Read only unique ID for this record."""
        return self._record_id

    @property
    def source_url(self) -> str:
        """
        str: Get or set the source URL.

        Setter validates type and strips whitespace, but does not force the
        URL to be valid immediately. Use is_url_valid() if you actually want
        to check the format.
        """
        return self._source_url

    @source_url.setter
    def source_url(self, new_url: str) -> None:
        if not isinstance(new_url, str):
            raise TypeError("source_url must be set to a string")
        self._source_url = new_url.strip()

    @property
    def text(self) -> str:
        """
        str: Get or set the full text content.

        Setter requires a non-empty string, because most of this class's
        behavior (keyword extraction) depends on text existing.
        """
        return self._text

    @text.setter
    def text(self, new_text: str) -> None:
        if not isinstance(new_text, str):
            raise TypeError("text must be set to a string")
        if not new_text.strip():
            raise ValueError("text cannot be empty")
        self._text = new_text

    @property
    def csv_blob(self) -> Optional[str]:
        """
        Optional[str]: Raw CSV text (unparsed). Can be None.
        """
        return self._csv_blob

    @csv_blob.setter
    def csv_blob(self, new_csv: Optional[str]) -> None:
        if new_csv is not None and not isinstance(new_csv, str):
            raise TypeError("csv_blob must be a string or None")
        self._csv_blob = new_csv
        # If CSV changes, cached parse is now stale
        self._parsed_rows = None

    @property
    def date_added(self) -> date:
        """datetime.date: Read only date when this record was added."""
        return self._date_added

    @property
    def parsed_csv(
        self,
    ) -> Optional[Union[List[Dict[str, object]], List[List[str]]]]:
        """
        Optional[List[dict] | List[List[str]]]: Returns cached parsed rows
        from the last successful call to parse_csv(). Read only.
        """
        return self._parsed_rows

    # ------------------------------------------------------------------
    # Instance methods (Project 1 functions now as behavior)
    # ------------------------------------------------------------------

    def is_url_valid(
        self,
        allowed_schemes: Iterable[str] = ("http", "https"),
    ) -> bool:
        """
        Check whether the stored source_url looks like a valid URL using
        validate_url_format from Project 1.

        Args:
            allowed_schemes: Iterable of acceptable schemes. Defaults to
                ("http", "https").

        Returns:
            True if the current source_url appears valid, otherwise False.

        Raises:
            TypeError: If source_url is not a string (should not happen if
                the setter was used correctly).
            ValidationError: If allowed_schemes is empty or invalid.

        Example:
            >>> rec.is_url_valid()
            True
        """
        return validate_url_format(self._source_url, allowed_schemes)

    def parse_csv(
        self,
        *,
        has_header: bool = True,
        delimiter: str = ",",
        quotechar: str = '"',
        required_fields: Optional[Sequence[str]] = None,
        type_map: Optional[Dict[str, Callable[[str], object]]] = None,
        trim_whitespace: bool = True,
    ) -> Union[List[Dict[str, object]], List[List[str]]]:
        """
        Parse the record's csv_blob into structured rows using parse_csv_data
        from Project 1, then cache the result in _parsed_rows.

        Args:
            has_header: Whether the first row is a header.
            delimiter: Field delimiter.
            quotechar: Quote character.
            required_fields: Column names that must be present if has_header is True.
            type_map: Mapping of column name to converter function. For example
                {"qty": int, "price": float}
            trim_whitespace: Strip whitespace from cells.

        Returns:
            The parsed rows (either list of dicts or list of lists). Also
            stored on self._parsed_rows for later access through parsed_csv.

        Raises:
            TypeError: If csv_blob is not a string.
            ValidationError: For bad delimiter/quotechar or missing columns.
            DataParseError: If a conversion in type_map fails.

        Example:
            >>> rec.csv_blob = "name,qty\\nPen,3\\nPencil,5"
            >>> rec.parse_csv(type_map={"qty": int})
            [{'name': 'Pen', 'qty': 3}, {'name': 'Pencil', 'qty': 5}]
            >>> rec.parsed_csv
            [{'name': 'Pen', 'qty': 3}, {'name': 'Pencil', 'qty': 5}]
        """
        if self._csv_blob is None:
            # Treat "no CSV" as valid but empty
            self._parsed_rows = []
            return self._parsed_rows

        parsed = parse_csv_data(
            self._csv_blob,
            has_header=has_header,
            delimiter=delimiter,
            quotechar=quotechar,
            required_fields=required_fields,
            type_map=type_map,
            trim_whitespace=trim_whitespace,
        )

        self._parsed_rows = parsed
        return parsed

    def extract_top_keywords(
        self,
        *,
        min_length: int = 3,
        stopwords: Optional[Iterable[str]] = None,
        top_n: Optional[int] = 10,
        keep_case: bool = False,
        include_bigrams: bool = False,
    ) -> List[str]:
        """
        Run keyword extraction on this record's text using extract_keywords
        from Project 1. Returns only the terms (not counts), sorted by
        frequency.

        Args:
            min_length: Minimum length for tokens to keep.
            stopwords: Words to exclude.
            top_n: Limit to this many results. Must be positive int or None.
            keep_case: Keep original case if True, otherwise lowercase first.
            include_bigrams: If True also consider two-word phrases.

        Returns:
            List of keyword strings, most frequent first.

        Raises:
            TypeError: If self._text is not a string.
            ValidationError: If min_length < 1 or top_n is invalid.

     """
        output = extract_keywords(
            self._text,
            min_length=min_length,
            stopwords=stopwords,
            top_n=top_n,
            keep_case=keep_case,
            return_counts=False,
            include_bigrams=include_bigrams,
        )
        return list(output)

    def keyword_counts(
        self,
        *,
        min_length: int = 3,
        stopwords: Optional[Iterable[str]] = None,
        top_n: Optional[int] = None,
        keep_case: bool = False,
        include_bigrams: bool = False,
    ) -> List[Tuple[str, int]]:
        """
        Same idea as extract_top_keywords, but returns (term, count) pairs.

        This mirrors extract_keywords(..., return_counts=True) from
        Project 1. Keeping this separate from extract_top_keywords()
        gives you two clearly named public methods, which is nice for
        your public interface.

        Args:
            min_length: Minimum token length.
            stopwords: Words to exclude.
            top_n: If set, only keep the top N terms.
            keep_case: Whether to lowercase or not.
            include_bigrams: Whether to include two word phrases.

        Returns:
            List of (term, count) tuples sorted by frequency.

        Raises:
            TypeError, ValidationError: See extract_keywords.

        """
        counted = extract_keywords(
            self._text,
            min_length=min_length,
            stopwords=stopwords,
            top_n=top_n,
            keep_case=keep_case,
            return_counts=True,
            include_bigrams=include_bigrams,
        )
        return list(counted)

    # ------------------------------------------------------------------
    # String / debug reps
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        """
        Human readable summary.

        
        """
        preview_len = len(self._text)
        url_ok = False
        try:
            url_ok = self.is_url_valid()
        except Exception:
            # If validate_url_format raised something, do not kill __str__
            url_ok = False

        return (
            f"ContentRecord {self._record_id} ({self._date_added})\n"
            f"URL valid? {url_ok}\n"
            f"{preview_len} chars of text"
        )

    def __repr__(self) -> str:
    
        return (
            f"ContentRecord(record_id={self._record_id!r}, "
            f"source_url={self._source_url!r}, "
            f"text_len={len(self._text)}, "
            f"csv_blob_len={len(self._csv_blob) if self._csv_blob else 0}, "
            f"date_added={self._date_added!r})"
        )


class SearchEngine:
    def __init__(self, records):        # Initialize the search engine with a list of records (dictionaries).
        if not isinstance(records, list):
            raise ValueError("Records should be a list of dictionaries.")
        self.records = records

    def calculate_relevance_scores(self, query, fields_weights):       # Calculate relevance scores for records based on a query.
        query_terms = query.lower().split()
        scores = []

        for record in self.records:
            score = 0
            for field, weight in fields_weights.items():
                text = record.get(field, "").lower()
                if not text:
                    continue
                field_terms = text.split()
                term_freq = {term: field_terms.count(term) / len(field_terms) for term in set(field_terms)}
                for qt in query_terms:
                    score += term_freq.get(qt, 0) * weight
            scores.append(score)
        return scores

    def format_search_results(self, results):        # Format a list of search result dictionaries into a readable string.

        if not results or not isinstance(results, list):
            return "No valid search results found."

        formatted = []
        for i, result in enumerate(results[:10], 1):       # Limit to top 10
            title = result.get("title", "No Title")
            snippet = result.get("snippet", "No description available.")
            formatted.append(f"{i}. {title}\n   {snippet}\n")    
        return "\n".join(formatted)