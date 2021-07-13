# 
# S370BALAsm V2.R1.M1
#
# This file is part of the S370BALAsm distribution.
# Copyright (c) 2021 James Salvino.
# 
# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import sys
import pickle

#
#assembler directives
assem_inst_list = [ 'USING', 
                    'DROP',
                    'DC', 
                    'DS', 
                    'EQU', 
                    'END' ]
#
#            MNEMONIC    OP-CODE OPERANDS              MACHINE-FORMAT
mach_inst_dict = {
            'A':          ('5A','R1,D2(X2,B2)',       'RX BD DD'),
            'AH':         ('4A','R1,D2(X2,B2)',       'RX BD DD'),
            'AL':         ('5E','R1,D2(X2,B2)',       'RX BD DD'),
            'ALR':        ('1E','R1,R2',              'RR'),
            'AP':         ('FA','D1(L1,B1),D2(L2,B2)','L1L2 BD DD BD DD'),
            'AR':         ('1A','R1,R2',              'RR'),
            'BAL':        ('45','R1,D2(X2,B2)',       'RX BD DD'),
            'BALR':       ('05','R1,R2',              'RR'),
            'BAS':        ('4D','R1,D2(X2,B2)',       'RX BD DD'),
            'BASR':       ('0D','R1,R2',              'RR'),
            'BASSM':      ('0C','R1,R2',              'RR'),
            'BC':         ('47','M1,D2(X2,B2)',       'MX BD DD'),
            'BCR':        ('07','M1,R2',              'MR'),
            'BCT':        ('46','R1,D2(X2,B2)',       'RX BD DD'),
            'BCTR':       ('06','R1,R2',              'RR'),
            'BSM':        ('0B','R1,R2',              'RR'),
            'BXH':        ('86','R1,R3,D2(B2)',       'RR BD DD'),
            'BXLE':       ('87','R1,R3,D2(B2)',       'RR BD DD'),
            'C':          ('59','R1,D2(X2,B2)',       'RX BD DD'),
            'CDS':        ('BB','R1,R3,D2(B2)',       'RR BD DD'),
            'CH':         ('49','R1,D2(X2,B2)',       'RX BD DD'), 
            'CL':         ('55','R1,D2(X2,B2)',       'RX BD DD'),
            'CLC':        ('D5','D1(L,B1),D2(B2)',    'LL BD DD BD DD'),
            'CLCL':       ('0F','R1,R2',              'RR'),
            'CLI':        ('95','D1(B1),I2',          'II BD DD'),
            'CLM':        ('BD','R1,M3,D2(B2)',       'RM BD DD'),
            'CLR':        ('15','R1,R2',              'RR'),
            'CP':         ('F9','D1(L1,B1),D2(L2,B2)','L1L2 BD DD BD DD'),
            'CR':         ('19','R1,R2',              'RR'),
            'CS':         ('BA','R1,R3,D2(B2)',       'RR BD DD'),
            'CVB':        ('4F','R1,D2(X2,B2)',       'RX BD DD'),
            'CVD':        ('4E','R1,D2(X2,B2)',       'RX BD DD'),
            'D':          ('5D','R1,D2(X2,B2)',       'RX BD DD'),
            'DP':         ('FD','D1(L1,B1),D2(L2,B2)','L1L2 BD DD BD DD'),
            'DR':         ('1D','R1,R2',              'RR'),
            'ED':         ('DE','D1(L,B1),D2(B2)',    'LL BD DD BD DD'),
            'EDMK':       ('DF','D1(L,B1),D2(B2)',    'LL BD DD BD DD'),
            'EX':         ('44','R1,D2(X2,B2)',       'RX BD DD'),
            'IC':         ('43','R1,D2(X2,B2)',       'RX BD DD'),
            'ICM':        ('BF','R1,M3,D2(B2)',       'RM BD DD'),
            'L':          ('58','R1,D2(X2,B2)',       'RX BD DD'),
            'LA':         ('41','R1,D2(X2,B2)',       'RX BD DD'),
            'LCR':        ('13','R1,R2',              'RR'),
            'LH':         ('48','R1,D2(X2,B2)',       'RX BD DD'),
            'LM':         ('98','R1,R3,D2(B2)',       'RR BD DD'),
            'LNR':        ('11','R1,R2',              'RR'),       
            'LPR':        ('10','R1,R2',              'RR'),
            'LR':         ('18','R1,R2',              'RR'),
            'LTR':        ('12','R1,R2',              'RR'),
            'M':          ('5C','R1,D2(X2,B2)',       'RX BD DD'),
            'MH':         ('4C','R1,D2(X2,B2)',       'RX BD DD'),
            'MP':         ('FC','D1(L1,B1),D2(L2,B2)','L1L2 BD DD BD DD'),
            'MR':         ('1C','R1,R2',              'RR'),
            'MVC':        ('D2','D1(L,B1),D2(B2)',    'LL BD DD BD DD'),
            'MVCIN':      ('E8','D1(L,B1),D2(B2)',    'LL BD DD BD DD'),
            'MVCL':       ('0E','R1,R2',              'RR'),
            'MVI':        ('92','D1(B1),I2',          'II BD DD'),
            'MVN':        ('D1','D1(L,B1),D2(B2)',    'LL BD DD BD DD'),
            'MVO':        ('F1','D1(L1,B1),D2(L2,B2)','L1L2 BD DD BD DD'),
            'MVZ':        ('D3','D1(L,B1),D2(B2)',    'LL BD DD BD DD'),
            'N':          ('54','R1,D2(X2,B2)',       'RX BD DD'),
            'NC':         ('D4','D1(L,B1),D2(B2)',    'LL BD DD BD DD'),
            'NI':         ('94','D1(B1),I2',          'II BD DD'),
            'NR':         ('14','R1,R2',              'RR'),
            'O':          ('56','R1,D2(X2,B2)',       'RX BD DD'),
            'OC':         ('D6','D1(L,B1),D2(B2)',    'LL BD DD BD DD'),
            'OI':         ('96','D1(B1),I2',          'II BD DD'),
            'OR':         ('16','R1,R2',              'RR'),
            'PACK':       ('F2','D1(L1,B1),D2(L2,B2)','L1L2 BD DD BD DD'),
            'S':          ('5B','R1,D2(X2,B2)',       'RX BD DD'),
            'SH':         ('4B','R1,D2(X2,B2)',       'RX BD DD'),
            'SL':         ('5F','R1,D2(X2,B2)',       'RX BD DD'),
            'SLA':        ('8B','R1,D2(X2,B2)',       'R0 BD DD'),
            'SLDA':       ('8F','R1,D2(X2,B2)',       'R0 BD DD'),
            'SLDL':       ('8D','R1,D2(X2,B2)',       'R0 BD DD'),
            'SLL':        ('89','R1,D2(X2,B2)',       'R0 BD DD'),
            'SLR':        ('1F','R1,R2',              'RR'),
            'SP':         ('FB','D1(L1,B1),D2(L2,B2)','L1L2 BD DD BD DD'),
            'SR':         ('1B','R1,R2',              'RR'),
            'SRA':        ('8A','R1,D2(X2,B2)',       'R0 BD DD'),
            'SRDA':       ('8E','R1,D2(X2,B2)',       'R0 BD DD'),
            'SRDL':       ('8C','R1,D2(X2,B2)',       'R0 BD DD'),
            'SRL':        ('88','R1,D2(X2,B2)',       'R0 BD DD'),
            'SRP':        ('F0','D1(L1,B1),D2(B2),I3','LI BD DD BD DD'),
            'ST':         ('50','R1,D2(X2,B2)',       'RX BD DD'),
            'STC':        ('42','R1,D2(X2,B2)',       'RX BD DD'),
            'STCM':       ('BE','R1,M3,D2(B2)',       'RM BD DD'),
            'STH':        ('40','R1,D2(X2,B2)',       'RX BD DD'),
            'STM':        ('90','R1,R3,D2(B2)',       'RR BD DD'),
            'SVC':        ('0A','I1',                 'II'),
            'TM':         ('91','D1(B1),I2',          'II BD DD'),
            'TR':         ('DC','D1(L,B1),D2(B2)',    'LL BD DD BD DD'),
            'TRT':        ('DD','D1(L,B1),D2(B2)',    'LL BD DD BD DD'),
            'UNPK':       ('F3','D1(L1,B1),D2(L2,B2)','L1L2 BD DD BD DD'),
            'X':          ('57','R1,D2(X2,B2)',       'RX BD DD'),
            'XC':         ('D7','D1(L,B1),D2(B2)',    'LL BD DD BD DD'),
            'XI':         ('97','D1(B1),I2',          'II BD DD'),
            'XR':         ('17','R1,R2',              'RR'),
            'ZAP':        ('F8','D1(L1,B1),D2(L2,B2)','L1L2 BD DD BD DD') }

