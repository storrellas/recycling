var express = require('express');
var router = express.Router();

/* GET recycling groups listing. */
router.post('/', function(req, res, next) {

  var recycling_groups = [
      {
          "id":1,
          "name": "Aluminium packaging",
          "icon": "http://link-to-the-icon.svg"
      },
      {
          "id":2,
          "name": "Batteries",
          "icon": "http://link-to-the-icon.svg"
      },
      {
          "id":3,
          "name": "Electric Equipment",
          "icon": "http://link-to-the-icon.svg"
      },
      {
          "id":4,
          "name": "Household Appliances",
          "icon": "http://link-to-the-icon.svg"
      },
      {
          "id":5,
          "name": "Glass",
          "icon": "http://link-to-the-icon.svg"
      },
      {
          "id":6,
          "name": "PET Bottles",
          "icon": "http://link-to-the-icon.svg"
      },
      {
          "id":7,
          "name": "Glass",
          "icon": "http://link-to-the-icon.svg"
      },
      {
          "id":8,
          "name": "PET Bottles",
          "icon": "http://link-to-the-icon.svg"
      },
      {
          "id":9,
          "name": "PET Bottles",
          "icon": "http://link-to-the-icon.svg"
      },
      {
          "id":10,
          "name": "PET Bottles",
          "icon": "http://link-to-the-icon.svg"
      }
  ];

    res.send(recycling_groups);
});

module.exports = router;
