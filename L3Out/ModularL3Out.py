from enum import Enum
import json


class SharedValues:
    _Attr = "attributes"
    _Child = "children"
    _Uni = "uni/"
    _Tenant = ""
    _StatusN = "status"
    _StatusC = "created"
    _StatusM = "modified"

    def __init__(self, jsonkey, children=False):
        self._JsonKey = jsonkey
        self._json2Post = {self._JsonKey: {str(self._Attr): {}, }}
        self.__initJson__()
        self._json2Post[self._JsonKey][self._Attr][self._StatusN] = self._StatusC + "," + self._StatusM
        self.__setDefaults__()
        if children: self.__addChild__()

    def __initJson__(self):
        for item in self.JsonAttr:
            self._json2Post[self._JsonKey][self._Attr][item.value] = ""

    def __addChild__(self):
        self._json2Post[self._JsonKey][self._Child] = []

    def tostring(self):
        return self._json2Post

    def __inserExisting__(self, exstring="", addstring=""):
        if exstring == "":
            return addstring
        else:
            return exstring + "," + addstring


class L3Out(SharedValues):
    _ObjectName = "l3extOut"
    _Prefix = "out-"

    class JsonAttr(Enum):
        Dn = "dn"
        Name = "name"
        Rn = "rn"

    def __init__(self, name, tenant):
        self._children = []
        self._L3OutName = name
        self._Tenant = tenant
        self._ExternalEPG = None
        self._NodeProfile = None
        self._Tenant = "tn-" + tenant
        self._Dn = self._Uni + self._Tenant + "/" + self._Prefix + self._L3OutName
        self._RouteMap = None

        SharedValues.__init__(self, self._ObjectName, True)

    def __setDefaults__(self):
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Dn.value] = self._Dn
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Name.value] = self._L3OutName
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Rn.value] = self._Prefix + self._L3OutName

    def setl3domain(self, name):
        self._json2postChild = L3Domain(name).tostring()
        self._children.append(self._json2postChild)

    def setVrf(self, name):
        self._json2postChild = VRF(name).tostring()
        self._children.append(self._json2postChild)

    def setExternalEpg(self, name):
        self._ExternalEPG = ExternalEpg(name)
        self._json2postChild = self._ExternalEPG.tostring()
        self._children.append(self._json2postChild)

    def setEnableBgp(self):
        self._EnableBgp = L3EnBGP()
        self._json2postChild = self._EnableBgp.tostring()
        self._children.append(self._json2postChild)

    def setEnableL3Multicast(self):
        self._EnableMulticast = L3EnMulticast()
        self._json2postChild = self._EnableMulticast.tostring()
        self._children.append(self._json2postChild)

    def setNodeProfile(self, name):
        self._NodeProfile = NodeProfile(name)
        self._json2postChild = self._NodeProfile.tostring()
        self._children.append(self._json2postChild)

    def nodeProfile(self):
        """
        :rtype: NodeProfile
        """
        if self._NodeProfile:
            return self._NodeProfile
        else:
            print("No Node Profile defined!")

    def externalEpg(self):
        """
        :rtype: ExternalEpg
        """
        if self._ExternalEPG:
            return self._ExternalEPG
        else:
            print("No ExternalEPG defined!")

    def setRouteMap(self, name):
        self._RouteMap = RouteMap(name)
        self._json2postChild = self._RouteMap.tostring()
        self._children.append(self._json2postChild)

    def routeMap(self):
        """
        :rtype: RouteMap
        """
        if self._RouteMap:
            return self._RouteMap
        else:
            print("No Route-Map defined!")

    def tostring(self):
        self._json2Post[self._JsonKey][self._Child] = self._children
        _jsonDump = json.dumps(self._json2Post)
        return self._json2Post