extended_mnemonic_inst_dict = {
            'B': '15',
            'BR': '15',
            'NOP': '0',
            'NOPR': '0',
            'BH': '2',
            'BHR': '2',
            'BL': '4',
            'BLR': '4',
            'BE': '8',
            'BER': '8',
            'BNH': '13',
            'BNHR': '13',
            'BNL': '11',
            'BNLR': '11',
            'BNE': '7',
            'BNER': '7',
            'BO': '1',
            'BOR': '1',
            'BP': '2',
            'BPR': '2',
            'BM': '4',
            'BMR': '4',
            'BNP': '13',
            'BNPR': '13',
            'BNM': '11',
            'BNMR': '11',
            'BNZ': '7',
            'BNZR': '7',
            'BZ': '8',
            'BZR': '8',
            'BNO': '14',
            'BNOR': '14' }   
            
ASC2EBC = ['00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00',    # 00 - 0F
           '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00',    # 10 - 1F
           '40', '00', '00', '7B', '00', '00', '00', '00', '00', '00', '00', '00', '6B', '00', '4B', '00',    # 20 - 2F
           'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', '00', '00', '00', '00', '00', '00',    # 30 - 3F
           '00', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6',    # 40 - 4F
           'D7', 'D8', 'D9', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', '00', '00', '00', '00', '00',    # 50 - 5F
           '00', '81', '82', '83', '84', '85', '86', '87', '88', '89', '91', '92', '93', '94', '95', '96',    # 60 - 6F
           '97', '98', '99', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', '00', '00', '00', '00', '00',    # 70 - 7F
           '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00',    # 80 - 8F
           '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00',    # 90 - 9F
           '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00',    # A0 - AF
           '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00',    # B0 - BF
           '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00',    # C0 - CF
           '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00',    # D0 - DF    
           '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00',    # E0 - EF
           '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00']    # F0 - FF            

