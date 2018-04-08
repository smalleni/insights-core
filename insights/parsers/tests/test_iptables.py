from insights.parsers.iptables import IPTablesConfiguration, IPTables, IP6Tables, IPTabPermanent, IP6TabPermanent
from insights.tests import context_wrap

IPTABLES_SAVE = """
# Generated by iptables-save v1.4.7 on Tue Aug 16 10:18:43 2016
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [769:196899]
:REJECT-LOG - [0:0]
:Drop - [0:0]
-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
-A INPUT -m state --state RELATED,ESTABLISHED -g ACCEPT
-A INPUT -s 192.168.0.0/24 -j ACCEPT
-A INPUT -s 192.168.2.0/24
-A INPUT -p icmp -j ACCEPT
-A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT
-A INPUT -j REJECT --reject-with icmp-host-prohibited
-A OUTPUT -d 192.168.0.23/32 -m comment --comment "Permit IP to device net-j" -j ACCEPT
-A DROP
-A REJECT-LOG -p tcp -j REJECT --reject-with tcp-reset
COMMIT
# Completed on Tue Aug 16 10:18:43 2016
# Generated by iptables-save v1.4.7 on Tue Aug 16 10:18:43 2016
*mangle
:PREROUTING ACCEPT [451:22060]
:INPUT ACCEPT [451:22060]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [594:47151]
:POSTROUTING ACCEPT [594:47151]
COMMIT
# Completed on Tue Aug 16 10:18:43 2016
# Generated by iptables-save v1.4.7 on Tue Aug 16 10:18:43 2016
*nat
:PREROUTING ACCEPT [0:0]
:POSTROUTING ACCEPT [3:450]
:OUTPUT ACCEPT [3:450]
COMMIT
# Completed on Tue Aug 16 10:18:43 2016
"""

PARSED_TCP_REJECT_RULE = {
    "table": "filter",
    "chain": "REJECT-LOG",
    "rule": "-p tcp -j REJECT --reject-with tcp-reset",
    "target_action": "jump",
    "constraints": "-p tcp",
    "target": "REJECT",
    "target_options": "--reject-with tcp-reset"
}


def check_iptables_rules_parsing(iptables_obj):
    ipt = iptables_obj
    assert len(ipt.rules) == 10
    assert len(ipt.get_chain("INPUT")) == 7
    assert len(ipt.get_chain("OUTPUT")) == 1
    assert len(ipt.table_chains("mangle")) == 5
    assert ipt.rules[-1] == PARSED_TCP_REJECT_RULE
    assert ipt.get_table("nat")[1] == {
        "policy": "ACCEPT",
        "table": "nat",
        "name": "POSTROUTING",
        "packet_counter": 3,
        "byte_counter": 450
    }
    assert "tcp-reset" in ipt
    assert "--sport" not in ipt
    assert ipt.get_rule("tcp-reset") == [PARSED_TCP_REJECT_RULE]
    assert ipt.get_chain("DROP") == [
                {'table': 'filter', 'rule': '', 'chain': 'DROP'}]


def test_iptables_configuration():
    ipt = IPTablesConfiguration(context_wrap(IPTABLES_SAVE))
    check_iptables_rules_parsing(ipt)


def test_iptables_save():
    ipt = IPTables(context_wrap(IPTABLES_SAVE))
    check_iptables_rules_parsing(ipt)


def test_iptables_permanent():
    ipt = IPTabPermanent(context_wrap(IPTABLES_SAVE))
    check_iptables_rules_parsing(ipt)


IP6TABLES_SAVE = """
# Generated by ip6tables-save v1.4.21 on Tue Jan 31 05:25:29 2017
*nat
:PREROUTING ACCEPT [0:0]
:INPUT ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
:POSTROUTING ACCEPT [0:0]
COMMIT
# Completed on Tue Jan 31 05:25:29 2017
# Generated by ip6tables-save v1.4.21 on Tue Jan 31 05:25:29 2017
*mangle
:PREROUTING ACCEPT [0:0]
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
:POSTROUTING ACCEPT [0:0]
COMMIT
# Completed on Tue Jan 31 05:25:29 2017
# Generated by ip6tables-save v1.4.21 on Tue Jan 31 05:25:29 2017
*security
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [8:512]
:FORWARD_direct - [0:0]
:INPUT_direct - [0:0]
:OUTPUT_direct - [0:0]
-A INPUT -j INPUT_direct
-A FORWARD -j FORWARD_direct
-A OUTPUT -j OUTPUT_direct
COMMIT
# Completed on Tue Jan 31 05:25:29 2017
# Generated by ip6tables-save v1.4.21 on Tue Jan 31 05:25:29 2017
*raw
:PREROUTING ACCEPT [0:0]
:OUTPUT ACCEPT [8:512]
:OUTPUT_direct - [0:0]
:PREROUTING_direct - [0:0]
-A PREROUTING -p ipv6-icmp -m icmp6 --icmpv6-type 134 -j ACCEPT
-A PREROUTING -m rpfilter --invert -j DROP
-A PREROUTING -j PREROUTING_direct
-A OUTPUT -j OUTPUT_direct
COMMIT
# Completed on Tue Jan 31 05:25:29 2017
# Generated by ip6tables-save v1.4.21 on Tue Jan 31 05:25:29 2017
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
:REJECT-LOG - [0:0]
-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
-A INPUT -s fe80::/64 -j ACCEPT
-A INPUT -s fe80::/64
-A INPUT -p ipv6-icmp -j ACCEPT
-A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT
-A INPUT -j REJECT --reject-with icmp6-adm-prohibited
-A REJECT-LOG -p tcp -j REJECT --reject-with tcp-reset
COMMIT
# Completed on Tue Jan 31 05:25:29 2017
"""


PARSED_TCP_REJECT_RULE_6 = {
    'table': 'filter',
    'chain': 'REJECT-LOG',
    'rule': '-p tcp -j REJECT --reject-with tcp-reset',
    'target_action': 'jump',
    'constraints': '-p tcp',
    'target': 'REJECT',
    'target_options': '--reject-with tcp-reset',
}


def check_ip6tables_rules_parsing(ip6tables_obj):
    ipt = ip6tables_obj
    assert len(ipt.rules) == 14
    assert len(ipt.get_chain("INPUT")) == 6
    assert len(ipt.table_chains("mangle")) == 5
    assert ipt.rules[-1] == PARSED_TCP_REJECT_RULE_6
    assert ipt.get_table("nat")[-1] == {
        'policy': 'ACCEPT',
        'table': 'nat',
        'byte_counter': 0,
        'name': 'POSTROUTING',
        'packet_counter': 0,
    }
    assert "tcp-reset" in ipt
    assert "--sport" not in ipt
    assert ipt.get_rule("tcp-reset") == [PARSED_TCP_REJECT_RULE]


def test_ip6tables_save():
    ipt = IP6Tables(context_wrap(IP6TABLES_SAVE))
    check_ip6tables_rules_parsing(ipt)


def test_ip6tables_permanent():
    ipt = IP6TabPermanent(context_wrap(IP6TABLES_SAVE))
    check_ip6tables_rules_parsing(ipt)