class NodeProfile(SharedValues):
    _ObjectName = "l3extLNodeP"
    _Prefix = "lnodep-"

    class JsonAttr(Enum):
        Name = "name"
        Rn = "rn"

    def __init__(self, name):
        self.Name = name
        SharedValues.__init__(self, self._ObjectName, True)
        self._children = []
        self._BgpPeer = None

    def __setDefaults__(self):
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Name.value] = self.Name
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Rn.value] = self._Prefix + self.Name

    def setNode(self, topology, rtid):
        self._Node = Node(topology, rtid)
        self._json2postChild = self._Node.tostring()
        self._children.append(self._json2postChild)

    def setInt(self, name):
        self._IntProfile = INT(name)
        self._json2postChild = self._IntProfile.tostring()
        self._children.append(self._json2postChild)

    def Int(self):
        """
        :rtype: INT
        """
        if self._IntProfile:
            return self._IntProfile
        else:
            print("No Int Profile defined!")

    def Node(self):
        """
        :rtype: Node
        """
        if self._Node:
            return self._Node
        else:
            print("No Node Profile defined!")

    def setBgpPeer(self, addr, pwd, ttl):
        self._BgpPeer = BgpPeer(addr, pwd, ttl)
        self._json2postChild = self._BgpPeer.tostring()
        self._children.append(self._json2postChild)

    def bgpPeer(self):
        """
        :rtype: BgpPeer
        """
        if self._BgpPeer:
            return self._BgpPeer
        else:
            print("No BGP Peer defined!")

    def tostring(self):
        self._json2Post[self._JsonKey][self._Child] = self._children
        return self._json2Post


class RouteMap(SharedValues):
    _ObjectName = "rtctrlProfile"
    _Prefix = "prof-"

    class JsonAttr(Enum):
        Name = "name"
        Type = "type"

    def __init__(self, name):
        self.Name = name
        SharedValues.__init__(self, self._ObjectName, True)
        self._children = []
        self._routeContextControl = None

    def __setDefaults__(self):
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Name.value] = self.Name
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Type.value] = 'combinable'

    def setRouteControlContext(self, name, action, order):
        self._routeContextControl = RouteContextControl(name, action, order)
        self._json2postChild = self._routeContextControl.tostring()
        self._children.append(self._json2postChild)

    def routeControlContext(self):
        """
        :rtype: RouteContextControl
        """
        if self._routeContextControl:
            return self._routeContextControl
        else:
            print("No RouteContext defined!")

    def tostring(self):
        self._json2Post[self._JsonKey][self._Child] = self._children
        return self._json2Post


class RouteContextControl(SharedValues):
    _ObjectName = "rtctrlCtxP"

    class JsonAttr(Enum):
        Name = "name"
        Action = "action"
        Order = "order"

    def __init__(self, name, action, order):
        self.Name = name
        self.Action = action
        self.Order = order
        SharedValues.__init__(self, self._ObjectName, True)
        self._children = []
        self._matchRules = None

    def __setDefaults__(self):
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Name.value] = self.Name
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Action.value] = self.Action
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Order.value] = self.Order

    def setMatchRules(self, ruleName):
        self._matchRules = MatchRules(ruleName)
        self._json2postChild = self._matchRules.tostring()
        self._children.append(self._json2postChild)

    def matchRules(self):
        """
        :rtype: MatchRules
        """
        if self._matchRules:
            return self._matchRules
        else:
            print("No Match Rule defined!")

    def tostring(self):
        self._json2Post[self._JsonKey][self._Child] = self._children
        return self._json2Post


class MatchRules(SharedValues):
    _ObjectName = "rtctrlRsCtxPToSubjP"

    class JsonAttr(Enum):
        RuleName = "tnRtctrlSubjPName"

    def __init__(self, ruleName):
        self.RuleName = ruleName
        SharedValues.__init__(self, self._ObjectName, False)
        self._children = []

    def __setDefaults__(self):
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.RuleName.value] = self.RuleName

    def tostring(self):
        return self._json2Post


