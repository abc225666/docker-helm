#!/usr/bin/env python3

import os
import subprocess
from distutils.util import strtobool
from jinja2 import Template

class Config():
    def __init__(
                self,
                api_server="",
                token="",
                config_path="",
                skip_tls=False,
                cert_data="",
                namespace="",
                values="",
                string_values="",
                debug=False,
                dry_run=False,
                release="",
                chart=""):
        self.api_server = api_server
        self.token = token
        self.config_path = config_path
        self.skip_tls = skip_tls
        self.cert_data = cert_data
        self.namespace = namespace
        self.values = values
        self.string_values = string_values
        self.debug = debug
        self.dry_run = dry_run
        self.release = release
        self.chart = chart

    @property
    def api_server(self):
        return self.__api_server
    @property
    def token(self):
        return self.__token
    @property
    def config_path(self):
        return self.__config_path
    @property
    def skip_tls(self):
        return self.__skip_tls
    @property
    def cert_data(self):
        return self.__cert_data
    @property
    def namespace(self):
        return self.__namespace
    @property
    def values(self):
        return self.__values
    @property
    def string_values(self):
        return self.__string_values
    @property
    def debug(self):
        return self.__debug
    @property
    def dry_run(self):
        return self.__dry_run
    @property
    def release(self):
        return self.__release
    @property
    def chart(self):
        return self.__chart

    @api_server.setter
    def api_server(self, api_server):
        self.__api_server = api_server
    @token.setter
    def token(self, token):
        self.__token = token
    @config_path.setter
    def config_path(self, config_path):
        self.__config_path = config_path
    @skip_tls.setter
    def skip_tls(self, skip_tls):
        self.__skip_tls = skip_tls
    @cert_data.setter
    def cert_data(self, cert_data):
        self.__cert_data = cert_data
    @namespace.setter
    def namespace(self, namespace):
        self.__namespace = namespace
    @values.setter
    def values(self, values):
        self.__values = values
    @string_values.setter
    def string_values(self, string_values):
        self.__string_values = string_values
    @debug.setter
    def debug(self, debug):
        self.__debug = debug
    @dry_run.setter
    def dry_run(self, dry_run):
        self.__dry_run = dry_run
    @release.setter
    def release(self, release):
        self.__release = release
    @chart.setter
    def chart(self, chart):
        self.__chart = chart


'''
return false if input is neither "true" nor "false", else change it to bool type
'''
def strToBoolHandler(s): 
    if s.lower() != "true" and s.lower() != "false":
        s = False
    else:
        s = strtobool(s)
    return s


def resolveEnv():
    api_server = os.environ.get("KUBE_SERVER") or os.environ.get("PLUGIN_KUBE_SERVER") or ""
    token = os.environ.get("KUBE_TOKEN") or os.environ.get("PLUGIN_KUBE_TOKEN") or ""
    config_path = os.environ.get("CONFIG_PATH") or os.environ.get("PLUGIN_CONFIG_PATH") or "/root/.kube/config"
    skip_tls = os.environ.get("SKIP_TLS") or os.environ.get("PLUGIN_SKIP_TLS") or "false"
    skip_tls = strToBoolHandler(skip_tls)
    cert_data = os.environ.get("CERT_DATA") or os.environ.get("PLUGIN_CERT_DATA") or ""
    namespace = os.environ.get("NAMESPACE") or os.environ.get("PLUGIN_NAMESPACE") or ""
    
    values = os.environ.get("PLUGIN_VALUES") or ""
    string_values = os.environ.get("PLUGIN_STRING_VALUES") or ""
    debug = os.environ.get("PLUGIN_DEBUG") or "false"
    debug = strToBoolHandler(debug)
    dry_run = os.environ.get("PLUGIN_DRY_RUN") or "false"
    dry_run = strToBoolHandler(dry_run)
    release = os.environ.get("PLUGIN_RELEASE") or ""
    chart = os.environ.get("PLUGIN_CHART") or ""

    return Config(
        api_server,
        token,
        config_path,
        skip_tls,
        cert_data,
        namespace,
        values,
        string_values,
        debug,
        dry_run,
        release,
        chart)
    


def genKubeconfig(conf):
    default_path = "/root/.kube/template_config"

    if conf.api_server == "":
        print("No api_server supply")
        exit(1)

    if conf.token == "":
        print("No token supply")
        exit(1)

    d = {
        "api_server": conf.api_server,
        "token": conf.token,
        "skip_tls": conf.skip_tls,
        "cert_data": conf.cert_data,
        "namespace": conf.namespace
    }

    with open(default_path, "r") as f:
        t = Template(f.read())

    if conf.debug:
        print(t.render(d))

    with open(conf.config_path,"w") as f:
        f.write(t.render(d))


def genCommand(conf):
    cmd = ["upgrade", "--install"]
    cmd.append(conf.release)
    cmd.append(conf.chart)
    if conf.values != "":
        cmd.append("--set")
        cmd.append(conf.values)
    if conf.string_values != "":
        cmd.append("--set-string")
        cmd.append(conf.string_values)
    if conf.debug:
        cmd.append("--debug")
    return cmd


def runHelm(arg):
    p = subprocess.Popen(["helm"].extend(cmd), shell=False)
    p.communicate()


if __name__ == "__main__":

    conf = resolveEnv()
    genKubeconfig(conf)

    cmd = genCommand(conf)
    if conf.debug:
        print(cmd)

    runHelm(cmd)
