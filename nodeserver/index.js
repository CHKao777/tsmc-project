const express = require('express');
const app = express();
const mongoose = require('mongoose');
const expressLayouts = require('express-ejs-layouts');
const company = ['tsmc', 'asml', 'applied materials', 'sumco'];
var Dates = [];
var intDates = [];
var TOTAL_URLC = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
var TSMC_WC = [];
var TSMC_URLC = [];
var ASML_WC = [];
var ASML_URLC = [];
var AM_WC = [];
var AM_URLC = [];
var S_WC = [];
var S_URLC = [];

app.set('view engine', 'ejs');
app.use(expressLayouts);

//catch now Date and deal with some operation
function settingDate() {
    console.log('in settingDate');
    return new Promise((resolve, reject) => {
        var today = new Date();
        //check what day of the week
        switch (today.getDay()) {
            case 0: { //Sunday
                today.setDate(today.getDate() - 13);
                break;
            }
            case 1: { //Monday
                today.setDate(today.getDate() - 7);
                break;
            }
            case 2: { //Tuesday
                today.setDate(today.getDate() - 8);
                break;
            }
            case 3: { //Wednesday
                today.setDate(today.getDate() - 9);
                break;
            }
            case 4: { //Thursday
                today.setDate(today.getDate() - 10);
                break;
            }
            case 5: { //Friday
                today.setDate(today.getDate() - 11);
                break;
            }
            case 6: { //Saturday
                today.setDate(today.getDate() - 12);
                break;
            }
        }
        //init 
        Dates.length = 0;
        intDates.length = 0;
        
        //transfer Date to YYYY-MM-DD format
        Dates.push(today.toISOString().split('T')[0]);

        //transfer Date to YYYYMMDD format
        intDates[0] = today.toLocaleDateString('en-GB').split('/').reverse().join('');

        //this for is used to push forward half a year
        for (let i = 1; i < 24; i++) {
            today.setDate(today.getDate() - 7);
            intDates[i] = today.toLocaleDateString('en-GB').split('/').reverse().join('');
            Dates.unshift(today.toISOString().split('T')[0]);
        }
        intDates.reverse();
        for (let i = 0; i < intDates.length; i++) {
            intDates[i] = parseInt(intDates[i])
        }
        console.log('out settingDate');
        resolve();
    });
}


//mongoDB connection
mongoose.connect('mongodb://mongodb:27017/tsmc_project', () => {
    console.log('DB connect!');
}, err => console.log("errormesageDBconnecting:" + err));


//mongoDB word_counts collection Schema defination
const wordSchema = mongoose.Schema({
    Date: String,
    Company: String,
    Word_Count: Number
})
const wordModel = mongoose.model('wordModel', wordSchema, 'word_counts');


//mongoDB url_counts collection Schema defination
const urlSchema = mongoose.Schema({
    Date: String,
    Company: String,
    Url_Count: Number
})
const urlModel = mongoose.model('urlModel', urlSchema, 'url_counts');

//catch the DB data and do something
async function run() {
    console.log('in run');
    //init
    TOTAL_URLC = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    TSMC_WC.length = 0;
    TSMC_URLC.length = 0;
    ASML_WC.length = 0;
    ASML_URLC.length = 0;
    AM_WC.length = 0;
    AM_URLC.length = 0;
    S_WC.length = 0;
    S_URLC.length = 0;

    try {
        let tmp1 = 0;
        let tmp2 = 0;
        for (let i = 0; i < company.length; i++) {
            for (let j = 0; j < Dates.length; j++) {
                const worddata = await wordModel.find({ Company: company[i], Date: Dates[j] });
                if (worddata.length == 0) {
                    if (i == 0) {
                        TSMC_WC.push(-1);
                    } else if (i == 1) {
                        ASML_WC.push(-1);
                    } else if (i == 2) {
                        AM_WC.push(-1);
                    } else if (i == 3) {
                        S_WC.push(-1);
                    }
                    continue;
                }

                for (let k = 0; k < worddata.length; k++) {
                    tmp1 += worddata[k].Word_Count;
                }
                if (i == 0) {
                    TSMC_WC.push(tmp1);
                } else if (i == 1) {
                    ASML_WC.push(tmp1);
                } else if (i == 2) {
                    AM_WC.push(tmp1);
                } else {
                    S_WC.push(tmp1);
                }
                tmp1 = 0;
            }
        }
        for (let i = 0; i < company.length; i++) {
            for (let j = 0; j < Dates.length; j++) {
                const urldata = await urlModel.find({ Company: company[i], Date: Dates[j] });
                if (urldata.length == 0) {
                    if (i == 0) {
                        TSMC_URLC.push(-1);
                    } else if (i == 1) {
                        ASML_URLC.push(-1);
                    } else if (i == 2) {
                        AM_URLC.push(-1);
                    } else if (i == 3) {
                        S_URLC.push(-1);
                    }
                    continue;
                }
                for (let k = 0; k < urldata.length; k++) {
                    tmp2 += urldata[k].Url_Count;
                }
                if (i == 0) {
                    TSMC_URLC.push(tmp2);
                } else if (i == 1) {
                    ASML_URLC.push(tmp2);
                } else if (i == 2) {
                    AM_URLC.push(tmp2);
                } else {
                    S_URLC.push(tmp2);
                }
                tmp2 = 0;
            }
        }
        for (let i = 0; i < Dates.length; i++) {
            const data = await urlModel.find({ Date: Dates[i] });
            if (data.length == 0) {
                TOTAL_URLC[i] = -1;
                continue;
            }
            for (let j = 0; j < data.length; j++) {
                TOTAL_URLC[i] += data[j].Url_Count;
            }
        }
    } catch (e) {
        console.log(e.message);
    }
    console.log('out run');
}

app.get('/', (req, res) => {
    res.render('homepage');
})

app.get('/wordcount', async (req, res) => {
    await settingDate();
    await run();
    console.log('in render');
    res.render('wordcount', {
        Dates_arr: intDates,
        tsmc_word_count: TSMC_WC,
        asml_word_count: ASML_WC,
        appliedmaterials_word_count: AM_WC,
        sumco_word_count: S_WC
    });
});
app.get('/urlcount', async (req, res) => {
    await settingDate();
    await run();
    console.log('in render');
    res.render('urlcount', {
        Dates_arr: intDates,
        tsmc_url_count: TSMC_URLC,
        asml_url_count: ASML_URLC,
        appliedmaterials_url_count: AM_URLC,
        sumco_url_count: S_URLC,
        total_url_count: TOTAL_URLC
    });
})

app.listen(3000, () => {
    console.log('http://localhost:3000');
})