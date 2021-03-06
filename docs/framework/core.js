/**

	@description: core framework Javascript

*/

var FWK;			//framework global


var xmlHttpLocal = null;
var SYNC = false;
//var gDisableAJAXcalls = false;
//var bCallBusyLock = false;

if(!FWK){
	FWK = {
		 
		 kontext: {},
		 getKontext: function(key){ return this.kontext[key]; },
		 setKontext: function(key,val){
		 
		 	this.kontext[key] = val;
		 	log("setting kontext " +key + "::" + val);
		 
		 },
		 pressNav: function(pattern,dv,clsUnpressed) {
		 
		 	//reset all buttons to original 
		    var counter = 0;
		    while(true){
		    
		    	counter += 1;
		    	var otherButtonTmp = document.getElementById(pattern + "" + counter);
		    	if(otherButtonTmp == null) {
		    		break;
		    	} else {
		    		otherButtonTmp.className = clsUnpressed;
		    	}
		    
		    }
		    
		    dv.className = clsUnpressed + 'Pressed';
		    
		 
		 
		 },
		 say: function() {
		 
			 /**
			 *	@description: runs local command via simple JS function call
			 *
			 *  @example: FWK.say("<<command name>>",p1,'p2',this,objJS, ... , Nth);
			 *
			 *	@man: say takes a textual command as first(0) argument
			 *  	  subsequent arguments (1 - N) are treated as parameters
			 *        target commands need to be aware of position, or ask for
			 *        parameters with the 'arg_1','arg_2' ... this is a problem? 
			 *        Would need command mapping data ... hmmm command metadata ... was in 
			 *        directory server once, not a bad idea $to do:
			 *
			 *  @author: Grant Steinfeld
			 *  @created: 2/2/2011
			 *  @lastmodified: 2/2/2011
			 *
			 *  			
			 *		               
			 */
			 
			 var commandName = null;
			 
			 var i;
			 var argLen = arguments.length;
			 
			 log(argLen);
			 
			 if(argLen > 0)
			 {
			 	commandName = arguments[0];
			 	
			 	var m = newMacro(commandName);
	
			 	for(i=1;i<argLen; i += 1) {
			 		addParam(m,"arg_" + i,arguments[i]);
			 	}
			 
			 	executeLocalCommand(this, m);
	
			 }	
		 	
	     },
		 id:"AgentIdea Framework"};

}


function xmlHttp_callback() 
{ 
    try
    {
        //readyState of 4 or 'complete' represents 
        //that data has been returned 
        if ( xmlHttpLocal.readyState == 4 || 
            xmlHttpLocal.readyState == 'complete' )
        {
            var response = xmlHttpLocal.responseText; 
            if (response.length > 0)
            {
                //log(response);
                processResponse(response);
                
            } 
        }
    }
    catch(e)
    {
        //smell fix this?
       log(" callback error: " + e.description + " \r\n\r\n RESP: " + response , "red");
       // var json = getJSONoffXML(response);
       // alert("JSON WAS " + json);
    }
    
    bCallBusyLock = false;
}

var msgCode = {

	high: { color : "red", background : "white" },
	warn: { color : "yellow", background : "black" },
	error: { color : "red", background : "black" },
	normal: { color : "black", background : "white" },
	info: { color : "blue", background : "white" }

};

