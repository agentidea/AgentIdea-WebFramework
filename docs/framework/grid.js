/**

	@description: core framework table based DOM grid

*/

function newGrid2(id,rows,cols,values,border,aGUID)
{
     
    var grid = new grid2();
    grid.id = id;
    grid.rows = rows;
    grid.cols = cols;
    grid.values = values;
    
    if(aGUID !=null)
        grid.setGUID(aGUID);
        
    if(border != null)
        grid.border = border;
        
    return grid;
}



////////////////////
// grid prototype
////////////////////
function grid2()
{
    var _gridTable =  document.createElement("table");      
    var _gridTableBody = document.createElement("tbody");  
    this.gridTable = _gridTable;
    this.gridTableBody = _gridTableBody;
    
    var _rows = 0;
    var _cols = 0;
    var _id;
    var _values = null;
    var _border = 0;
    
    
    var _GUID  = "not_set_yet";
    this.setGUID = function(rhs)
    {
        if(rhs != null)
        {
            _GUID = rhs; 
            _gridTableBody.setAttribute("GUID",rhs);
        }
    }
    
    this.getGUID = function(){return _GUID; }
    
    this.border = _border;
    
    this.values = _values;  //value array that hold
    
    this.rows = _rows;
    this.cols = _cols;
    
    this.id = _id;
    this.init = initializeGrid;

}


function initializeGrid( aGrid )
{

    if(aGrid.rows == 0 || aGrid.cols == 0 )
    {
        alert("invalid sized grid " + aGrid.rows + " : " + aGrid.cols );
        return;
    }

        aGrid.gridTableBody.id = this.id;
        aGrid.gridTable.appendChild( aGrid.gridTableBody );
       
       
       var elementCounter = 0;
       
        var gridRowCurrent,gridCellCurrent,gridCellTextCurrent,cellCode,gridCellDiv;
        
        for(var j = 0; j < aGrid.rows; j++) {
            
            gridRowCurrent = document.createElement("tr");

            for(var i = 0; i < aGrid.cols; i++) {
                cellCode = j + "." + i;// + "." + elementCounter;
                gridCellCurrent = document.createElement("td");
                //gridCellCurrent.valign = "top";
                gridCellCurrent.setAttribute("valign","top");
                gridCellDiv = document.createElement("div");
                gridCellDiv.id = aGrid.id + ".gridCell." + cellCode;
                gridCellDiv.className = "clsGridCell";
               
               //titles on or off here - mostly was for debugging purposes
               // gridCellDiv.title = gridCellDiv.id;
                
                // creates a Text Node
             //gridCellTextCurrent = document.createTextNode(gridCellDiv.id);
                // appends the Text Node we created into the cell <div>
               //gridCellDiv.appendChild(gridCellTextCurrent);
              
               //append value if there are any?
               if(aGrid.values != null)
               {    if(elementCounter<aGrid.values.length)
                    {
                        if( aGrid.values[elementCounter] != null)
                           gridCellDiv.appendChild( aGrid.values[elementCounter] );
                        
                        elementCounter++;
                    }
               }
               
               
               gridCellCurrent.appendChild(gridCellDiv);
                // appends the cell <td> into the row <tr>
                gridRowCurrent.appendChild(gridCellCurrent);
            }
            // appends the row <tr> into <tbody>
             aGrid.gridTableBody.appendChild(gridRowCurrent);
        }
 
        aGrid.gridTable.setAttribute("border",this.border);
        
        return aGrid;
}




function gridValues()
{
    var _name = null;
    var _val = null;
    var _x = 0;
    var _y = 0;
    
    this.name = _name;
    this.val = _val;
    this.x = _x;
    this.y = _y;
    
}

