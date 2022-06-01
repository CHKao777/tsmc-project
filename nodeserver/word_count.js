const mongoose = require('mongoose');
mongoose.connect('mongodb://locahost/tsmc_project')
const dataSchema = new mongoose.Schema({
    Date: String,
    Company: String,
    Word_count: Number
});
const dataModel = mongoose.model('wordmodel', dataSchema, 'word_count');
module.exports = dataModel;