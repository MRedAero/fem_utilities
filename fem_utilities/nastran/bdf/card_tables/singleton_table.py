__author__ = 'Michael Redmond'


class SingletonDecorator(object):
    def __init__(self, klass):
        self.klass = klass
        self.instance = None

    def __call__(self, h5file):
        if self.instance is None:
            self.instance = self.klass(h5file)
        else:
            self.instance.__init__(h5file)

        return self.instance