"""
Abstract base class for market analysis products.

This module defines the AbstractProduct class, which represents a generic
product within the consumer market and product trend analysis domain.
Subclasses must implement a concrete trend score calculation that is
appropriate for their specific product type.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class AbstractProduct(ABC):
    """
    Base class for products used in market analysis.

    This abstract class encapsulates common attributes and behavior for
    both physical and digital products, including sales volume, return
    counts, and customer satisfaction scores.

    Subclasses must implement a custom trend score calculation that
    reflects how the product performs in the market.
    """

    def __init__(self, name: str, sales: int, returns: int, satisfaction: float) -> None:
        """
        Initialize a new AbstractProduct instance.

        Parameters
        ----------
        name : str
            Human-readable product name. Must be a non-empty string.
        sales : int
            Number of units sold. Must be an integer greater than 0.
        returns : int
            Number of units returned. Must be an integer greater than or equal to 0.
        satisfaction : float
            Customer satisfaction score, typically a value between 0.0 and 5.0.

        Raises
        ------
        TypeError
            If any parameter has an invalid type.
        ValueError
            If any numeric parameter violates its value constraints.
        """
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not name.strip():
            raise ValueError("name must be a non-empty string")

        if not isinstance(sales, int):
            raise TypeError("sales must be an integer")
        if sales <= 0:
            raise ValueError("sales must be greater than 0")

        if not isinstance(returns, int):
            raise TypeError("returns must be an integer")
        if returns < 0:
            raise ValueError("returns must be greater than or equal to 0")

        if not isinstance(satisfaction, (int, float)):
            raise TypeError("satisfaction must be a number")
        if not 0.0 <= float(satisfaction) <= 5.0:
            raise ValueError("satisfaction must be between 0.0 and 5.0")

        self._name = name
        self._sales = sales
        self._returns = returns
        self._satisfaction = float(satisfaction)

    @property
    def name(self) -> str:
        """str: The human-readable product name."""
        return self._name

    @property
    def sales(self) -> int:
        """int: Total units sold."""
        return self._sales

    @property
    def returns(self) -> int:
        """int: Total units returned."""
        return self._returns

    @property
    def satisfaction(self) -> float:
        """float: Satisfaction score between 0.0 and 5.0."""
        return self._satisfaction

    @abstractmethod
    def calculate_trend_score(self) -> float:
        """
        Calculate an overall trend score for the product.

        Returns
        -------
        float
            Trend score for this product. Higher values represent stronger performance.
        """
        raise NotImplementedError

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the product into a serializable dictionary.

        Note: This stores only raw attributes. Derived values like trend score
        should be computed when needed (e.g., in reports).

        Returns
        -------
        dict
            Dictionary containing the core product data.
        """
        return {
            "name": self._name,
            "sales": self._sales,
            "returns": self._returns,
            "satisfaction": self._satisfaction,
        }

    def __str__(self) -> str:
        """Return a human-readable string representation."""
        return (
            f"{self.__class__.__name__}("
            f"name='{self._name}', sales={self._sales}, returns={self._returns}, "
            f"satisfaction={self._satisfaction:.2f}, trend_score={self.calculate_trend_score():.2f})"
        )

    def __repr__(self) -> str:
        """Return an unambiguous string representation for debugging."""
        return (
            f"{self.__class__.__name__}("
            f"name={self._name!r}, sales={self._sales!r}, returns={self._returns!r}, "
            f"satisfaction={self._satisfaction!r})"
        )
