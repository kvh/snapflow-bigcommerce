from typing import TypeVar

from snapflow import SnapflowModule
from .functions.import_orders import import_orders
from .functions.import_order_products import import_order_products

BigCommerceOrder = TypeVar("BigCommerceOrder")
BigCommerceOrderProduct = TypeVar("BigCommerceOrderProduct")

module = SnapflowModule("bigcommerce", py_module_path=__file__, py_module_name=__name__)
module.add_function(import_orders)
module.add_function(import_order_products)
