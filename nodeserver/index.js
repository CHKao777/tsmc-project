const express = require('express');
const app = express();
const mongoose = require('mongoose');
//const urlmodel = require('./url_count');
//const wordmodel = require('./word_count');
//const word_count = require('./word_count');
//const url_count = require('./url_count');
const company = ['tsmc', 'asml', 'applied materials', 'sumco'];
const Dates = [];
const TOTAL_URLC = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
const TSMC_WC = [];
const TSMC_URLC = [];
const ASML_WC = [];
const ASML_URLC = [];
const AM_WC = [];
const AM_URLC = [];
const S_WC = [];
const S_URLC = [];

app.set('view engine', 'ejs');

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
    console.log(Dates);
    console.log(Dates.length);
}
checkDate();

mongoose.connect('mongodb://localhost/tsmc_project', () => {
    console.log('DB connect!');
}, err => console.log("errormesageDBconnecting:" + err));

const wordSchema = mongoose.Schema({
    Date: String,
    Company: String,
    Word_Count: Number
})
const wordModel = mongoose.model('wordModel', wordSchema, 'word_counts');

const urlSchema = mongoose.Schema({
    Date: String,
    Company: String,
    Url_Count: Number
})
const urlModel = mongoose.model('urlModel', urlSchema, 'url_counts');

run();
async function run() {
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
                    console.log(worddata[k].Date);
                    tmp1 += worddata[k].Word_Count;
                }
                if (i == 0) {
                    TSMC_WC.push(tmp1);
                    //TSMC_URLC.push(tmp2);
                } else if (i == 1) {
                    ASML_WC.push(tmp1);
                    //ASML_URLC.push(tmp2);
                } else if (i == 2) {
                    AM_WC.push(tmp1);
                    //AM_URLC.push(tmp2);
                } else {
                    S_WC.push(tmp1);
                    //S_URLC.push(tmp2);
                }
                tmp1 = 0;
                //tmp2 = 0;
            }
        }
        for (let i = 0; i < company.length; i++) {
            for (let j = 0; j < Dates.length; j++) {
                const urldata = await urlModel.find({ Company: company[i], Date: Dates[j] });
                //console.log(urldata);
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
                    //TSMC_WC.push(tmp1);
                    TSMC_URLC.push(tmp2);
                } else if (i == 1) {
                    //ASML_WC.push(tmp1);
                    ASML_URLC.push(tmp2);
                } else if (i == 2) {
                    //AM_WC.push(tmp1);
                    AM_URLC.push(tmp2);
                } else {
                    //S_WC.push(tmp1);
                    S_URLC.push(tmp2);
                }
                //tmp1 = 0;
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
        //console.log(Dates);
        //console.log(ASML_WC);
    } catch (e) {
        console.log(e.message);
    }
}


app.get('/word_count', (req, res) => {
    res.render('wordcount', {
        Dates_arr: Dates,
        tsmc_word_count: TSMC_WC,
        asml_word_count: ASML_WC,
        appliedmaterials_word_count: AM_WC,
        sumco_word_count: S_WC
    });
});
app.get('/url_count', (req, res) => {
    res.render('urlcount', {
        Dates_arr: Dates,
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