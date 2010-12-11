from arch.common.machine import *
import arch.common.bits as bits
from arch.common.builders import get_MachineInstructionBuilder

MRO = MachineRegisterOperand
MIO = MachineImmediateOperand

class MIPSMachineInstruction(MachineInstruction):
    def __init__(self, *args):
        self.operands = args
    def __repr__(self):
        res = self.mnemonic + " "
        for op in self.operands:
            res += op.name + "=" + repr(op.value) + " "
        return res
MIB = get_MachineInstructionBuilder('arch.mips.machine',MIPSMachineInstruction)

class MIPSCodec(TableCodec):
    class SpecialCodec(TableCodec):
        def __init__(self):
            table = [ # bits 5..3 down, 2..0 across
                    ['_d_sll',   '_d_movci',  '_d_srl',    '_d_sra',    '_d_sllv',   None,   '_d_srlv',   '_d_srav'],
                    ['_d_jr',    '_d_jalr',   '_d_movz',   '_d_movn',   '_d_syscall','_d_break',  None,   '_d_sync'],
                    ['_d_mfhi',  '_d_mthi',   '_d_mflo',   '_d_mtlo',   None,   None,   None,   None],
                    ['_d_mult',  '_d_multu',  '_d_div',    '_d_divu',   None,   None,   None,   None],
                    ['_d_add',   '_d_addu',   '_d_sub',    '_d_subu',   '_d_and',    '_d_or',     '_d_xor',    '_d_nor'],
                    [None,  None,   '_d_slt',    '_d_sltu',   None,   None,   None,   None],
                    ['_d_tge',   '_d_tgeu',   '_d_tlt',    '_d_tltu',   '_d_teq',    None,   '_d_tne',    None],
                    [None,  None,   None,   None,   None,   None,   None,   None]
                    ]
            TableCodec.__init__(self,(2,0),(5,3),table)
                    
        def _d_sll(self,data):
            if bits.get(data,25,21):
                return None
            return MIB('sll',None)(
                        MRO('dest',bits.get(data,15,11)),
                        MRO('src',bits.get(data,20,16)),
                        MIO('shift',bits.get(data,10,6))
                     )
        def _d_movci(self,data):
            return None  
        def _d_srl(self,data):
            if bits.get(data,25,22):
                return None
            if bits.test(data,21):
                return MIB('rotr',None)(
                            MRO('dest',bits.get(data,15,11)),
                            MRO('src',bits.get(data,20,16)),
                            MIO('shift',bits.get(data,10,6))
                         )
            return MIB('srl',None)(
                        MRO('dest',bits.get(data,15,11)),
                        MRO('src',bits.get(data,20,16)),
                        MIO('shift',bits.get(data,10,6))
                     )

        def _d_sra(self,data):
            if bits.get(data,25,21):
                return None
            return MIB('sra',None)(
                        MRO('dest',bits.get(data,15,11)),
                        MRO('src',bits.get(data,20,16)),
                        MIO('shift',bits.get(data,10,6))
                     )
        def _d_sllv(self,data):
            if bits.get(data,10,6):
                return None
            return MIB('sllv',None)(
                        MRO('dest',bits.get(data,15,11)),
                        MRO('src',bits.get(data,20,16)),
                        MRO('shift',bits.get(data,25,21))
                     )
        def _d_srlv(self,data):
            if bits.get(data,10,7):
                return None
            if bits.test(data,6):
                return MIB('rotrv',None)(
                            MRO('dest',bits.get(data,15,11)),
                            MRO('src',bits.get(data,20,16)),
                            MIO('shift',bits.get(data,25,21))
                         )
            return MIB('srlv',None)(
                        MRO('dest',bits.get(data,15,11)),
                        MRO('src',bits.get(data,20,16)),
                        MIO('shift',bits.get(data,25,21))
                     )
        def _d_srav(self,data):
            if bits.get(data,10,6):
                return None
            return MIB('srav',None)(
                        MRO('dest',bits.get(data,15,11)),
                        MRO('src',bits.get(data,20,16)),
                        MRO('shift',bits.get(data,25,21))
                     )
                    
        def _d_jr(self,data):
            if bits.get(data,20,11):
                return None
            return MIB('jr',None)(
                        MRO('target',bits.get(data,25,21)),
                        MRO('hint',bits.get(data,10,6))
                     )
        def _d_jalr(self,data):
            if bits.get(data,20,16):
                return None
            return MIB('jalr',None)(
                        MRO('target',bits.get(data,25,21)),
                        MRO('return',bits.get(data,15,11)),
                        MRO('hint',bits.get(data,10,6))
                     )

        def _d_movz(self,data):
            if bits.get(data,10,6):
                return None
            return MIB('movz',None)(
                        MRO('src',bits.get(data,25,21)),
                        MRO('predicate',bits.get(data,20,16)),
                        MRO('dest',bits.get(data,15,11))
                     )
        def _d_movn(self,data):
            if bits.get(data,10,6):
                return None
            return MIB('movn',None)(
                        MRO('src',bits.get(data,25,21)),
                        MRO('predicate',bits.get(data,20,16)),
                        MRO('dest',bits.get(data,15,11))
                     )
        def _d_syscall(self,data):
            return MIB('syscall',None)(
                        MIO('code',bits.get(data,25,6))
                     )
        def _d_break(self,data):
            return MIB('break',None)(
                        MIO('code',bits.get(data,25,6))
                     )
        def _d_sync(self,data):
            if bits.get(data,25,11):
                return None
            return MIB('sync',None)(
                        MIO('stype',bits.get(data,10,6))
                     )
                    
        def _d_mfhi(self,data):
            if bits.get(data,25,16) or bits.get(data,10,6):
                return None
            return MIB('mfhi',None)(
                        MRO('dest',bits.get(data,15,11))
                     )
        def _d_mthi(self,data):
            if bits.get(data,20,6):
                return None
            return MIB('mthi',None)(
                        MRO('src',bits.get(data,25,21))
                     )
        def _d_mflo(self,data):
            if bits.get(data,25,16) or bits.get(data,10,6):
                return None
            return MIB('mflo',None)(
                        MRO('dest',bits.get(data,15,11))
                     )
        def _d_mtlo(self,data):
            if bits.get(data,20,6):
                return None
            return MIB('mtlo',None)(
                        MRO('src',bits.get(data,25,21))
                     )
                    
        def _d_mult(self,data):
            if bits.get(data,15,6):
                return None
            return MIB('mult',None)(
                        MRO('srca',bits.get(data,25,21)),
                        MRO('srcb',bits.get(data,20,16))
                     )
        def _d_multu(self,data):
            if bits.get(data,15,6):
                return None
            return MIB('multu',None)(
                        MRO('srca',bits.get(data,25,21)),
                        MRO('srcb',bits.get(data,20,16))
                     )
        def _d_div(self,data):
            if bits.get(data,15,6):
                return None
            return MIB('div',None)(
                        MRO('srca',bits.get(data,25,21)),
                        MRO('srcb',bits.get(data,20,16))
                     )
        def _d_divu(self,data):
            if bits.get(data,15,6):
                return None
            return MIB('divu',None)(
                        MRO('srca',bits.get(data,25,21)),
                        MRO('srcb',bits.get(data,20,16))
                     )
                    
        def _d_add(self,data):
            if bits.get(data,10,6):
                return None
            return MIB('add',None)(
                        MRO('srca',bits.get(data,25,21)),
                        MRO('srcb',bits.get(data,20,16)),
                        MRO('dest',bits.get(data,15,11))
                     )
            
        def _d_addu(self,data):
            if bits.get(data,10,6):
                return None
            return MIB('addu',None)(
                        MRO('srca',bits.get(data,25,21)),
                        MRO('srcb',bits.get(data,20,16)),
                        MRO('dest',bits.get(data,15,11))
                     )
        def _d_sub(self,data):
            if bits.get(data,10,6):
                return None
            return MIB('sub',None)(
                        MRO('srca',bits.get(data,25,21)),
                        MRO('srcb',bits.get(data,20,16)),
                        MRO('dest',bits.get(data,15,11))
                     )
        def _d_subu(self,data):
            if bits.get(data,10,6):
                return None
            return MIB('subu',None)(
                        MRO('srca',bits.get(data,25,21)),
                        MRO('srcb',bits.get(data,20,16)),
                        MRO('dest',bits.get(data,15,11))
                     )
        def _d_and(self,data):
            if bits.get(data,10,6):
                return None
            return MIB('and',None)(
                        MRO('srca',bits.get(data,25,21)),
                        MRO('srcb',bits.get(data,20,16)),
                        MRO('dest',bits.get(data,15,11))
                     )
        def _d_or(self,data):
            if bits.get(data,10,6):
                return None
            return MIB('or',None)(
                        MRO('srca',bits.get(data,25,21)),
                        MRO('srcb',bits.get(data,20,16)),
                        MRO('dest',bits.get(data,15,11))
                     )
        def _d_xor(self,data):
            if bits.get(data,10,6):
                return None
            return MIB('xor',None)(
                        MRO('srca',bits.get(data,25,21)),
                        MRO('srcb',bits.get(data,20,16)),
                        MRO('dest',bits.get(data,15,11))
                     )
        def _d_nor(self,data):
            if bits.get(data,10,6):
                return None
            return MIB('nor',None)(
                        MRO('srca',bits.get(data,25,21)),
                        MRO('srcb',bits.get(data,20,16)),
                        MRO('dest',bits.get(data,15,11))
                     )
                         
        def _d_slt(self,data):
            if bits.get(data,10,6):
                return None
            return MIB('slt',None)(
                        MRO('srca',bits.get(data,25,21)),
                        MRO('srcb',bits.get(data,20,16)),
                        MRO('dest',bits.get(data,15,11))
                     )
        def _d_sltu(self,data):
            if bits.get(data,10,6):
                return None
            return MIB('sltu',None)(
                        MRO('srca',bits.get(data,25,21)),
                        MRO('srcb',bits.get(data,20,16)),
                        MRO('dest',bits.get(data,15,11))
                     )
                    
        def _d_tge(self,data):
            return MIB('tge',None)(
                        MRO('srca',bits.get(data,25,21)),
                        MRO('srcb',bits.get(data,20,16)),
                        MRO('code',bits.get(data,15,6))
                     )
        def _d_tgeu(self,data):
            return MIB('tgeu',None)(
                        MRO('srca',bits.get(data,25,21)),
                        MRO('srcb',bits.get(data,20,16)),
                        MRO('code',bits.get(data,15,6))
                     )
        def _d_tlt(self,data):
            return MIB('tlt',None)(
                        MRO('srca',bits.get(data,25,21)),
                        MRO('srcb',bits.get(data,20,16)),
                        MRO('code',bits.get(data,15,6))
                     )
        def _d_tltu(self,data):
            return MIB('tltu',None)(
                        MRO('srca',bits.get(data,25,21)),
                        MRO('srcb',bits.get(data,20,16)),
                        MRO('code',bits.get(data,15,6))
                     )
        def _d_teq(self,data):
            return MIB('teq',None)(
                        MRO('srca',bits.get(data,25,21)),
                        MRO('srcb',bits.get(data,20,16)),
                        MRO('code',bits.get(data,15,6))
                     )
        def _d_tne(self,data):
            return MIB('tne',None)(
                        MRO('srca',bits.get(data,25,21)),
                        MRO('srcb',bits.get(data,20,16)),
                        MRO('code',bits.get(data,15,6))
                     )

    class RegimmCodec(TableCodec):
        def __init__(self):
            table = [ # bits 20..19 down, 18..16 across
                    ['_d_bltz',      '_d_bgez',   '_d_bltzl',      '_d_bgezl',      None,   None,   None,   None],
                    ['_d_tgei',      '_d_tgeiu',  '_d_tlti',       '_d_tltiu',      '_d_teqi',   None,   '_d_tnei',   None],
                    ['_d_bltzal',    '_d_bgezal', '_d_btlzall',    '_d_bgezall',    None,   None,   None,   None],
                    [None,      None,   None,       None,       None,   None,   None,   '_d_synci']
                    ]
            TableCodec.__init__(self, (18,16), (20,19), table)
                    
        def _d_bltz(self,data):
            return None      
        def _d_bgez(self,data):
            return None   
        def _d_bltzl(self,data):
            return None      
        def _d_bgezl(self,data):
            return None               
        def _d_tgei(self,data):
            return None      
        def _d_tgeiu(self,data):
            return None  
        def _d_tlti(self,data):
            return None       
        def _d_tltiu(self,data):
            return None      
        def _d_teqi(self,data):
            return None      
        def _d_tnei(self,data):
            return None   
        def _d_bltzal(self,data):
            return None    
        def _d_bgezal(self,data):
            return None 
        def _d_btlzall(self,data):
            return None    
        def _d_bgezall(self,data):
            return None             
        def _d_synci(self,data):
            return None
    class Special2Codec(TableCodec):
        def __init__(self):
            table = [ # bits 5..3 down, 2..0 across
                    ['_d_madd',  '_d_maddu',  '_d_mul',    None,   '_d_msub',   '_d_msubu',  None,   None],
                    [None,  None,   None,   None,   None,   None,   None,   None],
                    [None,  None,   None,   None,   None,   None,   None,   None],
                    [None,  None,   None,   None,   None,   None,   None,   None],
                    ['_d_clz',   '_d_clo',    None,   None,   None,   None,   None,   None],
                    [None,  None,   None,   None,   None,   None,   None,   None],
                    [None,  None,   None,   None,   None,   None,   None,   None],
                    [None,  None,   None,   None,   None,   None,   None,   '_d_sdbbp']
                    ]
            TableCodec.__init__(self, (2,0), (5,3), table)
                    
        def _d_madd(self,data):
            return None  
        def _d_maddu(self,data):
            return None  
        def _d_mul(self,data):
            return None       
        def _d_msub(self,data):
            return None   
        def _d_msubu(self,data):
            return None     
        def _d_clz(self,data):
            return None   
        def _d_clo(self,data):
            return None                   
        def _d_sdbbp(self,data):
            return None
    class Special3Codec(TableCodec):
        def __init__(self):
            table = [ # bits 5..3 down, 2..0 across
                ['_d_ext',   None,   None,   None,   '_d_ins',    None,   None,   None],
                [None,  None,   None,   None,   None,   None,   None,   None],
                [None,  None,   None,   None,   None,   None,   None,   None],
                [None,  None,   None,   None,   None,   None,   None,   None],
                ['_d_bshfl', None,   None,   None,   None,   None,   None,   None],
                [None,  None,   None,   None,   None,   None,   None,   None],
                [None,  None,   None,   None,   None,   None,   None,   None],
                [None,  None,   None,   '_d_rdhwr',  None,   None,   None,   None]
                ]
            TableCodec.__init__(self, (2,0), (5,3), table)
        def _d_ext(self,data):
            return None
        def _d_ins(self,data):
            return None
        def _d_bshfl(self,data):
            return None
        def _d_rdhwr(self,data):
            return None
    def __init__(self):
        table = [ #bits 31..29 down; 28..26 across
                ['_d_special', '_d_regimm',   '_d_j',    '_d_jal',  '_d_beq',      '_d_bne',  '_d_blez', '_d_bgtz'],
                ['_d_addi',    '_d_addiu',    '_d_slti', '_d_sltiu','_d_andi',     '_d_ori',  '_d_xori', '_d_lui'],
                ['_d_cop0',    '_d_cop1',     '_d_cop2', '_d_cop1x','_d_beql',     '_d_bnel', '_d_blezl','_d_bgtzl'],
                [None,      None,       None,   None,   '_d_special2', '_d_jalx', None,   '_d_special3'],
                ['_d_lb',      '_d_lh',       '_d_lwl',  '_d_lw',   '_d_lbu',      '_d_lhu',  '_d_lwr',  None],
                ['_d_sb',      '_d_sh',       '_d_swl',  '_d_sw',   None,       None,   '_d_swr',  '_d_cache'],
                ['_d_ll',      '_d_lwc1',     '_d_lwc2', '_d_pref', None,       '_d_ldc1', '_d_ldc2', None],
                ['_d_sc',      '_d_swc1',     '_d_swc2', None,   None,       '_d_sdc1', '_d_sdc2', None]
                ]
        TableCodec.__init__(self,(28,26),(31,29),table)
        self.class_decoders = { 
                'special' :MIPSCodec.SpecialCodec(),
                'regimm'  :MIPSCodec.RegimmCodec(),
                'special2':MIPSCodec.Special2Codec(),
                'special3':MIPSCodec.Special3Codec()
                }

    def _d_special(self,data):
        return self.class_decoders['special'].decode(data)
    def _d_regimm(self,data):
        return self.class_decoders['regimm'].decode(data)
    def _d_j(self,data):
        return None
    def _d_jal(self,data):
        return None
    def _d_beq(self,data):
        return None
    def _d_bne(self,data):
        return None
    def _d_blez(self,data):
        return None
    def _d_bgtz(self,data):
        return None
    def _d_addi(self,data):
        return None
    def _d_addiu(self,data):
        return None
    def _d_slti(self,data):
        return None
    def _d_sltiu(self,data):
        return None
    def _d_andi(self,data):
        return None
    def _d_ori(self,data):
        return None
    def _d_xori(self,data):
        return None
    def _d_lui(self,data):
        return None
    def _d_cop0(self,data):
        return None
    def _d_cop1(self,data):
        return None
    def _d_cop2(self,data):
        return None
    def _d_cop1x(self,data):
        return None
    def _d_beql(self,data):
        return None
    def _d_bnel(self,data):
        return None
    def _d_blezl(self,data):
        return None
    def _d_bgtzl(self,data):
        return None
    def _d_special2(self,data):
        return self.class_decoders['special2'].decode(data)
    def _d_jalx(self,data):
        return None
    def _d_special3(self,data):
        return self.class_decoders['special3'].decode(data)
    def _d_lb(self,data):
        return None
    def _d_lh(self,data):
        return None
    def _d_lwl(self,data):
        return None
    def _d_lw(self,data):
        return None
    def _d_lbu(self,data):
        return None
    def _d_lhu(self,data):
        return None
    def _d_lwr(self,data):
        return None
    def _d_sb(self,data):
        return None
    def _d_sh(self,data):
        return None
    def _d_swl(self,data):
        return None
    def _d_sw(self,data):
        return None
    def _d_swr(self,data):
        return None
    def _d_cache(self,data):
        return None
    def _d_ll(self,data):
        return None
    def _d_lwc1(self,data):
        return None
    def _d_lwc2(self,data):
        return None
    def _d_pref(self,data):
        return None
    def _d_ldc1(self,data):
        return None
    def _d_ldc2(self,data):
        return None
    def _d_sc(self,data):
        return None
    def _d_swc1(self,data):
        return None
    def _d_swc2(self,data):
        return None
    def _d_sdc1(self,data):
        return None
    def _d_sdc2(self,data):
        return None


class MIPSMachine(Machine):
    shortname = "MIPS"
    longname = "MIPS"
	
    def __init__(self,datastore):
        self.datastore = datastore
        self.codec = MIPSCodec()

    def disassemble(self, id):
        data = self.datastore.readBytes(id,4)
        return self.codec.decode(data)

machines = [MIPSMachine]