function displayMsg(s,severity)
{
	//expects optional severity object like msgCode.warn
	if(!severity){ severity = msgCode.normal; }

	if(s == null) s = "";
	
 	var dvMessage =  TheUte().findElement("dvMessage","div");
    if(dvMessage != null)
    {
        dvMessage.innerHTML = s + "<br />";
        
        if(severity != null)
        {
        	dvMessage.style.backgroundColor = severity.background;
        	dvMessage.style.color = severity.color;
        }
        else
        {
        	dvMessage.style.backgroundColor = "transparent";
        	dvMessage.style.color = "transparent";
        
        }
    }
}

	clearLocalLog = function()
	{
		var divLog       =  TheUte().findElement("divLog","div");
		divLog.innerHTML = "-------------------------------------------------------------";
	
	};
	
	toggleLog = function(o)
	{
		var logDiv = document.getElementById("divLogWindow");
		
		if(logDiv.style.display == "none")
		{
			logDiv.style.display = "block";
			//o.value = "hide debug";
			log("logging on");
		}
		else
		{
			logDiv.style.display = "none";
			//o.value = "show debug";
			log("logging off");
		}
			
	};
	
	ClearMessages = function(){
	
		displayMsg("");
	
	};
	
	WriteToPanel = function(panel,s)
	{
	  var oPanel = document.getElementById(panel);
	  if(oPanel != null)
	  {
	  	oPanel.innerHTML = s;
	  }
	
	};
	
	ClearBottomPanels = function()
	{
		WriteToPanel('north','');
		WriteToPanel('south','');
		WriteToPanel('east','');
		WriteToPanel('west','');
		WriteToPanel('center','');
	
	};
	





function log(s,color)
{
		var divLogWindow =  TheUte().findElement("divLogWindow","div");
		var divLog       =  TheUte().findElement("divLog","div");
		
		if(divLogWindow.style.display == "block") { 		//only log if log window is open
			//alert(s);
		    if(divLog != null)
		    {
		        divLog.innerHTML = s + "<br />" + divLog.innerHTML;
		        if(color != null)
		        	divLog.style.backgroundColor = color;
		    }
		    
	    }
    
   
    
}

function trace(s)
{
 var divLog =  TheUte().findElement("divLog","div");
    if(divLog != null)
        divLog.innerHTML += s;    

}

function processResponse(res)
{

     var resMacros = null;
     try
     { 
        resMacros = eval('(' + res + ')');
        //resMacros = eval(res);
        // log("JSON response RECEIVED was this <<" + res + ">> ",'blue');
     }
     catch(e)
     {
       //$to do: understand what the error was.
       log("RESPONSE eval() error :: " + e.description , 'black');
       log("JSON response RECEIVED was this <<" + res + ">> ");
       
       if( res.indexOf('unable to connect to MongoDB') != -1)
       {
       		displayMsg("Server Error, MongoDB is not running nor reachable",msgCode.error);
       }
       
       return;
       
     }
	 
	 
     var i = 0;
     for ( i = 0 ;i<resMacros.commands.length;i++)
     {
        executeLocalCommand( this, resMacros.commands[i] );
     }
}

procTimeout = function(){
//process local timeout
	    var sessionTimeoutMinutes = FWK.getKontext("sessionTimeoutMinutes");
	    if(sessionTimeoutMinutes)
	    {
	    	if(sessionTimeoutMinutes > 0)
	    	{
	    		var lastActive = FWK.getKontext("lastActive");
	    		
	    		if(lastActive) {
	    			var now = new Date();
	    			var nowT = now.getTime();
	    			var lastT = lastActive.getTime();
	    			
	    			var difTms = nowT - lastT;
	    			var difTsec = difTms / 1000;
	    			var sessionTimeoutSeconds = sessionTimeoutMinutes * 60;
	    			
	    			log(difTsec + " :: " + sessionTimeoutSeconds);
	    			
	    			
	    			if( difTsec > sessionTimeoutSeconds )
	    			{
	    				alert("Your session has timed out. \r\n\r\n You will be re-directed to the login screen");
	    				location.href = location.href;
	    				return true;

	    			}  
	    			
	    		}
	    		
	    		FWK.setKontext("lastActive",new Date());
	    	}
	    }
	    
	    return false;
	};



