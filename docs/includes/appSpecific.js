/*

	app specific components

*/




// DECLARE global TABLE
var gTABLE;
if(!gTABLE){
	var gTABLE = {
		'tableNumber':-1,
		'description':null,
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
		'date':null,
		'time':null,
		'hosts':[],
		'guests':[]
	
	};
}


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


function resetTable(t)
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

}

function validateTable(t)
{

	if(t.location.venue == null || t.location.venue.trim().length == 0)
	{
		return "venue required";
	}
	if(t.date == null || t.date.trim().length == 0)
	{
		return "date required";
	}
	
	if(t.time == null || t.time.trim().length == 0)
	{
		return "time required";
	}
	
	if(t.location.street == null || t.location.street.trim().length == 0)
	{
		return "street required";
	}

	if(t.location.city == null || t.location.city.trim().length == 0)
	{
		return "city required";
	}
	
	if(t.location.state == null || t.location.state.trim().length == 0)
	{
		return "state or region required";
	}
	
	if(t.location.zip == null || t.location.zip.trim().length == 0)
	{
		return "zip or postal code required";
	}
	
	if(t.location.zip == null || t.location.zip.trim().length == 0)
	{
		return "country required";
	}

	
	if(t.hosts.length == 0)
	{
		return "table requires at least one host";
	}
	
	if(t.guest.length == 0)
	{
		return "table requires at least one guest";
	}

	return "";

}

function validateUsers(userList)
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
			//to do validInputBox email ....
		
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


function validInputBox( inputBox, warnMsg)
{

		var val = inputBox.value.trim();
		
		if(val.length > 0)
		{
			
			//inputBox.className = 'clsCellValid'; 
			inputBox.style.backgroundColor = "#ffffff";
			displayMsg();
			return true;
		}
		else
		{
			
		    //inputBox.className = 'clsCellInvalid'; 
			displayMsg(warnMsg, msgCode.warn);
			
			//inputBox.focus();  //causes endless loop when focusing into another cell that requires validateion!!!
			inputBox.style.backgroundColor = "#ffcc99";
			return false;
		}
}

