#!/usr/bin/python
import re
from lib8051 import decode

def test(pc, asm, *bytes):
    try:
        insn = decode(pc, bytes)
    except NameError as (a):
        if re.match("^global name 'decode[^']*' is not defined", a.args[0]):
            print "Failed test for %s (%s) - could not decode"  % (" ".join(["%02x" % i for i in bytes]), asm)
            return 
        else:
            raise

    expected = asm.lower()
    got = str(insn.disasm).strip().replace("\t"," ").lower()
    if (got != expected):
        print "Failed test for %s" % " ".join(["%02x" % i for i in bytes])
        print "   .. expected: %s" % expected
        print "   .. got     : %s" % got
        #exit(1)
    if (insn.length != len(bytes)):
        print "Failed test for %s (%s)"  % (" ".join(["%02x" % i for i in bytes]), asm)
        print "   .. length supplied: %d - disasm reported: %d" %(len(bytes), insn.length)

# Tests for 0x00 - 0x0F
test(0x0000, "nop",             0x00)
test(0xCFFF, "ajmp 0xD023",     0x01, 0x23)
test(0x1234, "ljmp 0xCAFE",         0x02, 0xCA, 0xFE)
test(0x0000, "rr a",            0x03)
test(0x0000, "inc a",           0x04)
test(0x0000, "inc (0x42)",      0x05, 0x42)
test(0x0000, "inc @r0",         0x06)
test(0x0000, "inc @r1",         0x07)
test(0x0000, "inc r0",          0x08)
test(0x0000, "inc r1",          0x09)
test(0x0000, "inc r2",          0x0A)
test(0x0000, "inc r3",          0x0B)
test(0x0000, "inc r4",          0x0C)
test(0x0000, "inc r5",          0x0D)
test(0x0000, "inc r6",          0x0E)
test(0x0000, "inc r7",          0x0F)


# Tests for 0x10 - 0x0F
test(0x0005, "jbc (0xE0.1), 0x09",  0x10, 0xE1, 0x1)
test(0xCFFF, "acall 0xD023",        0x11, 0x23)
test(0x1234, "lcall 0xCAFE",        0x12, 0xCA, 0xFE)
test(0x0000, "rrc a",           0x13)
test(0x0000, "dec a",           0x14)
test(0x0000, "dec (0x42)",      0x15, 0x42)
test(0x0000, "dec @r0",         0x16)
test(0x0000, "dec @r1",         0x17)
test(0x0000, "dec r0",          0x18)
test(0x0000, "dec r1",          0x19)
test(0x0000, "dec r2",          0x1A)
test(0x0000, "dec r3",          0x1B)
test(0x0000, "dec r4",          0x1C)
test(0x0000, "dec r5",          0x1D)
test(0x0000, "dec r6",          0x1E)
test(0x0000, "dec r7",          0x1F)


# Tests for 0x20 - 0x2F
test(0x0006, "jb (0x20.4), 0x06",   0x20, 0x04, 0xFD)
test(0xCFFF, "ajmp 0xD123",     0x21, 0x23)
test(0xCFFF, "ret",         0x22)
test(0x0000, "rl a",            0x23)
test(0x0000, "add a, #0xCA",        0x24, 0xCA)
test(0x0000, "add a, (0xCA)",       0x25, 0xCA)
test(0x0000, "add a, @r0",      0x26)
test(0x0000, "add a, @r1",      0x27)
test(0x0000, "add a, r0",       0x28)
test(0x0000, "add a, r1",       0x29)
test(0x0000, "add a, r2",       0x2A)
test(0x0000, "add a, r3",       0x2B)
test(0x0000, "add a, r4",       0x2C)
test(0x0000, "add a, r5",       0x2D)
test(0x0000, "add a, r6",       0x2E)
test(0x0000, "add a, r7",       0x2F)

# Tests for 0x30 - 0x3F
test(0x0010, "jnb (0x22.7), 0x06",  0x30, 0x17, 0xF3)
test(0xCFFF, "acall 0xD123",        0x31, 0x23)
test(0xCFFF, "reti",            0x32)
test(0x0000, "rlc a",           0x33)
test(0x0000, "addc a, #0xCA",       0x34, 0xCA)
test(0x0000, "addc a, (0xCA)",      0x35, 0xCA)
test(0x0000, "addc a, @r0",         0x36)
test(0x0000, "addc a, @r1",     0x37)
test(0x0000, "addc a, r0",      0x38)
test(0x0000, "addc a, r1",      0x39)
test(0x0000, "addc a, r2",      0x3A)
test(0x0000, "addc a, r3",      0x3B)
test(0x0000, "addc a, r4",      0x3C)
test(0x0000, "addc a, r5",      0x3D)
test(0x0000, "addc a, r6",      0x3E)
test(0x0000, "addc a, r7",      0x3F)

