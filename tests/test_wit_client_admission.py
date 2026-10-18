"""Source-free additive WIT syntax/authority sanity checks, not a WIT compiler."""
import re
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class WitAdmissionTests(unittest.TestCase):
    def test_additive_surface_has_no_privileged_capabilities(self):
        text=(ROOT/'contracts/wit/act-client.wit').read_text()
        self.assertIn('package anticaptrad:client@0.1.0;',text)
        self.assertRegex(text,r'world\s+act-client\s*\{')
        self.assertRegex(text,r'translate:\s*func\(request:\s*request\)')
        for prohibited in ('service-role','database-url','api-key','bearer','admin','secret'):
            self.assertNotIn(prohibited,text.lower().replace('no ', ''))
    def test_semantic_bytes_are_explicitly_bounded_by_adapter_policy(self):
        policy=(ROOT/'contracts/wit/admission.v1.json').read_text()
        import json
        obj=json.loads(policy)
        self.assertLessEqual(obj['maxTextUtf8Bytes'],65536)
        self.assertEqual(obj['productionEnabled'],False)
        self.assertEqual(obj['peerTypeSpecJsonSchemaVerified'],False)
if __name__=='__main__':unittest.main()
