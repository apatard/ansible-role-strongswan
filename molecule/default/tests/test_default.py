import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_pkgs(host):
    p = host.package("strongswan")
    assert p.is_installed


def test_service(host):
    s = host.service("strongswan")
    assert s.is_enabled
    assert s.is_running
