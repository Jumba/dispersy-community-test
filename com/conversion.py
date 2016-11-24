from Tribler.Core.Utilities.encoding import encode, decode
from dispersy.conversion import BinaryConversion
from dispersy.message import DropPacket


class ExampleConversion(BinaryConversion):

    def __init__(self, community):
        super(ExampleConversion, self).__init__(community, "\x01")
        self.define_meta_message(chr(1), community.get_meta_message(u"example"), self._encode_example, self._decode_example)

    def _encode_example(self, message):
        packet = encode((message.payload.text, message.payload.amount))
        return packet,

    def _decode_example(self, placeholder, offset, data):
        try:
            offset, payload = decode(data, offset)
        except ValueError:
            raise DropPacket("Unable to decode the example-payload")

        if not isinstance(payload, tuple):
            raise DropPacket("Invalid payload type")

        text, amount = payload
        if not isinstance(text, str):
            raise DropPacket("Invalid 'text' type")
        if not isinstance(amount, int):
            raise DropPacket("Invalid 'amount' type")

        return offset, placeholder.meta.payload.implement(text, amount)

