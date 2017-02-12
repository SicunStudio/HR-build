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
    };
    for (i = 0; i < 9; i++) {
        total += Number(f[i].value);
    };
    return [self_total, total];
};
