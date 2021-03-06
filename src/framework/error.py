class MongoDocNotFoundException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class MongoTreeCorruptException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)   
 
class WrongNumberParametersException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InvalidParameterTypeException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InvalidCommandSpecificationException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class UnexpectedParameterException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)       
class MissingCommandSpecificationException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)         
class MissingParameterException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)       
class RequiredParameterMissingException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)       
class MongoConnectionException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class MongoInstanceException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class OutOfSequenceException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value) 
class CommandNotFoundException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)                    
class SendMailException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)     

class InvalidRequestMethod(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)                 
class KeyNotFoundException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)      
class WebserviceException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)     
        
class NewPasswordMismatchException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)     
    
class OldPasswordMismatchException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)         
    