var express = require('express');
var router = express.Router();

/* GET likes listing. */
router.post('/', function(req, res, next) {

  var likes = [
      {
          "news_id":0,
          "likes":965
      },
      {
          "news_id":1,
          "likes":200
      },
      {
          "news_id":2,
          "likes":32
      },
      {
          "news_id":3,
          "likes":0
      },
      {
          "news_id":4,
          "likes":965
      }
  ]

  if(typeof req.body.id !== 'undefined' && req.body.id){
    // they send an id via post, they want a single new
    res.send(news[req.body.id]);

  }else {
    // if they don't send an id, they want them all
    if(typeof req.body.start !== 'undefined' && req.body.start && req.body.end !== 'undefined' && req.body.end){
      //they specified the quantity of news that they want

      let return_news = []
      for (i = req.body.start; i <= req.body.end; i++) {
        console.log(i)
        return_news.push(news[i]);
      }


      res.send(return_news);
    }else{
      //they don't specify the quantity that they want, so we give them all
      res.send(news);
    }
  }
  console.log(req.body.id);
});

module.exports = router;
