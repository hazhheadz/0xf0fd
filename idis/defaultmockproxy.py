from datastore import DataStore


# Temporary mock operand until the type system gets sorted out
class DefaultMock(object):
    """ Mock object created when there
    is nothing in the DB about a given address """

    class OperandMock(object):
        def __init__(self, value):
            self.value = value

        def render(self, ds, segment):
            return "0x%02x" % self.value, 0

    class DisasmMock(object):
        def __init__(self, value):
            self.mnemonic = ".db"
            self.operands = [DefaultMock.OperandMock(value)]

    def __init__(self, ds, addr):
        self.value = ds.readBytes(addr, 1)[0]
        self.disasm = DefaultMock.DisasmMock(self.value)
        self.typename = "default"
        self.typeclass = "default"
        self.addr = addr
        self.label = None
        self.cdict = {}
        self.length = 1
        self.comment = ""


class DefaultMockProxy(object):
    """Proxy that returns "mock" objects for any memory location that is
        valid but does not have a real repr in the datastore"""

    def __init__(self, datastore):
        self.__subject = datastore

    def __iter__(self):
        raise TypeError("'DefaultMockProxy' object is not iterable")

    # Deprecated interface, use lookup
    def __contains__(self, ident):
        status, value = self.lookup(ident)
        return status == DataStore.LKUP_OK

    # Deprecated interface, use lookup
    def __getitem__(self, ident):
        status, value = self.lookup(ident)
        if status == DataStore.LKUP_OK:
            return value

        raise KeyError

    def __setitem__(self, ident, value):
        self.__subject.__setitem__(ident, value)

    def __createDefault(self, ident):
        # Only return a defaults object if we're within a valid memory range
        try:
            self.readBytes(ident, 1)
            mi = DefaultMock(self, ident)
            return mi
        except IOError:
            return None

    # find the instruction that includes this address
    def findStartForAddress(self, seekaddr):
        stat, obj = self.lookup(seekaddr)

        if stat == self.LKUP_OK:
            return seekaddr

        elif stat == self.LKUP_NONE:
            return None

        elif stat == self.LKUP_OVR:
            return obj.addr

    def lookup(self, ident):
        real_lookup_status, real_result = self.__subject.lookup(ident)

        if real_lookup_status in [DataStore.LKUP_OK, DataStore.LKUP_OVR]:
            return real_lookup_status, real_result

        default_result = self.__createDefault(ident)

        if default_result:
            return DataStore.LKUP_OK, default_result

        return DataStore.LKUP_NONE, None

    def __getattr__(self, name):
        return getattr(self.__subject, name)
