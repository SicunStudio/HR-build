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
    result: result.toString(),
    id: document.getElementById("id").innerText,
    name: document.getElementById("name").innerText,
  };
  $.ajax({
    type: 'POST',
    url: '/submit_freetime/',
    data: data,
    dataType: 'json',
    success: function(data){
      //TODO: 后台要回传一些数据，如处理成功的提示。
      //TODO: 但是具体如何处理，还要取决于怎么样设计录入部分（自动接续逐一录入，还是每次都要重新检索）
      Materialize.toast(data.backMessage['message'], 4000, "toast-info")
    },
    error: function(xhr, type){}
  })

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




function searchPerson() {
    var search_bar = document.getElementById("search-bar");
    var data = {
        depart: search_bar.getElementsByTagName("select")[0].value,
        direction: search_bar.getElementsByTagName("select")[1].value,
        content: search_bar.getElementsByTagName("input")[2].value
    };
    // console.log(data);
    if (data['depart'] == '' || data['direction'] == '' || data['content'] == '') {
        console.log("Invalid search!");
    }
    else {
        $.ajax({
            type: 'GET',
            url: '/get_person_freetime/',
            data: data,
            dataType: 'json',
            success: function(data) {
                if (show_person(data.result)) {
                    show_freetime(data.freetime);
                }
            },
            error: function(xhr, type) {}
        });
    }
}





function show_person(data) {
    var target_range = document.getElementsByName("search-result")[0];
    var target = target_range.getElementsByTagName("span");
    // console.log(data);
    target[0].innerText = data[1];
    target[1].innerText = data[0];
    if (data[0] != "") {
        console.log("person in db!");
        return 1;
    }
    else {
        return 0;
    }
}



function show_freetime(data) {
    var target_range = document.getElementsByName("free-time-picker")
    // console.log(target_range);
}
