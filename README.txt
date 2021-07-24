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
# You must have Python V3 installed on your PC or Mac.
#
# In an effort to make this as fun for me
# as possible (which of course is my aim),
# there is some, but not extensive 
# error checking. If you have bad assembler code
# S370BALAsm will abend, and hopefully you will 
# be able to fix your problem. Always look at your code
# first before blaming the assembler.
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
# ASCII text file. IMPORTANT NOTE: TAB
# characters are NOT supported and MUST NOT
# appear in your text file. Insure that your
# editor replaces the tab character with the
# appropriate number of spaces or do not
# use the TAB key.
#
# The source code input file MUST exist in your current
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
# Operands MUST start in col 16 and end by col 49.
# Operands of any kind extending beyond col 49 will cause an error
# or erratic behavior.
# Optional comments on a source line MUST begin no earlier than col 51
# or beyond.
# An asterisk in col 1 denotes a comment line.
#
# 1     10       16       51
# Label Mnemonic Operands Comments
# [0:8] [9:14]   [15:50]  [50:]
#
# Constant types currently supported:
# C, X, B, F, H, D, P, A, Y
#
# The following assembler directives are supported:
# 'USING', 'DC', 'DS', 'EQU' and 'END'.
#
# Note: the EQU directive ONLY supports an operand
# of '*' or a single value. No arithmetic is allowed
# as an operand of an EQU.
#
# Use of the implict length operator is supported on RX type instructions.
# For example:     LA    1,L'DATAAREA
#
# The following assembler directives are tolerated (meaning they are 
# permitted in the source file but are ignored and are made into a comment):
# 'CSECT', 'PRINT', 'DROP', and 'LTORG'.
#
# Please note that even though LTORG is not supported, literals (for example, =F'0') 
# are supported. When encountered, the assembler will create a new data constant 
# on the fly and add it before the END statement.
#
# The following MVS IO macros are supported:
# 'OPEN', 'GET', 'PUT', 'CLOSE', 'DCB' and 'WTO'.
# Please see README_IO.txt for more information on how to use these macros.
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
# If you need a full function assembler, please consider
# using IFOX00 under MVS3.8J or Z390 Portable Mainframe Assembler 
# and Emulator (Copyright 2011-13 Automated Software Tools Corporation).
#
# If you encounter a bug, feel free to open a GitHub issue
# and I will attempt to look at it. I may ask for the source code
# file that you are trying to assemble.
#
# Have fun with this and I hope you find it useful!
#
# 
# Here is a sample program to assemble: 
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
