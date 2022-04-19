import sys
import json
import logging
import functools

class Dispatcher:
    def __init__(self, name):
        self.logger = logging.getLogger(f"TheiaPy.Dispatcher({name})")
        self._on_mtype_hooks = {}

        self.name = name
        self.bot_info = {}
        self.plugin_cfg = {}

    def on_mtype(self, *mtypes):
        def inner(func):
            for mtype in mtypes:
                self.logger.debug(f"on_mtype: registering {func!r} for {mtype!r}")

                if not mtype in self._on_mtype_hooks:
                    self._on_mtype_hooks[mtype] = []
                self._on_mtype_hooks[mtype].append(func)

            return func
        return inner

    def on_command(self, cmdname):
        def inner(func):
            @functools.wraps(func)
            def wrapper(mdata, *args, **kwargs):
                if not mdata["message"]["command_invocation"]:
                    return None
                if not mdata["message"]["command_invocation"]["command"] == cmdname:
                    return None

                return func(mdata, *args, **kwargs)

            self.logger.debug(f"on_command: registering {func!r} for command name {cmdname!r}")
            return self.on_mtype("CommandInvoke")(wrapper)
        return inner

    def _handle_line(self, line):
        if len(line.strip()) == 0:
            return

        data = json.loads(line)
        for mtype, mdata in data.items():
            if mtype == "BotInfo":
                self.logger.debug("_handle_line: updating bot_info")
                self.bot_info = mdata

            if mtype == "PluginConfig":
                if "plugin-name" in mdata and mdata["plugin-name"] == self.name:
                    self.logger.debug("_handle_line: updating plugin_cfg")
                    self.plugin_cfg = mdata

            if mtype in self._on_mtype_hooks:
                self.logger.debug(f"_handle_line: calling hooks for mtype={mtype!r}")
                for _fn in self._on_mtype_hooks[mtype]:
                    _fn(mdata)

    def run(self):
        self.logger.info(f"started")
        for line in sys.stdin:
            self._handle_line(line.rstrip())

    def config_get(self, key, default=None):
        for cfgtype in ["config-bot", "config-plugin"]:
            if cfgtype in self.plugin_cfg and key in self.plugin_cfg[cfgtype]:
                return self.plugin_cfg[cfgtype][key]

        return default
