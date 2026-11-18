"""Offline proposal only. No production imports, network, or spend authorization."""
from decimal import Decimal, InvalidOperation
import re


class EvidenceRefused(ValueError):
    pass


def _pair(amount, currency):
    # API Price.amount is an exact string; integer fixtures are refused.
    # binary floats, booleans and implicit conversion are deliberately refused.
    if type(amount) is not str:
        raise EvidenceRefused('amount type unknown')
    if not re.fullmatch(r'0(?:\.0+)?', amount):
        raise EvidenceRefused('amount format unknown')
    try:
        value = Decimal(amount)
    except (InvalidOperation, ValueError):
        raise EvidenceRefused('amount invalid') from None
    if not value.is_finite() or value.is_signed() or value != 0:
        raise EvidenceRefused('amount must be explicit unsigned zero')
    if currency not in ('usd', 'eur', 'inr', 'pln', 'gbp'):
        raise EvidenceRefused('currency missing or unknown')
    return value, currency


def normalize_overage(payload, *, source):
    """Return evidence only, never permission to POST.

    source must identify raw_api or historical_provenance. Historical evidence
    cannot stand in for a fresh raw response. Present malformed representations
    are refused even when another representation is valid.
    """
    if type(payload) is not dict or source not in ('raw_api', 'historical_provenance'):
        raise EvidenceRefused('unknown evidence source or payload')
    pairs = []
    paths = []
    if 'current_overage' in payload:
        nested = payload['current_overage']
        if type(nested) is not dict or set(nested) != {'amount', 'currency'}:
            raise EvidenceRefused('nested Price incomplete or unknown')
        pairs.append(_pair(nested['amount'], nested['currency']))
        paths.append('current_overage.amount/currency')
    flat_keys = ('current_overage_amount', 'current_overage_currency')
    if any(k in payload for k in flat_keys):
        if source == 'raw_api':
            raise EvidenceRefused('flattened keys are not raw API evidence')
        if not all(k in payload for k in flat_keys):
            raise EvidenceRefused('flattened evidence incomplete')
        pairs.append(_pair(payload[flat_keys[0]], payload[flat_keys[1]]))
        paths.append('current_overage_amount/current_overage_currency')
    if not pairs or (source == 'raw_api' and 'current_overage' not in payload):
        raise EvidenceRefused('documented nested evidence absent')
    if any(pair != pairs[0] for pair in pairs):
        raise EvidenceRefused('contradictory representations')
    return {'amount': '0', 'currency': pairs[0][1], 'source': source,
            'paths': paths, 'freshness_assessed': False, 'authorizes_generation': False}
