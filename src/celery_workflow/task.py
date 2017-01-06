class Task(_Task):
    """Use the more convenient Workflow class."""

    def workflow(self, *args, **kwargs):
        signature = super(Task, self).subtask(*args, **kwargs)
        return Workflow(signature)
    subtask = signature = workflow

    def w(self, *args, **kwargs):
        return self.workflow(args, kwargs)

    def wi(self, *args, **kwargs):
        return self.workflow(args, kwargs, immutable=True)
