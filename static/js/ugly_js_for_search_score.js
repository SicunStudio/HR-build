/**
 * Search AJAX Module ---- Just make your experience comfortable!
 *     * Search issues
 * @param issues
 */

function show_result(score){
    var bfr = "";
    for (var each in score) {
        // ugliest lines in the whole world!!!
        bfr += "<li class=\"collection-item\"><div>" + score[each].title + "<a href=\"/downloading/" + score[each].title + "\" class=\"secondary-content\"><i class=\"material-icons\">file_download</i></a><a  href=\"#!\" class=\"secondary-content\" onclick=\"delete_file(\'/deleting/" + score[each].title + "\')\"><i class=\"material-icons\">delete</i></a></div></li>";
    }
    document.getElementById("result-container").innerHTML=bfr;
    if (bfr == "") {
        document.getElementById("result-container").style.display="none";
    } else {
        document.getElementById("result-container").style.display="block";
    }

    // Toast if EMPTY RESULT
	if(bfr == ""){
		Materialize.toast("查询结果为空", 3000, "toast-warning")
	}
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
    });
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

function delete_file(url) {
    var s = confirm("删除后将不可恢复！确认要删除吗？");
    if (s == true) {
        console.log("deletion comfirmed!");
        location.href=url;
    } else {
        console.log("deletion declined!");
    }
}