class BgpPeer(SharedValues):
    _ObjectName = "bgpPeerP"
    _Prefix = "peerP-"

    class JsonAttr(Enum):
        Rn = "rn"
        Addr = "addr"
        PWD = "password"
        TTL = "ttl"

    def __init__(self, addr, pwd, ttl="1"):
        self._Addr = addr
        self._PWD = pwd
        self._TTL = ttl
        self._children = []
        SharedValues.__init__(self, self._ObjectName, True)

    def __setDefaults__(self):
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Addr.value] = self._Addr
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.PWD.value] = self._PWD
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.TTL.value] = self._TTL
        self._json2Post[self._JsonKey][self._Attr][
            self.JsonAttr.Rn.value] = self._Prefix + "[" + self._Addr + "]"

    def tostring(self):
        self._json2Post[self._JsonKey][self._Child] = self._children
        return self._json2Post

    def setBgpAS(self, asn):
        self._BgpAs = self.BgpAS(asn)
        self._json2postChild = self._BgpAs.tostring()
        self._children.append(self._json2postChild)

    def setBgpLocalAS(self, localas, asnprop="replace-as"):
        self._BgpLocalAs = self.BgpLocalAS(localas, asnprop)
        self._json2postChild = self._BgpLocalAs.tostring()
        self._children.append(self._json2postChild)

    class BgpAS(SharedValues):
        _ObjectName = "bgpAsP"

        class JsonAttr(Enum):
            Rn = "rn"
            Asn = "asn"

        def __init__(self, asn):
            self._Asn = asn
            self._children = []
            SharedValues.__init__(self, self._ObjectName, True)

        def __setDefaults__(self):
            self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Asn.value] = self._Asn
            self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Rn.value] = "as"

        def tostring(self):
            return self._json2Post

    class BgpLocalAS(SharedValues):
        _ObjectName = "bgpLocalAsnP"

        class JsonAttr(Enum):
            Rn = "rn"
            LocalASN = "localAsn"
            ASNProp = "asnPropagate"

        def __init__(self, localas, asnprop):
            self._LocalASN = localas
            self._ASNProp = asnprop
            self._children = []
            SharedValues.__init__(self, self._ObjectName, True)

        def __setDefaults__(self):
            self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.ASNProp.value] = self._ASNProp
            self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.LocalASN.value] = self._LocalASN
            self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Rn.value] = "localasn"

        def tostring(self):
            return self._json2Post


class Node(SharedValues):
    _ObjectName = "l3extRsNodeL3OutAtt"
    _Prefix = "rsnodeL3OutAtt-"

    class JsonAttr(Enum):
        Rn = "rn"
        Loopback = "rtrIdLoopBack"
        TDn = "tDn"
        RouterID = "rtrId"

    def __init__(self, topology, rtid):
        self.Topology = topology
        self.RtId = rtid
        self._children = []
        SharedValues.__init__(self, self._ObjectName, True)
        self._IpRoute = None

    def __setDefaults__(self):
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Loopback.value] = "no"
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.TDn.value] = self.Topology
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.RouterID.value] = self.RtId
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Rn.value] = self._Prefix + "[" + self.Topology + "]"

        self._l3extInfraNodeP = self.l3extInfraNodeP()
        self._json2postChild = self._l3extInfraNodeP.tostring()
        self._children.append(self._json2postChild)

    def setIpRoute(self, ip, pref, nexthop, prefnexthop):
        self._IpRoute = self.IpRoute(ip, pref, nexthop, prefnexthop)
        self._json2postChild = self._IpRoute.tostring()
        self._children.append(self._json2postChild)

    def intNode(self):
        if self._IntNodeSpecific:
            return self._IntNodeSpecific
        else:
            print("No Int Node Profile defined!")

    def setLoopback(self, addr):
        self._Loopback = self.Loopback(addr)
        self._json2postChild = self._Loopback.tostring()
        self._children.append(self._json2postChild)

    def tostring(self):
        self._json2Post[self._JsonKey][self._Child] = self._children
        return self._json2Post

    class Loopback(SharedValues):
        _ObjectName = "l3extLoopBackIfP"

        class JsonAttr(Enum):
            Addr = "addr"

        def __init__(self, addr):
            self._Addr = addr
            self._children = []
            SharedValues.__init__(self, self._ObjectName, False)

        def __setDefaults__(self):
            self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Addr.value] = self._Addr

        def tostring(self):
            return self._json2Post

    class IpRoute(SharedValues):
        _ObjectName = "ipRouteP"

        class JsonAttr(Enum):
            Ip = "ip"
            Pref = "pref"

        def __init__(self, ip, pref, nexthop, prefnexthop):
            self._Ip = ip
            self._Pref = pref
            self._children = []
            SharedValues.__init__(self, self._ObjectName, True)
            self._Nexthop = self.setNextHopIP(nexthop, prefnexthop)

        def __setDefaults__(self):
            self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Ip.value] = self._Ip
            self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Pref.value] = self._Pref

        def tostring(self):
            self._json2Post[self._JsonKey][self._Child] = self._children
            return self._json2Post

        def setNextHopIP(self, nexthopip, pref):
            self._Nexthop = self.IpRouteNextHop(nexthopip, pref)
            self._json2postChild = self._Nexthop.tostring()
            self._children.append(self._json2postChild)

        class IpRouteNextHop(SharedValues):
            _ObjectName = "ipNexthopP"

            class JsonAttr(Enum):
                NextHopIp = "nhAddr"
                Pref = "pref"

            def __init__(self, nexthopip, pref):
                self._NextHopIp = nexthopip
                self._Pref = pref

                SharedValues.__init__(self, self._ObjectName)

            def __setDefaults__(self):
                self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.NextHopIp.value] = self._NextHopIp
                self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Pref.value] = self._Pref

            def tostring(self):
                return self._json2Post

    class l3extInfraNodeP(SharedValues):
        _ObjectName = "l3extInfraNodeP"

        class JsonAttr(Enum):
            FabricExtCtrlPeering = "fabricExtCtrlPeering"

        def __init__(self):
            SharedValues.__init__(self, self._ObjectName, True)
            self._children = []

        def __setDefaults__(self):
            self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.FabricExtCtrlPeering.value] = "false"