function TableCreateForm(attachPoint)
{

    
    var _lblPageHeader = document.createTextNode('Create New Event');
    var _dvPageHeader = document.createElement('DIV');
    _dvPageHeader.className = 'clsPageHeader';
    _dvPageHeader.appendChild(_lblPageHeader);
    
    
	var _txtTableLocation = TheUte().getInputBox('','txtTableLocation',null,null,'clsInput','venue');
	
	/*
	_txtTableLocation.onblur = function()
	{
		if( validInputBox( _txtTableLocation,'location field is required, please enter a valid string') )
		{
			gTABLE.location.venue = _txtTableLocation.value;
			log("setting to :" + gTABLE.location.venue );
		}
	};

		('location','venue','venue field is required')
		
		
		*/
		
	if( typeof _txtTableLocation.addEventListener != 'function') {
		//ie
		(function(ttt){
			
			ttt.attachEvent('onblur', function(){
				 
				if( validInputBox( ttt,'venue field is required, please enter a valid string') )
				{
					gTABLE['location']['venue'] = ttt.value;
				}
				
				}, false);
			
		})(_txtTableLocation);
		
	
	}
	else {
		//mozilla
		(function(ttt){
			
			ttt.addEventListener('blur', function(){
				
				if( validInputBox( ttt,'venue field is required, please enter a valid string') )
				{
					gTABLE['location']['venue'] = ttt.value;
					
				}
				
				}, false);
			
		})(_txtTableLocation);
	
	}
	
	
	
		
	
	
	var _txtTableStreet = TheUte().getInputBox('','txtTableStreet',null,null,'clsInput','street');
	
		
	if( typeof _txtTableStreet.addEventListener != 'function') {
		//ie
		(function(ttt){
			
			ttt.attachEvent('onblur', function(){
				 
				if( validInputBox( ttt,'first line of street information is required') )
				{
					gTABLE.location.street = ttt.value;
				}
				
				}, false);
			
		})(_txtTableStreet);
		
	
	}
	else {
		//mozilla
		(function(ttt){
			
			ttt.addEventListener('blur', function(){
				
				if( validInputBox( ttt,'first line of street information is required') )
				{
					gTABLE.location.street = ttt.value;
					
				}
				
				}, false);
			
		})(_txtTableStreet);
	
	}
	
	//
	// the direct .onblur seems to work ???
	//
	
	var _txtTableStreet2 = TheUte().getInputBox('','txtTableStreet2',null,null,'clsInput','street 2');
	_txtTableStreet2.onblur = function()
	{
		gTABLE.location.street2 = _txtTableStreet2.value;
	
	};
	
	var _txtTableCity = TheUte().getInputBox('','txtTableCity',null,null,'clsInput','city');
	_txtTableCity.onblur = function()
	{
		if(validInputBox(_txtTableCity,'city is required'))
			gTABLE.location.city = _txtTableCity.value;
	
	};
	var _txtTableState = TheUte().getInputBox('','txtTableState',null,null,'clsInput','state');
	_txtTableState.onblur = function()
	{
		if(validInputBox(_txtTableState,'state or province or region is required'))
			gTABLE.location.state = _txtTableState.value;
	};
	var _txtTableZip = TheUte().getInputBox('','txtTableZip',null,null,'clsInput','zip/postal code');
	_txtTableZip.onblur = function()
	{
		if(validInputBox(_txtTableZip,'zip or postal code required'))
			gTABLE.location.zip=_txtTableZip.value;
			
	
	};
	var _txtTableCountry = TheUte().getInputBox('','txtTableCountry',null,null,'clsInput','country');
	_txtTableCountry.onblur = function()
	{
		if(validInputBox(_txtTableCountry,'country is required'))
			gTABLE.location.country = _txtTableCountry.value;
	
	};
	var _txtTableURL = TheUte().getInputBox('','txtTableURL',null,null,'clsInput','event location website');
	_txtTableURL.onblur = function()
	{
		gTABLE.location.url = _txtTableURL.value;
	
	};
	
	var _txtTableDate = TheUte().getInputBox('','txtTableDate',null,null,'clsInput','date');
	_txtTableDate.onblur = function()
	{
		if(validInputBox(_txtTableDate,'date is required'))
			gTABLE.date = _txtTableDate.value;
			
	
	};
	
	var _txtTableTime = TheUte().getInputBox('','txtTableTime',null,null,'clsInput','time');
	_txtTableTime.onblur = function()
	{
		if(validInputBox(_txtTableTime,'time is required'))
			gTABLE.time = _txtTableTime.value;
	
	};
	
	var _txtTableDescription  = TheUte().getTextArea('','txtTableDescription',null,null,'clsTextArea');
	_txtTableDescription.onblur = function()
	{
		gTABLE.description = _txtTableDescription.value;
	
	};
	
	
	var _saveCmd = TheUte().getButton("cmdSave","save table","save this table",null,"clsActionButton");
	var _cancelCmd = TheUte().getButton("cmdCancel","cancel","cancel out of this screen",null,"clsActionButton");
	
	_cancelCmd.onclick = function()
	{
	
		resetTable(gTABLE);
		location.href = location.href;
	
	};
	
	_saveCmd.onclick = function()
	{
		
		
		
		//var errs = validateTable(gTABLE);
		var errs = "";
		
		//log("saving" + errs);
		
		//reflect through form and get as JSON;
		var tableJSON = JSON.stringify(gTABLE);

		if(errs.trim().length == 0)
		{
		
			if( (validateUsers(gTABLE.hosts) == true) &&  (validateUsers(gTABLE.guests) == true) )
			{
				log("passed validation, save ...");
				log(tableJSON);
				
				
				var tableJSON64 = TheUte().encode64( tableJSON );
				
				resetTable(gTABLE);
				
				var SaveNewEvent = newMacro("SaveNewEvent");
				addParam(SaveNewEvent,"table64",tableJSON64);
				addParam(SaveNewEvent,"panel",attachPoint.id);
				processJSON(SaveNewEvent);
	
			}
			else
			{
				displayMsg("Please check host/guest information for missing data",msgCode.warn);
			}
		
		}
		else
		{
			displayMsg("" + errs, msgCode.warn);
		}
		
		//log(tableJSON);
		
	
	};
	
	var _dvTableLocation = document.createElement('DIV');
	
	var _lblTableLocation = document.createTextNode('venue');
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
		gTABLE.hosts.push(tmpUser);
		UserCreateForm(_dvHosts,tmpUser,gTABLE.hosts);
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
		gTABLE.guests.push(tmpUser);
		UserCreateForm(_dvGuests,tmpUser,gTABLE.guests);
	};

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
	
	vals.push( document.createTextNode("city") );
	vals.push( _txtTableCity);
	vals.push( document.createTextNode("state") );
	vals.push( _txtTableState);
	vals.push( document.createTextNode("zip") );
	vals.push( _txtTableZip);
	vals.push( document.createTextNode("country") );
	vals.push( _txtTableCountry);
	
	
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
		s += " &";
		
	}
	
	//remove last &
	s = s.trim().substring(0,s.length-1);
	
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







//drek
/*


	
*/