function executeLocalCommand(scope, macro)
{

	if(procTimeout()) { return; }

	//
	// PRE JS command
	//
/*	
    try {
    
    	var preJS = TheUte().unravel(macro.preJS64);
    	eval(preJS);
    	
    } catch(exp) {
    	if(preJS !== undefined) {
    	    
    		log("WARN: In command ["+ macro.name +"]There could a problem with the PreJavascript " + exp.description);
    		log("preJavaScript[" + preJS + "]");
    	}
    	
    }
 */   
    
    //var s = "cmd" + macro.name + "(macro);";
    var s = "CMDS.cmd" + macro.name;
    //log("LOCAL :: eval(" + s + ")" );
    log("LOCAL :: runCommand(" + s + ")" );
    
    //$to do: what if the eval fails ... there is no inspection of the JS objects here ...
    // if commands were part of a namespace, like CMD.showThisAndThat(macro); it would be possible to reflect hasOwnProperty();
    
    var fnPtr = eval(s);
    runCommand(scope, fnPtr(macro));
    
    log("LOCAL Command: " + s);
    
    //
    // POST JS command
    //
   
/* 
     try {
    
    	var postJS = TheUte().unravel(macro.postJS64);
    	eval(postJS);
    	
    } catch(exp) {
    	if(postJS !== undefined) {
    	    
    		log("WARN: In command ["+ macro.name +"]There could a problem with the PostJavascript " + exp.description);
    		log("postJavaScript[" + postJS + "]");
    	}
    	
    }
*/   
    
}


function processJSON(macro)
{
	//PYTHON PEER
	
	
	 //if(bCallBusyLock == true || gDisableAJAXcalls == true)
	 //   {
	         //$to do: why are some browsers re-entrant and others not????
	         // Firefox is ...
	        // processJSON(macro);
	       // log(macro.name + " was re-entrant");
	        //return;
	   // }
	     
	    if(procTimeout()) { return; }

	   // bCallBusyLock = true;
	    
	    xmlHttpLocal = getXMLHTTP();
	    
	    
	    //package macro into outward bound itinerary
	    
	    var itinerary = new Itinerary(FWK.kontext);
	    itinerary.inCommands.push(macro);
	    
	    var jsonString = JSON.stringify(itinerary);
	   	   
	    if (xmlHttpLocal!=null)
	    {
	        try {
	
	        
	           log("Posting to " + url);
	            
	            //xmlHttpLocal.onreadystatechange=state_Change;
	            xmlHttpLocal.open("POST",url,SYNC);
	            xmlHttpLocal.setRequestHeader("Accept","text/xml");
	            xmlHttpLocal.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
	
				log("REQ " + jsonString);
				//log("");
				
	            jsonString = TheUte().encode64(jsonString);
	            
	            //alert("posting " + jsonString);
	            
	            xmlHttpLocal.send(jsonString);
	        }
	        catch(exp)
	        {
	            alert("XMLHTTP COM error " + exp.description);
	            //gDisableAJAXcalls = true;
	        }
	     
	    }
	    else
	    {
	        alert("Your browser seems to be unable to support XMLHTTP");
    }

}


function processRequestAsString(macro)
{
	//build request string
	var req = url
	req += macro.name;
	req += "%20";
	
	//alert(req);
	
	for(var i = 0;i<macro.parameters.length;i++)
	{
		req += macro.parameters[i].value;
		req += "%20"
	}
	
	xmlHttpLocal = getXMLHTTP();
	
	if (xmlHttpLocal!=null)
	{
		try {
			log("GET request to " + req);
			xmlHttpLocal.open("GET",req,true);
			xmlHttpLocal.send();
		}
		catch(exp)
		{
			alert("XMLHTTP COM STRING error " + exp.description);
			gDisableAJAXcalls = 1;
		}

	}
	else
	{
		alert("Your browser seems to be unable to support XMLHTTP");
	}

	

}

