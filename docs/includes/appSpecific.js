/*

	app specific components

*/

var TABLE = {

	'tableNumber':-1,
	'name':'',
	'description':null,
	'location':{
		'name':null,
		'street':null,
		'street2':null,
		'zip':null,
		'state':null,
		'city':null,
		'country':null,
		'url':null
	},
	'date':null,
	'time':null,
	'hosts':[],
	'guests':[]

};


var UserStates = {
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


var User = {

	firstName:"",
	lastName:"",
	middleName:"",
	email:"",
	state:0

};





function validate(userList)
{

	for ( user in userList )
	{
		var tmpUser = userList[user];
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
			//to do validate email ....
		
		}
	
	}
	
	return true;


}

function UserCreateForm(attachPoint,user,list)
{
	var _user = user;
	var dvUser = document.createElement("DIV");
	
	var _txtOrdinal = document.createTextNode(list.length);
	var _lblOrdinal = document.createElement("DIV");
	_lblOrdinal.className = 'clsOrdinal';
	
	_lblOrdinal.appendChild(_txtOrdinal);
	
	var _txtFirstName= TheUte().getInputBox('','txtFirstName',null,null,'clsInput','First Name');
	var _lblFirstName = document.createTextNode('First Name');
	
	var _txtLastName= TheUte().getInputBox('','txtLastName',null,null,'clsInput','Last Name');
	var _lblLastName = document.createTextNode('Last Name');
	
	var _txtEmail= TheUte().getInputBox('','txtEmail',null,null,'clsInput','Email Address');
	var _lblEmail = document.createTextNode('Email');
	
	
	_txtFirstName.onblur = function()
	{
		user.firstName = this.value;
	};
	_txtLastName.onblur = function()
	{
		user.lastName = this.value;
	};
	_txtEmail.onblur = function()
	{
		user.email = this.value;
	};
	
	
	
	var _cxlCmd = TheUte().getButton("cmdDelete","remove","delete this user",null,"clsActionButton");
	
	_cxlCmd.onclick = function () {
	
		user.state = UserStates.deleted;
		//dvUser.style.display = "none";
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
	
}





function ShowNewTableForm(panel)
{


  var oPanel = document.getElementById(panel);
  if(oPanel != null)
  {
    ClearBottomPanels();
    
    TableCreateForm(oPanel);
  }
  else
  {
  	alert("no panel " + panel + " found");
  }


}


function TableCreateForm(attachPoint)
{

	//var tmpTable = Object.create(TABLE);
	var tmpTable = TABLE;
    
    var _lblPageHeader = document.createTextNode('Create New Event');
    var _dvPageHeader = document.createElement('DIV');
    _dvPageHeader.className = 'clsPageHeader';
    _dvPageHeader.appendChild(_lblPageHeader);
    
    
	var _txtTableLocation = TheUte().getInputBox('','txtTableLocation',null,null,'clsInput','location');
	_txtTableLocation.onblur = function()
	{
		tmpTable.location.name = this.value;
	};
	
	var _txtTableStreet = TheUte().getInputBox('','txtTableStreet',null,null,'clsInput','street');
	_txtTableStreet.onblur = function()
	{
		tmpTable.location.street = this.value;
	
	};
	var _txtTableStreet2 = TheUte().getInputBox('','txtTableStreet2',null,null,'clsInput','street 2');
	_txtTableStreet2.onblur = function()
	{
		tmpTable.location.street2 = this.value;
	
	};
	
	var _txtTableCity = TheUte().getInputBox('','txtTableCity',null,null,'clsInput','city');
	_txtTableCity.onblur = function()
	{
		tmpTable.location.city = this.value;
	
	};
	var _txtTableState = TheUte().getInputBox('','txtTableState',null,null,'clsInput','state');
	_txtTableState.onblur = function()
	{
		tmpTable.location.state = this.value;
	
	};
	var _txtTableZip = TheUte().getInputBox('','txtTableZip',null,null,'clsInput','zip/postal code');
	_txtTableZip.onblur = function()
	{
		tmpTable.location.zip = this.value;
	
	};
	var _txtTableCountry = TheUte().getInputBox('','txtTableCountry',null,null,'clsInput','country');
	_txtTableCountry.onblur = function()
	{
		tmpTable.location.country = this.value;
	
	};
	var _txtTableURL = TheUte().getInputBox('','txtTableURL',null,null,'clsInput','event location website');
	_txtTableURL.onblur = function()
	{
		tmpTable.location.url = this.value;
	
	};
	
	var _txtTableDate = TheUte().getInputBox('','txtTableDate',null,null,'clsInput','date');
	_txtTableDate.onblur = function()
	{
		tmpTable.date = this.value;
	
	};
	
	var _txtTableTime = TheUte().getInputBox('','txtTableTime',null,null,'clsInput','time');
	_txtTableTime.onblur = function()
	{
		tmpTable.time = this.value;
	
	};
	
	var _txtTableDescription  = TheUte().getTextArea('','txtTableDescription',null,null,'clsTextArea');
	_txtTableDescription.onblur = function()
	{
		tmpTable.description = this.value;
	
	};
	
	
	var _saveCmd = TheUte().getButton("cmdSave","save","save this event",null,"clsActionButton");
	
	_saveCmd.onclick = function()
	{
	
		//reflect through form and get as JSON;
		var tableJSON = JSON.stringify(tmpTable);
		
		// $to do:  validate table form here 
		
		
		if( (validate(tmpTable.hosts) == true) &&  (validate(tmpTable.guests) == true) )
		{
			log("passed validation, save ...");
			log(tableJSON);
			
			var tableJSON64 = TheUte().encode64( tableJSON );
			
			var SaveNewEvent = newMacro("SaveNewEvent");
			addParam(SaveNewEvent,"table64",tableJSON64);
			addParam(SaveNewEvent,"panel",attachPoint.id);
			processJSON(SaveNewEvent);

		}
		else
		{
			alert("Please check host/guest information for missing data");
		}
		
		
		//log(tableJSON);
		
	
	};
	
	var _dvTableLocation = document.createElement('DIV');
	
	var _lblTableLocation = document.createTextNode('location');
	var _lblTableStreet = document.createTextNode('street');
	var _lblTableStreet2 = document.createTextNode('street 2');
	
	var _lblTableCity = document.createTextNode('city');
	var _lblTableState = document.createTextNode('state');
	var _lblTableCountry = document.createTextNode('country');
	
	var _lblTableDate = document.createTextNode('date');
	var _lblTableTime = document.createTextNode('time');
	var _lblTableDescription = document.createTextNode('description');
	
	
	var _dvHosts = document.createElement('DIV');
	_dvHosts.className = 'clsPanelHead';
	var _dvGuests = document.createElement('DIV');
	_dvGuests.className = 'clsPanelHead';
	
	var _lblHosts = document.createTextNode('hosts');
	var _lblGuests = document.createTextNode('guests');
	
	var spanAddHost = document.createElement('SPAN');
	spanAddHost.className = 'clsAdd';
	var lblAddHost = document.createTextNode('+');
	spanAddHost.appendChild(lblAddHost);
	
	_dvHosts.appendChild(spanAddHost);
	_dvHosts.appendChild(_lblHosts);
	
	spanAddHost.onclick = function()
	{
		var tmpUser = Object.create(User);
		tmpUser.state = UserStates.host;
		tmpTable.hosts.push(tmpUser);
		UserCreateForm(_dvHosts,tmpUser,tmpTable.hosts);
	};
	

	var spanAddGuest = document.createElement('SPAN');
	var lblAddGuest = document.createTextNode('+');
	spanAddGuest.appendChild(lblAddGuest);
	spanAddGuest.className = 'clsAdd';
	
	_dvGuests.appendChild(spanAddGuest);
	_dvGuests.appendChild(_lblGuests);
	spanAddGuest.onclick = function()
	{
		var tmpUser = Object.create(User);
		tmpUser.state = UserStates.init;
		tmpTable.guests.push(tmpUser);
		UserCreateForm(_dvGuests,tmpUser,tmpTable.guests);
	};

	var vals = new Array();
	
	vals.push(_dvPageHeader);
	vals.push(null);
	
	vals.push(_dvTableLocation.appendChild(_lblTableLocation));
	vals.push(_txtTableLocation);
	
	vals.push( _lblTableDescription );
	vals.push( _txtTableDescription );
	
	vals.push( _lblTableDate );
	vals.push( _txtTableDate );
	vals.push( _lblTableTime );
	vals.push( _txtTableTime );
	
	
	vals.push( _lblTableStreet );
	vals.push( _txtTableStreet );	
	vals.push( _lblTableStreet2 );
	vals.push( _txtTableStreet2 );	
	
	vals.push( document.createTextNode("city") );
	vals.push( _txtTableCity);
	vals.push( document.createTextNode("state") );
	vals.push( _txtTableState);
	vals.push( document.createTextNode("zip") );
	vals.push( _txtTableZip);
	vals.push( document.createTextNode("country") );
	vals.push( _txtTableCountry);
	
	



	
	vals.push( _dvHosts );
	vals.push( _dvGuests );

	vals.push( null);
	vals.push(_saveCmd);

	var g = newGrid2('tableCreationGrid',vals.length/2,2,vals);
	g.init(g);

	attachPoint.appendChild( g.gridTable );
	
	_txtTableLocation.focus();
}





function InviteMx(objTable, attachPoint)
{

	

	
	log("processing invites for table# " + objTable.tableNumber);
	
	
	
	var s = "Dear {guest.firstName} ";
	s += " \r\n\r\n";
	s += " Please attend table #" + objTable.tableNumber;
	s += " at " + objTable.location.name;
	s += "\r\n";
	s += " in city " + objTable.location.city;
	s += "\r\n\r\n";
	s += " Thanks! ";
	s += "\r\n";
	for(host in objTable.hosts)
	{
		s += " " + objTable.hosts[host].firstName;
		s += " & ";
		
	}
	
	//remove last &
	
	var _txtInvite  = TheUte().getTextArea(s,'txtInvite',null,null,'clsTextArea');
	_txtInvite.className = "clsInvite";
	
	var lblInvite = document.createTextNode("invite");
	
	var vals = [];
	vals.push( lblInvite );
	vals.push( _txtInvite  );

	vals.push( null);
	
	var _sendCmd = TheUte().getButton("cmdSave","send all","send invites to all",null,"clsActionButton");
	
	_sendCmd.onclick = function()
	{
		log("sending invites");
	}
	vals.push(_sendCmd);

	var g = newGrid2('inviteGrid',vals.length/2,2,vals);
	g.init(g);

	attachPoint.appendChild( g.gridTable );
	


}