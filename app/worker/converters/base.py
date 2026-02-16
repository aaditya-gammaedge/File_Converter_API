class BaseConverter:
    """
    Base class for all converters.

    """

    def convert(self, input_path: str, output_path: str):
        raise NotImplementedError("convert() method not implemented")