# Test for 0x40 to 0x4F
test(0x0002, "jc 0x04",         0x40, 0)
test(0xCFFF, "ajmp 0xD223",     0x41, 0x23)
test(0x0000, "orl (0x22), a",       0x42, 0x22)
test(0x0000, "orl (0x22), #0x32",   0x43, 0x22, 0x32)
test(0x0000, "orl a, #0x32",        0x44, 0x32)
test(0x0000, "orl a, (0x22)",       0x45, 0x22)
test(0x0000, "orl a, @r0",      0x46)
test(0x0000, "orl a, @r1",      0x47)
test(0x0000, "orl a, r0",       0x48)
test(0x0000, "orl a, r1",       0x49)
test(0x0000, "orl a, r2",       0x4A)
test(0x0000, "orl a, r3",       0x4B)
test(0x0000, "orl a, r4",       0x4C)
test(0x0000, "orl a, r5",       0x4D)
test(0x0000, "orl a, r6",       0x4E)
test(0x0000, "orl a, r7",       0x4F)

# Test for 0x50 to 0x5F
test(0x0002, "jnc 0x04",        0x50, 0)
test(0xCFFF, "acall 0xD223",        0x51, 0x23)
test(0x0000, "anl (0x22), a",       0x52, 0x22)
test(0x0000, "anl (0x22), #0x32",   0x53, 0x22, 0x32)
test(0x0000, "anl a, #0x32",        0x54, 0x32)
test(0x0000, "anl a, (0x22)",       0x55, 0x22)
test(0x0000, "anl a, @r0",      0x56)
test(0x0000, "anl a, @r1",      0x57)
test(0x0000, "anl a, r0",       0x58)
test(0x0000, "anl a, r1",       0x59)
test(0x0000, "anl a, r2",       0x5A)
test(0x0000, "anl a, r3",       0x5B)
test(0x0000, "anl a, r4",       0x5C)
test(0x0000, "anl a, r5",       0x5D)
test(0x0000, "anl a, r6",       0x5E)
test(0x0000, "anl a, r7",       0x5F)

# Tests for 0x60 to 0x6F
test(0x0002, "jz 0x04",         0x60, 0)
test(0xCFFF, "ajmp 0xD323",     0x61, 0x23)
test(0x0000, "xrl (0x22), a",       0x62, 0x22)
test(0x0000, "xrl (0x22), #0x32",   0x63, 0x22, 0x32)
test(0x0000, "xrl a, #0x32",        0x64, 0x32)
test(0x0000, "xrl a, (0x22)",       0x65, 0x22)
test(0x0000, "xrl a, @r0",      0x66)
test(0x0000, "xrl a, @r1",      0x67)
test(0x0000, "xrl a, r0",       0x68)
test(0x0000, "xrl a, r1",       0x69)
test(0x0000, "xrl a, r2",       0x6A)
test(0x0000, "xrl a, r3",       0x6B)
test(0x0000, "xrl a, r4",       0x6C)
test(0x0000, "xrl a, r5",       0x6D)
test(0x0000, "xrl a, r6",       0x6E)
test(0x0000, "xrl a, r7",       0x6F)

# Tests for 0x70 to 0x7f
test(0x0002, "jnz 0x04",        0x70, 0)
test(0xCFFF, "acall 0xD323",        0x71, 0x23)
test(0x0000, "orl c, (0xc0.4)",     0x72, 0xC4)
test(0x0000, "jmp @A + DPTR",       0x73)
test(0x0000, "mov a, #0x32",        0x74, 0x32)
test(0x0000, "mov (0x22), #0x32",   0x75, 0x22, 0x32)
test(0x0000, "mov @r0, #0x32",      0x76, 0x32)
test(0x0000, "mov @r1, #0x32",      0x77, 0x32)
test(0x0000, "mov r0, #0x32",       0x78, 0x32)
test(0x0000, "mov r1, #0x32",       0x79, 0x32)
test(0x0000, "mov r2, #0x32",       0x7A, 0x32)
test(0x0000, "mov r3, #0x32",       0x7B, 0x32)
test(0x0000, "mov r4, #0x32",       0x7C, 0x32)
test(0x0000, "mov r5, #0x32",       0x7D, 0x32)
test(0x0000, "mov r6, #0x32",       0x7E, 0x32)
test(0x0000, "mov r7, #0x32",       0x7F, 0x32)