#
# S370BALAsm.py (c) 2021 - James Salvino.
#
# This assembler is meant to assemble IBM S/370 problem
# state instructions to create the data structures needed
# for the S370BALEmu S/370 Emulator (c) 2021 - James
# Salvino.
#
# This is a basic implementation of the IBM S/370 
# Assembler - IFOX00. It is meant to be a teaching 
# aid or to test out small pieces of code using
# the S370BALEmu S/370 Emulator.
#
# This assembler will NOT create an object module
# that can be used on an IBM mainframe (either
# a real one or one run virtually under Hercules).
# 
# S370BALAsm is written in Python V3.
# In an effort to make this as fun for me
# as possible (which of course is my aim)
# there is precious little, if any, extensive 
# error checking. If you have bad assembler code
# S370BALAsm will abend, and hopefully you will 
# be able to fix your problem.
#
# Also, for you Python purists out there, this
# code is not necessarily PEP 8 complient nor
# may be the most efficient Python code you have 
# ever seen.
#
#
# Syntax and Usage Notes:
#
# The source code input file MUST be a plain
# ASCII text file. It MUST exist in your current
# working directory and have the file type of
# s370 (for example: test.s370)
#
# Invoke the assembler as follows:
#
# S370BALAsm.py filename [-debug]
#
# Where filename is the name of your ASCII text 
# source code file (without the .s370). 
# You can use the -debug switch to display
# important data structures as they are built.
#
# At the end of a successful assembly, a listing 
# file is created in the current working directory
# named filename.s370PRN. And the 3 data structures
# [instrdata.p, sourcecode.p, symdict.p]
# required by S370BALEmu are also created in the
# current working directory.
#
# Labels and Field Names MUST start in col 1.
# Mnemonics and Assembler Directives MUST start in col 10.
# Operands MUST start in col 16.
# An asterisk in col 1 denotes a comment line.
# Optional comments on a source line MUST begin in col 50
# or beyond.
#
# 1     10       16       50
# Label Mnemonic Operands Comments
# [0:8] [9:14]   [15:50]  [50:]
#
# Constant types currently supported:
# C, X, B, F, H, D, P, A, Y
#
# The following assembler directives are supported:
# 'USING', 'DC', 'DS', 'EQU' and 'END'.
#
# All assemblies MUST start at location 0
#
# The first two statements in the source code MUST 
# establish your base register as follows:
#
# BALR  R12,0    (base reg can be anything you want) 
# USING *,R12
#
# Do NOT save registers 14-12 at beginning
# or restore them at the end as you would normally do.
#
# A branch to register 14 is required at the end
# of your program (see the sample below). If you 
# plan on using reg 14 in your program then you MUST
# save it prior to using it, then restore it before
# issuing the branch to reg 14 to exit.
#
# Multiple base registers are NOT supported.
#
# Currently DSECTs are NOT supported.
#
# Conditional assembly is NOT supported.
#
# Macro definitions are NOT supported.
# 
# Again this program is intended as an aid
# in teaching the basics of IBM S/370 Assembler coding.
# Not every possible function is implemented - not even 
# the ones considered by most to be critical or important.
#
# Have fun with this and I hope you find it useful!
#
#
# sample program to assemble: 
#
# 000000 ['05', 'C0',                       BALR  R12,0 
# 000002                                    USING *,R12
# 000002  '41', '30', 'C0', '1A',           LA    R3,AREA1
# 000006  '41', '40', '00', '04',           LA    R4,4
# 00000A  '92', 'F0', '30', '00',  LOOP     MVI   0(R3),C'0'
# 00000E  '41', '30', '30', '01',           LA    R3,1(,R3)
# 000012  '46', '40', 'C0', '08',           BCT   R4,LOOP
# 000016  '41', 'F0', '00', '00',           LA    R15,0
# 00001A  '07', 'FE',                       BR    R14
# 00001C  'FF', 'FF', 'FF', 'FF']  AREA1    DC    XL4'FFFFFFFF'
#                                  R0       EQU   0
#                                  ...
#                                  R15      EQU   15
#                                           END            
#         
# {'AREA1   ': ('0000001C', '00000004')}
#


#Convert a negative signed integer to a 2, 4 or 8 byte hex string in two's complement format
def cvtint2scomp(x, numb=32):
    t = bin(x)[3:]
    b = '0'*(numb-len(t)) + t   #expand by propagating a '0' out to 32 or 64 bits
    #flip the bits in b creating num1 
    num1 = ''
    for bit in b:
        if bit == '0':
            num1 = num1 + '1'
        else:
            num1 = num1 + '0'
    t = hex(int(num1,2) + int('0001',2))[2:].upper()
    return [ t[i:i+2] for i in range(0,len(t),2) ]


#Convert a signed integer to a 2, 4, 8 byte hex string 
def cvtint2hex(x, numbytes=4):
    if x < 0:
        return cvtint2scomp(x, (numbytes*8))
    else:
        t = hex(x).lstrip('0x').rjust((numbytes*2),'0').upper()
        return [ t[i:i+2] for i in range(0,len(t),2) ]

        
#Convert integer to packed decimal
def cvtint2pdec(i, pdlen):
    str_i = str(i)    
    if str_i[0] == '-':
        sign = 'D'
        str_i = str_i[1:]
    else:
        sign = 'C'
    t = str_i.rjust((pdlen*2)-1,'0') + sign
    return [ t[i:i+2] for i in range(0,len(t),2) ]


