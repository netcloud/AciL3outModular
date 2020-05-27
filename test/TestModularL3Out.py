# <editor-fold desc="Imports">
import unittest
from L3Out.ModularL3Out import L3Out
# </editor-fold>


class TestModularL3Out(unittest.TestCase):

    def test_simple(self):
        l3_out_2_post = L3Out("L3Out-Name-xyz", "Tenant-Name-xyz")
        l3_out_2_post.setEnableBgp()
        l3_out_2_post.setExternalEpg('External')
        l3_out_2_post.externalEpg().setL3ExtSubnet('0.0.0.0/0', False, False)
        l3_out_2_post.setNodeProfile('Node')
        l3_out_2_post.nodeProfile().setNode('topology/pod-1/node-111','10.1.1.111')
        l3_out_2_post.nodeProfile().setInt('INT')
        l3_out_2_post.nodeProfile().Int().setIntNode('sub-interface', "vlan-123", '10.1.2.1/30', 'topology/pod-1/paths-111/pathep-[eth1/50]')
        l3_out_2_post.nodeProfile().Int().intNode().setBgpPeer('10.1.2.2', 'Secure-PWD')
        l3_out_2_post.nodeProfile().Int().intNode().bgpPeer().setBgpAS('65412')

        test_dict = {'l3extOut': {'attributes': {'dn': 'uni/tn-Tenant-Name-xyz/out-L3Out-Name-xyz', 'name': 'L3Out-Name-xyz', 'rn': 'out-L3Out-Name-xyz', 'status': 'created,modified'}, 'children': [{'bgpExtP': {'attributes': {'rn': 'bgpExtP', 'status': 'created,modified'}}}, {'l3extInstP': {'attributes': {'name': 'External', 'rn': 'instP-External', 'status': 'created,modified'}, 'children': [{'l3extSubnet': {'attributes': {'aggregate': '', 'ip': '0.0.0.0/0', 'rn': 'extsubnet-[0.0.0.0/0]', 'status': 'created,modified'}}}]}}, {'l3extLNodeP': {'attributes': {'name': 'Node', 'rn': 'lnodep-Node', 'status': 'created,modified'}, 'children': [{'l3extRsNodeL3OutAtt': {'attributes': {'rn': 'rsnodeL3OutAtt-[topology/pod-1/node-111]', 'rtrIdLoopBack': 'no', 'tDn': 'topology/pod-1/node-111', 'rtrId': '10.1.1.111', 'status': 'created,modified'}, 'children': [{'l3extInfraNodeP': {'attributes': {'fabricExtCtrlPeering': 'false', 'status': 'created,modified'}, 'children': []}}]}}, {'l3extLIfP': {'attributes': {'rn': 'lifp-INT', 'name': 'INT', 'status': 'created,modified'}, 'children': [{'l3extRsPathL3OutAtt': {'attributes': {'mac': '00:22:BD:F8:19:FF', 'ifInstT': 'sub-interface', 'encap': 'vlan-123', 'addr': '10.1.2.1/30', 'tDn': 'topology/pod-1/paths-111/pathep-[eth1/50]', 'rn': 'rspathL3OutAtt-[topology/pod-1/paths-111/pathep-[eth1/50]]', 'status': 'created,modified'}, 'children': [{'bgpPeerP': {'attributes': {'rn': 'peerP-[10.1.2.2]', 'addr': '10.1.2.2', 'password': 'Secure-PWD', 'status': 'created,modified'}, 'children': [{'bgpAsP': {'attributes': {'rn': 'as', 'asn': '65412', 'status': 'created,modified'}, 'children': []}}]}}]}}]}}]}}]}}

        self.assertDictEqual(l3_out_2_post.tostring(), test_dict)


if __name__ == '__main__':
    unittest.main()
