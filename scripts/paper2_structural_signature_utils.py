"""Small validation helpers for Paper 2 structural-signature v1."""

from typing import Any, Iterable

from paper2_claim_ir_validate import normalize_text
from paper2_structural_signature_constants import ABSENCE_STATES, PRESENT_STATE

class ValidationError(ValueError):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def expect_object(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{context}: expected object")
    return value


def expect_list(value: Any, context: str) -> list[Any]:
    if not isinstance(value, list):
        fail(f"{context}: expected array")
    return value


def expect_string(value: Any, context: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        fail(f"{context}: expected string")
    if not allow_empty and not value.strip():
        fail(f"{context}: empty string")
    return value


def expect_bool(value: Any, context: str) -> bool:
    if not isinstance(value, bool):
        fail(f"{context}: expected boolean")
    return value


def exact_keys(obj: dict[str, Any], expected: set[str], context: str) -> None:
    actual = set(obj)
    if actual != expected:
        fail(
            f"{context}: key mismatch; "
            f"missing={sorted(expected - actual)} extra={sorted(actual - expected)}"
        )


def unique_strings(values: Any, context: str, *, nonempty: bool = False) -> list[str]:
    items = expect_list(values, context)
    if nonempty and not items:
        fail(f"{context}: must not be empty")
    out: list[str] = []
    for index, item in enumerate(items):
        out.append(expect_string(item, f"{context}[{index}]"))
    if len(out) != len(set(out)):
        fail(f"{context}: duplicate values")
    return out


def reject_json_nulls(value: Any, path: str = "root") -> None:
    if value is None:
        fail(f"{path}: JSON null is forbidden; use an explicit state object")
    if isinstance(value, dict):
        for key, item in value.items():
            reject_json_nulls(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            reject_json_nulls(item, f"{path}[{index}]")


def stateful(value: Any, context: str) -> dict[str, Any]:
    obj = expect_object(value, context)
    state = obj.get("state")
    if state == PRESENT_STATE:
        exact_keys(obj, {"state", "value"}, context)
        reject_json_nulls(obj["value"], f"{context}.value")
    elif state in ABSENCE_STATES:
        exact_keys(obj, {"state"}, context)
    else:
        fail(f"{context}.state: unexpected value {state!r}")
    return obj


def normalize_source_ref(ref: str) -> str:
    return normalize_text(ref)


def string_tree(value: Any, path: str) -> Iterable[tuple[str, str]]:
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from string_tree(item, f"{path}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from string_tree(item, f"{path}.{key}")


def reject_source_label_leakage(attempt: dict[str, Any], labels: list[str]) -> None:
    needles = [normalize_text(label) for label in labels if normalize_text(label)]
    # Source-facing labels are intentionally absent from attempt analysis fields.
    for path, text_value in string_tree(attempt, "attempt"):
        normalized = f" {normalize_text(text_value)} "
        for needle in needles:
            if f" {needle} " in normalized:
                fail(f"{path}: source-facing construct label leaks into analysis surface")