def handle_DC(spec):
    if "'" in spec:
        (type, const) = spec.rstrip("'").split("'")
    elif '(' in spec:
        (type, const) = spec.rstrip(')').split('(')
    else:
        raise Exception('Bad DC spec')
    if len(type) > 1:
        (type, num_bytes) = type.split('L')     #handle XLn  or  CLn
        num_bytes = int(num_bytes)
    else:
        num_bytes = 0
        
    if spec[0] == 'X':
        byte_array = [ const[i:i+2] for i in range(0,len(const),2) ]
        if len(byte_array) < num_bytes:
            for i in range(0,num_bytes-len(byte_array)):
                byte_array.insert(0, '00')
        
    elif spec[0] == 'C':
        byte_array = [ ASC2EBC[ord(const[i])] for i in range(0,len(const)) ]
        if len(byte_array) < num_bytes:
            for i in range(0,num_bytes-len(byte_array)):
                byte_array.append('40')

    elif spec[0] == 'B':
        t = hex(int(const,2))[2:].upper()
        if (len(t) % 2) != 0:
            t = '0' + t
        byte_array = [ t[i:i+2] for i in range(0,len(t),2) ]
        
    elif spec[0] == 'H':
        byte_array = cvtint2hex(int(const), numbytes=2)
        
    elif spec[0] == 'F':
        byte_array = cvtint2hex(int(const), numbytes=4)
        
    elif spec[0] == 'D':
        byte_array = cvtint2hex(int(const), numbytes=8)
        
    elif spec[0] == 'L':
        pass
        
    elif spec[0] == 'P':
        byte_array = cvtint2pdec(int(const), num_bytes)
        
    elif spec[0] == 'Z':
        pass
        
    elif spec[0] == 'A':
        if const[0].isalpha():
            (addr, num_bytes_dict) = symbol_table_dict[const]
            const = addr
        if num_bytes > 0:
            byte_array = cvtint2hex(int(const), numbytes=num_bytes)
        else:
            byte_array = cvtint2hex(int(const), numbytes=4)
                
    elif spec[0] == 'Y':
        if const[0].isalpha():
            (addr, num_bytes_dict) = symbol_table_dict[const]
            const = addr
        byte_array = cvtint2hex(int(const), numbytes=2) 
        
    elif spec[0] == 'V':
        pass

    if num_bytes == 0:
        num_bytes = len(byte_array)
    
    return (num_bytes, byte_array)


def handle_DS(spec):
    gotZero = False
    if spec[0] == '0':                              #handle 0D, 0CL80
        gotZero = True
        spec = spec[1:]

    num_repeats = 1
    if len(spec) > 1:
        if spec[0].isnumeric():                     #handle 18F
            if spec[1].isnumeric():
                num_repeats = int(spec[0:2])
                spec = spec[2:]
            else:
                num_repeats = int(spec[0:1])
                spec = spec[1:]        
        else:
            (type, num_bytes) = spec.split('L')     #handle XLn  or  CLn
            num_bytes = int(num_bytes)
    else:
        num_bytes = 1
       
    if spec[0] == 'X':
        byte_array = [ '00' for i in range(0,num_bytes) ]
        
    elif spec[0] == 'C':
        byte_array = [ '40' for i in range(0,num_bytes) ]

    elif spec[0] == 'B':
        num_bytes =  1 * num_repeats
        byte_array = ['00']
        
    elif spec[0] == 'H':
        num_bytes =  2 * num_repeats
        byte_array = [ '00' for i in range(0,num_bytes) ]
        
    elif spec[0] == 'F':
        num_bytes =  4 * num_repeats
        byte_array = [ '00' for i in range(0,num_bytes) ]
        
    elif spec[0] == 'D':
        num_bytes =  8 * num_repeats
        byte_array = [ '00' for i in range(0,num_bytes) ]
        
    elif spec[0] == 'L':
        pass
        
    elif spec[0] == 'P':
        byte_array = [ '00' for i in range(0,num_bytes) ]
        
    elif spec[0] == 'Z':
        pass
        
    elif spec[0] == 'A':
        num_bytes =  4
        byte_array = [ '00' for i in range(0,num_bytes) ]
        
    elif spec[0] == 'Y':
        num_bytes =  2
        byte_array = [ '00' for i in range(0,num_bytes) ]
        
    elif spec[0] == 'V':
        pass

    if gotZero:
        return (num_bytes, [])

    return (num_bytes, byte_array)


def handle_RR(operands):
    (reg1, reg2) = operands.split(',')
    if reg1[0].isalpha():
        reg1 = symbol_table_dict[reg1]
    if reg2[0].isalpha():
        reg2 = symbol_table_dict[reg2]
        
    return hex(int(reg1))[2:].upper() + hex(int(reg2))[2:].upper()  


def handle_II(operand):
    if operand[0].isalpha():
        operand = symbol_table_dict[operand]
        
    return hex(int(operand))[2:].upper().rjust(2,'0')


def handle_IIBDDD(operands, base_reg):
    (BDDD, II) = operands.split(',')
    
    if II.startswith('C'):
        Idata = ASC2EBC[ord(II[2])]
    elif II.startswith('X'):
        Idata = II[2:4]
        
    BDDDdata = parse_BDDD(BDDD, base_reg)
            
    return Idata + BDDDdata


def handle_RRBDDD(operands, base_reg):
    (R1, R3, BDDD) = operands.split(',')

    if R1[0].isalpha():
        R1 = symbol_table_dict[R1]
    R1data = hex(int(R1))[2:].upper()
    
    if R3[0].isalpha():
        R3 = symbol_table_dict[R3]
    R3data = hex(int(R3))[2:].upper()    
    
    BDDDdata = parse_BDDD(BDDD, base_reg)
            
    return R1data + R3data + BDDDdata


#handle the shift instructions
#BDDD does NOT address data; they are the number of bits to shift
def handle_R0BDDD(operands):
    (R0, BDDD) = operands.split(',')
    
    if R0[0].isalpha():
        R0 = symbol_table_dict[R0]
    R0data = hex(int(R0))[2:].upper()
    
    num_to_shift = '0' + hex(int(BDDD))[2:].upper().rjust(3,'0')

    return R0data + '0' + num_to_shift


