from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date
from http import HTTPStatus
from typing import Iterator

from dcp.data_format import Records
from dcp.utils.common import ensure_datetime, utcnow

import snapflow_bigcommerce as bigcommerce
from snapflow import datafunction, Context
from snapflow.helpers.connectors.connection import HttpApiConnection

BIGCOMMERCE_API_BASE_URL = "https://api.bigcommerce.com/stores/"
ENTRIES_PER_PAGE = 250


@dataclass
class ImportBigCommerceOrdersState:
    latest_modified_date_imported: datetime


@datafunction(
    namespace="bigcommerce",
    state_class=ImportBigCommerceOrdersState,
    display_name="Import BigCommerce order products",
)
def import_order_products(
    ctx: Context,
    api_key: str,
    store_id: str,
    from_date: date = None,
    to_date: date = None,
) -> Iterator[Records[bigcommerce.BigCommerceOrderProduct]]:
    params = {
        "limit": 50,  # Keep small so we get good incremental progress on sub-calls
        "min_date_created": from_date,
        "max_date_created": to_date,
        "sort": "date_modified:asc",
    }
    latest_modified_date_imported = ctx.get_state_value("latest_modified_date_imported")
    latest_modified_date_imported = ensure_datetime(latest_modified_date_imported)

    if latest_modified_date_imported:
        params["min_date_modified"] = latest_modified_date_imported

    page = 1
    while ctx.should_continue():
        params["page"] = page

        resp = HttpApiConnection().get(
            url=f"{BIGCOMMERCE_API_BASE_URL}{store_id}/v2/orders",
            params=params,
            headers={"X-Auth-Token": api_key, "Accept": "application/json",},
        )

        # check if there is anything left to process
        if resp.status_code == HTTPStatus.NO_CONTENT:
            break

        json_resp = resp.json()

        assert isinstance(json_resp, list)

        order_products = []
        for order in json_resp:
            resp = HttpApiConnection(ratelimit_params=dict(calls=100, period=30)).get(
                url=f"{BIGCOMMERCE_API_BASE_URL}{store_id}/v2/orders/{order['id']}/products",
                params={"limit": ENTRIES_PER_PAGE},
                headers={"X-Auth-Token": api_key, "Accept": "application/json",},
            )
            if resp.status_code == HTTPStatus.NO_CONTENT:
                continue
            # TODO: pagination, if order has more than LIMIT items
            order_products = resp.json()

            assert isinstance(order_products, list)
            yield order_products

        latest_modified_date_imported = max(
            [r.get("date_modified", latest_modified_date_imported) for r in json_resp]
        )
        ctx.emit_state_value(
            "latest_modified_date_imported", latest_modified_date_imported
        )
        page += 1
