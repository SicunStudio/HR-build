/**
 * Search AJAX Module ---- Just make your experience comfortable!
 *     * Search issues
 * @param issues
 */

function show_result(score){
    var bfr = "";
    for (var each in score) {
        // ugliest lines in the whole world!!!
        bfr += ("<li class=\"collection-item\"><pre><a href=\"/score_page/" + score[each].title + "\" class=\"teal-text\" style=\"font-size:2em\">" + score[each].title + "</a>&nbsp;&nbsp;&nbsp;&nbsp;of " + score[each].depart + "&nbsp;&nbsp;&nbsp;&nbsp;@ " + score[each].date + "<a href=\"/downloading/" + score[each].title + "\" class=\"secondary-content\"><i class=\"small material-icons\">file_download</i></a><a  href=\"#!\" class=\"secondary-content\" onclick=\"delete_file(\'/deleting/" + score[each].title + "\')\"><i class=\"small material-icons\">delete</i></a></pre></li>");
    }
    if (bfr == "") {
        document.getElementById("result-container").style.display="none";
        Materialize.toast("查询结果为空", 3000, "toast-warning")
    } else {
        document.getElementById("result-container").style.display="block";
        document.getElementById("result-container").innerHTML=bfr;
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
        // console.log("deletion comfirmed!");
        location.href=url;
    } else {
        // console.log("deletion declined!");
    }
}


function change_searchbox() {
    // TODO: items "flash back" before being replaced by a new one
    if ($("#direction").val() == "date") {
        $("#content-wrap").fadeOut(250);
        var bfr ="<input name=\"content\" id=\"content\" type=\"date\" class=\"datepicker\" onchange=\"search()\" placeholder=\"请选择日期\" required>";
        $("#content-wrap").html(bfr);
        $('.datepicker').pickadate({
            selectMonths: true, // Creates a dropdown to control month
            selectYears: 15 // Creates a dropdown of 15 years to control year
        });
        // TODO: automatically open datepicker
        $("#content-wrap").fadeIn(250);

    } else if ($("#direction").val() == "depart") {
        $("#content-wrap").fadeOut(250);
        var bfr = "\
        <select name=\"content\" id=\"content\" onchange=\"search()\" required>\
        <option value=\"苟\" disabled selected>请选择部门</option>\
        <option value=\"财务部\">财务部</option>\
        <option value=\"秘书部\">秘书部</option>\
        <option value=\"人力资源部\">人力资源部</option>\
        <option value=\"社团部\">社团部</option>\
        <option value=\"行政监察部\">行政监察部</option>\
        <option value=\"外联部\">外联部</option>\
        <option value=\"公共关系部\">公共关系部</option>\
        <option value=\"宣传部\">宣传部</option>\
        <option value=\"媒体部\">媒体部</option>\
        <option value=\"思存工作室\">思存工作室</option>\
        <option value=\"新媒体工作室\">新媒体工作室</option>\
        <option value=\"社团外联企划小组\">社团外联企划小组</option>\
        <option value=\"文艺拓展部\">文艺拓展部</option>\
        <option value=\"其它\">其它</option>\
        </select>";
        $("#content-wrap").html(bfr);
        $('select').material_select();
        // TODO: placeholder should be displayed in grey
        $("#content-wrap").fadeIn(250);

    } else if ($("#direction").val() == "title") {
        $("#content-wrap").fadeOut(250);
        var bfr = "<input name=\"content\" id=\"content\" type=\"text\" class=\"black-text\" placeholder=\"请输入表格标题\" onkeypress=\"EnterKeyToSearch()\" required>";
        $("#content-wrap").html(bfr);
        $("#content-wrap").fadeIn(250);

    } else {
        // mayby no one will see this
        Materialize.toast("DON'T MESS UP WITH MY CODE!", 3000, "error");
    }
}