function processRequest(macro)
{
	//.NET PEER
	
    if(bCallBusyLock == true || gDisableAJAXcalls == 1)
    {
         //$to do: why are some browsers re-entrant and others not????
        return;
    }
     
     
    bCallBusyLock = true;
    
    xmlHttpLocal = getXMLHTTP();
    //VAr macroTxt = serializeMacroForRequest(macro);
   
    if (xmlHttpLocal!=null)
    {
        try {

        
           alert("posting to " + url);
            
            //xmlHttpLocal.onreadystatechange=state_Change;
            xmlHttpLocal.open("POST",url,SYNC);
            xmlHttpLocal.setRequestHeader("Accept","text/xml");
            xmlHttpLocal.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
           //xmlHttpLocal.setRequestHeader("SOAPAction","''");
           // xmlHttpLocal.setRequestHeader("Cache-Control","no-cache");

            
            //alert("before encoding  \r\n\r\n" + macroTxt);
            //log("ajax request: \r\n\r\n" + macroTxt);

            macroTxt = TheUte().encode64(macroTxt);
            macroTxt = TheUte().URLEncode(macroTxt);
            
            xmlHttpLocal.send("serializedMacro=" + macroTxt);
        }
        catch(exp)
        {
            alert("XMLHTTP COM error " + exp.description);
            gDisableAJAXcalls = 1;
        }
     
    }
    else
    {
        alert("Your browser seems to be unable to support XMLHTTP");
    }
    
    
}


function getJSONoffXML(text)
{
        
    //.NET PEER seems like a string truncate could work equall well here
    //substring off<?xml ...?><string></string>
    //slippery, what is xml def changes!!!! unlikely?
    var jsonMid = text.substring(93,(text.length-9));
    return jsonMid;

}

function getXMLHTTP()
{

   var xmlHttp2 = null;

   if (window.ActiveXObject)
   {
            //all windows ActiveX broser shall use MSXML ( IE7 and later )
            //alert("MSXL capable");
            // ...otherwise, use the ActiveX control for IE5.x and IE6
            xmlHttp2 = GetMSXmlHttp();
            xmlHttp2.onreadystatechange = xmlHttp_callback;
  } 
  else
  if (window.XMLHttpRequest)
  {
    
        //alert(" native XMLHTTP ... ");
        // If , Mozilla, Safari, etc: Use native object
        xmlHttp2 = new XMLHttpRequest();
        xmlHttp2.onload = xmlHttp_callback;
        xmlHttp2.onerror = xmlHttp_callback;

        
    }
    else
    {
        alert("FATAL ERROR :: unrecognized xmlHTTP unsupported by this browser");
    }

    return xmlHttp2;
}

function CreateXmlHttp(clsid)
{
    var xmlHttp = null;
    try
    {
        xmlHttp = new ActiveXObject(clsid);
        lastclsid = clsid;
        return xmlHttp;
    }
    catch(e) 
    {}

}
function GetMSXmlHttp()
{
//"Msxml2.DOMDocument.3.0","Msxml2.DOMDocument.6.0",
    var xmlHttp = null;
    var clsids = ["Msxml2.XMLHTTP.6.0",
    "Msxml2.XMLHTTP.4.0",
    "Msxml2.XMLHTTP.3.0",
    "MSXML2.XMLHTTP" ];
    
    for(var i=0; i<clsids.length && xmlHttp == null; i++)
    {
        xmlHttp = CreateXmlHttp(clsids[i]);
    }
    
    if(xmlHttp == null) alert("unable to create MSXML.XMLHTTP");
    
    return xmlHttp;
}






function getParameterVal(key,macro)
{
    var res = null;
    
    for( var i =0;i<macro.paramCount;i++)
    {
        if(macro.parameters[i].name == key)
        {
            res = macro.parameters[i].value;
            break;
        }
    }
    
    return res;
}