# Tests for 0x80 to 0x8f
test(0x0002, "sjmp 0x04",       0x80, 0)
test(0xCFFF, "ajmp 0xD423",     0x81, 0x23)
test(0x0000, "anl c, (0xc0.4)",     0x82, 0xC4)
test(0x0000, "movc a, @a + pc",     0x83)
test(0x0000, "div ab",          0x84)
test(0x0000, "mov (0xAA), (0xCC)",  0x85, 0xCC, 0xAA)   # References differ to the byte order
    # Using the majority ordering
test(0x0000, "mov (0x32), @r0",     0x86, 0x32)
test(0x0000, "mov (0x32), @r1",     0x87, 0x32)
test(0x0000, "mov (0x32), r0",      0x88, 0x32)
test(0x0000, "mov (0x32), r1",      0x89, 0x32)
test(0x0000, "mov (0x32), r2",      0x8A, 0x32)
test(0x0000, "mov (0x32), r3",      0x8B, 0x32)
test(0x0000, "mov (0x32), r4",      0x8C, 0x32)
test(0x0000, "mov (0x32), r5",      0x8D, 0x32)
test(0x0000, "mov (0x32), r6",      0x8E, 0x32)
test(0x0000, "mov (0x32), r7",      0x8F, 0x32)

# Tests for 0x90 to 0x9F
test(0x0002, "mov dptr, #0x1234",   0x90, 0x12, 0x34)
test(0xCFFF, "acall 0xD423",        0x91, 0x23)
test(0x0000, "mov (0xc0.4), c",     0x92, 0xC4)
test(0x0000, "movc a, @a + dptr",   0x93)
test(0x0000, "subb a, #0xCA",       0x94, 0xCA)
test(0x0000, "subb a, (0xCA)",      0x95, 0xCA)
test(0x0000, "subb a, @r0",         0x96)
test(0x0000, "subb a, @r1",     0x97)
test(0x0000, "subb a, r0",      0x98)
test(0x0000, "subb a, r1",      0x99)
test(0x0000, "subb a, r2",      0x9A)
test(0x0000, "subb a, r3",      0x9B)
test(0x0000, "subb a, r4",      0x9C)
test(0x0000, "subb a, r5",      0x9D)
test(0x0000, "subb a, r6",      0x9E)
test(0x0000, "subb a, r7",      0x9F)

# Tests for 0xA0 - 0xAF
test(0x0000, "orl c, /(0xc0.4)",        0xA0, 0xC4)
test(0xCFFF, "ajmp 0xD523",     0xA1, 0x23)
test(0x0000, "mov c, (0xc0.4)",     0xA2, 0xC4)
test(0x0000, "inc dptr",        0xA3)
test(0x0000, "mul ab",          0xA4)
#0xA5 is unimplemented opcode
test(0x0000, "mov @r0, (0x32)",     0xA6, 0x32)
test(0x0000, "mov @r1, (0x32)",     0xA7, 0x32)
test(0x0000, "mov r0, (0x32)",      0xA8, 0x32)
test(0x0000, "mov r1, (0x32)",      0xA9, 0x32)
test(0x0000, "mov r2, (0x32)",      0xAA, 0x32)
test(0x0000, "mov r3, (0x32)",      0xAB, 0x32)
test(0x0000, "mov r4, (0x32)",      0xAC, 0x32)
test(0x0000, "mov r5, (0x32)",      0xAD, 0x32)
test(0x0000, "mov r6, (0x32)",      0xAE, 0x32)
test(0x0000, "mov r7, (0x32)",      0xAF, 0x32)


# Tests for 0xB0 - 0xBF
test(0x0000, "anl c, /(0xc0.4)",        0xB0, 0xC4)
test(0xCFFF, "acall 0xD523",        0xB1, 0x23)
test(0x0000, "cpl (0xc0.4)",        0xB2, 0xC4)
test(0x0000, "cpl c",           0xB3)
test(0x0002, "cjne a, #0x12, 0x46", 0xB4, 0x12, 0x41)
test(0x0003, "cjne a, (0x12), 0x47",    0xB5, 0x12, 0x41)
test(0x0002, "cjne @r0, #0x12, 0x46",   0xB6, 0x12, 0x41)
test(0x0002, "cjne @r1, #0x12, 0x46",   0xB7, 0x12, 0x41)
test(0x0002, "cjne r0, #0x12, 0x46",    0xB8, 0x12, 0x41)
test(0x0002, "cjne r1, #0x12, 0x46",    0xB9, 0x12, 0x41)
test(0x0002, "cjne r2, #0x12, 0x46",    0xBA, 0x12, 0x41)
test(0x0002, "cjne r3, #0x12, 0x46",    0xBB, 0x12, 0x41)
test(0x0002, "cjne r4, #0x12, 0x46",    0xBC, 0x12, 0x41)
test(0x0002, "cjne r5, #0x12, 0x46",    0xBD, 0x12, 0x41)
test(0x0002, "cjne r6, #0x12, 0x46",    0xBE, 0x12, 0x41)
test(0x0002, "cjne r7, #0x12, 0x46",    0xBF, 0x12, 0x41)