#    oper1,oper2
#MVC AREA1,AREA2
#MVC AREA1+5,AREA2
#MVC AREA1,AREA2+5
#MVC AREA1+5,AREA2+5
#MVC AREA1(2),AREA2
#MVC AREA1+5(2),AREA2
def handle_LLBDDDBDDD(operands, base_reg):
    (oper1, oper2) = operands.rsplit(',',1)

    if oper1[0].isnumeric():
        (D1L, B1) = oper1.split(',')
        B1 = B1.rstrip(')')
        if B1[0].isalpha():
            B1 = symbol_table_dict[B1]    
        (D1, L) = D1L.split('(')
        D1 = hex(int(D1))[2:].upper().rjust(3,'0') 
        L = hex(int(L)-1)[2:].upper().rjust(2,'0')
        B1 = hex(int(B1))[2:].upper() 
    else:
        (oper1, exlen_int) = parse_explicitlen(oper1)
        (oper1, offset) = parse_plusminus(oper1)
        (addr, num_bytes) = symbol_table_dict[oper1]
        D1 = hex((addr+offset)-2)[2:].upper().rjust(3,'0')
        if exlen_int == 0:
            L = hex(num_bytes-1)[2:].upper().rjust(2,'0')
        else:
            L = hex(exlen_int-1)[2:].upper().rjust(2,'0')
        B1 = base_reg
        
    if oper2[0].isnumeric():
        (D2, B2) = oper2.split('(')
        B2 = B2.rstrip(')')
        if B2[0].isalpha():
            B2 = symbol_table_dict[B2]    
        D2 = hex(int(D2))[2:].upper().rjust(3,'0') 
        B2 = hex(int(B2))[2:].upper() 
    else:
        (oper2, offset) = parse_plusminus(oper2)
        (addr, num_bytes) = symbol_table_dict[oper2]
        D2 = hex((addr+offset)-2)[2:].upper().rjust(3,'0')
        B2 = base_reg        
        
    return L + B1 + D1 + B2 + D2


#handle the SRP instruction
#SRP D1(L1,B1),shftval(b2+d2),rnddigit(i3)
#the i3 value is the rounding digit to be used.
#with this instruction operand-2 (b2+d2) is not used to address storage. 
#it is used to determine the shift value.
def handle_LIBDDDBDDD(operands, base_reg):
    if operands[0].isnumeric():      #then D1(L1,B1),x,y
        (D1L1, B1, D2B2, I3) = operands.split(',')
        (D1, L1) = D1L1.split('(')
        B1 = B1.rstrip(')')
        if B1[0].isalpha():
            B1 = symbol_table_dict[B1]    
        D1 = hex(int(D1))[2:].upper().rjust(3,'0') 
        L1 = hex(int(L1)-1)[2:].upper()
        B1 = hex(int(B1))[2:].upper() 
    else:                            #then FIELD1,x,y
        (oper1, D2B2, I3) = operands.split(',')
        (oper1, exlen_int) = parse_explicitlen(oper1)
        (oper1, offset) = parse_plusminus(oper1)
        (addr, num_bytes) = symbol_table_dict[oper1]
        D1 = hex((addr+offset)-2)[2:].upper().rjust(3,'0')
        if exlen_int == 0:
            L1 = hex(num_bytes-1)[2:].upper()
        else:
            L1 = hex(exlen_int-1)[2:].upper()
        B1 = base_reg

    I3 = hex(int(I3))[2:].upper() 
    D2B2 = hex(int(D2B2))[2:].upper().rjust(4,'0') 
        
    return L1 + I3 + B1 + D1 + D2B2


def handle_L1L2BDDDBDDD(operands, base_reg):
    if operands.count(',') == 3:                         # 0(6,R6),0(5,R5)
        (D1L1, B1, D2L2, B2) = operands.split(',')
        (D1, L1) = D1L1.split('(')
        B1 = B1.rstrip(')')
        if B1[0].isalpha():
            B1 = symbol_table_dict[B1]    
        D1 = hex(int(D1))[2:].upper().rjust(3,'0') 
        L1 = hex(int(L1)-1)[2:].upper()
        B1 = hex(int(B1))[2:].upper() 
        (D2, L2) = D2L2.split('(')
        B2 = B2.rstrip(')')
        if B2[0].isalpha():
            B2 = symbol_table_dict[B2]    
        D2 = hex(int(D2))[2:].upper().rjust(3,'0') 
        L2 = hex(int(L2)-1)[2:].upper()
        B2 = hex(int(B2))[2:].upper()                     
    elif operands.count(',') == 2:
        if operands[0].isalpha():                        # AREA1,0(5,R5)
            (oper1, D2L2B2) = operands.split(',')
            (oper1, exlen_int) = parse_explicitlen(oper1)
            (oper1, offset) = parse_plusminus(oper1)
            (addr, num_bytes) = symbol_table_dict[oper1]
            D1 = hex((addr+offset)-2)[2:].upper().rjust(3,'0')
            if exlen_int == 0:
                L1 = hex(num_bytes-1)[2:].upper()
            else:
                L1 = hex(exlen_int-1)[2:].upper()
            B1 = base_reg
            (D2L2, B2) = D2L2B2.split(',')
            (D2, L2) = D2L2.split('(')
            B2 = B2.rstrip(')')
            if B2[0].isalpha():
                B2 = symbol_table_dict[B2]    
            D2 = hex(int(D2))[2:].upper().rjust(3,'0') 
            L2 = hex(int(L2)-1)[2:].upper()
            B2 = hex(int(B2))[2:].upper()             
        else:                                            # 0(5,R5),AREA1
            (D1L1B1, oper2) = operands.rsplit(',',1)
            (D1L1, B1) = D1L1B1.split(',')
            (D1, L1) = D1L1.split('(')
            B1 = B1.rstrip(')')
            if B1[0].isalpha():
                B1 = symbol_table_dict[B1]    
            D1 = hex(int(D1))[2:].upper().rjust(3,'0') 
            L1 = hex(int(L1)-1)[2:].upper()
            B1 = hex(int(B1))[2:].upper()
            (oper2, exlen_int) = parse_explicitlen(oper2)
            (oper2, offset) = parse_plusminus(oper2)            
            (addr, num_bytes) = symbol_table_dict[oper2]
            D2 = hex((addr+offset)-2)[2:].upper().rjust(3,'0')
            if exlen_int == 0:
                L2 = hex(num_bytes - 1)[2:].upper()
            else:
                L2 = hex(exlen_int - 1)[2:].upper()
            B2 = base_reg
    elif operands.count(',') == 1:                       # AREA1,AREA2
        (oper1, oper2) = operands.split(',')
        (oper1, exlen_int) = parse_explicitlen(oper1)
        (oper1, offset) = parse_plusminus(oper1)
        (addr, num_bytes) = symbol_table_dict[oper1]
        D1 = hex((addr+offset)-2)[2:].upper().rjust(3,'0')
        if exlen_int == 0:
            L1 = hex(num_bytes-1)[2:].upper()
        else:
            L1 = hex(exlen_int-1)[2:].upper()
        B1 = base_reg
        (oper2, exlen_int) = parse_explicitlen(oper2)
        (oper2, offset) = parse_plusminus(oper2)            
        (addr, num_bytes) = symbol_table_dict[oper2]
        D2 = hex((addr+offset)-2)[2:].upper().rjust(3,'0')
        if exlen_int == 0:
            L2 = hex(num_bytes-1)[2:].upper()
        else:
            L2 = hex(exlen_int-1)[2:].upper()
        B2 = base_reg  
        
    return L1 + L2 + B1 + D1 + B2 + D2
    

