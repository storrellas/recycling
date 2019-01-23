var express = require('express');
var router = express.Router();
var bodyParser = require('body-parser');

/* GET news listing. */
router.post('/', function(req, res, next) {
  var filteredNews;

  var news = [{
        "id": 1,
        "title": "Donec aliquam",
        "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean elementum sollicitudin porttitor. Pellentesque ligula lectus, molestie vel pharetra ac, scelerisque ut nibh. Nunc consequat auctor tempus. Fusce pretium molestie nunc, ut tincidunt metus venenatis nec. Proin rutrum fringilla condimentum. Ut sed arcu eu diam sollicitudin semper. Sed vitae diam vel quam rhoncus scelerisque. Praesent tellus turpis, placerat eu orci vitae, efficitur pretium magna. Sed pellentesque sem accumsan vehicula blandit. Donec in cursus risus, vel suscipit erat. Donec metus nunc, aliquet sit amet ornare eget, cursus vel urna. Suspendisse bibendum feugiat lorem, vitae dictum massa luctus id.",
        "category": "Ipsum",
        "icon": "www.path-to-icon.path/icon.svg",
        "main_image": "www.path-to-image.path/icon.svg",
        "scheduled_date": "1547812406",
        "published": true,
        "timestamp": "1547812406",
        "author": "Admin"
      },
      {
        "id": 2,
        "title": "Vestibulum ante ipsum",
        "content": "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Etiam molestie nulla turpis. Praesent non ligula aliquam, imperdiet justo a, aliquet mi. Pellentesque eu congue nisi, ac varius mi. Nam commodo lobortis leo, scelerisque efficitur nisl finibus non. Maecenas elementum nisi eget diam egestas commodo. Vestibulum pulvinar auctor fringilla. Mauris non metus nec urna euismod venenatis nec eleifend risus. Donec iaculis urna non arcu tempus bibendum. Curabitur vehicula est eget imperdiet sodales. Nam convallis tellus eu elementum pharetra. Nullam pharetra ex non placerat consequat.",
        "category": "Lorem",
        "icon": "www.path-to-icon.path/icon.svg",
        "main_image": "www.path-to-image.path/icon.svg",
        "scheduled_date": "1547812375",
        "published": true,
        "timestamp": "1547812375",
        "author": "Admin"
      },
      {
        "id": 3,
        "title": "Curabitur sit amet",
        "content": "Curabitur sit amet maximus lorem. Interdum et malesuada fames ac ante ipsum primis in faucibus. Cras porttitor, enim sed venenatis ornare, mauris nisi bibendum tortor, eu hendrerit eros leo ac justo. Donec quis finibus est, vel placerat arcu. Mauris faucibus lacinia nibh, a lacinia elit fringilla non. Integer mauris mauris, facilisis id ornare non, tristique vitae erat. Maecenas at dignissim tellus, eu scelerisque arcu. Vivamus sit amet mi tincidunt, dignissim lorem et, auctor quam. Duis et lacus a augue egestas venenatis.",
        "category": "Ipsum",
        "icon": "www.path-to-icon.path/icon.svg",
        "main_image": "www.path-to-image.path/icon.svg",
        "scheduled_date": "1547812303",
        "published": true,
        "timestamp": "1547812303",
        "author": "Admin"
      },
      {
        "id": 4,
        "title": "Sed arcu turpis",
        "content": "Sed arcu turpis, consequat vitae ante at, euismod tincidunt est. Sed sollicitudin ullamcorper faucibus. Duis tellus dui, pharetra et augue vel, facilisis elementum tortor. Nunc malesuada lorem at lectus elementum posuere ac et nisi. Maecenas eget mollis tortor. Pellentesque posuere, eros in dignissim commodo, leo felis dictum ipsum, eget imperdiet mauris metus ac felis. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Quisque lectus dui, interdum in enim in, aliquet vulputate velit. In hac habitasse platea dictumst. Cras ipsum neque, aliquet non finibus at, imperdiet ut nisl. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nulla iaculis eu lectus et congue. Aliquam erat volutpat. Pellentesque pellentesque elit vitae nunc luctus, in blandit felis dapibus.",
        "category": "Lorem",
        "icon": "www.path-to-icon.path/icon.svg",
        "main_image": "www.path-to-image.path/icon.svg",
        "scheduled_date": "1547812245",
        "published": true,
        "timestamp": "1547812245",
        "author": "Admin"
      },
      {
        "id": 5,
        "title": "Lorem ipsum dolor sit amet",
        "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean elementum sollicitudin porttitor. Pellentesque ligula lectus, molestie vel pharetra ac, scelerisque ut nibh. Nunc consequat auctor tempus. Fusce pretium molestie nunc, ut tincidunt metus venenatis nec. Proin rutrum fringilla condimentum. Ut sed arcu eu diam sollicitudin semper. Sed vitae diam vel quam rhoncus scelerisque. Praesent tellus turpis, placerat eu orci vitae, efficitur pretium magna. Sed pellentesque sem accumsan vehicula blandit. Donec in cursus risus, vel suscipit erat. Donec metus nunc, aliquet sit amet ornare eget, cursus vel urna. Suspendisse bibendum feugiat lorem, vitae dictum massa luctus id.",
        "category": "Lorem",
        "icon": "www.path-to-icon.path/icon.svg",
        "main_image": "www.path-to-image.path/icon.svg",
        "scheduled_date": "1547812081",
        "published": true,
        "timestamp": "1547812081",
        "author": "Admin"
      }];

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
