from plenum.test import waits
from plenum.test.node_request.helper import sdk_ensure_pool_functional
from plenum.test.restart.helper import get_group, restart_nodes

nodeCount = 7


def test_restart_groups_6_of_7_np_no_tm(looper, txnPoolNodeSet, tconf, tdir,
                                        sdk_pool_handle, sdk_wallet_client, allPluginsPath):
    tm = tconf.ToleratePrimaryDisconnection + waits.expectedPoolElectionTimeout(len(txnPoolNodeSet))

    restart_group = get_group(txnPoolNodeSet, 6, include_primary=False)

    restart_nodes(looper, txnPoolNodeSet, restart_group, tconf, tdir, allPluginsPath,
                  after_restart_timeout=tm, restart_one_by_one=False)
    sdk_ensure_pool_functional(looper, txnPoolNodeSet, sdk_wallet_client, sdk_pool_handle)
