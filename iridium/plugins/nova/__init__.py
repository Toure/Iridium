class NovaPlugin(type):
    def __init__(cls, name, bases, what):
        super().__init__(what)
        if not hasattr(cls, 'registry'):
            cls.registry = set()
        else:
            cls.registry.add(cls)
            cls.registry -= set(bases)

    def __iter__(cls):
        """

        :param cls:
        :return:
        """
        return iter(cls.registry)
