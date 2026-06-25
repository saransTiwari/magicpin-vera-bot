from fastapi import FastAPI
import json

from stores import (
    merchant_store,
    category_store,
    customer_store,
    trigger_store
)

from composer import compose

app = FastAPI()

# Auto-load merchants dataset
@app.get("/")
def home():
    return {"message": "Magicpin Vera Bot is running"}
try:
    with open(
        "dataset/merchants_seed.json",
        "r",
        encoding="utf-8"
    ) as f:

        merchants = json.load(f).get(
            "merchants",
            []
        )

        for merchant in merchants:
            merchant_store[
                merchant["merchant_id"]
            ] = merchant

except Exception as e:
    print(
        f"Failed to load merchants dataset: {e}"
    )


@app.get("/v1/healthz")
def healthz():
    return {
        "status": "ok"
    }


@app.get("/v1/metadata")
def metadata():
    return {
        "name": "Saransh Vera Bot",
        "version": "1.0"
    }


@app.post("/v1/context")
def context(payload: dict):

    scope = payload.get("scope")
    context_id = payload.get("context_id")

    if scope == "merchant":
        merchant_store[
            context_id
        ] = payload.get(
            "payload",
            {}
        )

    elif scope == "category":
        category_store[
            context_id
        ] = payload.get(
            "payload",
            {}
        )

    elif scope == "customer":
        customer_store[
            context_id
        ] = payload.get(
            "payload",
            {}
        )

    elif scope == "trigger":
        trigger_store[
            context_id
        ] = payload.get(
            "payload",
            {}
        )

    return {
        "accepted": True
    }


@app.post("/v1/tick")
def tick(payload: dict):

    merchant_id = payload.get(
        "merchant_id"
    )

    merchant = merchant_store.get(
        merchant_id,
        {}
    )

    category = merchant.get(
        "category_slug",
        ""
    )

    trigger = payload.get(
        "trigger",
        {}
    )

    return compose(
        category,
        merchant,
        trigger
    )


@app.post("/v1/reply")
def reply(payload: dict):

    return {
        "handled": True,
        "next_action": "continue"
    }

