/**
 * Search AJAX Module ---- Just make your experience comfortable!
 * 	* Search issues
 * @param issues
 */

function show_result(issues){
	var bfr = "";
	for (var id in issues) {
		console.log(issues[id]);
		// ugliest lines in the whole world!!!
		bfr += ""
	}
	document.getElementById("result-table").innerHTML=bfr;
}

function search(){
	var search_data = {
		"d": document.getElementById("direction").value,
		"c": document.getElementById("content").value
	};
	$.ajax({
		type: 'GET',
		url: /searching_score/,
		data: search_data,
		dataType: 'json',
		success: function(data){
			show_result(data.result);
		},
		error: function(xhr, type){

		}
	})
	//location.href="/searching_issue?d=" + direction + "&c=" + content;
}

/**
 * Support pressing Enter key to perform a search
 * @constructor
 */
function EnterKeyToSearch() {
	var key;
	if(window.event)
		key = event.keyCode;
	else if(event.which)
		key = event.which;
	var keychar = String.fromCharCode(key);

	if (keychar == "\r"){
		console.log("SEARCHBOX: Enter key pressed");
		search();
	}
}
