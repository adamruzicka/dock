"""
Pre build plugin which injects custom yum repository in dockerfile.
"""
import os
import re
import uuid
import sys
from dock.plugin import PreBuildPlugin


def alter_dockerfile(df, cmd):
    regex = re.compile(r"(?P<FROM>FROM\s+.*)", re.MULTILINE)
    sub_func = lambda match: match.group('FROM') + "\nRUN " + cmd
    return regex.sub(sub_func, df)


class RunCmdInContainerPlugin(PreBuildPlugin):
    key = "run_cmd_in_container"

    def __init__(self, tasker, workflow, cmd):
        """
        constructor

        :param tasker: DockerTasker instance
        :param workflow: DockerBuildWorkflow instance
        :param cmd: str, Command to execute
        """
        # call parent constructor
        super(RunCmdInContainerPlugin, self).__init__(tasker, workflow)
        self.cmd = cmd

    def run(self):
        """
        run the plugin
        """

        with open(self.workflow.builder.df_path, "r+") as fd:
            df = fd.read()
            out = alter_dockerfile(df, self.cmd)
            fd.seek(0)
            fd.truncate()
            fd.write(out)
