from typing import TypeVar

from snapflow import SnapflowModule
from .snaps.import_orders import import_orders

BigCommerceOrder = TypeVar("BigCommerceOrder")

module = SnapflowModule(
    "bigcommerce",
    py_module_path=__file__,
    py_module_name=__name__,
    schemas=["schemas/bigcommerce.yml", ],
    snaps=[import_orders, ],

)
module.export()