class INT(SharedValues):
    _ObjectName = "l3extLIfP"
    _Prefix = "lifp-"

    class JsonAttr(Enum):
        Rn = "rn"
        Name = "name"
        Status = "status"

    def __init__(self, name):
        self._Name = name
        self._IntNodeSpecific = None
        self._children = []
        SharedValues.__init__(self, self._ObjectName, True)

    def __setDefaults__(self):
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Name.value] = self._Name
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Rn.value] = self._Prefix + self._Name
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Status.value] = self._StatusC + "," + self._StatusM

    def tostring(self):
        self._json2Post[self._JsonKey][self._Child] = self._children
        return self._json2Post

    def setIntNode(self, inttype, encap, ip, path, mac="00:22:BD:F8:19:FF", ):
        self._IntNodeSpecific = IntNodeSpecific(inttype, encap, ip, path, mac)
        self._json2postChild = self._IntNodeSpecific.tostring()
        self._children.append(self._json2postChild)

    def intNode(self):
        """
        :rtype: IntNodeSpecific
        """
        if self._IntNodeSpecific:
            return self._IntNodeSpecific
        else:
            print("No Int Node Profile defined!")


class IntNodeSpecific(SharedValues):
    _ObjectName = "l3extRsPathL3OutAtt"
    _Prefix = "rspathL3OutAtt-"
    _Local = "local"

    class IntTypes(Enum):
        L3SubInt = "sub-interface"
        L3Int = "l3-port"
        L3SVI = "ext-svi"

    class JsonAttr(Enum):
        Mac = "mac"
        IntType = "ifInstT"
        Encap = "encap"
        Ip = "addr"
        TDn = "tDn"
        Rn = "rn"

    def __init__(self, inttype, encap, ip, path, mac):
        self._children = []
        self._IntType = inttype
        self._MacAddr = mac
        self._Encap = encap
        self._Ip = ip
        self._Path = path
        self._BgpPeer = None
        self._l3SVI = None
        SharedValues.__init__(self, self._ObjectName, True)

    def __setDefaults__(self):
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Mac.value] = self._MacAddr
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.IntType.value] = self._IntType
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Encap.value] = self._Encap
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Ip.value] = self._Ip
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.TDn.value] = self._Path
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Rn.value] = self._Prefix + "[" + \
                                                                             self._json2Post[self._JsonKey][
                                                                                 self._Attr][
                                                                                 self.JsonAttr.TDn.value] + "]"

    def setvlancope(self, scope):
        self._json2Post[self._JsonKey][self._Attr]["encapScope"] = self._Local

    def setBgpPeer(self, addr, pwd):
        self._BgpPeer = self.BgpPeer(addr, pwd)
        self._json2postChild = self._BgpPeer.tostring()
        self._children.append(self._json2postChild)

    def setl3SVI(self, addr, side):
        self._l3SVI = self.L3SVI(addr, side)
        self._json2postChild = self._l3SVI.tostring()
        self._children.append(self._json2postChild)

    def bgpPeer(self):
        """
        :rtype: BgpPeer
        """
        if self._BgpPeer:
            return self._BgpPeer
        else:
            print("No BGP Peer defined!")

    def l3SVI(self):
        """
        :rtype: L3SVI
        """
        if self._l3SVI:
            return self._l3SVI
        else:
            print("No l3SVI definied!")

    def tostring(self):
        self._json2Post[self._JsonKey][self._Child] = self._children
        return self._json2Post

    class L3SVI(SharedValues):
        _ObjectName = "l3extMember"

        class JsonAttr(Enum):
            Addr = "addr"
            Side = "side"

        class Site(Enum):
            LeafA = "A"
            LeafB = "B"

        def __init__(self, addr, side):
            self._Addr = addr

            if str(side).lower() in str(self.Site.LeafA.value).lower():
                self._Side = self.Site.LeafA.value
            elif str(side).lower() in str(self.Site.LeafB.value).lower():
                self._Side = self.Site.LeafB.value
            else:
                print("Site not specified")
            self._children = []

            SharedValues.__init__(self, self._ObjectName, True)
            self._l3SVISecondIP = None

        def __setDefaults__(self):
            self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Addr.value] = self._Addr
            self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Side.value] = self._Side

        def setl3SVISecondIP(self, addr):
            self._l3SVISecondIP = self.L3SVISecondIP(addr)
            self._json2postChild = self._l3SVISecondIP.tostring()
            self._children.append(self._json2postChild)

        def l3SVISecondIP(self):
            """
            :rtype: L3SVISecondIP
            """
            if self._l3SVISecondIP:
                return self._l3SVISecondIP
            else:
                print("No l3SVISecondIP definied!")

        def tostring(self):
            self._json2Post[self._JsonKey][self._Child] = self._children
            return self._json2Post

        class L3SVISecondIP(SharedValues):
            _ObjectName = "l3extIp"

            class JsonAttr(Enum):
                Addr = "addr"

            def __init__(self, addr):
                self._Addr = addr

                SharedValues.__init__(self, self._ObjectName)

            def __setDefaults__(self):
                self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Addr.value] = self._Addr

            def tostring(self):
                return self._json2Post

    class BgpPeer(SharedValues):
        _ObjectName = "bgpPeerP"
        _Prefix = "peerP-"

        class JsonAttr(Enum):
            Rn = "rn"
            Addr = "addr"
            PWD = "password"

        def __init__(self, addr, pwd):
            self._Addr = addr
            self._PWD = pwd
            self._children = []

            SharedValues.__init__(self, self._ObjectName, True)

        def __setDefaults__(self):
            self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Addr.value] = self._Addr
            self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.PWD.value] = self._PWD
            self._json2Post[self._JsonKey][self._Attr][
                self.JsonAttr.Rn.value] = self._Prefix + "[" + self._Addr + "]"

        def tostring(self):
            self._json2Post[self._JsonKey][self._Child] = self._children
            return self._json2Post

        def setBgpAS(self, asn):
            self._BgpAs = self.BgpAS(asn)
            self._json2postChild = self._BgpAs.tostring()
            self._children.append(self._json2postChild)

        def setBgpLocalAS(self, localas, asnprop="replace-as"):
            self._BgpLocalAs = self.BgpLocalAS(localas, asnprop)
            self._json2postChild = self._BgpLocalAs.tostring()
            self._children.append(self._json2postChild)

        class BgpAS(SharedValues):
            _ObjectName = "bgpAsP"

            class JsonAttr(Enum):
                Rn = "rn"
                Asn = "asn"

            def __init__(self, asn):
                self._Asn = asn
                self._children = []
                SharedValues.__init__(self, self._ObjectName, True)

            def __setDefaults__(self):
                self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Asn.value] = self._Asn
                self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Rn.value] = "as"

            def tostring(self):
                return self._json2Post

        class BgpLocalAS(SharedValues):
            _ObjectName = "bgpLocalAsnP"

            class JsonAttr(Enum):
                Rn = "rn"
                LocalASN = "localAsn"
                ASNProp = "asnPropagate"

            def __init__(self, localas, asnprop):
                self._LocalASN = localas
                self._ASNProp = asnprop
                self._children = []
                SharedValues.__init__(self, self._ObjectName, True)

            def __setDefaults__(self):
                self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.ASNProp.value] = self._ASNProp
                self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.LocalASN.value] = self._LocalASN
                self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Rn.value] = "localasn"

            def tostring(self):
                return self._json2Post


