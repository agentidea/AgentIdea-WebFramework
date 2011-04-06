#
# simple command line parser
#

from ply import lex 
from ply import yacc

class Parameter():
    def __init__(self,name,value):
        self.name = name
        self.value = value

class Command():
    
    def __init__(self, name):
        self.name = name
        self.parameters = []
     
    def addParam(self,name,value):   
        p = Parameter(name,value)
        self.parameters.append(p)
        
    def __repr__(self):
        return "command(%s, %s)" % (self.name, str( self.parameters ))



reserved = (
    'LOCAL', 'REMOTE', 'ASYNC', 'MULTI', 
    )

tokens =  reserved + (

    #verb                 
    'COMMAND_NAME',
    
    #literals ( quoted string phrases, strings,number
    'PARAM_PHRASE','PARAM_STRING','PARAM_NUMBER',

    
    # Assignment (=)
    'EQUALS',

    # Delimeters ( ) ,
    'LPAREN', 'RPAREN', 'COMMA'
    )

# Completely ignored characters
t_ignore = r' \x0c' # IGNORE SPACES, FORM FEEDS

# Newlines
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

#HOW TO DYNAMICALLY POPULATE A TUPLE?
t_COMMAND_NAME    = (
             r'AUTHENTICATE|INTIALIZE|LOGIN|REPORT|'
             r'FIRE|ORBIT|SPIN'
             )



# Assignment operators
t_EQUALS           = r'='

# Delimeters
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_COMMA            = r','

# Comments
def t_comment(t):
    r' /\*(.|\n)*?\*/'
    t.lineno += t.value.count('\n')

def t_PARAM_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_PARAM_STRING    = r'[a-zA-Z_][a-zA-Z0-9_]*'

t_PARAM_PHRASE = r'\"([^\\\n]|(\\.))*?\"'  # String literal ( from K&R C 2nd ed. )


def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

lexer = lex.lex()





#parser


def p_commands(p):
    """
    commands : command 
    commands : command command
    commands : command command command
    commands : command command command command
    commands : command command command command command
    commands : command command command command command command
    commands : command command command command command command command
    commands : command command command command command command command command
    """
    ret = []
    
    numCommands = len(p)
    for i in range(numCommands):
        ret.append(p[i])
        
    p[0] = ret

def p_command(p):
    """
    command : name parameter_list
    """
    
    #command : name seen_name parameter_list
    p[0] = p[1] 

def ap_seen_name(p):
    "seen_name :"
    print " saw a command name = " , p[-1]
    p[0] = "babu"
    

def p_name(p):
    """ name : COMMAND_NAME """
    #    p[0] p[1]
    p[0] = Command(p[1])
    

def p_parameter_list(p):
    """
    parameter_list : param
    parameter_list : param param
    parameter_list : param param param
    parameter_list : param param param param
    parameter_list : param param param param param
    parameter_list : param param param param param param
    parameter_list : param param param param param param param
    parameter_list : param param param param param param param param
    """
    pass

def p_parameter(p):
    """ 
    param : PARAM_PHRASE
    param : PARAM_STRING
    param : PARAM_NUMBER
    """
    
    param = p[1]
    cmd = None
    counter = -1
    
    while(True):
        if p[counter] != None:
            cmd = p[counter]
            break
        counter = counter -1
        
        
    
    #'PARAM_PHRASE','PARAM_STRING','PARAM_NUMBER',
    p[0] = cmd.addParam('param',param)
    
    
def p_error(p):
    raise TypeError("unknown text at %r" % (p.value,))
    
yacc.yacc()    



def parseCommndLine(s):
    parseList = yacc.parse(s)
    
    return parseList
        
def getParams(params):
    s = ""
    for param in params:
        s = s +  str(param.value) + ","

    return s

s = """

/* basic minilanguage to run commands */

LOGIN radical
AUTHENTICATE "5hL0 moOo zx0 FOX"
REPORT attitude tree house rock
REPORT far away tree "schedule of  7" YELLOW 55 98 200
LOGIN katie


"""

commands = parseCommndLine(s)
print 'parsed '

for cmd in commands:
    if(cmd):
        print cmd.name + " -- " + getParams(cmd.parameters)




#lexer.input(s)

# Tokenize
#while True:
#    tok = lexer.token()
#    if not tok: break      # No more input
#    print tok.type, tok.value, tok.lexpos





