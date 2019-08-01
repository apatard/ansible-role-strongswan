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
        ("/etc/ipsec.d/cacerts/caCert.der"),
        ("/etc/ipsec.d/certs/peerCert.der"),
        ("/etc/ipsec.d/private/peerKey.der"),
        ("/etc/ipsec.conf"),
        ("/etc/ipsec.secrets")
    ],
)
def test_file(host, fname):
    with host.sudo():
        f = host.file(fname)
        assert f.exists


def test_ipsec_secrets(host):
    content = b'"C = CH, O = strongSwan, CN = peer" "C = CH, O = strongSwan, CN = server" : RSA peerKey.der'
    with host.sudo():
        f = host.file("/etc/ipsec.secrets")
        assert f.exists
        assert f.mode == 0o0640
        assert content in f.content


@pytest.mark.parametrize(
    "content",
    [
        (b'conn conn1'),
        (b'authby=rsasig'),
        (b'leftrsasigkey=%cert'),
        (b'rightrsasigkey=%cert')
    ],
)
def test_ipsec_conf(host, content):
    assert content in host.file("/etc/ipsec.conf").content
