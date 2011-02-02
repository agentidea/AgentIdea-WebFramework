/*

    AgentIdea - util functions
  
*/

//Crockfords 'object' clone
if( typeof Object.create !== 'function')
{
	Object.create = function(o) {
		var F = function() {};
		F.prototype = o;
		return new F();
	};
}

//
//Language Extension Methods
//

/* FUNCTIONAL ASPECTS 
Array.method('reduce', function (f, value) {
	var i;
	for(i=0; i< this.length; i += 1) {
		value = f(this[i], value);
	}
	return value;
 });
 */
 
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
*
*
* $to do: re-write with regex
*
*/ 
String.prototype.pullRest = function(pattern) {
	if( this.startsWith ) {
		return this.substring(pattern.length,this.length);
	}
	else
	{
		return "";
	}
}

/**
* @
* @return boolean if a value is found in an array
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







function getTuple(code) {

    var retTup = null;
    
    var tups = storyView.StoryController.CurrentStory.storyTuples;
    var len = tups.length;
    for (var i = 0; i < len; i++) {
        var t = tups[i];
        if (t.code == code) {
            retTup = t;
            break;
        }
    }

    return retTup;

}


function reflect(o,delim)
{

    var description = "";
    
    if(!delim) delim = "|";
    
    for (var i in o)
    {
        var property = o[i];
        description += i + " = " + property + delim;     
    }

    return (description);
}

	
	var _theUte = null;
	function TheUte()
	{
	    if(_theUte == null)
	        _theUte = new utils();
	        
	    return _theUte;
	}
	
	
	
	function utils()
	{
	    this.findElement = findElement;
	    this.removeChildren = removeChildrenElements;
	    this.hasChildren = hasChildrenElements;
	    this.newGrid = newGrid;
	    this.setGridCell = setGridCell;
	    this.callout = callout;
	    this.getButton = getButton2;
	    this.unravel = function(what)
	    {
  			return this.decode64(this.URLDecode(what));
	    
	    };
	    
	    
	    this.getTimestamp = function()
	    {
	    	var d=new Date();
	    	return d;
	    
	    };
	    
	    this.getTextArea = getTextArea;
	    this.getInputBox = getInputBox;
	    this.getPassword = getPassword;
	    this.getSelect = getSelect;
	    this.getSelect2 = getSelect2;
	    this.getSelect3 = getSelect3;
	    this.getSelectColor = getSelectColor;
	    this.getCheckbox = getCheckbox;

	    
	    var _keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
		this.keyStr = _keyStr;
		this.filterText = filterText;
		this.encode64 = encode64;
		this.decode64 = decode64;
		
		this.padNum = function(num,numPlaces)
		{


		    var newNum = 100 + num;
		    var paddedNum = newNum + "";
		    //alert(paddedNum);
		    var partialNum = paddedNum.substring(paddedNum.length-2,3);
		    return partialNum;
		
		}
		
		
		
		this.URLEncode = URLEncoder;
		this.URLDecode = URLDecoder;
		
		
		this.getSpacer = function(w,h)
		{
		    var _dv = document.createElement("DIV");
		    _dv.style.width = w;
		    _dv.style.height = h;
		    return _dv;
		    
		
		}
		
		this.pullStringOffStack = function(aStack)
        {
            var ret = null;
            if(aStack!=null)
            {
              var i = 0;
              aStack.reverse();
              
              var character = "";
              while( aStack.length > 0)
              {
                var tmpCharInt =  aStack.pop();
                
                var tmpChar = String.fromCharCode(tmpCharInt);
                
                if(tmpCharInt == 190)
                {
                    character += ".";
                }
                else
                if(tmpCharInt == 191)
                {
                    character += "/";
                }
                else
                {
                    character += tmpChar;
                }
              }

               ret = character;
            }
            
            return ret;
        }
        
        this.cleanStack = function(aStack)
        {
            while( aStack.length > 0)
            {
                var garbage = aStack.pop();
                garbage = null;
                
            }
            
        }
	
	}
	
	
// ====================================================================
//       URLEncode and URLDecode functions
//
// Copyright Albion Research Ltd. 2002
// http://www.albionresearch.com/
//
// You may copy these functions providing that 
// (a) you leave this copyright notice intact, and 
// (b) if you use these functions on a publicly accessible
//     web site you include a credit somewhere on the web site 
//     with a link back to http://www.albionresarch.com/
//
// If you find or fix any bugs, please let us know at albionresearch.com
//
// SpecialThanks to Neelesh Thakur for being the first to
// report a bug in URLDecode() - now fixed 2003-02-19.
// ====================================================================
function URLEncoder( plaintext )
{
	// The Javascript escape and unescape functions do not correspond
	// with what browsers actually do...
	var SAFECHARS = "0123456789" +					// Numeric
					"ABCDEFGHIJKLMNOPQRSTUVWXYZ" +	// Alphabetic
					"abcdefghijklmnopqrstuvwxyz" +
					"-_.!~*'()";					// RFC2396 Mark characters
	var HEX = "0123456789ABCDEF";

	//var plaintext = document.URLForm.F1.value;
	var encoded = "";
	for (var i = 0; i < plaintext.length; i++ ) {
		var ch = plaintext.charAt(i);
	    if (ch == " ") {
		    encoded += "+";				// x-www-urlencoded, rather than %20
		} else if (SAFECHARS.indexOf(ch) != -1) {
		    encoded += ch;
		} else {
		    var charCode = ch.charCodeAt(0);
			if (charCode > 255) {
			    alert( "Unicode Character '" 
                        + ch 
                        + "' cannot be encoded using standard URL encoding.\n" +
				          "(URL encoding only supports 8-bit characters.)\n" +
						  "A space (+) will be substituted." );
				encoded += "+";
			} else {
				encoded += "%";
				encoded += HEX.charAt((charCode >> 4) & 0xF);
				encoded += HEX.charAt(charCode & 0xF);
			}
		}
	} // for

	return encoded;
}//;

function URLDecoder( encoded )
{
   // Replace + with ' '
   // Replace %xx with equivalent character
   // Put [ERROR] in output if %xx is invalid.
   var HEXCHARS = "0123456789ABCDEFabcdef"; 
  // var encoded = document.URLForm.F2.value;
   var plaintext = "";
   var i = 0;
   while (i < encoded.length) {
       var ch = encoded.charAt(i);
	   if (ch == "+") {
	       plaintext += " ";
		   i++;
	   } else if (ch == "%") {
			if (i < (encoded.length-2) 
					&& HEXCHARS.indexOf(encoded.charAt(i+1)) != -1 
					&& HEXCHARS.indexOf(encoded.charAt(i+2)) != -1 ) {
				plaintext += unescape( encoded.substr(i,3) );
				i += 3;
			} else {
				alert( 'Bad escape combination near ...' + encoded.substr(i) );
				plaintext += "%[ERROR]";
				i++;
			}
		} else {
		   plaintext += ch;
		   i++;
		}
	} // while
   //document.URLForm.F1.value = plaintext;
   return plaintext;
}//;

function filterText(input)
{
    var output = "";
    var char1;
    var i=0;
    
    for(i=0;i< input.length;i++)
    {
        char1 = input.charCodeAt(i);
        //alert(char1);
        if(char1 == 8212)
        {
            //long dash
           // alert("long");
            output += "-";
        }
        else
        if(char1 == 8220)
        {
            //fancy open quotes
           // alert("long");
            output += "\"";
        }
        else
        if(char1 == 8221)
        {
            //fancy closed quotes
            //alert("long");
            output += "\"";
        }
        else
        if(char1 == 8217)
        {
            //fancy single quote
            //alert("long");
            output += "'";
        }
        else
        if(char1 > 1000 )
        {
            //alert("ignoring char " +  input.charAt( i ));
            output += " ";
        }
        
        else
        {
            output += input.charAt( i );
        }
    }
    
    return output;
}


function encode64(input) {
// Base64 code from Tyler Akins -- http://rumkin.com
   var output = "";
   
  // if(input == "") return "";
   
   var lsKeyStr = this.keyStr;
   var chr1, chr2, chr3;
   var enc1, enc2, enc3, enc4;
   var i = 0;

   do {
      chr1 = input.charCodeAt(i++);
      chr2 = input.charCodeAt(i++);
      chr3 = input.charCodeAt(i++);

      enc1 = chr1 >> 2;
      enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
      enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
      enc4 = chr3 & 63;

      if (isNaN(chr2)) {
         enc3 = enc4 = 64;
      } else if (isNaN(chr3)) {
         enc4 = 64;
      }

      output = output + lsKeyStr.charAt(enc1) + lsKeyStr.charAt(enc2) + 
         lsKeyStr.charAt(enc3) + lsKeyStr.charAt(enc4);
   } while (i < input.length);
   
   
  // alert(input + " converted to " + output);
   
   return output;
}

function decode64(input) {
   var output = "";
   
 //  if(input == "") return "";
   
   var lsKeyStr = this.keyStr;
   var chr1, chr2, chr3;
   var enc1, enc2, enc3, enc4;
   var i = 0;

   // remove all characters that are not A-Z, a-z, 0-9, +, /, or =
   input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");

   do {
      enc1 = lsKeyStr.indexOf(input.charAt(i++));
      enc2 = lsKeyStr.indexOf(input.charAt(i++));
      enc3 = lsKeyStr.indexOf(input.charAt(i++));
      enc4 = lsKeyStr.indexOf(input.charAt(i++));

      chr1 = (enc1 << 2) | (enc2 >> 4);
      chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
      chr3 = ((enc3 & 3) << 6) | enc4;

      output = output + String.fromCharCode(chr1);

      if (enc3 != 64) {
         output = output + String.fromCharCode(chr2);
      }
      if (enc4 != 64) {
         output = output + String.fromCharCode(chr3);
      }
   } while (i < input.length);

   return output;
}	
function removeChildrenElements(parentElem)
{
    
    var i = 0;
    
    if(document.all)
    {
        var currentLength = parentElem.children.length;

        for (i=0; i<currentLength; i++)
	    {
		    parentElem.removeChild( parentElem.children[0] );
	    }
	}
	else
	{
	  for (i=0;i<parentElem.childNodes.length;i++)
	  {
            parentElem.removeChild(parentElem.childNodes[i] );
      }
	
	}
}
function hasChildrenElements(parentElem)
{

    var currentLength = 0;
    if(document.all)
    {
        currentLength= parentElem.children.length;
	}
	else
	{
	    currentLength = parentElem.childNodes.length;

	}

	if (currentLength == 0)
	    return false;
	else
	    return true;
	    
}
	function getSelect2(id,arrayDelimetedVals,callback)
	{
		var sel = document.createElement("SELECT");
		sel.id = id;
		var items = arrayDelimetedVals;
		
		if(callback != null)
		    sel.onchange = callback;

		for(i=0;i<items.length;i++)
		{
			if(document.all)
			{
			    //ie
			    var ooption = document.createElement("OPTION");
			    sel.options.add(ooption);
			    ooption.innerText = items[i];
			    ooption.value = i;
			}
			else
			{
			    //netscape
			    sel.options[i] = new Option(items[i],i + "");
			}
		}
		
		
		return sel;
	}	
	
	function getSelect3(id,arrayDelimetedVals,callback,selIndx,aClassName)
	{
		var sel = document.createElement("SELECT");
		sel.id = id;
		
		sel.className = aClassName;
		
		var items = arrayDelimetedVals;
		
		if(callback != null)
		    sel.onchange = callback;

		for(i=0;i<items.length;i++)
		{
			if(document.all)
			{
			    //ie
			    var ooption = document.createElement("OPTION");
			    sel.options.add(ooption);
			    ooption.innerText = items[i];
			    ooption.value = i;
			}
			else
			{
			    //netscape
			    sel.options[i] = new Option(items[i],i + "");
			}
			
			if(selIndx == i)
			{
			    //alert("sel @ " + i);
			    //sel.options[i].setAttribute("SELECTED","1");
			    sel.options[i].selected = true;
			}
		}
		
		
		return sel;
	}

	function getSelectColor(id, arrayVals,arrayTxt,arrayColors, callback, selIndx, aClassName) {
	    var sel = document.createElement("SELECT");
	    sel.id = id;
	    sel.className = aClassName;
	    var items = arrayVals;
	    if (callback != null) 
	        sel.onchange = callback;
	    

	    for (i = 0; i < items.length; i++) {
	        if (document.all) {
	            //ie
	            var ooption = document.createElement("OPTION");
	            sel.options.add(ooption);
	            ooption.innerText = arrayTxt[i];
	            ooption.value = items[i];
	            
	        }
	        else {
	            //netscape
	            sel.options[i] = new Option(arrayTxt[i], items[i]);
	        }

	        if (arrayColors != null) {
	            sel.options[i].style.color = arrayColors[i];
	        }
	        
	        if (selIndx == i) {
	            sel.options[i].selected = true;
	        }
	    }

	    return sel;
	}	
	
	
	
	function getCheckbox(id,title,bChecked,e)
	{
	    var chk = document.createElement("INPUT");
	    chk.type = "checkbox";
	    chk.id = id;
	    chk.name = id;
	    chk.title = title;
	    
	    if(e != null)
	        chk.onclick = e;
	    
	    if(bChecked)
	    {
	        chk.checked = true;
	       // alert("check pleeeze");
	       // chk.setAttribute("selected",true);
	        
	    }
	    
	    return chk;
	
	}
	
	function getSelect(pipeDelimetedVals, callback,id)
	{
		var sel = document.createElement("SELECT");
		var items = pipeDelimetedVals.split("|");
		
		if(callback != null)
		    sel.onchange = callback;
		    
		

		for(i=0;i<items.length;i++)
		{
			if(document.all)
			{
			    var ooption = document.createElement("OPTION");
			    sel.options.add(ooption);
			    ooption.innerText = items[i];
			    ooption.value = i;
			}
			else
			{
			    sel.options[i] = new Option(items[i],i + "");
			}
		}
		
		
		return sel;
	}
	
    function getTextArea(val,id,focusHandler,blurHandler,className)
	{
			var textArea = document.createElement("TEXTAREA");
			textArea.value = val;
			textArea.title = val;
			textArea.id = id;
			textArea.name = id;
			
			if(focusHandler != null)
				textArea.onfocus = focusHandler;
				
			if(blurHandler != null)
			{
				//textArea.onblur = blurHandler;
			        if(document.all)
			        {
			            //alert("da");
			            textArea.onblur = blurHandler;
                       // textArea.attachEvent("onblur",blurHandler);
                    }else{
                        //alert("other");
                        //textArea.addEventListener("blur",blurHandler,false);
                        // textArea.onBlur = blurHandler;
                    }
	
			}
				
		    if(className != null)
			    textArea.className = className;
			
			//textArea.style.overflow = "auto";
			return textArea;
	}
	
	function getInputBox(val,id,focusHandler,blurHandler,className,title)
	{
			var inputBox = document.createElement("INPUT");
			inputBox.value = val;
			
			if(title == null)
			    inputBox.title = val;
			else
			    inputBox.title = title;
			    
			inputBox.id = id;
			if (focusHandler != null) {
			    inputBox.onfocus = focusHandler;
			}
			if (blurHandler != null) {
			   
			    inputBox.onblur = blurHandler;
			}
			inputBox.className = className;
			return inputBox;
	}
	function getPassword(val,id,focusHandler,blurHandler,className,title)
	{
			var inputBox = document.createElement("INPUT");
			inputBox.type = "password";
			inputBox.value = val;
			
			if(title == null)
			    inputBox.title = val;
			else
			    inputBox.title = title;
			    
			inputBox.id = id;
			if(focusHandler != null)
			    inputBox.onfocus = focusHandler;
			if(blurHandler != null)
			    inputBox.onblur = blurHandler;
			inputBox.className = className;
			return inputBox;
	}	
	
	
	function getButton2(id,val,title,e,buttonStyle)
	{
		var button = document.createElement("INPUT");
		button.type = "button";
		button.value = val;
		button.title = title;
		button.id = id;
		button.onclick = e;
		
		
		if(buttonStyle == null) buttonStyle = "clsButton";
		button.className = buttonStyle;
		return button;
	}
	
	function callout()
	{
	    //call back function from button.
	   if(ns6)
	   {
	       //alert(this.id);
	        this.value="hah";
	   }
	   if(ie4)
	   {
	        //alert("IE");
	      
	        var v = window.event;
		    var srcElem = v.srcElement;
		    //alert("id " + srcElem.id);
		    srcElem.value="hah";
		
	        //srcElem.setAttribute("sty = "#000000";
	   }
	   
	   
	    
	}
	
	function findElement(key,elementTagName)
    {
        //seems to be ie specific????
        //var elem = document.all.item("divA");

        var tags = document.getElementsByTagName(elementTagName);
        
        for(var i=0;i<tags.length;i++)
        {
           //alert("found divs " + tags[i].id);
            if(tags[i].id == key)
            {
                return tags[i];
            }
        }
    }
    
    
    // grid that has to be bound to DOM
    
    function setGridCell(gridName,row,col,val)
    {
        //get the div by id
        var  cellKeyCode = gridName + ".gridCell." + row + "." + col;
        var gridDiv = this.findElement( cellKeyCode, "div" );
        gridDiv.appendChild( val );
    
    }
    
    function newGrid(gridName,numRows,numCols,attachPoint)
    {
    
        var grid = document.createElement("table");
        grid.id = gridName;
        
        attachPoint.appendChild(grid);  //early binding to ensure setGridCell can work
        
        var gridBody = document.createElement("tbody");
        var elementCounter = 0;
        var gridRowCurrent,gridCellCurrent,gridCellTextCurrent,cellCode,gridCellDiv;
        
        for(var j = 0; j < numRows; j++) {
            gridRowCurrent = document.createElement("tr");

            for(var i = 0; i < numCols; i++) {
                cellCode = j + "." + i; // + "." + elementCounter;
                elementCounter++;
                gridCellCurrent = document.createElement("td");
                gridCellDiv = document.createElement("div");
                gridCellDiv.id = gridName + ".gridCell." + cellCode;
                gridCellDiv.className = "clsGridCell";
                // creates a Text Node
               gridCellTextCurrent = document.createTextNode(gridCellDiv.id);
                // appends the Text Node we created into the cell <td>
               gridCellDiv.appendChild(gridCellTextCurrent);
               gridCellCurrent.appendChild(gridCellDiv);
                // appends the cell <td> into the row <tr>
                gridRowCurrent.appendChild(gridCellCurrent);
            }
            // appends the row <tr> into <tbody>
            gridBody.appendChild(gridRowCurrent);
        }

        // appends <tbody> into <table>
        grid.appendChild(gridBody);
       
        
        grid.setAttribute("border","8");
        
       // return grid;
    }
