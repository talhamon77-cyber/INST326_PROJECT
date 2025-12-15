"""
Concrete product type representing a physical item.

This module defines the PhysicalProduct class, which extends AbstractProduct
with attributes specific to tangible goods such as weight.
"""

from __future__ import annotations

from typing import Any, Dict, Type, TypeVar

from abstract_product import AbstractProduct

PhysicalProductType = TypeVar("PhysicalProductType", bound="PhysicalProduct")


class PhysicalProduct(AbstractProduct):
    """
    Product representing a physical good in the marketplace.

    Adds a weight attribute and calculates trend score by penalizing
    return rate and weight (shipping/handling cost proxy).
    """

    def __init__(
        self,
        name: str,
        sales: int,
        returns: int,
        satisfaction: float,
        weight: float,
    ) -> None:
        super().__init__(name=name, sales=sales, returns=returns, satisfaction=satisfaction)

        if not isinstance(weight, (int, float)):
            raise TypeError("weight must be a number")
        if float(weight) <= 0.0:
            raise ValueError("weight must be greater than 0")

        self._weight = float(weight)

    @property
    def weight(self) -> float:
        """float: Product weight in kilograms."""
        return self._weight

    def calculate_trend_score(self) -> float:
        """
        Calculate the trend score for a physical product.

        Rewards sales and satisfaction; penalizes return rate and weight.

        Returns
        -------
        float
            Trend score (non-negative).
        """
        return_rate = self._returns / self._sales
        base_score = self._sales * 0.1 + self._satisfaction * 20.0
        penalty = return_rate * 50.0 + self._weight * 0.5
        return max(base_score - penalty, 0.0)

    def to_dict(self) -> Dict[str, Any]:
        """Convert this product into a serializable dictionary."""
        data = super().to_dict()
        data.update({"type": "physical", "weight": self._weight})
        return data

    @classmethod
    def from_dict(cls: Type[PhysicalProductType], data: Dict[str, Any]) -> PhysicalProductType:
        """
        Create a PhysicalProduct from a dictionary.

        Required keys: name, sales, returns, satisfaction, weight
        """
        return cls(
            name=data["name"],
            sales=data["sales"],
            returns=data["returns"],
            satisfaction=data["satisfaction"],
            weight=data["weight"],
        )
