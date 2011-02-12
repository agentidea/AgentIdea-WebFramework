/**

	custom commands

*/

cmdShowEvents = function(macro)	{
	var panel = macro.parameters[0].value;
	
	ClearBottomPanels();
	ClearMessages();
	
	var m = newMacro("ShowEvents");
	addParam(m,"panel",panel);
	processJSON(m);
	
	};
	
	
cmdShowNewTable = function(macro){
	  var panel = macro.parameters[0].value;
	  var oPanel = document.getElementById(panel);
	  if(oPanel != null){
	    ClearBottomPanels();
	    APP.tafelCreateForm(oPanel);
	  }
	  else{
	  	alert("no panel " + panel + " found");
	  }
	};
	
cmdProcessInvites = function(macro)
	{
		ClearBottomPanels();
		ClearMessages();
		
		var id = macro.parameters[0].value;
		var panel = macro.parameters[1].value;
		
		var m = newMacro("ProcessInvites");
		addParam(m,"panel",panel);
		addParam(m,"table_id",id);
		processJSON(m);
	
	};	
cmdEditEvent = function(macro)
	{
		var id = macro.parameters[0].value;
		var panel = macro.parameters[1].value;
		alert("to follow ... Edit event " + id + " here");
	
	};
		
cmdDeleteEvent = function(macro)
	{
		var id = macro.parameters[0].value;
		var panel = macro.parameters[1].value;
		var tableName=macro.parameters[2].value;
		
		var shouldDelete = confirm("Are you sure you want to delete table #" + tableName + "?");
		if(shouldDelete)
		{
			ClearBottomPanels();
			ClearMessages();
			
			var m = newMacro("DeleteEvent");
			addParam(m,"panel",panel);
			addParam(m,"table_id",id);
			processJSON(m);
		}
	
	};	