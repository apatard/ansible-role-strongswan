import os

import pytest
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


@pytest.mark.parametrize(
    "fname",
    [
        ("/etc/ipsec.conf"),
        ("/etc/ipsec.secrets")
    ],
)
def test_file(host, fname):
    with host.sudo():
        f = host.file(fname)
        assert f.exists


def test_ipsec_secrets(host):
    content = b'172.17.0.2 1.2.3.4 : PSK "super wooper dooper secret"'
    with host.sudo():
        f = host.file("/etc/ipsec.secrets")
        assert f.exists
        assert f.mode == 0o0640
        assert content in f.content


@pytest.mark.parametrize(
    "content",
    [
        (b'conn conn1'),
        (b'right=1.2.3.4'),
        (b'rightsubnet=2.3.4.0/24'),
    ],
)
def test_ipsec_conf(host, content):
    assert content in host.file("/etc/ipsec.conf").content
