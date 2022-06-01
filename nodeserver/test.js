/*
new Date().toISOString()
"2016-02-18T23:59:48.039Z"

new Date().toISOString().split('T')[0];
"2016-02-18"

new Date().toISOString().replace('-', '/').split('T')[0].replace('-', '/');
"2016/02/18"

new Date().toLocaleString().split(',')[0]
"2/18/2016"
 */
const Dates = [];
function checkDate() {
    var today = new Date();
    switch (today.getDay()) {
        case 0: {
            today.setDate(today.getDate() - 13);
            break;
        }
        case 1: {
            today.setDate(today.getDate() - 7);
            break;
        }
        case 2: {
            today.setDate(today.getDate() - 8);
            break;
        }
        case 3: {
            today.setDate(today.getDate() - 9);
            break;
        }
        case 4: {
            today.setDate(today.getDate() - 10);
            break;
        }
        case 5: {
            today.setDate(today.getDate() - 11);
            break;
        }
        case 6: {
            today.setDate(today.getDate() - 12);
            break;
        }
    }
    Dates.push(today.toISOString().split('T')[0]);
    for (let i = 0; i < 23; i++) {
        today.setDate(today.getDate() - 7);
        Dates.unshift(today.toISOString().split('T')[0]);
    }
    //console.log(Dates);
    //console.log(Dates.length);

}

checkDate();

//var date = new Date().toISOString().replace('-', '/').split('T')[0].replace('-', '/');
//console.log(date);