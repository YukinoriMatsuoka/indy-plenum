from plenum.common.util import randomString
from plenum.test.cli.helper import checkClientConnected
from plenum.test.eventually import eventually


def testClientNames(cli, validNodeNames, createAllNodes):
    """
    Test adding clients with valid and invalid names(prefixed with node names).
    Also testing adding clients with duplicate names
    """
    cName = "Joe"

    def checkClientNotAddedWithNodeName(name):
        # Count of cli.clients should still be 1
        assert len(cli.clients) == 1
        # nm should not be in cli.client
        assert name not in cli.clients

        msg = cli.lastPrintArgs['msg']
        # Appropriate error msg should be printed
        assert msg == "Client name cannot start with node names, which are {}." \
                      "".format(', '.join(validNodeNames))


    cli.enterCmd("new client {}".format(cName))
    # Count of cli.clients should be 1
    assert len(cli.clients) ==1
    # Client name should be in cli.client
    assert cName in cli.clients

    cli.looper.run(eventually(checkClientConnected, cli, validNodeNames, cName,
                              retryWait=1, timeout=5))

    # Add clients with name same as a node name or starting with a node name
    for i, nm in enumerate(validNodeNames):
        # Adding client with name same as that of a node
        cli.enterCmd("new client {}".format(nm))
        checkClientNotAddedWithNodeName(nm)

        # Adding client with name prefixed with that of a node
        cli.enterCmd("new client {}{}".format(nm, randomString(3)))
        checkClientNotAddedWithNodeName(nm)

    cli.enterCmd("new client {}".format(cName))
    # Count of cli.clients should be 1
    assert len(cli.clients) == 1
    # Client name should be in cli.client
    assert cName in cli.clients

    msg = cli.lastPrintArgs['msg']
    # Appropriate error msg should be printed
    assert msg == "Client {} already exists.".format(cName)

