//
//   $to do:   convert to local commands
//


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
	
	};

	ShowNavigation = function(panel)
	{
		var m = newMacro("ShowNavigation");
		addParam(m,"panel",panel);
		processJSON(m);

	};
	
	ShowEvents = function(panel)
	{
		ClearBottomPanels();
		
		var m = newMacro("ShowEvents");
		addParam(m,"panel",panel);
		processJSON(m);
	
	};


	
	ShowAbout = function(panel)
	{
		ClearBottomPanels();
		
		var m = newMacro("ShowAbout");
		addParam(m,"panel",panel);
		processJSON(m);
	
	};
	
	ProcessInvites = function(button, panel)
	{
		ClearBottomPanels();
		
		log(panel);
		log(button.id);
		
		var m = newMacro("ProcessInvites");
		addParam(m,"panel",panel);
		addParam(m,"table_id",button.id);
		processJSON(m);
	
	};
	
	
	
	DeleteEvent = function(button, panel)
	{
		log("Delete event " + button.id);
	
	};