#all the permutations of 'xx RX BD DD'
#STC   R4,134(0,12)
#STC   R4,134(5,12)     #using R5 as index reg
#STC   R4,134(,12)
#STC   R4,134(12)       #using R12 as index reg; R0 as base reg
#STC   R4,134           #says store the char at low core loc x'86'
#STC   R4,AREA1
#STC   R4,AREA1+1
#STC   R4,AREA1(R5)     #using R5 as index reg
#STC   R4,AREA1+1(R5)   #using R5 as index reg    
def handle_RXBDDD(operands, base_reg):
    if operands.count(',') == 1:
        (R1,oper2) = operands.split(',')
        if R1[0].isalpha():
            R1 = symbol_table_dict[R1]
        R1data = hex(int(R1))[2:].upper()
        if oper2[0].isalpha():                             #STC   R4,AREA1 / STC   R4,AREA1+1
            X2 = '0'                                       #STC   R4,AREA1(R5) / STC   R4,AREA1+1(R5)
            if '(' in oper2:
                (fieldn, Xreg) = oper2.split('(')
                X2 = Xreg.rstrip(')')
                if X2[0].isalpha():
                    X2 = symbol_table_dict[X2]
                X2 = hex(int(X2))[2:].upper()
                oper2 = fieldn
            (oper2, offset) = parse_plusminus(oper2)
            if isinstance(symbol_table_dict[oper2],tuple):
                (addr, num_bytes) = symbol_table_dict[oper2]
            else:
                addr = symbol_table_dict[oper2]
            D2 = hex((addr+offset)-2)[2:].upper().rjust(3,'0')
            B2 = base_reg              
        else:                                              #STC   R4,134 
            X2 = '0'
            B2 = '0'
            if '(' in oper2:                               #STC   R4,134(12)
                (disp, Xreg) = oper2.split('(')
                X2 = Xreg.rstrip(')')
                if X2[0].isalpha():
                    X2 = symbol_table_dict[X2]
                X2 = hex(int(X2))[2:].upper() 
                oper2 = disp
            D2 = hex(int(oper2))[2:].upper().rjust(3,'0')
    else:                                                  #STC   R4,134(5,12) / STC   R4,134(,12) / 
        (R1,oper2) = operands.split(',',1)
        if R1[0].isalpha():
            R1 = symbol_table_dict[R1]
        R1data = hex(int(R1))[2:].upper()
        (D2, X2B2) = oper2.split('(')
        (X2, B2) = X2B2.split(',')
        if X2 == '':
            X2 = '0'
        else:
            if X2[0].isalpha():
                X2 = symbol_table_dict[X2]
            X2 = hex(int(X2))[2:].upper()             
        B2 = B2.rstrip(')')
        if B2[0].isalpha():
            B2 = symbol_table_dict[B2]    
        B2 = hex(int(B2))[2:].upper()   
        D2 = hex(int(D2))[2:].upper().rjust(3,'0')
       
    return R1data + X2 + B2 + D2
    
    
def parse_BDDD(BDDD, base_reg):
    if BDDD[0].isalpha():
        (BDDD, offset) = parse_plusminus(BDDD)
        (addr, num_bytes) = symbol_table_dict[BDDD]
        DDDdata = hex((addr+offset)-2)[2:].upper().rjust(3,'0')    #adjust for base_reg = 2 and assembly starting at 0
        Bdata = base_reg
    else:
        (DDD, B) = BDDD.rstrip(')').split('(')
        DDDdata = hex(int(DDD))[2:].upper().rjust(3,'0')
        if B[0].isalpha():
            B = symbol_table_dict[B]
        Bdata = hex(int(B))[2:].upper()
        
    return Bdata + DDDdata


def parse_plusminus(fieldn):
    offset = 0
    if '+' in fieldn:
        (fn, off) = fieldn.split('+')
        offset = int(off)
    elif '-' in fieldn:
        (fn, off) = fieldn.split('-')
        offset = int(off) * -1
    else:
        fn = fieldn

    return (fn, offset)


def parse_explicitlen(oper):
    exlen_int = 0
    if '(' in oper:
        (fieldn, exlen) = oper.split('(')
        exlen = exlen.rstrip(')')
        if exlen[0].isalpha():
            exlen = symbol_table_dict[exlen]
        exlen_int = int(exlen)
        oper = fieldn

    return (oper, exlen_int)
    
    
