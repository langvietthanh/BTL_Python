import os 
import io 
import tokenize 
import token 
from typing import List ,Tuple 

PROJECT_ROOT =os .path .dirname (os .path .dirname (os .path .abspath (__file__ )))

EXCLUDE_DIRS ={'.git','.venv','venv','__pycache__','dist','build','.cursor','.agent-tools'}


def is_probable_docstring (prev_tokens :List [tokenize .TokenInfo ],tok :tokenize .TokenInfo )->bool :
    if tok .type !=token .STRING :
        return False 

    significant =[t for t in prev_tokens if t .type not in (token .ENCODING ,token .NL ,token .NEWLINE ,token .INDENT ,token .DEDENT ,token .COMMENT )]
    if not significant :
        return True 


    last_sig =None 
    for t in reversed (significant ):
        if t .type not in (token .NL ,token .NEWLINE ,token .INDENT ,token .DEDENT ):
            last_sig =t 
            break 
    if last_sig and last_sig .string ==':':

        before_colon =None 
        for t in reversed (significant [:-1 ]):
            if t .type not in (token .NL ,token .NEWLINE ,token .INDENT ,token .DEDENT ):
                before_colon =t 
                break 
        if before_colon and before_colon .type ==token .NAME and before_colon .string in ('def','class'):

            if prev_tokens and prev_tokens [-1 ].type ==token .INDENT :
                return True 
    return False 


def strip_comments_and_docstrings (source :str )->str :
    result_tokens :List [Tuple [int ,str ]]=[]
    prev_tokens :List [tokenize .TokenInfo ]=[]
    g =tokenize .generate_tokens (io .StringIO (source ).readline )
    for tok in g :
        if tok .type ==token .COMMENT :
            continue 
        if tok .type ==token .STRING and is_probable_docstring (prev_tokens ,tok ):
            continue 

        result_tokens .append ((tok .type ,tok .string ))
        prev_tokens .append (tok )
    return tokenize .untokenize (result_tokens )


def process_file (path :str )->None :
    try :
        with open (path ,'r',encoding ='utf-8')as f :
            src =f .read ()
        new_src =strip_comments_and_docstrings (src )
        if new_src !=src :
            with open (path ,'w',encoding ='utf-8')as f :
                f .write (new_src )
            print (f"Stripped comments: {path }")
    except Exception as e :
        print (f"Skip {path }: {e }")


def main ():
    for root ,dirs ,files in os .walk (PROJECT_ROOT ):
        dirs [:]=[d for d in dirs if d not in EXCLUDE_DIRS ]
        for fname in files :
            if fname .endswith ('.py'):
                process_file (os .path .join (root ,fname ))


if __name__ =='__main__':
    main ()
