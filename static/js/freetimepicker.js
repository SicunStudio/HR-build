/**
 * Created by AnCla on 2017/4/26 0026.
 */
/** ###################### FREE-TIME PICKER CONTROLLER ###################### **/

/**
 * @CORE-FUNCTION
 * Act the free time picker when you click a cell.
 *  - Change color
 *  - Mark your chosen free time cell with attr.
 * @param cellID  The cell you clicked.
 */
function handleFreeTimePick(cellID){
    var cell = $("#"+cellID);
    if(cell.attr("freetime_checked") == "yes"){
        cell.attr("freetime_checked", "no");
        cell.css("background-color", "#FFFFFF");
    }
    else{
        cell.attr("freetime_checked", "yes");
        cell.css("background-color", "#4db6ac")
    }
}


/**
 * @CALLBACK-Function-Required
 * Analyse free time table, gather your picked free time value,
 *  and submit them to database with your defined callback function.
 * @CALLBACK-FUNCTION-Format
 *      A normal function with one parameter: result.
 *      Our gathered result will directly pass into it, and it will be called finally.
 * @param method_to_background: Your callback function's name.
 *      NOTICE: Just function name. Parameter isn't required.
 */
function submitFreeTimePick(method_to_background){
    var tds = document.getElementsByName("free-time-picker");
    var result = [];

    for(var i=0; i<tds.length; i++){
        var cell = $("#"+tds[i].id);
        if(cell.attr("freetime_checked") == "yes"){
            result.push(tds[i].id)
        }
    }

    //For debug
    //alert("已统计的空闲时间如下：\n" + result.toString());

    // Call your defined callback method
    method_to_background(result)

}

/**
 * Clear the free time picker. This is benefit for refilling the table.
 */
function clearFreeTimePick(){
    var tds = document.getElementsByName("free-time-picker");
    for(var i=0; i<tds.length; i++){
        var cell=$("#"+tds[i].id);
        cell.attr("freetime_checked", "no");
        cell.css("background-color", "#FFFFFF")
    }
}

/**
 * @INIT-CODE
 * Initialize the free time picker.
 * @type {NodeList}
 */
var tds = document.getElementsByName("free-time-picker");
for(var i=0; i<tds.length; i++)
{
    $("#"+tds[i].id).attr("onclick","handleFreeTimePick('"+tds[i].id+"')")
    .attr("freetime_checked", "no")
}