# Tests for 0xC0 - 0xCF
test(0x0000, "push (0x13)",     0xC0, 0x13)
test(0xCFFF, "ajmp 0xD623",     0xC1, 0x23)
test(0x0000, "clr (0xc0.4)",        0xC2, 0xC4)
test(0x0000, "clr c",           0xC3)   
test(0x0000, "swap a",          0xC4)   
test(0x0000, "xch a, (0xCA)",       0xC5, 0xCA)
test(0x0000, "xch a, @r0",      0xC6)
test(0x0000, "xch a, @r1",      0xC7)
test(0x0000, "xch a, r0",       0xC8)
test(0x0000, "xch a, r1",       0xC9)
test(0x0000, "xch a, r2",       0xCA)
test(0x0000, "xch a, r3",       0xCB)
test(0x0000, "xch a, r4",       0xCC)
test(0x0000, "xch a, r5",       0xCD)
test(0x0000, "xch a, r6",       0xCE)
test(0x0000, "xch a, r7",       0xCF)

# Tests for 0xD0-0xDF
test(0x0000, "pop (0x14)",      0xD0, 0x14)
test(0xCFFF, "acall 0xD623",        0xD1, 0x23)
test(0x0000, "setb (0xc0.4)",       0xD2, 0xC4)
test(0x0000, "setb c",          0xD3)   
test(0x0000, "da a",            0xD4)   
test(0x1234, "djnz (0x10), 0x1260", 0xD5, 0x10, 0x2A)
test(0x0000, "xchd a, @r0",         0xD6)
test(0x0000, "xchd a, @r1",     0xD7)   
test(0x1234, "djnz r0, 0x1260",     0xD8, 0x2A)
test(0x1234, "djnz r1, 0x1260",     0xD9, 0x2A)
test(0x1234, "djnz r2, 0x1260",     0xDA, 0x2A)
test(0x1234, "djnz r3, 0x1260",     0xDB, 0x2A)
test(0x1234, "djnz r4, 0x1260",     0xDC, 0x2A)
test(0x1234, "djnz r5, 0x1260",     0xDD, 0x2A)
test(0x1234, "djnz r6, 0x1260",     0xDE, 0x2A)
test(0x1234, "djnz r7, 0x1260",     0xDF, 0x2A)

# Tests for 0xE0-0xEF
test(0x0000, "movx a, @dptr",       0xE0)
test(0xCFFF, "ajmp 0xD723",     0xE1, 0x23)
test(0x0000, "movx a, @R0",     0xE2)
test(0x0000, "movx a, @R1",     0xE3)
test(0x0000, "clr a",           0xE4)
test(0x0000, "mov a, (0x22)",       0xE5, 0x22)
test(0x0000, "mov a, @r0",      0xE6)
test(0x0000, "mov a, @r1",      0xE7)
test(0x0000, "mov a, r0",       0xE8)
test(0x0000, "mov a, r1",       0xE9)
test(0x0000, "mov a, r2",       0xEA)
test(0x0000, "mov a, r3",       0xEB)
test(0x0000, "mov a, r4",       0xEC)
test(0x0000, "mov a, r5",       0xED)
test(0x0000, "mov a, r6",       0xEE)
test(0x0000, "mov a, r7",       0xEF)

# Tests for 0xF0- 0xFF
test(0x0000, "movx @dptr, a",       0xF0)
test(0xCFFF, "acall 0xD723",        0xF1, 0x23)
test(0x0000, "movx @R0, a",     0xF2)
test(0x0000, "movx @R1, a",     0xF3)
test(0x0000, "cpl a",           0xF4)
test(0x0000, "mov (0x22), a",       0xF5, 0x22)
test(0x0000, "mov @r0, a",  0xF6)
test(0x0000, "mov @r1, a",      0xF7)
test(0x0000, "mov r0, a",       0xF8)
test(0x0000, "mov r1, a",       0xF9)
test(0x0000, "mov r2, a",       0xFA)
test(0x0000, "mov r3, a",       0xFB)
test(0x0000, "mov r4, a",       0xFC)
test(0x0000, "mov r5, a",       0xFD)
test(0x0000, "mov r6, a",       0xFE)
test(0x0000, "mov r7, a",       0xFF)


