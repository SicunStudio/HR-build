function count_now(name) {
    $("#"+name).each(function(index, this_form) {
        result = count_each(name);
        // TODO: is getElementsByTagName() safe enough??
        this_form.getElementsByTagName("span")[0].innerHTML=result[0];
        this_form.getElementsByTagName("span")[1].innerHTML=result[1];
    });
};


function count_each(name) {
    var self_total = 0, total = 0;
    var i;
    var f = document.getElementsByName(name);
    for (i = 1; i <= 5; i++) {
        self_total += Number(f[i].value);
    }
    for (i = 1; i <= 9; i++) {
        total += Number(f[i].value);
    }
    return [self_total, total];
};


function submit_now(name, e) {
    var f = document.getElementsByName(name);
    // console.log(f);
    // JSON data is sent in RANDOM order!!!
    var data = {
        "name": name,
        "dim-self": Number(f[1].value),
        "act-self": Number(f[2].value),
        "act-num": Number(f[3].value),
        "dly-self": Number(f[4].value),
        "dly-act": Number(f[5].value),
        "mntr-dim": Number(f[6].value),
        "mntr-act": Number(f[7].value),
        "attd": Number(f[8].value),
        "bonus": Number(f[9].value),
        "total": Number(f[11].innerHTML)
    };
    $.ajax({
        type: 'POST',
        url: /scoring_page/,
        data: JSON.stringify(data),
        contentType: 'application/json; charsef=UTF-8',
        dataType: 'json',
        success: function(data){
            var result = data.result;
            var i;
            var f = document.getElementsByName(result["name"]);
            // TODO: code structue could be simplified using jQuery
            f[1].value = result["dim-self"];
            f[2].value = result["act-self"];
            f[3].value = result["act-num"];
            f[4].value = result["dly-self"];
            f[5].value = result["dly-act"];
            f[6].value = result["mntr-dim"];
            f[7].value = result["mntr-act"];
            f[8].value = result["attd"];
            f[9].value = result["bonus"];
            toast_msg =
            Materialize.toast(
                $("<div>成功写入 "+result['name']+" 的分数！</div>"),
                3000, 'toast-success');
            $("ul li a[href=#"+result['name']+"]").attr("class", "teal-text")
        },
        error: function(xhr, type){
            Materialize.toast(
                $("<div>数据交换失败！</div>"),
                3000, 'toast-error'
            )
        }
    });
}
