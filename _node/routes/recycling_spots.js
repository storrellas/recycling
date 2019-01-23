var express = require('express');
var router = express.Router();

/* GET recycling spots listing. */
router.post('/', function(req, res, next) {

  var recycling_spots = [
      {
          "id": 1,
          "name": "Donec aliquam",
          "location":
              {
                  "lat": "41.3823236",
                  "long": "2.1635519"
              },

          "opening_hours": "Mon-Fri 08:00 19:00 Sat 09:00 18:00",
          "groups":
              [ 1, 2, 5, 6 ]
      },
      {
          "id": 2,
          "name": "Lorem ipsum",
          "location":
              {
                  "lat": "41.382393",
                  "long": "2.160481"
              },

          "opening_hours": "Mon-Fri 08:00 19:00 Sat 09:00 18:00",
          "groups":
              [ 8, 3, 5, 9 ]
      },
      {
          "id": 3,
          "name": "Fusce sed",
          "location":
              {
                  "lat": "41.383757",
                  "long": "2.163222"
              },

          "opening_hours": "Mon-Fri 08:00 19:00 Sat 09:00 18:00",
          "groups":
              [ 4, 1, 3 ]
      },
      {
          "id": 4,
          "name": "Cras in semper",
          "location":
              {
                  "lat": "41.383959",
                  "long": "2.161348"
              },

          "opening_hours": "Mon-Fri 08:00 19:00 Sat 09:00 18:00",
          "groups":
              [ 3, 1, 0 ]
      },
      {
          "id": 5,
          "name": "Vestibulum vel sapien ante",
          "location":
              {
                  "lat": "41.381699",
                  "long": "2.161349"
              },

          "opening_hours": "Mon-Fri 08:00 19:00 Sat 09:00 18:00",
          "groups":
              [ 3, 5, 8 ]
      },
      {
          "id": 6,
          "name": "Posuere lectus",
          "location":
              {
                  "lat": "41.38335044069438",
                  "long": "2.1649382237137615"
              },

          "opening_hours": "Mon-Fri 08:00 19:00 Sat 09:00 18:00",
          "groups":
              [ 1, 8, 9, 10, 2, 3 ]
      },
      {
          "id": 7,
          "name": "Suspendisse blandit",
          "location":
              {
                  "lat": "41.383853110283255",
                  "long": "2.163802388357908"
              },

          "opening_hours": "Mon-Fri 08:00 19:00 Sat 09:00 18:00",
          "groups":
              [ 1, 2, 3, 4 ]
      },
      {
          "id": 8,
          "name": "Pellentesque malesuada",
          "location":
              {
                  "lat": "41.38410525272171",
                  "long": "2.162745522155774"
              },

          "opening_hours": "Mon-Fri 08:00 19:00 Sat 09:00 18:00",
          "groups":
              [ 5, 9, 10 ]
      },
      {
          "id": 9,
          "name": "Aliquam mollis",
          "location":
              {
                  "lat": "41.38464750676399",
                  "long": "2.161626003393053"
              },

          "opening_hours": "Mon-Fri 08:00 19:00 Sat 09:00 18:00",
          "groups":
              [ 1, 5, 4, 9 ]
      },
      {
          "id": 10,
          "name": "Aenean tempor",
          "location":
              {
                  "lat": "41.38380189138359",
                  "long": "2.160343371517456"
              },

          "opening_hours": "Mon-Fri 08:00 19:00 Sat 09:00 18:00",
          "groups":
              [ 10, 2, 3, 5 ]
      }
  ];

  if(typeof req.body.lat !== 'undefined' && req.body.lat && req.body.long !== 'undefined' && req.body.long){
    // they send an id via post, they want a single new
    res.send(recycling_spots);

  }else {
      res.statusCode = 400;
      res.send('400: BAD REQUEST.');
  }
});

module.exports = router;
