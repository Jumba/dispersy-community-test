from dispersy.payload import Payload

class ExamplePayload(Payload):
    class Implementation(Payload.Implementation):
        def __init__(self, meta, text, amount):
            assert isinstance(text, str)
            assert isinstance(amount, int)
            super(ExamplePayload.Implementation, self).__init__(meta)
            self._text = text
            self._amount = amount

        @property
        def text(self):
            return self._text

        @property
        def amount(self):
            return self._amount
        

class TextPayload(Payload):
    class Implementation(Payload.Implementation):
        def __init__(self, meta, text):
            assert isinstance(text, unicode)
            assert len(text.encode("UTF-8")) <= 255
            super(TextPayload.Implementation, self).__init__(meta)
            self._text = text

        @property
        def text(self):
            return self._text
