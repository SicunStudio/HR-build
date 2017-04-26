/** ###################### FREE-TIME PICKER CONTROLLER ###################### **/

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

var tds = document.getElementsByName("free-time-picker");
for(var i=0; i<tds.length; i++)
{
    $("#"+tds[i].id).attr("freetime_checked", "no")
}

/** ###################### DATABASE RENDERER SECTION ###################### **/

/** ================== Section 1: Query by Member ================= **/

/**
 * Query a person's free time from database.
 * @param refresh_only: Set true if you only use this function for refreshing.
 * @returns {number} -1 if fails.
 * @dependency show_person(data).
 */
function searchPerson(refresh_only)
{
    var search_bar = document.getElementById("search-bar");
    var data = {
        depart: search_bar.getElementsByTagName("select")[0].value,
        direction: search_bar.getElementsByTagName("select")[1].value,
        content: search_bar.getElementsByTagName("input")[2].value
    };
    // console.log(data);
    if (data['depart'] == '' || data['direction'] == '' || data['content'] == '') {
        console.log("Invalid search!");
        //Give a toast
        showInpageToast("无效检索，请检查关键字！", "warning");
        return -1;
    }
    else {
        $.ajax({
            type: 'GET',
            url: '/get_person_freetime/',
            data: data,
            dataType: 'json',
            success: function(data) {
                // console.log(data);
                if (show_person(data.result)) {
                    show_freetime(data.freetime);
                    // No need to show this toast if you use this func to refresh
                    if(!refresh_only)
                        showInpageToast("人员已检索到，空闲时间显示在此", "success");
                }
                else {
                    showInpageToast("未检索到成员！", "warning");
                    clearFreeTimePick();         //Clearing free time picker on failure is a mature choice
                }
            },
            error: function(xhr, type) {
                clearFreeTimePick();         //Clearing free time picker on failure is a mature choice
            }
        });
    }
}


/**
 * @INNER-TOOL
 * After querying a person, parse the returned AJAX data from the backend, and generate the following data:
 *  - Name
 *  - ID
 * Then, give a result of found or not.
 * This function is used by searchPerson() to determine if we should render and toast, or not.
 * @param data
 *      AJAX data from backend.
 * @returns {number}
 *      If found, return 1, also print Name and ID on the top of free time picker;
 *      If not found, return 0 instead.
 */
function show_person(data) {
    var target_range = document.getElementsByName("search-result")[0];
    var target = target_range.getElementsByTagName("span");
     console.log(data);
    target[0].innerText = data[1];
    target[1].innerText = data[0];
    if (data[0] != "") {
        console.log("This person is in db!");
        return 1;
    }
    else {
        return 0;
    }
}


/**
 * Render a person's recorded free time (if have) to the free time picker.
 * @param data
 */
function show_freetime(data) {
    var target_range = document.getElementsByName("free-time-picker");
    console.log(data);
    // TODO: only loop 4 times...
    /*
    for (var each in target_range) {
    var target = target_range[each];
    console.log(data[each+1]);
    if (data[each+1] == 0) {
    $(target).attr("freetime_checked", "no");
    $(target).css("background-color", "#FFFFFF");
}
else if (data[each+1] == 1) {
$(target).attr("freetime_checked", "yes");
$(target).css("background-color", "#4db6ac");
}
}
*/
    // var tds = document.getElementsByName("free-time-picker");
    for (var i = 0; i < target_range.length; i++) {
        var cell = $("#" + target_range[i].id);
        if (data[i+1] == 0 || data.length == 0) {
            cell.attr("freetime_checked", "no");
            cell.css("background-color", "#FFFFFF");
        } else if (data[i+1] == 1) {
            cell.attr("freetime_checked", "yes");
            cell.css("background-color", "#4db6ac");
        }
    }



}



/** ###################### RESULT RENDERER SECTION ###################### **/

function show_result(persons){
	var bfr = "";
	for (var id in persons) {
		// ugliest lines in the whole world!!!
		bfr += "			<div class=\"card\">\
						<div class=\"card-content\">\
							<div class=\"row\">\
								<span class=\"card-title col s4 left\"><a href=\"/update/" + id + "\"\ class=\"light-green-text text-darken-4\">" + persons[id][0] + "</a></span>\
								<span class=\"card-title col s7\">" + id + "</span>\
							</div>\
							<div class=\"row\">\
								<table class=\"striped col s12\">\
									<tr>\
										<th>性别</th><td>" + persons[id][1] + "</td>\
										<th>QQ</th><td>" + persons[id][2] + "</td>\
									</tr>\
									<tr>\
										<th>电话</th><td>" + persons[id][3] + "</td>\
										<th>微信</th><td>" + persons[id][4] + "</td>\
									</tr>\
									<tr>\
										<th>应急联系方式</th><td>" + persons[id][5] + "</td>\
										<th>院系</th><td>" + persons[id][6] + "</td>\
									</tr>\
									<tr>\
										<th>班级</th><td>" + persons[id][7] + "</td>\
										<th>寝室</th><td>" + persons[id][8] + "</td>\
									</tr>\
									<tr>\
										<th>部门</th><td>" + persons[id][9] + "</td>\
										<th>组别</th><td>" + persons[id][10] + "</td>\
									</tr>\
									<tr>\
										<th>职务</th><td>" + persons[id][11] + "</td>\
										<th>加入时间</th><td>" + persons[id][12] + "</td>\
									</tr>\
								</table>\
							</div>\
						</div>\
					</div>\
					"
	}
	document.getElementById("result-table").innerHTML=bfr;
	// Toast if EMPTY RESULT
	if(bfr == ""){
		Materialize.toast("查询结果为空", 3000, "toast-warning")
	}
}


/** ###################### ADDITIONAL TWEAK FEATURES ###################### **/

/**
 * Press ENTER key to perform a search. This is a must for every mature sites.
 * @constructor
 */
function EnterKeyToSearch_Person() {
	var key;
	if(window.event)
		key = event.keyCode;
	else if(event.which)
		key = event.which;
	var keychar = String.fromCharCode(key);

	if (keychar == "\r"){
		console.log("SEARCHBOX: Enter key pressed");
		searchPerson();
	}

}