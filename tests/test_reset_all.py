import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'reset-all.sh'

class ResetTest(unittest.TestCase):
    def run_reset(self, args, confirmation='', fail=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docker = root / 'docker'
            docker.write_text('''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
args=sys.argv[1:]
with open(os.environ['COMMANDS'], 'a') as log: log.write(json.dumps(args)+'\\n')
if '--filter' in args:
    assert args[args.index('--filter')+1]=='label=com.docker.compose.project=test-project'
    if os.environ.get('FAIL_DISCOVERY')=='1': sys.exit(1)
    # A separate project exists in this fixture but is never selected.
    kind='container' if args[0]=='ps' else args[0]
    print('selected-'+kind)
else:
    assert all(not arg.startswith('other-') for arg in args)
''')
            docker.chmod(0o755)
            log = root / 'commands'
            env = dict(os.environ, PATH=f'{root}:{os.environ["PATH"]}', COMMANDS=str(log))
            if fail: env['FAIL_DISCOVERY'] = '1'
            result = subprocess.run(['bash', str(SCRIPT), *args], input=confirmation,
                                    text=True, capture_output=True, env=env)
            calls = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
            return result, calls

    def test_default_is_dry_run_and_each_resource_is_filtered(self):
        result, calls = self.run_reset(['--project', 'test-project'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(calls), 4)
        self.assertIn('selected-volume', result.stdout)
        self.assertTrue(all('--filter' in call for call in calls))

    def test_cancel_and_eof_stop_all_deletions(self):
        for text in ('no\n', ''):
            result, calls = self.run_reset(['--project', 'test-project', '--execute'], text)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(len(calls), 4)

    def test_execute_deletes_only_selected_resources_without_prune(self):
        result, calls = self.run_reset(['--project', 'test-project', '--execute'], 'test-project\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls[4:], [['rm', '--force', 'selected-container'],
                                    ['image', 'rm', 'selected-image'],
                                    ['volume', 'rm', 'selected-volume'],
                                    ['network', 'rm', 'selected-network']])

    def test_failed_discovery_does_not_delete(self):
        result, calls = self.run_reset(['--project', 'test-project', '--execute'], 'test-project\n', True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(len(calls), 1)

    def test_missing_or_invalid_project_never_calls_docker(self):
        for args in ([], ['--project', '-bad'], ['--project', 'a b'], ['--project']):
            result, calls = self.run_reset(args)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(calls, [])

if __name__ == '__main__': unittest.main()
