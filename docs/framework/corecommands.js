/**

	@description: core framework commands

*/

	cmdSetKontext = function(macro)
	{
		FWK.setKontext(macro.parameters[0].name,macro.parameters[0].value);
	};

	cmdIntialize = function(macro)
	{
	
		var m = newMacro("Initialize");
		var panel = macro.parameters[0].value;
		addParam(m,"panel",panel);
		processJSON(m);
	
	};
	
	cmdLocalLogin = function(macro)
	{
		log("local login");
		
		var m = newMacro("Authenticate");
		
		var panel = macro.parameters[0].value;
		var usr = document.getElementById("usr").value;
		var pwd = document.getElementById("pwd").value;
		
		addParam(m,"usr",TheUte().encode64(usr));
		addParam(m,"pwd",TheUte().encode64(pwd));
		addParam(m,"panel",panel);
		processJSON(m);
	
	};
	
	cmdShowNavigation = function(macro)
	{
		var m = newMacro("ShowNavigation");
		var panel = macro.parameters[0].value;
		addParam(m,"panel",panel);
		processJSON(m);

	};
	

	cmdShowAbout = function(macro)
	{
		log("session id: " +  FWK.kontext.SessionGUID );
		
		ClearBottomPanels();
		ClearMessages();
		var panel = macro.parameters[0].value;
		var m = newMacro("ShowAbout");
		addParam(m,"panel",panel);
		processJSON(m);
	};

function cmdAlertAndRefresh(macro)
{
   cmdAlert(macro);
   location.href = location.href;  //refresh!

}

function cmdAlert(macro)
{
   var msg64 = getParameterVal("msg",macro);
   var msg = TheUte().URLDecode(msg64);
   msg =  TheUte().decode64(msg);
   
   
   var msgDiv = document.getElementById('dvMessage');
   if(msgDiv != null)
   {
   		msgDiv.style.display = "block";
   		msgDiv.innerHTML = msg;
   
   }
   else
   {
   		alert(msg);
   }
   
}

function cmdDisplayLog(macro)
{
	var panel = macro.parameters[0].value;
	var lines = macro.parameters[1].value;
	
	
	log("in local command, about to request log " + lines + " details to paint to " + panel);
	
	var m = newMacro("ShowRemoteLog");
	addParam(m,"panel",panel);
	addParam(m,"lines",lines);
	//addParam(m,"file","pyLog.txt");
	processJSON(m);
	
	
	var TexAreaLog = document.getElementById("TexAreaLog");
	
	try {
		//sroll to more or less the end of the text area
		TexAreaLog.scrollTop = ( TexAreaLog.scrollHeight + TexAreaLog.clientHeight ) * 2;
	}
	catch(scrollingError) {
		log("log window scrolling error :: " + scrollingError.description);
	}


		

}

function cmdRemoveRemoteLog(macro)
{
	var go = confirm("This action cannot be undone.  Backup? Proceed?");
	if(go) {
		var panel = macro.parameters[0].value;
		var m = newMacro("RemoveRemoteLog");
		addParam(m,"panel",panel);
		//addParam(m,"file","pyLog.txt");
		processJSON(m);
	} else {
		log("Action Undone");
	}
}


/**
* @description: clear xWindow
*/

function cmdClearXwindow(macro)
{
	var _idX = macro.parameters[0].value;
	var dvToClearId = "window" + _idX.pull('x');
	var dvToClear = document.getElementById(dvToClearId);
	//$to do: this seems not to clear the window entirely ... could be a div nesting issue
	//TheUte().removeChildren(dvToClear);
	dvToClear.innerHTML = "";
	
}


function cmdDisplay(macro)
{

  var panel =  getParameterVal("panel",macro);
  var html64 =  getParameterVal("html64",macro);
  
  var h = TheUte().URLDecode(html64);
  var hs =  TheUte().decode64(h);

  //?put hooks here to floating free form div orientation x,y,z?
  
  var oPanel = document.getElementById(panel);
  if(oPanel != null)
  {
    log("cmdDisplay(" + panel + ")" );
  	oPanel.innerHTML = hs;
  }
  else
  {
  	alert("no panel " + panel + " found");
  }

}

function cmdDisplayWindowTitle(macro)
{
	  
    var html64 =  getParameterVal("html64",macro);

    var h = TheUte().URLDecode(html64);
    var hs =  TheUte().decode64(h);
	
	document.title = hs;

}


function cmdLoadAppSpecificJS(macro)
{

	var J64 = getParameterVal("JSON64",macro);
	var moduleToPass = getParameterVal("JSmoduleToCall",macro);
	var panel =  getParameterVal("panel",macro);
    var oPanel = document.getElementById(panel);
    
  	if(oPanel != null)
  	{
  		var j =   TheUte().URLDecode(J64);
    	var js =  TheUte().decode64(j);
    
  		var tableObj = eval('(' + js + ')');
  		
  		//var expression = "(" + moduleToPass + "(\"" + J64 + "\"," + oPanel + "); )" ;
  		var expression = moduleToPass + "(tableObj,oPanel);";
  		//log("");
    	//log("about to eval() expression [" + expression + "]");
    	//log("");
    	eval(expression);
    	
    	
  
  	}
}
