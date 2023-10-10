from dataclasses import dataclass


@dataclass
class LoggingExtras:
    Success = {"status": "success"}
    PriceError = {"status": "failed", "kind": "PriceError"}
    ItemError = {"status": "failed", "kind": "ItemError"}
