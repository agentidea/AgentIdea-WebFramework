

/**
*	Javascript Language Extension
*
*/

/**
* Crockfords Object clone
*/
if( typeof Object.create !== 'function')
{
	Object.create = function(o) {
		var F = function() {};
		F.prototype = o;
		return new F();
	};
}
 
 
 
String.prototype.trim = function() {
	return this.replace(/^\s+|\s+$/g,"");
}
String.prototype.ltrim = function() {
	return this.replace(/^\s+/,"");
}
String.prototype.rtrim = function() {
	return this.replace(/\s+$/,"");
}




String.prototype.startsWith = function(pattern) {
	return (this.match("^"+pattern)==pattern)
}


/**
*	@description: Pulls part of a string, excluding the pattern
*   @example: if string is say txtFirstName, and the pattern passed is txt, then return FirsName
*   @return: string - pattern
*
* 	$to do: re-write with regex
*
*/ 

String.prototype.pull = function(pattern) {
	if( this.startsWith ) {
		return this.substring(pattern.length,this.length);
	}
	else
	{
		return "";
	}
}


/**
* @description: indexOf an array if not already implemented, else use the Array's Index of method
* @return: boolean if a value is found in an array
*
*/

Array.prototype.has = (
	  !Array.indexOf ? function (o)
	  {
	      var l = this.length + 1;
          while (l -= 1)
          {
            if (this[l - 1] === o)
            {            
            	return true;        
            }
           }    
	       return false;  
	  } : function (o)
	  {
			return (this.indexOf(o) !== -1);  
	  });


