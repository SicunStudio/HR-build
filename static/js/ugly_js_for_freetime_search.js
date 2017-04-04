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

function submitFreeTimePick(){
    var tds = document.getElementsByName("free-time-picker");
    var result=[];

    for(var i=0; i<tds.length; i++){
        var cell=$("#"+tds[i].id);
        if(cell.attr("freetime_checked") == "yes"){
            result.push(tds[i].id)
        }
    }

    //For debug
    //alert("已统计的空闲时间如下：\n" + result.toString());

    //TODO: 接下来可以将统计信息发往后台了。就用AJAX。
    var data={
        result: result.toString()
    };
    // console.log(data);
    if (data['result'] == '') {
        Materialize.toast("请选择空闲时间！", 4000, "toast-info");
    }
    else {
        $.ajax({
            type: 'POST',
            url: '/searching_freetime/',
            data: data,
            dataType: 'json',
            success: function(data) {
                //TODO: 后台要回传一些数据，如处理成功的提示。
                //TODO: 但是具体如何处理，还要取决于怎么样设计录入部分（自动接续逐一录入，还是每次都要重新检索）
                show_result(data.result);
                Materialize.toast("搜索完成！", 4000, "toast-info")
            },
            error: function(xhr, type) {}
        })
    }

}



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
    $("#"+tds[i].id).attr("onclick","handleFreeTimePick('"+tds[i].id+"')")
    .attr("freetime_checked", "no")
}



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
