"""Isolated Docker integration: creates and removes only uniquely named fixtures.
Requires a locally available image (RESET_TEST_IMAGE, default nginx:stable-alpine).
"""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import uuid

SCRIPT = Path(__file__).resolve().parents[1] / 'reset-all.sh'

def docker(*args):
    return subprocess.run(['docker', *args], check=True, text=True, capture_output=True).stdout.strip()

class DockerResetTest(unittest.TestCase):
    def test_other_project_survives(self):
        token = uuid.uuid4().hex
        projects = [f'reset-test-{token}-selected', f'reset-test-{token}-other']
        containers, images, volumes, networks = [], [], [], []
        try:
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                for project in projects:
                    (root / 'Dockerfile').write_text(
                        f'FROM {os.environ.get("RESET_TEST_IMAGE", "nginx:stable-alpine")}\n'
                        f'LABEL com.docker.compose.project="{project}"\n')
                    docker('build', '--pull=false', '--network=none', '-t', project, str(root))
                    images.append(project)
                    volumes.append(docker('volume', 'create', '--label', f'com.docker.compose.project={project}', project))
                    networks.append(docker('network', 'create', '--label', f'com.docker.compose.project={project}', project))
                    containers.append(docker('create', '--label', f'com.docker.compose.project={project}',
                                             '--network', project, '-v', f'{project}:/fixture', project))
                result = subprocess.run(['bash', str(SCRIPT), '--project', projects[0], '--execute'],
                                        input=projects[0]+'\n', text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                for kind, resources in [('container', containers), ('image', images),
                                        ('volume', volumes), ('network', networks)]:
                    missing = subprocess.run(['docker', kind, 'inspect', resources[0]], capture_output=True)
                    self.assertNotEqual(missing.returncode, 0, f'selected {kind} remains')
                    docker(kind, 'inspect', resources[1])
        finally:
            # Cleanup is limited to the exact fixture IDs/names, never host-wide prune.
            for kind, resources in [('container', containers), ('image', images),
                                    ('volume', volumes), ('network', networks)]:
                for resource in resources:
                    args = ['docker', kind, 'rm']
                    if kind == 'container': args.append('--force')
                    subprocess.run([*args, resource], capture_output=True)

if __name__ == '__main__': unittest.main()
