const mongoose = require('mongoose');
mongoose.connect('mongodb://locahost/tsmc_project')
const dataSchema = new mongoose.Schema({
    Date: String,
    Company: String,
    Url_count: Number
});
const dataModel = mongoose.model('urlmodel', dataSchema, 'url_count');
module.exports = dataModel;