class L3EnBGP(SharedValues):
    _ObjectName = "bgpExtP"

    class JsonAttr(Enum):
        Rn = "rn"

    def __init__(self):
        SharedValues.__init__(self, self._ObjectName)

    def __setDefaults__(self):
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Rn.value] = self._ObjectName


class L3EnMulticast(SharedValues):
    _ObjectName = "pimExtP"

    class JsonAttr(Enum):
        Status = "status"

    def __init__(self):
        SharedValues.__init__(self, self._ObjectName)

    def __setDefaults__(self):
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Status.value] = self._StatusC + "," + self._StatusM


class L3Domain(SharedValues):
    _ObjectName = "l3extRsL3DomAtt"
    _Prefix = "l3dom-"

    class JsonAttr(Enum):
        tDn = "tDn"

    def __init__(self, name):
        self.Name = name
        SharedValues.__init__(self, self._ObjectName)

    def __setDefaults__(self):
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.tDn.value] = self._Uni + self._Prefix + self.Name

    def tostring(self):
        return self._json2Post


class VRF(SharedValues):
    _ObjectName = "l3extRsEctx"

    class JsonAttr(Enum):
        VrfName = "tnFvCtxName"

    def __init__(self, name):
        self.Name = name
        SharedValues.__init__(self, self._ObjectName)

    def __setDefaults__(self):
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.VrfName.value] = self.Name
        self._json2Post[self._JsonKey][self._Attr][self._StatusN] = self._StatusC + "," + self._StatusM

    def tostring(self):
        return self._json2Post