# ----------------------------------------------------------
# main starts here
# ----------------------------------------------------------

debug = False

# Process Command Line parameters
#  
if len(sys.argv)-1 > 0:
    file_name = sys.argv[1]
    try:
        if sys.argv[2] == '-debug':
            debug = True
    except IndexError:
        pass
else:
    print('s370 file name missing')
    exit(1)
        
#open the source code file and create a list from assembler statements    
inputfi = open(file_name+'.s370', 'r')
source_code_list = [line.rstrip('\n') for line in inputfi]

#--------------------------------------------------------------#
#pass 1 logic
#
#iterate over sourcecode
#build address / op code list
#build symbol table dictionary
#resolve literals
#resolve DCs and DSs
#replace extended mnemonic branch instructions with BCs
#

print('Step 1: Executing Pass 1 Logic')

address_opcode_list = []
symbol_table_dict = {}
program_ctr = 0
sl_ctr = 0
lit_suffix = 1

while True:
    sl = source_code_list[sl_ctr]
    
    #handle a comment
    if sl[0] == '*':
        sl_ctr = sl_ctr + 1
        continue
        
    #handle literals as operands
    t = sl[15:50].rstrip(' ')
    if '=' in t:
        (oper1, lit) = t.split('=')
        lit_name = 'LT' + str(lit_suffix).rjust(3,'0')
        source_code_list[sl_ctr] = sl[0:15] + oper1 + lit_name
        new_DC = lit_name + '    DC    ' + lit
        source_code_list.insert(len(source_code_list)-1, new_DC)
        lit_suffix = lit_suffix + 1

    mnemonic = sl[9:14].rstrip(' ')
    
    if mnemonic in assem_inst_list:
        if mnemonic == 'USING':
            pass
            
        elif mnemonic == 'DROP':
            pass
            
        elif mnemonic == 'EQU':
            if sl[15] == '*':
                symbol_table_dict[sl[0:8].rstrip(' ')] = program_ctr
            else:
                symbol_table_dict[sl[0:8].rstrip(' ')] = sl[15:50].rstrip(' ')
                
        elif mnemonic == 'DC':
            DC_num_bytes_tot = 0                             #handle possible multiple constants on
            const_array_tot = []                             #one DC
            DC_list = sl[15:50].rstrip(' ').split(',')
            for x in DC_list:
                (DC_num_bytes, const_array) = handle_DC(x)
                DC_num_bytes_tot = DC_num_bytes_tot + DC_num_bytes
                for y in const_array:
                    const_array_tot.append(y)
            address_opcode_list.append((program_ctr, ''.join(const_array_tot)))
            #add label on same line as DC to symbol table dict
            if sl[0] != ' ':
                symbol_table_dict[sl[0:8].rstrip(' ')] = (program_ctr, DC_num_bytes_tot) 
            program_ctr = program_ctr + DC_num_bytes_tot
            
        elif mnemonic == 'DS':
            (DS_num_bytes, const_array) = handle_DS(sl[15:50].rstrip(' '))
            # an empty const_array list indicates we had a 'DS  0F, 0D, 0CL4', etc
            if const_array:     
                address_opcode_list.append((program_ctr, ''.join(const_array)))
            #add label on same line as DS to symbol table dict
            if sl[0] != ' ':
                symbol_table_dict[sl[0:8].rstrip(' ')] = (program_ctr, DS_num_bytes)
            # an empty const_array list indicates we had a 'DS  0F, 0D, 0CL4', etc
            if const_array:      
                program_ctr = program_ctr + DS_num_bytes

        elif mnemonic == 'END':
            break
    else:
        if mnemonic in extended_mnemonic_inst_dict.keys():
            bc_mnemonic = 'BC     '
            if mnemonic.endswith('R'):
                bc_mnemonic = 'BCR    '
            source_code_list[sl_ctr] = source_code_list[sl_ctr][0:9] + bc_mnemonic + extended_mnemonic_inst_dict[mnemonic] + ',' + source_code_list[sl_ctr][15:]
            sl = source_code_list[sl_ctr]
            mnemonic = sl[9:14].rstrip(' ')
            
        (op_code, operands, machine_format) = mach_inst_dict[mnemonic]
        inst_len = len(machine_format.split(' ')) + 1
        address_opcode_list.append((program_ctr, op_code))
        #add label on same line as inst to symbol table dict
        if sl[0] != ' ':
            symbol_table_dict[sl[0:8].rstrip(' ')] = program_ctr
        program_ctr = program_ctr + inst_len
        
    sl_ctr = sl_ctr + 1

if debug:      
    print(address_opcode_list)    
    print(symbol_table_dict)

#--------------------------------------------------------------#
#pass 2 logic
#
#iterate over source_code_list 
#resolve USING to establish base reg
#add operand code to address_opcode_list
#

print('Step 2: Executing Pass 2 Logic')

sl_ctr = 0
aol_ctr = 0
base_reg = '0'

