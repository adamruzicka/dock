from dock.plugin import PostBuildPlugin


__all__ = ('PostBuildRunCmdPlugin', )


class PostBuildRunCmdPlugin(PostBuildPlugin):
    key = "post_run_cmd"

    def __init__(self, tasker, workflow, image_id, cmd):
        """
        constructor

        :param tasker: DockerTasker instance
        :param workflow: DockerBuildWorkflow instance
        """
        # call parent constructor
        super(PostBuildRunCmdPlugin, self).__init__(tasker, workflow)
        self.image_id = image_id
        self.cmd = cmd

    def run(self):
        container_id = self.tasker.run(
            self.image_id,
            command="-c '"+self.cmd+"'",
            create_kwargs={"entrypoint": "/bin/sh"},
            start_kwargs={},
        )
        self.tasker.wait(container_id)
        plugin_output = self.tasker.logs(container_id, stream=False)
        self.tasker.remove_container(container_id)
        return plugin_output