class ExternalEpg(SharedValues):
    _ObjectName = "l3extInstP"
    _Prefix = "instP-"

    class JsonAttr(Enum):
        Name = "name"
        Rn = "rn"

    def __init__(self, name):
        self.Name = name
        SharedValues.__init__(self, self._ObjectName, True)
        self._children = []

    def __setDefaults__(self):
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Name.value] = self.Name
        self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Rn.value] = self._Prefix + self.Name

    def setProvideContract(self, ctname):
        self._CtProvide = self.ContractProvide(ctname)
        self._json2postChild = self._CtProvide.tostring()
        self._children.append(self._json2postChild)

    def setConsumeContract(self, ctname):
        self._CtConsume = self.ContractConsume(ctname)
        self._json2postChild = self._CtConsume.tostring()
        self._children.append(self._json2postChild)

    def setRouteMap(self, routeMap, direction):
        self._attachRouteMap = self.AttachRouteMap(routeMap, direction)
        self._json2postChild = self._attachRouteMap.tostring()
        self._children.append(self._json2postChild)

    def setL3ExtSubnet(self, ip="0.0.0.0/0", exportctrl=False, importctrl=True):
        self._L3ExtSubnet = self.L3ExtSubnet(ip, exportctrl, importctrl)
        self._json2postChild = self._L3ExtSubnet.tostring()
        self._children.append(self._json2postChild)

    def tostring(self):
        self._json2Post[self._JsonKey][self._Child] = self._children
        return self._json2Post

    class AttachRouteMap(SharedValues):
        _ObjectName = "l3extRsInstPToProfile"

        class JsonAttr(Enum):
            RouteMap = "tnRtctrlProfileName"
            Direction = "direction"

        def __init__(self, routeMap, direction):
            self._RouteMap = routeMap
            self._Direction = direction
            SharedValues.__init__(self, self._ObjectName)

        def __setDefaults__(self):
            self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.RouteMap.value] = self._RouteMap
            self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Direction.value] = self._Direction

    class ContractProvide(SharedValues):
        _ObjectName = "fvRsProv"
        _MatchT = "AtleastOne"
        _Prio = "unspecified"

        class JsonAttr(Enum):
            Contract = "tnVzBrCPName"

        def __init__(self, ctname):
            self.CtName = ctname
            SharedValues.__init__(self, self._ObjectName)

        def __setDefaults__(self):
            self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Contract.value] = self.CtName
            self._json2Post[self._JsonKey][self._Attr][self._StatusN] = self._StatusC + "," + self._StatusM

    class ContractConsume(SharedValues):
        _ObjectName = "fvRsCons"
        _Prio = "unspecified"

        class JsonAttr(Enum):
            Contract = "tnVzBrCPName"

        def __init__(self, ctname):
            self.CtName = ctname
            SharedValues.__init__(self, self._ObjectName)

        def __setDefaults__(self):
            self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Contract.value] = self.CtName
            self._json2Post[self._JsonKey][self._Attr][self._StatusN] = self._StatusC + "," + self._StatusM

    class L3ExtSubnet(SharedValues):
        _ObjectName = "l3extSubnet"
        _Prefix = "extsubnet-"

        class JsonAttr(Enum):
            Aggregate = "aggregate"
            Ip = "ip"
            Rn = "rn"

        def __init__(self, ip, exportctrl, importctrl):
            SharedValues.__init__(self, self._ObjectName)
            self.setSubnet(ip, exportctrl, importctrl)

        def __setDefaults__(self):
            return

        def setSubnet(self, ip="0.0.0.0/0", exportctrl=False, importctrl=True):
            self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Ip.value] = ip
            self._json2Post[self._JsonKey][self._Attr][self.JsonAttr.Rn.value] = self._Prefix + "[" + ip + "]"
            return self._json2Post
