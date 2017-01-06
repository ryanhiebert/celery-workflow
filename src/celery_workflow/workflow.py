from result import WorkflowResult


class Workflow(object):
    """Like a Signature, but it knows about more stuff."""

    def __init__(self, signature):
        self.signature = signature

    def apply_async(self, *args, **kwargs):
        return WorkflowResult(self.signature.apply_async(*args, **kwargs))

    def apply(self, *args, **kwargs):
        return self.signature.apply(*args, **kwargs)

    def delay(self, *args, **kwargs):
        return WorkflowResult(self.signature.delay(*args, **kwargs))

    def __call__(self, *args, **kwargs):
        return self.signature.__call__(*args, **kwargs)

    def set(self, *args, **kwargs):
        return self.signature.set(*args, **kwargs)

    def __and__(self, other):
        return Group(self.signature, self.other)

    def __or__(self, other):
        return Chain(self.signature, self.other)


class Group(Workflow):
    def __new__(cls):
        """Unwrap groups of groups."""

    def __init__(self):
        pass


class Chain(Workflow):
    def __new__(cls):
        """Convert to a Chord if the left is a Group."""

    def __init__(self):
        pass


class Chord(Workflow):
    pass