while True:
    sl = source_code_list[sl_ctr]
    
    #handle a comment
    if sl[0] == '*':
        sl_ctr = sl_ctr + 1
        continue
        
    mnemonic = sl[9:14].rstrip(' ')
    
    if mnemonic in assem_inst_list:
        if mnemonic == 'USING':
            (scope, reg) = sl[15:50].rstrip(' ').split(',')
            if reg[0].isalpha():
                reg = symbol_table_dict[reg]
            if scope == '*':
                base_reg = hex(int(reg))[2:].upper()
            else:
                pass
            
        elif mnemonic == 'DROP':
            pass
            
        elif mnemonic == 'EQU':
            pass
                
        elif mnemonic == 'DC':
            pass
            
        elif mnemonic == 'DS':
            pass
            
        elif mnemonic == 'END':
            break
    else:
        (op_code, operands, machine_format) = mach_inst_dict[mnemonic]
        inst_len = len(machine_format.split(' ')) + 1
        
        if machine_format == 'RR' or machine_format == 'MR':
            code = handle_RR(sl[15:50].rstrip(' '))

        elif machine_format == 'LL BD DD BD DD':
            code = handle_LLBDDDBDDD(sl[15:50].rstrip(' '), base_reg)
            
        elif machine_format == 'L1L2 BD DD BD DD':
            code = handle_L1L2BDDDBDDD(sl[15:50].rstrip(' '), base_reg)

        elif machine_format == 'RX BD DD' or machine_format == 'MX BD DD':
            code = handle_RXBDDD(sl[15:50].rstrip(' '), base_reg)
            
        elif machine_format == 'RR BD DD' or machine_format == 'RM BD DD':
            code = handle_RRBDDD(sl[15:50].rstrip(' '), base_reg)
            
        elif machine_format == 'II BD DD':
            code = handle_IIBDDD(sl[15:50].rstrip(' '), base_reg)           

        elif machine_format == 'R0 BD DD':    #only the shift instructions use this one
            code = handle_R0BDDD(sl[15:50].rstrip(' '))           
            
        elif machine_format == 'II':          #only the SVC instruction use this one
            code = handle_II(sl[15:50].rstrip(' '))           

        elif machine_format == 'LI BD DD BD DD':
            code = handle_LIBDDDBDDD(sl[15:50].rstrip(' '), base_reg)
            
        (addr, opc) = address_opcode_list[aol_ctr]
        address_opcode_list[aol_ctr] = (addr, opc+code)            
            
        aol_ctr = aol_ctr + 1

    sl_ctr = sl_ctr + 1

if debug:    
    print(address_opcode_list)    
    print(symbol_table_dict)

    print(' ')

#--------------------------------------------------------------#
#create the assembler output listing
#

print('Step 3: Create the assembler output listing')

#open the assembler output print file    
outputfi = open(file_name+'.s370PRN', 'w')

sl_ctr = 0
aol_ctr = 0

instrdata = []
work_source_code_list = []

while True:
    sl = source_code_list[sl_ctr]

    mnemonic = sl[9:14].rstrip(' ')
    operand = sl[15:50].rstrip(' ')

    if sl[0] != '*' and (mnemonic in mach_inst_dict.keys() or (mnemonic == 'DC' or mnemonic == 'DS')):
        if mnemonic == 'DS' and operand[0] == '0':
            (addr, code) = address_opcode_list[aol_ctr]
            listing_line = hex(addr).lstrip('0x').rjust(6,'0').upper() + ' ' + 48*' ' + ' ' + sl
            if debug:
                print(listing_line)
            outputfi.write(listing_line + '\n')
        else:
            (addr, code) = address_opcode_list[aol_ctr]
            if len(code) > 46:
                display_code = code[0:46]
            else:
                display_code = code
            display_addr = hex(addr).lstrip('0x').rjust(6,'0').upper()
            assem_output = display_addr + ' ' + display_code
            if debug:
                print(assem_output, (54-len(assem_output))*' ', sl)
            outputfi.write(assem_output + ' ' + (54-len(assem_output))*' ' + ' ' + sl + '\n')    
            aol_ctr = aol_ctr + 1
            instrdata.extend([code[i:i+2] for i in range(0,len(code),2) ])
            work_source_code_list.append(assem_output + ' ' + (54-len(assem_output))*' ' + ' ' + sl)
    else:
        if debug:
            print(display_addr, (54-len(display_addr))*' ', sl)
        outputfi.write(display_addr + ' ' + (54-len(display_addr))*' ' + ' ' + sl + '\n')
        
    if mnemonic == 'END':
        break
        
    sl_ctr = sl_ctr + 1

#--------------------------------------------------------------#
#build the instruction/data list and the symbol & source code 
#dictionaries for the S370BALEmu
#

print('Step 4: Build the required S370BALEmu data structures')

symdict = {}
source_code_dict = {}

for line in work_source_code_list:
    try:
        t = int(line[0:6],16)   #are col 1-6 valid hex digits
        if line[7] in '0123456789ABCDEF' and (' DC ' not in line and ' DS ' not in line):
                source_code_dict[line[0:6]] = line[65:106].rstrip(' ')
    except ValueError:
        pass

for k in symbol_table_dict.keys():
    if isinstance(symbol_table_dict[k],tuple):
        (addr, num_bytes) = symbol_table_dict[k]
        dict_addr = hex(addr).lstrip('0x').rjust(8,'0').upper()
        dict_num_bytes = hex(num_bytes).lstrip('0x').rjust(8,'0').upper()
        symdict[k.ljust(8,' ')] = (dict_addr, dict_num_bytes)

#--------------------------------------------------------------#
#display the 3 data structures (if the -debug flag is true)
#and pickle them for the S370BALEmu
#  
if debug:
    print(symdict)
    print(' ')

pickle.dump( symdict, open( "symdict.p", "wb" ) )
#symdict = pickle.load( open( "symdict.p", "rb" ) )

if debug:
    print(source_code_dict)
    print(' ')

pickle.dump( source_code_dict, open( "sourcecode.p", "wb" ) )
#source_code_dict = pickle.load( open( "sourcecode.p", "rb" ) )

if debug:
    print(instrdata)
    print(' ')

pickle.dump( instrdata, open( "instrdata.p", "wb" ) )  
#instrdata = pickle.load( open( "instrdata.p", "rb" ) )

exit()
