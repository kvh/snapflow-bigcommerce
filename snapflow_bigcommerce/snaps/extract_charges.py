from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from http import HTTPStatus

import snapflow_bigcommerce as bigcommerce
from snapflow import SnapContext, Param, Snap
from snapflow.helpers.connectors.connection import HttpApiConnection
from snapflow.storage.data_formats import RecordsIterator
from snapflow.utils.common import ensure_datetime, utcnow

BIGCOMMERCE_API_BASE_URL = "https://api.bigcommerce.com/stores/"
ENTRIES_PER_PAGE = 250


@dataclass
class ImportBigCommerceOrdersState:
    latest_imported_at: datetime


@Snap(
    "import_orders",
    module="bigcommerce",
    state_class=ImportBigCommerceOrdersState,
    display_name="Import BigCommerce orders",
)
@Param("store_id", "str")
@Param("api_key", "str")
@Param("from_date", "date", default=None)
@Param("to_date", "date", default=None)
def import_orders(ctx: SnapContext) -> RecordsIterator[bigcommerce.BigCommerceOrder]:
    api_key = ctx.get_param("api_key")
    store_id = ctx.get_param("store_id")
    from_date = ctx.get_param("from_date")
    to_date = ctx.get_param("to_date")

    params = {
        "limit": ENTRIES_PER_PAGE,
        "min_date_created": from_date,
        "max_date_created": to_date
    }
    latest_imported_at = ctx.get_state_value("latest_imported_at")
    latest_imported_at = ensure_datetime(latest_imported_at)

    if latest_imported_at:
        params["min_date_created"] = latest_imported_at

    while ctx.should_continue():
        page = 1
        while True:
            params["page"] = page
            ctx.emit_state_value("latest_imported_at", utcnow())

            resp = HttpApiConnection().get(
                url="{}{}/v2/orders".format(BIGCOMMERCE_API_BASE_URL, store_id),
                params=params,
                headers={
                    "X-Auth-Token": api_key,
                    "Accept": "application/json",
                }
            )

            # check if there is anything left to process
            if resp.status_code == HTTPStatus.NO_CONTENT:
                break

            json_resp = resp.json()
            assert isinstance(json_resp, list)

            yield resp.json()
            page += 1
