"""Synthetic fixtures only; no account access or production guard imports."""
import unittest
from normalization_proposal import normalize_overage, EvidenceRefused


def raw(amount='0', currency='usd'):
    return {'current_overage': {'amount': amount, 'currency': currency}}


class Normalization(unittest.TestCase):
    def test_documented_nested_zero_is_evidence_only(self):
        result = normalize_overage(raw(), source='raw_api')
        self.assertEqual(result['amount'], '0')
        self.assertFalse(result['authorizes_generation'])

    def test_historical_flat_zero_is_labelled_historical(self):
        p = {'current_overage_amount': '0', 'current_overage_currency': 'usd'}
        self.assertEqual(normalize_overage(p, source='historical_provenance')['source'],
                         'historical_provenance')
        with self.assertRaises(EvidenceRefused):
            normalize_overage(p, source='raw_api')

    def test_matching_dual_representations(self):
        p = raw('0.00') | {'current_overage_amount': 0, 'current_overage_currency': 'usd'}
        self.assertEqual(len(normalize_overage(p, source='raw_api')['paths']), 2)

    def test_invalid_amounts_refused(self):
        for amount in (None, True, False, [], {}, '', 'zero', 'NaN', 'Infinity',
                       '-0', '-0.00', '-1', '0.01', 1, -1, 0.0, ' 0', '0 ', '0e0'):
            with self.subTest(amount=amount), self.assertRaises(EvidenceRefused):
                normalize_overage(raw(amount), source='raw_api')

    def test_absent_null_malformed_and_unknown_refused(self):
        for payload in (None, [], {}, {'current_overage': None}, {'current_overage': []},
                        {'current_overage': {}}, {'current_overage': {'amount': '0'}},
                        {'current_overage': {'currency': 'usd'}},
                        {'current_overage': raw()['current_overage'] | {'unknown': 0}},
                        {'current_overage_amount': '0'}):
            with self.subTest(payload=payload), self.assertRaises(EvidenceRefused):
                normalize_overage(payload, source='raw_api')

    def test_missing_unknown_currency_refused(self):
        for currency in (None, '', 'USD', 'xxx', 0, [], {}):
            with self.subTest(currency=currency), self.assertRaises(EvidenceRefused):
                normalize_overage(raw(currency=currency), source='raw_api')

    def test_dual_contradiction_or_malformed_never_falls_back(self):
        for extra in ({'current_overage_amount': '1', 'current_overage_currency': 'usd'},
                      {'current_overage_amount': '0', 'current_overage_currency': 'gbp'},
                      {'current_overage_amount': None, 'current_overage_currency': 'usd'},
                      {'current_overage_amount': '0'}):
            with self.subTest(extra=extra), self.assertRaises(EvidenceRefused):
                normalize_overage(raw() | extra, source='raw_api')
        with self.assertRaises(EvidenceRefused):
            normalize_overage({'current_overage': None, 'current_overage_amount': '0',
                               'current_overage_currency': 'usd'}, source='raw_api')

    def test_unknown_source_refused(self):
        with self.assertRaises(EvidenceRefused):
            normalize_overage(raw(), source='cached_api')


if __name__ == '__main__':
    unittest.main()
