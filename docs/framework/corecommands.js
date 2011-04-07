/**
	@description: core framework commands 
	@authors: Grant Steinfeld, Oren Kredo
	@changeHistory: refactored to use Module pattern
					added command specifications.
	
*/

var CMDS = (function (commands) {
	
	commands = commands||{};
	
	
	
	commands.specSetKontext = { 
							'name':'SetKontext',
							'description':'set a browser based session variable',
							'params':[
								{'name':'panel','req':1,'type':'unicode','seq':0}
							]};
							
	commands.cmdSetKontext = function(macro) {
		FWK.setKontext(macro.parameters[0].name,macro.parameters[0].value);
	};


	commands.specIntialize = { 
							'name':'Intialize',
							'description':'application intialization; often the Main() entry point ...',
							'params':[
								{'name':'panel','req':1,'type':'unicode','seq':0}
							]};
							
	commands.cmdIntialize = function(macro) {
		var m = newMacro("Initialize");
		var panel = macro.parameters[0].value;
		addParam(m,"panel",panel);
		processJSON(m);
	};
	
	
	commands.specSignout = { 
							'name':'Signout',
							'description':'logout of this application',
							'params':[]};
							
	commands.cmdSignout = function(macro) {
		ClearBottomPanels();
		ClearMessages();
		WriteToPanel('farwest','');
		var m = newMacro("Signout");
		processJSON(m);
	};
	
	
	commands.specProcCommandLine = { 
							'name':'ProcCommandLine',
							'description':'process command line driven macro command',
							'params':[
								{'name':'CommandLineTextBoxID','req':1,'type':'unicode','seq':0}
							]};
							
	commands.cmdProcCommandLine = function(macro) {
		var TxtID = macro.parameters[0].value;
		
		var txtBox = document.getElementById(TxtID);
		
		if(txtBox != null){
			if(txtBox.value.trim().length > 0) {
				log("ECHO " + txtBox.value);
				
				//parse line into command
				// pass onto the remote PLY mechanism
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
	
	
	commands.specShowLocalCommands = { 
							'name':'ShowLocalCommands',
							'description':'reflect over local JavaScript Command specifications',
							'params':[
								{'name':'panel','req':1,'type':'unicode','seq':0}
							]};
							
	commands.cmdShowLocalCommands = function(macro){
		
		
		var panel = macro.parameters[0].value;
		var html = "";
		
		html += "<table class='clsCMDtable'>";
		
		var obj;
		for( obj in CMDS) {
			
		        if(obj.startsWith("spec")){   
				      
					  
					  //console.log("spec == " +                  obj.pull("spec")); 
					  
					  var specString = "var commandSpec = CMDS." + obj + ";";
					  console.log(specString);
					  
					  eval ( specString )
					  
					  if(commandSpec) {
					  	
							html += "<tr>";
					  	
							html += "<td><div class='clsCMDname'>";
							
							html += commandSpec.name;
							
							html += "</div></td>";
							
							html += "<td><div class='clsCMDdescription'>";
							
							html += commandSpec.description;
							
							html += "</div></td>";
							
							html += "</tr><tr>"
							
							
							html += "<td  colspan='2'>";
							
								html += "<div class='clsCMDparams'><table border='0'><tr>";
								for( param in commandSpec.params)
								{
									html += "<td><div class='clsCMDparam'>";
									html += commandSpec.params[param].name;
									html += "</div></td>";
									
								}
								html += "</tr></table></div>";
							
							html += "</td>";
						
						
							html += "</tr>";
						
					  }
					  
					  
				}  
						  
						  
				//if(obj.startsWith("cmd")){ 
				        //console.log("command == " +                  obj.pull("cmd"));  
						   //}  
						   
						   
						   
		 }
		 
		 html += "</table>";
		
		
		 var dvPanel = document.getElementById(panel);
		 
		 dvPanel.innerHTML = html;
		 
		 
	};
	
	
	
	
	commands.specLocalLogin = { 
							'name':'LocalLogin',
							'description':'login to this application',
							'params':[
								{'name':'panel','req':1,'type':'unicode','seq':0}
							]};
							
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
		
		//hash password out of clear text
		var enc = hex_md5(pwd.value);

		addParam(m,"usr",TheUte().encode64(usr.value));
		addParam(m,"pwd",TheUte().encode64(enc));
		addParam(m,"panel",panel);
		processJSON(m);
	};
	
	
	commands.specShowAbout = { 
							'name':'ShowNavigation',
							'description':'Show navigation',
							'params':[
								{'name':'panel','req':1,'type':'unicode','seq':0}
							]};
							
	commands.cmdShowNavigation = function(macro) {
		ClearBottomPanels();
		ClearMessages();
		var m = newMacro("ShowNavigation");
		var panel = macro.parameters[0].value;
		addParam(m,"panel",panel);
		processJSON(m);
	};
	
	
	commands.specShowHelp = { 
							'name':'ShowHelp',
							'description':'Show help associated with this application',
							'params':[
								{'name':'panel','req':1,'type':'unicode','seq':0}
							]};
							
	commands.cmdShowHelp = function(macro) {
		ClearBottomPanels();
		ClearMessages();
		var panel = macro.parameters[0].value;
		var m = newMacro("ShowHelp");
		addParam(m,"panel",panel);
		processJSON(m);

	};


	commands.specShowSupport = { 
							'name':'ShowSupport',
							'description':'Show help associated with this application',
							'params':[
								{'name':'panel','req':1,'type':'unicode','seq':0}
							]};
							
    	commands.cmdShowSupport = function(macro) {
		ClearBottomPanels();
		ClearMessages();
		var panel = macro.parameters[0].value;
		var m = newMacro("ShowSupport");
		addParam(m,"panel",panel);
		processJSON(m);

	};	


	commands.specShowAdmin = { 
							'name':'ShowAdmin',
							'description':'Show administration panel for this application',
							'params':[
								{'name':'panel','req':1,'type':'unicode','seq':0}
							]};
	commands.cmdShowAdmin = function(macro) {
		//ClearBottomPanels();
		ClearMessages();
		var m = newMacro("CommandsReflect");
		var panel = macro.parameters[0].value;
		addParam(m,"panel",panel);
		processJSON(m);
	};
	
	
	commands.specPasswd = { 
							'name':'Passwd',
							'description':'change user passowrd, passes credentials md5 encoded',
							'params':[
								{'name':'usernameTXT','req':1,'type':'unicode','seq':0},
								{'name':'pwdOldTXT','req':1,'type':'unicode','seq':1},
								{'name':'pwdNewTXT','req':1,'type':'unicode','seq':2},
								{'name':'pwdConfirmTXT','req':1,'type':'unicode','seq':3}
								
							]};
							
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
	
	
	commands.specShowPwdReset = { 
							'name':'ShowPwdReset ',
							'description':'Show password reset screen',
							'params':[
								{'name':'panel','req':1,'type':'unicode','seq':0}
							]};
	commands.cmdShowPwdReset = function(macro) {
		ClearBottomPanels();
		ClearMessages();
		var m = newMacro("ShowPwdReset");
		var panel = macro.parameters[0].value;
		addParam(m,"panel",panel);
		processJSON(m);
	};
	
	
	commands.specShowConsole = { 
							'name':'ShowConsole',
							'description':'Show console',
							'params':[
								{'name':'panel','req':1,'type':'unicode','seq':0}
							]};
	commands.cmdShowConsole = function(macro) {
		ClearBottomPanels();
		ClearMessages();
		var m = newMacro("ShowCommandLine");
		var panel = macro.parameters[0].value;
		addParam(m,"panel",panel);
		processJSON(m);
	};
	
	
	commands.specShowToc = { 
							'name':'ShowToc',
							'description':'Show table of contents for this application',
							'params':[
								{'name':'panel','req':1,'type':'unicode','seq':0}
							]};
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



	commands.specShowAbout = { 
							'name':'ShowAbout',
							'description':'Show information about this application',
							'params':[
								{'name':'panel','req':1,'type':'unicode','seq':0}
							]};

	commands.cmdShowAbout = function(macro) {

		ClearMessages();
		var panel = macro.parameters[0].value;
		var m = newMacro("ShowAbout");
		addParam(m,"panel",panel);
		processJSON(m);
	};

	//commands.cmdAlertAndRefresh = function(macro) {
	//   cmdAlert(macro);
	//   location.href = location.href;  //refresh!
	//};

	commands.specAlert = { 
							'name':'Alert',
							'description':'display alert dialog',
							'params':[
								{'name':'msg','req':1,'type':'base64','seq':0}
							]};
							
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
	};


	commands.specDisplayLog = { 
							'name':'DisplayLog',
							'description':'Tail Server Log',
							'params':[
								{'name':'panel','req':1,'type':'unicode','seq':0},
								{'name':'lines','description':'number of lines to tail','req':1,'type':'int','seq':1}
							]};
							
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
	};


	commands.specRemoveRemoteLog = { 
							'name':'RemoveRemoteLog',
							'description':'Remove Server Log',
							'params':[
								{'name':'panel','req':1,'type':'unicode','seq':0}
							]};
							
	commands.cmdRemoveRemoteLog = function(macro) {
		var go = confirm("This action cannot be undone.  Backup? Proceed?");
		if(go) {
			var panel = macro.parameters[0].value;
			var m = newMacro("RemoveRemoteLog");
			addParam(m,"panel",panel);
			processJSON(m);
		} else {
			log("Action Undone");
		}
	};




	commands.specClearXwindow = { 
							'name':'ClearXwindow',
							'params':[
								{'name':'dvToClear','req':1,'type':'unicode','seq':0}
							]};


	commands.cmdClearXwindow = function(macro) {
		var _idX = macro.parameters[0].value;
		var dvToClearId = "window" + _idX.pull('x');
		var dvToClear = document.getElementById(dvToClearId);
		//$to do: this seems not to clear the window entirely ... could be a div nesting issue
		//TheUte().removeChildren(dvToClear);
		dvToClear.innerHTML = "";
	};


	
	
	commands.specDisplay = { 
							'name':'Display',
							'params':[
								{'name':'panel','req':1,'type':'unicode'},
								{'name':'html64','req':1,'type':'base64'}
							]};

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


	commands.specDisplayWindowTitle = { 
							'name':'DisplayWindowTitle',
							'params':[
								{'name':'html64','req':1,'type':'unicode','seq':0}
							]};
							
	commands.cmdDisplayWindowTitle = function(macro) {
	    var html64 =  getParameterVal("html64",macro);
	    var h = TheUte().URLDecode(html64);
	    var hs =  TheUte().decode64(h);
	    document.title = hs;
	};


	commands.specLoadAppSpecificJS = { 
							'name':'LoadAppSpecificJS',
							'params':[
								{'name':'JSON64','req':1,'type':'unicode','seq':0},
								{'name':'JSmoduleToCall','req':1,'type':'unicode','seq':1},
								{'name':'panel','req':1,'type':'unicode','seq':2}
							]};
							
	commands.cmdLoadAppSpecificJS = function(macro) {
		var J64 = getParameterVal("JSON64",macro);
		var moduleToPass = getParameterVal("JSmoduleToCall",macro);
		var panel =  getParameterVal("panel",macro);
	    var oPanel = document.getElementById(panel);
	    
		if(oPanel != null) {
			var j =   TheUte().URLDecode(J64);
			var js =  TheUte().decode64(j);
			var tableObj = eval('(' + js + ')');
			//$to do: add try/catch
			var expression = moduleToPass + "(tableObj,oPanel);";
			eval(expression);
		}
	};

 	return commands;

}(CMDS));
