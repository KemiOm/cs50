function getRemainder(num1, num2) {
    var math = ((num1 - (num1 % num2)) / num2);
    return math
}

function get_cents() {

    do {
        const readlineSync = require('readline-sync')

        let form = readlineSync.question("Enter desired amount of cents. ");
        var want = parseFloat(form)
    }
    while (want < 0);

return want
}


function get_dimes(want){
    var dimes;
    dimes = getRemainder(want, 10);
    cents = want - (dimes * 10)
    return dimes;
}

function get_quarters(want){
    var quarters;
    quarters = getRemainder(want, 25);
    cents = want - (quarters * 25);
    return quarters;
}

function get_nickels(want){
    var nickels;
    nickels = getRemainder(want, 5);
    cents = want - (nickels * 25);
    return nickels;
}

function get_pennies(want){
    var pennies;
    pennies = getRemainder(want, 1);
    cents = want - (pennies * 25);
    return pennies;
}

var Input = get_cents()

// calculate number of quarters to give to custome
var total_quarters = get_quarters(Input)
var cents1 = Input - total_quarters * 25

var total_dimes = get_dimes(Input)
var cents2 = cents1 - total_dimes* 10

var total_nickels = get_nickels(Input)
var cents3 = cents2 - total_nickels * 5

var total_pennies = get_pennies(Input)
var cents4 = cents3 - total_pennies * 1

var sum = total_quarters + total_dimes + total_nickels + total_pennies;
console.log(sum)





