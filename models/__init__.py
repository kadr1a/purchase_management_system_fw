"""Классы предметной области системы управления закупками."""

from .application import Application
from .product import Product
from .purchase_order import PurchaseOrder
from .supplier import Supplier

__all__ = ["Product", "Supplier", "Application", "PurchaseOrder"]
