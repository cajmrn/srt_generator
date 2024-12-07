class ProcessorBase:
    def process(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement the `process` method.")
