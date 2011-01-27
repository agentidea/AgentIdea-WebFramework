//
//   $to do:   convert to local commands
//


	

	ShowNavigation = function(panel)
	{
		var m = newMacro("ShowNavigation");
		addParam(m,"panel",panel);
		processJSON(m);

	};

	
	ShowEvents = function(panel)
	{
		ClearBottomPanels();
		ClearMessages();
		
		var m = newMacro("ShowEvents");
		addParam(m,"panel",panel);
		processJSON(m);
	
	};


	
	ShowAbout = function(panel)
	{
		ClearBottomPanels();
		ClearMessages();
		
		var m = newMacro("ShowAbout");
		addParam(m,"panel",panel);
		processJSON(m);
	
	};
	
	ProcessInvites = function(button, id,panel)
	{
		ClearBottomPanels();
		ClearMessages();

		var m = newMacro("ProcessInvites");
		addParam(m,"panel",panel);
		addParam(m,"table_id",id);
		processJSON(m);
	
	};
	
	
	EditEvent = function(button,id, panel)
	{
		alert("to follow ... Edit event " + id + " here");
	
	};
	DeleteEvent = function(button,id, panel, tableName)
	{
	
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