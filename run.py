import logging
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from com.community import ExampleCommunity
from com.dispersy.dispersy import Dispersy
from com.dispersy.endpoint import StandaloneEndpoint

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
import time

def start_dispersy():
    master_key = "3081a7301006072a8648ce3d020106052b8104002703819200040578e79f08d3270c5af04ace5b572ecf46eef54502c1" \
                 "4f3dc86f4cd29e86f05dad976b08da07b8d97d73fc8243459e09b6b208a2c8cbf6fdc7b78ae2668606388f39ef0fa715cf2" \
                 "104ad21f1846dd8f93bb25f2ce785cced2c9231466a302e5f9e0e70f72a3a912f2dae7a9a38a5e7d00eb7aef23eb42398c38" \
                 "59ffadb28ca28a1522addcaa9be4eec13095f48f7cf35".decode("HEX")
    dispersy = Dispersy(StandaloneEndpoint(1235, '0.0.0.0'), unicode('.'), u'dispersy.db')
    dispersy.statistics.enable_debug_statistics(True)
    dispersy.start(autoload_discovery=True)

    my_member = dispersy.get_new_member()
    master_member = dispersy.get_member(public_key=master_key)

    community = ExampleCommunity.init_community(dispersy, master_member, my_member)

    LoopingCall(lambda:community.send_example("Test", int(time.time()))).start(1.0)


def main():
    reactor.callWhenRunning(start_dispersy)
    reactor.run()

if __name__ == "__main__":
    main()
