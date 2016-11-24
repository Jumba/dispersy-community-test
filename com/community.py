import logging

from .conversion import ExampleConversion
from .payload import ExamplePayload

from dispersy.authentication import MemberAuthentication
from dispersy.community import Community
from dispersy.conversion import DefaultConversion
from dispersy.destination import CommunityDestination
from dispersy.distribution import DirectDistribution
from dispersy.message import Message, DelayMessageByProof
from dispersy.resolution import PublicResolution

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class ExampleCommunity(Community):

    @classmethod
    def get_master_members(cls, dispersy):
    	master_key = "3081a7301006072a8648ce3d020106052b8104002703819200040578e79f08d3270c5af04ace5b572ecf46eef54502c1" \
                     "4f3dc86f4cd29e86f05dad976b08da07b8d97d73fc8243459e09b6b208a2c8cbf6fdc7b78ae2668606388f39ef0fa715cf2" \
                     "104ad21f1846dd8f93bb25f2ce785cced2c9231466a302e5f9e0e70f72a3a912f2dae7a9a38a5e7d00eb7aef23eb42398c38" \
                     "59ffadb28ca28a1522addcaa9be4eec13095f48f7cf35".decode("HEX")

    	master = dispersy.get_member(public_key=master_key)
        return [master]

    def initialize(self):
        super(ExampleCommunity, self).initialize()
        logger.info("Example community initialized")

    def initiate_meta_messages(self):
        return super(ExampleCommunity, self).initiate_meta_messages() + [
            Message(self, u"example",
                    MemberAuthentication(encoding="sha1"),
                    PublicResolution(),
                    DirectDistribution(),
                    CommunityDestination(node_count=10),
                    ExamplePayload(),
                    self.check_message,
                    self.on_example),
        ]

    def initiate_conversions(self):
        return [DefaultConversion(self), ExampleConversion(self)]

    def check_message(self, messages):
        for message in messages:
            allowed, _ = self._timeline.check(message)
            if allowed:
                yield message
            else:
                yield DelayMessageByProof(message)

    def send_example(self, text, amount, store=True, update=True, forward=True):
        logger.debug("sending example")
        meta = self.get_meta_message(u"example")
        message = meta.impl(authentication=(self.my_member,),
                            distribution=(self.claim_global_time(),),
                            payload=((text, amount),))
        self.dispersy.store_update_forward([message], store, update, forward)

    def on_example(self, messages):
        for message in messages:
            logger.debug("received example message")

