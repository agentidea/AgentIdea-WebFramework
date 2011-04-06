/**
	@description: core framework commands refactored to use Module pattern
*/

var CMDS = (function (commands) {
	
	commands = commands||{};
	//var commands = {};

	commands.cmdSetKontext = function(macro) {
		FWK.setKontext(macro.parameters[0].name,macro.parameters[0].value);
	};

	commands.cmdIntialize = function(macro) {
		console.log("in Init");
		var m = newMacro("Initialize");
		var panel = macro.parameters[0].value;
		addParam(m,"panel",panel);
		processJSON(m);
	};
	
	commands.cmdSignout = function(macro) {
		ClearBottomPanels();
		ClearMessages();
		WriteToPanel('farwest','');
		var m = newMacro("Signout");
		processJSON(m);
	};
	
	commands.cmdProcCommandLine = function(macro) {
		var TxtID = macro.parameters[0].value;
		
		var txtBox = document.getElementById(TxtID);
		
		if(txtBox != null){
			if(txtBox.value.trim().length > 0) {
				log("ECHO " + txtBox.value);
				
				//parse line into command
				
				// line = command + param1 + param2 ... paramN
				// command = word
				// param = word | quoted phrase
				// word = a-z |0-9
				// quoted phrase = quote + word + quote
				// quote = " | ' 
			}
			else
			{
				txtBox.value = "listusers *";
			}
			
			txtBox.focus();
		}
	};
	
	commands.cmdLocalLogin = function(macro) {
		var m = newMacro("Authenticate");
		var panel = macro.parameters[0].value;
		var usr = document.getElementById("txtUsr");
		var pwd = document.getElementById("txtPwd");
		
		if(usr.value.trim().length == 0) {
			displayMsg("username may not be blank",msgCode.warn);
			usr.focus();
			return;
		}
		
		if(pwd.value.trim().length == 0) {
		displayMsg("password may not be blank",msgCode.warn);
			pwd.focus();
			return;
		}
		
		var enc = hex_md5(pwd.value);
		
		//log("password encrypted for transmittal ... [" + enc + "]");
		
		addParam(m,"usr",TheUte().encode64(usr.value));
		addParam(m,"pwd",TheUte().encode64(enc));
		addParam(m,"panel",panel);
		processJSON(m);
	};
	
	commands.cmdShowNavigation = function(macro) {
		ClearBottomPanels();
		ClearMessages();
		var m = newMacro("ShowNavigation");
		var panel = macro.parameters[0].value;
		addParam(m,"panel",panel);
		processJSON(m);
	};
	
	commands.cmdShowHelp = function(macro) {
		ClearBottomPanels();
		ClearMessages();
		var panel = macro.parameters[0].value;
		var m = newMacro("ShowHelp");
		addParam(m,"panel",panel);
		processJSON(m);

	};

    	commands.cmdShowSupport = function(macro) {
		ClearBottomPanels();
		ClearMessages();
		var panel = macro.parameters[0].value;
		var m = newMacro("ShowSupport");
		addParam(m,"panel",panel);
		processJSON(m);

	};	

	commands.cmdShowAdmin = function(macro) {
		//ClearBottomPanels();
		ClearMessages();
		var m = newMacro("CommandsReflect");
		var panel = macro.parameters[0].value;
		addParam(m,"panel",panel);
		processJSON(m);
	};
	
	commands.cmdPasswd = function(macro) {
		var txtUsername = macro.parameters[0].value;
		var txtPwdOld = macro.parameters[1].value;
		var txtPwdNew = macro.parameters[2].value;
		var txtPwdConfirm = macro.parameters[3].value;
		
		//retrieve text box values
		username = document.getElementById(txtUsername).value;
		oldpassword= document.getElementById(txtPwdOld).value;
		newpassword = document.getElementById(txtPwdNew).value;
		newpasswordConfirm = document.getElementById(txtPwdConfirm).value;
		
		
		if(username.trim().length == 0) { displayMsg("Username may not be blank",msgCode.warn); return;}
		if(oldpassword.trim().length == 0) { displayMsg("Old Password may not be blank",msgCode.warn);  return;}
		if(newpassword.trim().length == 0) { displayMsg("New Password may not be blank",msgCode.warn);  return;}
		if(newpasswordConfirm.trim().length == 0) { displayMsg("New Password Confirm may not be blank",msgCode.warn);  return;}
		
		if(newpassword.trim() == newpasswordConfirm.trim() ) {

			var m= newMacro("Passwd");
			addParam(m,"username",username);
			addParam(m,"oldPassword",hex_md5(oldpassword));
			addParam(m,"newPassword",hex_md5(newpassword));
			addParam(m,"newPasswordConfirm",hex_md5(newpasswordConfirm));
			processJSON(m);
		}
		else
		{
			displayMsg("passwords did not match",msgCode.warn);
		}
	};
	
	commands.cmdShowPwdReset = function(macro) {
		ClearBottomPanels();
		ClearMessages();
		var m = newMacro("ShowPwdReset");
		var panel = macro.parameters[0].value;
		addParam(m,"panel",panel);
		processJSON(m);
	};
	
	commands.cmdShowConsole = function(macro) {
		ClearBottomPanels();
		ClearMessages();
		var m = newMacro("ShowCommandLine");
		var panel = macro.parameters[0].value;
		addParam(m,"panel",panel);
		processJSON(m);
	};
	
	commands.cmdShowToc = function(macro) {
		ClearBottomPanels();
		ClearMessages();
		var m = newMacro("ShowToc");
		var what = macro.parameters[0].value;
		var panel = macro.parameters[1].value;
		var orientation = macro.parameters[2].value;
		addParam(m,"what",what);
		addParam(m,"panel",panel);
		addParam(m,"orientation",orientation);
		processJSON(m);
	};

	commands.cmdShowAbout = function(macro) {
		//log("session id: " +  FWK.kontext.SessionGUID );
		
		//ClearBottomPanels();
		ClearMessages();
		var panel = macro.parameters[0].value;
		var m = newMacro("ShowAbout");
		addParam(m,"panel",panel);
		processJSON(m);
	};

	commands.cmdAlertAndRefresh = function(macro) {
	   cmdAlert(macro);
	   location.href = location.href;  //refresh!
	}

	commands.cmdAlert = function(macro) {
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

	commands.cmdDisplayLog = function(macro) {
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

	commands.cmdRemoveRemoteLog = function(macro) {
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

	commands.cmdClearXwindow = function(macro) {
		var _idX = macro.parameters[0].value;
		var dvToClearId = "window" + _idX.pull('x');
		var dvToClear = document.getElementById(dvToClearId);
		//$to do: this seems not to clear the window entirely ... could be a div nesting issue
		//TheUte().removeChildren(dvToClear);
		dvToClear.innerHTML = "";
	}

	commands.cmdDisplay = function(macro) {

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
	};

	commands.cmdDisplayWindowTitle = function(macro) {
	    var html64 =  getParameterVal("html64",macro);
	    var h = TheUte().URLDecode(html64);
	    var hs =  TheUte().decode64(h);
	    document.title = hs;
	}

	commands.cmdLoadAppSpecificJS = function(macro) {
		var J64 = getParameterVal("JSON64",macro);
		var moduleToPass = getParameterVal("JSmoduleToCall",macro);
		var panel =  getParameterVal("panel",macro);
	    	var oPanel = document.getElementById(panel);
	    
		if(oPanel != null) {
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

 	return commands;

}(CMDS));
