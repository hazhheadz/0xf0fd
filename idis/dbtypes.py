from arch import getDecoder


class CommentPosition:
    POSITION_BEFORE = 0
    POSITION_RIGHT = 1
    POSITION_BOTTOM = 2
    
class proxy_dict(dict):
    def __getstate__(self):
        return dict([i for i in self.__dict__.items() if i[0] != 'parent'])

    def __init__(self, parent, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.parent = parent

    def __setitem__(self, k,v):
        if self.parent:
            self.parent()
        return dict.__setitem__(self, k,v)

    def __delitem__(self, v):
        if self.parent:
            self.parent()
        return dict.__delitem__(self, v)


# On set force-update parameter
class SUD(object):
    def __init__(self, name, validator = None):
        self.name = name
        self.validator = validator
    def __get__(self, instance, owner):
        if self.name not in instance.__dict__:
            raise AttributeError, self.name
        return instance.__dict__[self.name]
        
    def __set__(self, instance, value):
        if self.validator: assert self.validator(value)
        instance.__dict__[self.name] = value
        instance.push_changes()



class Segment(object):
    def __init__(self, data, base_addr):
        self.__data = data
        self.__base_addr = base_addr


    def __getlength(self):
        return len(self.__data)
    length = property(__getlength)
    
    def __getbaseaddr(self):
        return self.__base_addr
    base_addr = property(__getbaseaddr)
    
    def readBytes(self, start, length = 1):
        if (start < self.__base_addr or start >= self.__base_addr + self.__getlength()):
            raise IOError, "not in segment"
        return self.__data[start-self.__base_addr:start-self.__base_addr+length]

class Symbol(object):
    TYPE_LOCAL = 0
    TYPE_FNENT = 1
    TYPE_MULTIUSE = 2
    
    def __init__(self, datastore, address, name, type = TYPE_LOCAL):
            self.ds = datastore
            self.address = address
            self.name = name
            self.type = type
    
    def __str__(self):
        return self.name


# Temporary mock operand until the type system gets sorted out
class DefaultMock(object):
    """ Mock object created when there is nothing in the DB about a given address """
    class OperandMock(object):
        def __init__(self, value):
            self.value = value

        def render(self, ds):
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


# Information about a memory location
class MemoryInfo(object):
    @staticmethod
    def createForTypeName(ds, addr, typename):
        """ Create an MemoryInfo object, given only the desired typename"""        
        decoder = getDecoder(ds, typename)
        decoded = decoder.disassemble(addr, saved_params=None)
        m = MemoryInfo("key!!",
                ds = ds,
                addr = addr,
                length = decoded.length(),
                typeclass = decoder.typeclass,
                typename = decoder.shortname,
                disasm = decoded,
                persist_attribs = None)

        return m

    @staticmethod 
    def createFromParams(ds, addr, length, typename, typeclass, persist_attribs):
        try:
            saved_params = persist_attribs["saved_params"]
        except KeyError:
            saved_params = {}
        
        decoder = getDecoder(ds, typename)
        
        decoded = decoder.disassemble(addr, saved_params=saved_params)
        assert decoded.length() == length

        m = MemoryInfo("key!!",
                ds = ds,
                addr = addr,
                length = decoded.length(),
                typeclass = decoder.typeclass,
                typename = decoder.shortname,
                disasm = decoded,
                persist_attribs = persist_attribs)

        return m

    def __getstate__(self):
        dont_save = ["xrefs", "ds_link"]
        return dict([i for i in self.__dict__.items() if i[0] not in dont_save])

    def __setstate__(self, d):
        self.__dict__ = d
        self.__cdict.parent = self.push_changes

        # mutable, not serialized
        self.xrefs = []

    # Addr is read-only, since its a primary key. 
    # Delete and recreate to change
    def __get_addr(self): return self._addr
    addr = property(__get_addr)

    # length of this memory opcode
    length = SUD("_length")
    
    # Text form of the decoding [TODO: rename?]
    disasm = SUD("_disasm")
    
    # Check comments against the main DB
    def __setcomment(self, text):
    
        self.ds.comments.setComment(self.addr, text, CommentPosition.POSITION_RIGHT)        
    def __getcomment(self):
        comment = self.ds.comments.getComments(self.addr, position=CommentPosition.POSITION_RIGHT)
        if not comment:
            return ""
        return comment[0]
        
    comment = property(__getcomment, __setcomment)
    
    # General type of the data
    # Currently two valid values ["code", "data"]
    def __validate_typeclass(value):
        return value in ["code", "data", "default"]
    
    typeclass = SUD("_typeclass", __validate_typeclass)
    __validate_typeclass = staticmethod(__validate_typeclass)
    
    
    # Actual type of the data
    typename = SUD("_typename")

    # Check symbol against main datasource
    def __setlabel(self, label):
        self.ds.symbols.setSymbol(self.addr, label)     
    def __getlabel(self):
        return self.ds.symbols.getSymbol(self.addr)
    label = property(__getlabel, __setlabel)
    
    def __get_cdict(self): return self.__cdict
    cdict = property(__get_cdict)
    
    def __init__(self, ff, addr, length, typeclass, typename, disasm, ds, persist_attribs):
        assert ff == "key!!" # Make sure all incorrect instantiations are gone

        self.ds = ds
        # legacy
        self.ds_link = None

        # Create the custom properties dictionary
        self.__cdict = dict() #proxy_dict(self.push_changes)
        
        if not persist_attribs:
            self.persist_attribs = proxy_dict(self.push_changes)
        else:
            self.persist_attribs = persist_attribs
                                
        self._addr = addr
        self._length = length
        self._disasm = disasm
        
        assert MemoryInfo.__validate_typeclass(typeclass)
        self._typeclass = typeclass
        
        self._typename = typename
        
        # Should go away too
        self.xrefs = []
        

    def push_changes(self):
        if (self.ds_link):
            self.ds_link(self.addr, self)


