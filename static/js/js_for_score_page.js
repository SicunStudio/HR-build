function count_now() {
    $("form").each(function(index, this_form) {
        result = count_each(this_form);
        // console.log(total);
        this_form.getElementsByTagName("span")[0].innerHTML=result[0];
        this_form.getElementsByTagName("span")[1].innerHTML=result[1];
    });
};


function count_each(f) {
    var self_total = 0, total = 0;
    var i;
    for (i = 0; i < 5; i++) {
        self_total += Number(f[i].value);
    }
    for (i = 0; i < 9; i++) {
        total += Number(f[i].value);
    }
    return [self_total, total];
};


function submit_now(tgt_person, e) {
    f = $(e).parent()[0]
    // console.log(f);
    var data = {
        "dim-self": Number(f[0].value),
        "act-self": Number(f[1].value),
        "act-num": Number(f[2].value),
        "dly-self": Number(f[3].value),
        "dly-act": Number(f[4].value),
        "mntr-dim": Number(f[5].value),
        "mntr-act": Number(f[6].value),
        "attd": Number(f[7].value),
        "bonus": Number(f[8].value)
    };
    // console.log(data);
    $.ajax({
        type: 'POST',
        url: /scoring_page/,
        data: JSON.stringify(data),
        contentType: 'application/json; charsef=UTF-8',
        dataType: 'json',
        success: function(data){
            var i;
            for (i = 0; i < 9; i++) {
                $("form[id="+tgt_person+"]")[i].value = data[i];
            }
        },
        error: function(xhr, type){

        }
    });
}
