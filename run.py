from twisted.internet import reactor
from com.dispersy.dispersy import Dispersy
from com.dispersy.endpoint import StandaloneEndpoint
from com.community import ExampleCommunity
import logging

logging.basicConfig()

def main():
    reactor.exitCode = 0
    reactor.run()
    master_key = "3081a7301006072a8648ce3d020106052b8104002703819200040578e79f08d3270c5af04ace5b572ecf46eef54502c1" \
                     "4f3dc86f4cd29e86f05dad976b08da07b8d97d73fc8243459e09b6b208a2c8cbf6fdc7b78ae2668606388f39ef0fa715cf2" \
                     "104ad21f1846dd8f93bb25f2ce785cced2c9231466a302e5f9e0e70f72a3a912f2dae7a9a38a5e7d00eb7aef23eb42398c38" \
                     "59ffadb28ca28a1522addcaa9be4eec13095f48f7cf35".decode("HEX")
    dispersy = Dispersy(StandaloneEndpoint(1234, '0.0.0.0'), unicode('/root/disperst_test/'), u'dispersy.db')
    dispersy.statistics.enable_debug_statistics(True)
    dispersy.start(autoload_discovery=True)

    my_member = dispersy.get_new_member()
    master_member = dispersy.get_member(public_key=master_key)

    community = ExampleCommunity.init_community(dispersy, master_member, my_member)

    exit(reactor.exitCode)

if __name__ == "__main__":
    main()
