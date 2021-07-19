Open the file 'report_with_macros.s370'  to see how do these I/O macros work. They are as much like MVS as I can get them.

Like all statements they need to adhere to the 1-10-16-51 rule (labels start in col 1, macro names start in col 10, macro 
operands start in col 16 and must end before col 50, and comments start in col 51). 

Open a file:

[label]  OPEN  (dcb_name, INPUT)
[label]  OPEN  (dcb_name, OUTPUT)

Notes:
1) Single file ONLY. Can NOT open multiple files in one OPEN statement
2) The INPUT/OUTPUT operands are required, but are ignored by the program
3) The parentheses are required

examples:

INOPEN   OPEN  (INDCB,INPUT)
*
OUOPEN   OPEN  (OUTDCB,OUTPUT)

-------------------------------------------------
Write a record to a file:

[label]      PUT    dcb_name,data_area

example:
WTITLE   PUT   OUTDCB,PTITLE

-------------------------------------------------
Read a record from a file:

[label]     GET     dcb_name,data_area

example:
READREC  GET   INDCB,PAYREC                       READ IN EMPLOYEE REC

-------------------------------------------------
Close a file:

[label]  CLOSE (dcb_name)

Notes:
1) Single file ONLY. Can NOT close multiple files in one CLOSE statement
2) The parentheses are required

-------------------------------------------------
Define a file:
label     DCB    dcb_operands separated by commas

Notes:
1) Single line ONLY - NO continuation lines allowed
2) MACRF is included for MVS compatibility only, it is ignored otherwise
2) DSORG is included for MVS compatibility only, it is ignored otherwise
3) DCBs for INPUT files MUST include the EODAD, otherwise the DCB is treated as an OUTPUT file
4) *** IMPORTANT***  - DDNAME specifies either the real PC file name OR the name of an environment variable pointing to the real PC file name.
If you do not have an environment variable set, then the name specified on the DDNAME= is the name that the emulator will use.

How to set environment variables:
    Windows example:
    set INDD=SALARIES.INPUT
    set OUTDD=REPORT.OUTPUT

    Linux example:
    export INDD=SALARIES.INPUT
    export OUTDD=REPORT.OUTPUT


examples:
INDCB    DCB   MACRF=GM,DDNAME=INDD,DSORG=PS,EODAD=INCLOS               
OUTDCB   DCB   MACRF=PM,DDNAME=OUTDD,DSORG=PS         


-------------------------------------------------
Write data to terminal:

[label]  WTO   data_area

Notes:
1) Single data area ONLY.
2) It is assumed that data_area points to valid EBCDIC characters.

-------------------------------------------------
