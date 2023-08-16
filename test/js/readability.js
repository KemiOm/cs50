var readlineSync = require('readline-sync');
var prompt = readlineSync.question('Text:');
console.log('\n' + prompt);
// calculate letters

        var letters = 0;
        for(var i = 0; i <prompt.length; i++)
        if ((prompt[i].(/[a-zA-Z]/).test(prompt[i]))
        {
            letters ++;
        }




    var words = 1;
    for (var i = 0; i < prompt.length; i++)
    {
// represent the space in single quotes''
        if (prompt[i] == ' ')
        {
            words++;
        }

    }


    var sentences = 0;
    for (var j = 0; j < prompt.length; j++)
    {
        if (prompt[j] == '.' || prompt[j] == '!' || prompt[j] == '?')
        {
            sentences++;
        }

    }


    let L = (100.0 * letters) / words;
    let S = (100.0 * sentences) / words;
    var index = Math.round(0.0588 * L - 0.296 * S - 15.8);


    if (index < 1)
    {
        console.log('Before Grade 1');
    }
    else if (index < 16)
    {
        console.log('Grade'+ index);
    }
    else
    {
        console.log('Grade 16+');
    }