function assembleMacro(name)
{
    log("about to assemble " + name);
    var m = newMacro(name);
  
    //check through form elements to see if there are indeed macro elements bound to the DOM
    var unFiltered = document.getElementsByTagName('*');
    var s = "";
    var tagName = null;
    var tag = null;
    var parameterCount = 0;
    
    for(var i=0;i<unFiltered.length;i++)
    {
        tag = unFiltered[i];
        tagName = tag.tagName;

        if(tagName == "INPUT" || tagName == "TEXTAREA")
        {
            if(tag.id != null && tag.id.indexOf("m_") != -1)
            {
                addParam(m,tag.id.split('_')[1],tag.value);
                parameterCount++;
                
                //alert("INPUT Parameter name :: " + p.name + " :: val " + p.value );
            }
        }
    }
    m.paramCount = parameterCount;
    return m;
}

function serializeMacroForRequest(passedMacro)
{

    /*
    <?xml version="1.0" encoding="utf-8"?>
<Macro xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
parameterCount="1" xmlns="http://tempuri.org/">
  <Parameters>
    <Parameter>
      <Val>hello </Val>
      <Name>msg</Name>
    </Parameter>
  </Parameters>
  <Name>DisplayAlert</Name>
</Macro>

    */
    var s = "";
    
    s += "<Macro ";
    s += " xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' ";
    s += " xmlns:xsd='http://www.w3.org/2001/XMLSchema' parameterCount='"+passedMacro.parameters.length+"'>";
    
    s += "<Name>";
    s += passedMacro.name
    s += "</Name>";
    s += "<UserCurrentTxID>";
    s += passedMacro.UserCurrentTxID
    s += "</UserCurrentTxID>";    
    
    
    s += "<Parameters>";
    for(var i = 0;i<passedMacro.parameters.length;i++)
    {
        s+= "<Parameter>";
        s+= "<Name>";
        s += passedMacro.parameters[i].name;
        s+= "</Name>";
        s+= "<Val>";
        s += passedMacro.parameters[i].value;
        s+= "</Val>";
        s+= "</Parameter>";
    
    }
    s += "</Parameters>";
    s += "</Macro>";

    return s;
}



function newMacro(name)
{
	
    var m = new macro();
    m.name = name;
    if( typeof gUserCurrentTxID != "undefined")  //HORRIBLE dependency from realtime updating idea
    {
        if(gUserCurrentTxID != null)
        {
        
            m.UserCurrentTxID = gUserCurrentTxID;
        }
     }

    return m;
}

function addParam( m, name, val )
{
    var param = new parameter();
    param.name = name;
    param.value = val;
    
    m.parameters.push(param);
}

function Itinerary(aKontext){

	var _kontext = aKontext;
	this.kontext = _kontext
	
	var _inCommands = [];
	var _outCommands = [];

	this.inCommands = _inCommands;
	this.outCommands = _outCommands;

}



function macro()
{
   var _name = null;
   this.name = _name;
   var _paramCount = 0;
   this.paramCount = _paramCount;
   var _parameters = []; //new Array();
   this.parameters = _parameters;
   var _UserCurrentTxID = "not_set_yet";
   this.UserCurrentTxID = _UserCurrentTxID;

}

function parameter()
{
   var _name = null;
   this.name = _name;
   var _val = null;
   this.value = _val;
}



// some core functions for logging etc

var statusBarRef = null;
var historyDivRef = null;
var xyRef = null;


function status(msg)
{
    history(msg);
}


function logMsg(msg)
{
    var logDiv = document.getElementById("LogDiv");
    if(logDiv != null)
    {
        logDiv.style.display="block";
        logDiv.innerHTML = "<p>" + msg + "</p>" + logDiv.innerHTML;
    
    }

}

 /**
  *  @description: runs local commands without use of eval() 
  *
  *  @created: 3/31/2011
  *                             
  */
var runCommand = function (scope, method, overrideArguments){
 return function(){
	 var args = (overrideArguments)?overrideArguments:arguments;
	 return method.apply(scope, args);
 }
};


