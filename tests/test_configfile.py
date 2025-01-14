import pytest
from clixon.args import parse_config
from clixon.parser import parse_file

config_xml = """
<clixon-config xmlns="http://clicon.org/config">
  <CLICON_CONFIGFILE>/usr/local/etc/controller.xml</CLICON_CONFIGFILE>
  <CLICON_FEATURE>ietf-netconf:startup</CLICON_FEATURE>
  <CLICON_FEATURE>clixon-restconf:allow-auth-none</CLICON_FEATURE>
  <CLICON_YANG_DIR>/usr/local/share/clixon</CLICON_YANG_DIR>
  <CLICON_YANG_MAIN_DIR>/usr/local/share/clixon/controller</CLICON_YANG_MAIN_DIR>
  <CLICON_CLI_MODE>operation</CLICON_CLI_MODE>
  <CLICON_CLI_DIR>/usr/local/lib/controller/cli</CLICON_CLI_DIR>
  <CLICON_CLISPEC_DIR>/usr/local/lib/controller/clispec</CLICON_CLISPEC_DIR>
  <CLICON_BACKEND_DIR>/usr/local/lib/controller/backend</CLICON_BACKEND_DIR>
  <CLICON_SOCK>/usr/local/var/controller.sock</CLICON_SOCK>
  <CLICON_BACKEND_PIDFILE>/usr/local/var/controller.pidfile</CLICON_BACKEND_PIDFILE>
  <CLICON_XMLDB_DIR>/usr/local/var/controller</CLICON_XMLDB_DIR>
  <CLICON_STARTUP_MODE>init</CLICON_STARTUP_MODE>
  <CLICON_SOCK_GROUP>clicon</CLICON_SOCK_GROUP>
  <CLICON_STREAM_DISCOVERY_RFC5277>true</CLICON_STREAM_DISCOVERY_RFC5277>
  <CLICON_RESTCONF_USER>www-data</CLICON_RESTCONF_USER>
  <CLICON_RESTCONF_PRIVILEGES>drop_perm</CLICON_RESTCONF_PRIVILEGES>
  <CLICON_RESTCONF_INSTALLDIR>/usr/local/sbin</CLICON_RESTCONF_INSTALLDIR>
  <CLICON_VALIDATE_STATE_XML>true</CLICON_VALIDATE_STATE_XML>
  <CLICON_CLI_HELPSTRING_TRUNCATE>true</CLICON_CLI_HELPSTRING_TRUNCATE>
  <CLICON_CLI_HELPSTRING_LINES>1</CLICON_CLI_HELPSTRING_LINES>
  <CLICON_YANG_SCHEMA_MOUNT>true</CLICON_YANG_SCHEMA_MOUNT>
  <autocli>
     <module-default>true</module-default>
     <list-keyword-default>kw-nokey</list-keyword-default>
     <treeref-state-default>true</treeref-state-default>
     <rule>
       <name>include controller</name>
       <module-name>clixon-controller</module-name>
       <operation>enable</operation>
     </rule>
     <rule>
       <name>include example</name>
       <module-name>clixon-example</module-name>
       <operation>enable</operation>
     </rule>
     <rule>
       <name>include junos</name>
       <module-name>junos-conf-root</module-name>
       <operation>enable</operation>
     </rule>
     <rule>
       <name>include arista system</name>
       <module-name>openconfig-system</module-name>
       <operation>enable</operation>
     </rule>
     <rule>
       <name>include arista interfaces</name>
       <module-name>openconfig-interfaces</module-name>
       <operation>enable</operation>
     </rule>
     <!-- there are many more arista/openconfig top-level modules -->
  </autocli>
  <CONTROLLER_PYAPI_MODULE_FILTER>filter</CONTROLLER_PYAPI_MODULE_FILTER>
  <CONTROLLER_PYAPI_MODULE_PATH>modules path</CONTROLLER_PYAPI_MODULE_PATH>
  <CONTROLLER_PYAPI_PIDFILE>pidfile</CONTROLLER_PYAPI_PIDFILE>
</clixon-config>
"""

invalid_config_xml = """
<clixon-config xmlns="http://clicon.org/config">
    <CLICON_CONFIGFILE>/usr/local/etc/controller.xml</CLICON_CONFIGFILE>
    <CONTROLLER_PYAPI_MODULE_PATH>modules path</CONTROLLER_PYAPI_MODULE_PATH>
</clixon-config>
"""


def test_parse_config():
    """
    Test that the config file is parsed correctly.
    """

    with open("/tmp/config.xml", "w") as fd:
        fd.write(config_xml)

    config = parse_file("/tmp/config.xml")
    clixon_config = config.clixon_config

    sockpath = clixon_config.CLICON_SOCK.cdata
    modulepath = clixon_config.CONTROLLER_PYAPI_MODULE_PATH.cdata
    modulefilter = clixon_config.CONTROLLER_PYAPI_MODULE_FILTER.cdata
    pidfile = clixon_config.CONTROLLER_PYAPI_PIDFILE.cdata

    assert sockpath == "/usr/local/var/controller.sock"
    assert modulepath == "modules path"
    assert modulefilter == "filter"
    assert pidfile == "pidfile"


def test_parse_invalid_config():
    """
    Test that invalid config is handled correctly.
    """

    with open("/tmp/config.xml", "w") as fd:
        fd.write(invalid_config_xml)

    config = parse_file("/tmp/config.xml")

    with pytest.raises(AttributeError):
        clixon_config = config.clixon_config

        sockpath = clixon_config.CLICON_SOCK.cdata
        modulepath = clixon_config.CONTROLLER_PYAPI_MODULE_PATH.cdata
        modulefilter = clixon_config.CONTROLLER_PYAPI_MODULE_FILTER.cdata
        pidfile = clixon_config.CONTROLLER_PYAPI_PIDFILE.cdata

        assert sockpath == "/usr/local/var/controller.sock"
        assert modulepath == ["modules path"]
        assert modulefilter == "filter"
        assert pidfile == "pidfile"


def test_args_parse_config():
    """
    Test that the config file is parsed correctly using parse_config.
    """

    with open("/tmp/config.xml", "w") as fd:
        fd.write(config_xml)

    sockpath, modulepath, modulefilter, pidfile = parse_config(
        "/tmp/config.xml")

    assert sockpath == "/usr/local/var/controller.sock"
    assert modulepath == ["modules path"]
    assert modulefilter == "filter"
    assert pidfile == "pidfile"
