"""
Concrete product type representing a digital item.

This module defines the DigitalProduct class, which extends AbstractProduct
with attributes specific to digital goods such as downloads.
"""

from __future__ import annotations

from typing import Any, Dict, Type, TypeVar

from abstract_product import AbstractProduct

DigitalProductType = TypeVar("DigitalProductType", bound="DigitalProduct")


class DigitalProduct(AbstractProduct):
    """
    Product representing a digital good in the marketplace.

    Adds a downloads attribute and calculates trend score by rewarding
    engagement while lightly penalizing return rate.
    """

    def __init__(
        self,
        name: str,
        sales: int,
        returns: int,
        satisfaction: float,
        downloads: int,
    ) -> None:
        super().__init__(name=name, sales=sales, returns=returns, satisfaction=satisfaction)

        if not isinstance(downloads, int):
            raise TypeError("downloads must be an integer")
        if downloads < 0:
            raise ValueError("downloads must be greater than or equal to 0")

        self._downloads = downloads

    @property
    def downloads(self) -> int:
        """int: Total download count."""
        return self._downloads

    def calculate_trend_score(self) -> float:
        """
        Calculate the trend score for a digital product.

        Rewards downloads + satisfaction + sales; penalizes return rate.

        Returns
        -------
        float
            Trend score (non-negative).
        """
        return_rate = self._returns / self._sales
        base_score = self._sales * 0.1 + self._satisfaction * 25.0
        engagement_bonus = self._downloads * 0.05
        penalty = return_rate * 20.0
        return max(base_score + engagement_bonus - penalty, 0.0)

    def to_dict(self) -> Dict[str, Any]:
        """Convert this product into a serializable dictionary."""
        data = super().to_dict()
        data.update({"type": "digital", "downloads": self._downloads})
        return data

    @classmethod
    def from_dict(cls: Type[DigitalProductType], data: Dict[str, Any]) -> DigitalProductType:
        """
        Create a DigitalProduct from a dictionary.

        Required keys: name, sales, returns, satisfaction, downloads
        """
        return cls(
            name=data["name"],
            sales=data["sales"],
            returns=data["returns"],
            satisfaction=data["satisfaction"],
            downloads=data["downloads"],
        )
