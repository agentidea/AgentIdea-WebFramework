var tafel;
var APP;
var UserStates;
var User;

if(!tafel){
	tafel = {
		'tableNumber':-1,
		'location':{
			'venue':null,
			'street':null,
			'street2':null,
			'zip':null,
			'state':null,
			'city':null,
			'country':null,
			'url':null
		},
		'meta':{
			'date':null,
			'time':null,
			'description':null
		},
		'hosts':[],
		'guests':[]
	
	};
}

if(!UserStates){
 	UserStates = {
    "raw":0,
	"init":1,
	"validated":2,
	"invited":3,
	"accepted":4,
	"unsure":5,
	"declined":6,
	"nocall":7,
	"host":8,
	"deleted":9

	};
}

if(!User) {
	User = {

	firstName:"",
	lastName:"",
	middleName:"",
	email:"",
	state:0
	};
}

if(!APP) {
	APP = {
	
			
			inviteMx: function(objTable, attachPoint)
			{

				log("processing invites for table# " + objTable.tableNumber);

				var s = " Dear {guest.firstName}, ";
				s += " \r\n\r\n";
				s += " You are invited to attend table #" + objTable.tableNumber;
				
				s += " at " + objTable.location.venue;
				
				s += "\r\n";
				
				
				if( objTable.location.url != null )
				{
					s += " \r\n";
					s += " Table venue website is ";
					s += objTable.location.url;
					s += " \r\n";
					s += " \r\n";
				}
				
				s += " on " + objTable.meta.date;
				s += "  at " + objTable.meta.time;
				s += "\r\n";
				
				
				
				s += "\r\n";
				s += " The address is," 
				s += "\r\n";
				s += "\t" + objTable.location.street;
				s += "\r\n";
				s += "\t" + objTable.location.street2;
				s += "\r\n";
				s += "\t" + objTable.location.city;
				s += "\r\n";
				s += "\t" + objTable.location.state;
				
				s += ", " + objTable.location.zip;
				s += "\r\n";
				s += "\t" + objTable.location.country;
				s += "\r\n";
				s += "\r\n";
				s += " We look forward to seeing you there";
				
				s += "\r\n\r\n";
				s += "Thanks! ";
				s += "\r\n";
				for(host in objTable.hosts)
				{
					s += " " + objTable.hosts[host].firstName;
					s += " &";
					
				}
				
				//remove last &
				s = s.trim();
				s = s.substring(0,s.length-1);
				
				var _txtInvite  = TheUte().getTextArea(s,'txtInvite',null,null,'clsTextArea');
				_txtInvite.className = "clsInvite";
				_txtInvite.title = "";
				
				var lblInvite = document.createTextNode("Invitation Template:");
				
				var vals = [];
				vals.push( lblInvite );
				vals.push(null);
				vals.push( _txtInvite  );
			
				vals.push( null);
				
				var sendCmd = TheUte().getButton("cmdSend","send invite to all","send invites to all",null,"clsActionButton");
				
				sendCmd.onclick = function()
				{
					alert("to do: sending invites to all");
				}
				
				var cmdSendIndividually = TheUte().getButton("cmdSendIndividually","send invite individually","send invites to all",null,"clsActionButton");
				
				cmdSendIndividually.onclick = function()
				{
					alert("to do: sending one by one, with option to modify message for each guest ...");
				}
				
				vals.push(sendCmd);
				vals.push(cmdSendIndividually);
			
				var g = newGrid2('inviteGrid',vals.length,1,vals);
				g.init(g);
			
				attachPoint.appendChild( g.gridTable );
				
			
			
			},
	
			showNewTableForm: function(panel){
			
			  var oPanel = document.getElementById(panel);
			  if(oPanel != null){
			    ClearBottomPanels();
			    this.tafelCreateForm(oPanel);
			  }
			  else{
			  	alert("no panel " + panel + " found");
			  }
			},
	
			validateUsers: function(userList)
			{
				
				
				/*
				var l = [1,2,3,4,770];
				
				var add = function(a,b)
				{
					return a + b;
				
				}
				
				var sum = l.reduce(add,0);
				log(sum);
				*/
				
				
				var lenUsers = userList.length;
				if( lenUsers == 0) {
					return false;
				}
				
				for ( var i=0; i < lenUsers; i+= 1 )
				{
					var tmpUser = userList[i];
					
					if( tmpUser != null)
					{
					
						if( tmpUser.state == UserStates.deleted ) continue;
						
						if(tmpUser.firstName.trim().length == 0)
						{
							return false;
						}
						if( tmpUser.lastName.trim().length == 0)
						{
							return false;
						}
						if( tmpUser.email.trim().length == 0)
						{
							return false;
						}
						else
						{
							//to do validInputBox email ....
						
						}
						
					}	

				}
				
				return true;
				
				
			},
			validateTableForm: function(){
			
				ClearMessages();
				
				//var locationExcludeList = ['street2','url']; 
				var locationExcludeList = new Array();
				locationExcludeList.push('street2');
				locationExcludeList.push('url');
				
			    var _inputBoxes = document.getElementsByTagName("input");
				var lenInputs = _inputBoxes.length;
				var i = 0;
				for( i = 0; i < lenInputs; i += 1) {
				
					if( _inputBoxes[i].id.startsWith("txtLocation")) {

						var key = _inputBoxes[i].id.pullRest("txtLocation").toLowerCase();
						
						if( _inputBoxes[i].value.trim().length == 0) {
						
							if(locationExcludeList.has(key) == true) {
								log("optional field, so do nothing");
								continue;
							}
							else{
							
								displayMsg(key + " required",msgCode.warn);
							 	_inputBoxes[i].focus();
								return false;
							}
							
						}
					}
					else {
						if( _inputBoxes[i].id.startsWith("txtMeta")) {
	
							var key = _inputBoxes[i].id.pullRest("txtMeta").toLowerCase();
							if( _inputBoxes[i].value.trim().length == 0){
							 displayMsg(key + " required",msgCode.warn);
							 _inputBoxes[i].focus();
							 return false;
							}
						}
					}
				}
				return true;
			
			},
			populateTable: function(t){
				
				var _inputBoxes = document.getElementsByTagName("input");
				var lenInputs = _inputBoxes.length;
				var i = 0;
				for( i = 0; i < lenInputs; i += 1) {
				
					if( _inputBoxes[i].id.startsWith("txtLocation")) {

						var key = _inputBoxes[i].id.pullRest("txtLocation").toLowerCase();
						t['location'][key] = _inputBoxes[i].value;
					}
					else {
						if( _inputBoxes[i].id.startsWith("txtMeta")) {
	
							var key = _inputBoxes[i].id.pullRest("txtMeta").toLowerCase();
							t['meta'][key] = _inputBoxes[i].value;
						}
					}
				}
			},
			resetTable: function(t)
			{
				t.tableNumber = -1;
				t.description = null;
				t.location.venue = null;
				t.location.street = null;
				t.location.street2 = null;
				t.location.zip = null;
				t.location.state = null;
				t.location.city = null;
				t.location.url = null;
				t.date = null;
				t.time = null;
				t.hosts = [];
				t.guests = [];
				
				log("reset table");
			
			},
			userCreateForm: function(attachPoint,user,list){
				var _user = user;
				var dvUser = document.createElement("DIV");
				
				var _txtOrdinal = document.createTextNode(list.length);
				var _lblOrdinal = document.createElement("DIV");
				_lblOrdinal.className = 'clsOrdinal';
				
				_lblOrdinal.appendChild(_txtOrdinal);
				
				var _txtFirstName= TheUte().getInputBox('','txtUserFirstName',null,null,'clsInput','First Name');
				var _lblFirstName = document.createTextNode('First Name');
				
				var _txtLastName= TheUte().getInputBox('','txtUserLastName',null,null,'clsInput','Last Name');
				var _lblLastName = document.createTextNode('Last Name');
				
				var _txtEmail= TheUte().getInputBox('','txtUserEmail',null,null,'clsInput','Email Address');
				var _lblEmail = document.createTextNode('Email');
				
				
				_txtFirstName.onblur = function(){
					_user.firstName = this.value;
				};
				_txtLastName.onblur = function(){
					_user.lastName = this.value;
				};
				_txtEmail.onblur = function(){
					_user.email = this.value;
				};
			
				var _cxlCmd = TheUte().getButton("cmdDelete","remove","delete this user",null,"clsActionButton");
				_cxlCmd.onclick = function () {
				
					user.state = UserStates.deleted;
					TheUte().removeChildren(dvUser);
				};
				
				
				var vals = new Array();
				vals.push(null);vals.push(_lblOrdinal);
				vals.push(_lblFirstName);
				vals.push(_txtFirstName);
				vals.push(_lblLastName);
				vals.push(_txtLastName);
				vals.push(_lblEmail);
				vals.push(_txtEmail);
				vals.push(null);
				vals.push(_cxlCmd);
				
				var g = newGrid2('newUserGrid',vals.length/2,2,vals);
				g.init(g);
				
				
				dvUser.className = 'clsCell';
				dvUser.appendChild( g.gridTable );
				attachPoint.appendChild( dvUser  );
				
				
			},
			tafelCreateForm: function(attachPoint)
			{

			    var _lblPageHeader = document.createTextNode('Create New Table');
			    var _dvPageHeader = document.createElement('DIV');
			    _dvPageHeader.className = 'clsPageHeader';
			    _dvPageHeader.appendChild(_lblPageHeader);
			    
			    
				var _txtTableLocation = TheUte().getInputBox('','txtLocationVenue',null,null,'clsInput','venue');
				var _txtTableStreet = TheUte().getInputBox('','txtLocationStreet',null,null,'clsInput','street');
				var _txtTableStreet2 = TheUte().getInputBox('','txtLocationStreet2',null,null,'clsInput','OPTIONAL street 2');
				var _txtTableCity = TheUte().getInputBox('','txtLocationCity',null,null,'clsInput','city');
				var _txtTableState = TheUte().getInputBox('','txtLocationState',null,null,'clsInput','state');
				var _txtTableZip = TheUte().getInputBox('','txtLocationZip',null,null,'clsInput','zip/postal code');
				var _txtTableCountry = TheUte().getInputBox('','txtLocationCountry',null,null,'clsInput','country');
				var _txtTableURL = TheUte().getInputBox('','txtLocationURL',null,null,'clsInput','OPTIONAL event location website URL');
				var _txtTableDate = TheUte().getInputBox('','txtMetaDate',null,null,'clsInput','date');
				var _txtTableTime = TheUte().getInputBox('','txtMetaTime',null,null,'clsInput','time');
				var _txtTableDescription  = TheUte().getTextArea('','txtTableDescription',null,null,'clsTextArea');
				var _saveCmd = TheUte().getButton("cmdSave","save table","save this table",null,"clsActionButton");
				var _cancelCmd = TheUte().getButton("cmdCancel","cancel","cancel out of this screen",null,"clsActionButton");
				
				
				_cancelCmd.onclick = function()
				{
					APP.resetTable(tafel);
					location.href = location.href;
				};
				
				
				_saveCmd.onclick = function()
				{
				
				
					if( APP.validateTableForm() == true)
					{
						if( ( APP.validateUsers( tafel.hosts ))
							&&  ( APP.validateUsers( tafel.guests )) )
						{
							
							APP.populateTable(tafel);
							
							var tableJSON = JSON.stringify(tafel);
							var tableJSON64 = TheUte().encode64( tableJSON );
		
							log(tableJSON);
							
							APP.resetTable(tafel);
							displayMsg("");
							
							var SaveNewEvent = newMacro("SaveNewEvent");
							addParam(SaveNewEvent,"table64",tableJSON64);
							addParam(SaveNewEvent,"panel",attachPoint.id);
							processJSON(SaveNewEvent);
							
						}
						else
						{
							displayMsg("Please fill out all guest/host information",msgCode.warn);
						}
					}
					else
					{
						log("form did not validate correctly");
					}
					
				};
				
				var _dvTableLocation = document.createElement('DIV');
				var _lblTableLocation = document.createTextNode('venue');
				var _lblTableStreet = document.createTextNode('street');
				var _lblTableStreet2 = document.createTextNode('street 2');
				var _lblTableURL = document.createTextNode('web site');
				
				var _lblTableCity = document.createTextNode('city');
				var _lblTableState = document.createTextNode('state');
				var _lblTableZip = document.createTextNode('zip');
				var _lblTableCountry = document.createTextNode('country');
				
				var _lblTableDate = document.createTextNode('date');
				var _lblTableTime = document.createTextNode('time');
				var _lblTableDescription = document.createTextNode('description');
				
				
				var _dvHosts = document.createElement('DIV');
				_dvHosts.className = 'clsPanelHead';
				var _dvGuests = document.createElement('DIV');
				_dvGuests.className = 'clsPanelHead';
				
				var _lblHosts = document.createTextNode('Hosts');
				var _lblGuests = document.createTextNode('Guests');
				var dvLblHosts = document.createElement("DIV");
				var dvLblGuests = document.createElement("DIV");
				dvLblHosts.className = "clsH5";
				dvLblGuests.className = "clsH5";
				dvLblHosts.title = "click here to add a new host";
				dvLblGuests.title = "click here to add a new guest";
				
				
				var spanAddHost = document.createElement('SPAN');
				spanAddHost.className = 'clsAdd';
				var lblAddHost = document.createTextNode('add a new host');
				spanAddHost.appendChild(lblAddHost);
				
				dvLblHosts.appendChild(spanAddHost);
				_dvHosts.appendChild(dvLblHosts);
				_dvHosts.appendChild(_lblHosts);
				
				spanAddHost.onclick = function()
				{
					var tmpUser = Object.create(User);
					tmpUser.state = UserStates.host;
					tafel.hosts.push(tmpUser);
					APP.userCreateForm(_dvHosts,tmpUser,tafel.hosts);
				};
				
			
				var spanAddGuest = document.createElement('SPAN');
				var lblAddGuest = document.createTextNode('add a new guest');
				spanAddGuest.appendChild(lblAddGuest);
				spanAddGuest.className = 'clsAdd';
				
				dvLblGuests.appendChild(spanAddGuest);
				_dvGuests.appendChild(dvLblGuests);
				_dvGuests.appendChild(_lblGuests);
				spanAddGuest.onclick = function()
				{
					var tmpUser = Object.create(User);
					tmpUser.state = UserStates.init;
					tafel.guests.push(tmpUser);
					APP.userCreateForm(_dvGuests,tmpUser,tafel.guests);
				};
				
			
				//
				// add form elements to a html grid
				//
				
				var vals = new Array();
				vals.push(_dvPageHeader);
				vals.push(null);
				vals.push(_dvTableLocation.appendChild(_lblTableLocation));
				vals.push(_txtTableLocation);
				//vals.push( _lblTableDescription );
				//vals.push( _txtTableDescription );
				
				vals.push( _lblTableStreet );
				vals.push( _txtTableStreet );	
				vals.push( _lblTableStreet2 );
				vals.push( _txtTableStreet2 );	
				vals.push( _lblTableCity );
				vals.push( _txtTableCity);
				vals.push( _lblTableState );
				vals.push( _txtTableState);
				vals.push( _lblTableZip );
				vals.push( _txtTableZip);
				vals.push( _lblTableCountry );
				vals.push( _txtTableCountry );
				vals.push( _lblTableURL );
				vals.push( _txtTableURL );
				
				vals.push( _lblTableDate );
				vals.push( _txtTableDate );
				vals.push( _lblTableTime );
				vals.push( _txtTableTime );
				vals.push( _dvHosts );
				vals.push( _dvGuests );
				vals.push( _cancelCmd );
				vals.push(_saveCmd);
				var g = newGrid2('tableCreationGrid',vals.length/2,2,vals,0);
				g.init(g);
			
				attachPoint.appendChild( g.gridTable );
				
			
				
				_txtTableLocation.focus();
			}
						
	
	};
}