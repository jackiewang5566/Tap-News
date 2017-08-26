var express = require('express');
var router = express.Router();

// GET news summary list
router.get('/userId/:userId/pageNum/:pageNum', function (req, res, next) {
    user_id = req.params['userId'];
    page_num = req.params['pageNum'];

    rpc_client.getNewsSummariesForUser(user_id, page_num, function (response) {
        res.json(response);
    })
});

module.exports = router;