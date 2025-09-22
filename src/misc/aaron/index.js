(function() {
"use strict";

class MathHelpers {
  static getMiles(l1, l2) {
    l1 = new google.maps.LatLng(l1.lat, l1.lng);
    l2 = new google.maps.LatLng(l2.lat, l2.lng);
    let meters = google.maps.geometry.spherical.computeDistanceBetween(l1, l2);
    return meters / 1609.344;
  }

  static dateDiff(d2, d1) {
    let diff = d2 - d1;
    return isNaN(diff) ? NaN : {
      diff : diff,
      ms : Math.floor( diff            % 1000 ),
      s  : Math.floor( diff /     1000 %   60 ),
      m  : Math.floor( diff /    60000 %   60 ),
      h  : Math.floor( diff /  3600000 %   24 ),
      d  : (diff / 86400000).toFixed(1)
    };
  }

  static mod(x, y) {
    return ((x % y) + y) % y;
  }

  static formatDate(d) {
    return d.getFullYear() + "/" + (d.getMonth()+1) + "/" + d.getDate() + " " + d.toLocaleTimeString();
  }
}

class Tweet {
  constructor(aaronsJourney, tweetJson) {
    _.extend(this, tweetJson);
    this.date = new Date(this.created_at);
    this.aaronsJourney = aaronsJourney;
    if(this.latitude && this.longitude) {
      this.lat_lng = { lat: this.latitude, lng: this.longitude };
      this.marker = new google.maps.Marker({
        map: this.aaronsJourney.map,
        position: this.lat_lng,
        title: this.text,
        animation: google.maps.Animation.DROP,
      });

      this.marker.addListener('click', this.showInfo.bind(this));
    }
  }

  getNextTweet(delta) {
    let tweets = this.aaronsJourney.tweets;
    let currentIndex = _.indexOf(tweets, this);
    return tweets[MathHelpers.mod(currentIndex + delta, tweets.length)];
  }

  toHtml() {
    let links = "";
    let regex = /(http:\/\/[^\s]*)/gi;
    let last = 0;
    let img_link_count = 0;
    let match;
    while(match = regex.exec(this.text)) {
      links += this.text.substring(last, match.index);

      let pictar = (/http:\/\/twitgoo.*/).test(match[0]);
      if(pictar) {
        let image = "<img width='200px' src='" + this.image_urls[img_link_count] + "' />";
        links += "<a target='_blank' href='" + this.image_urls[img_link_count] + "'>" + image + "</a>";
        img_link_count++;
      } else {
        links += "<a target='_blank' href='" + match[0] + "'>" + match[0] + "</a>";
      }
      last = match.index + match[0].length;
    }
    links += this.text.substring(last);

    let firstMarkedTweet = _.find(this.aaronsJourney.tweets, function(tweet) { return tweet.lat_lng; });
    let markedTweet = this.findThisOrPreviousMarkedTweet();
    let previousTweet = (this == firstMarkedTweet ? this : this.getNextTweet(-1)).findThisOrPreviousMarkedTweet();

    let day = MathHelpers.dateDiff(this.date, firstMarkedTweet.date).d;
    let distanceHome;
    let distanceToday;
    let distanceTotal;
    if(markedTweet) {
      distanceHome = MathHelpers.getMiles(markedTweet.lat_lng, firstMarkedTweet.lat_lng);
      distanceToday = MathHelpers.getMiles(markedTweet.lat_lng, previousTweet.lat_lng);
      // You may instead use computeLength() to calculate the length of a given path if you have several locations.
      // distanceTotal = last_marked_tweet.distance_total + tweet.distance_today;
      distanceTotal = distanceHome;
    } else {
      distanceHome = 0;
      distanceToday = 0;
      distanceTotal = 0;
    }

    let str = MathHelpers.formatDate(this.date) + " <b>Day " + (day) + "</b> ";
    str += "<br/>" + distanceToday.toFixed(1) + " miles since last marked tweet / " + distanceTotal.toFixed(1) + " total / " + distanceHome.toFixed(1) + " from home";
    str += " / " + (distanceTotal/day).toFixed(2) + " ave miles/day";
    str += "<br/><a target='_blank' href='http://twitter.com/Aaron2Phipps'><img style='margin-right: 3px;' align='left' src='https://pbs.twimg.com/profile_images/753528282/ollie_and_aaron_bigger.jpg' /></a>" + links;
    return "<div><p>" + str + "</p></div>";
  }

  showInfo() {
    if(Tweet.lastVisibleTweet) {
      Tweet.lastVisibleTweet.infoWindow.close();
      delete Tweet.lastVisibleTweet.infoWindow;
    }

    let markedTweet = this.findThisOrPreviousMarkedTweet();
    if(markedTweet) {
      this.infoWindow = new google.maps.InfoWindow({ content: this.toHtml() });
      this.infoWindow.open(this.aaronsJourney.map, markedTweet.marker);
      Tweet.lastVisibleTweet = this;
    }
  }

  findThisOrPreviousMarkedTweet() {
    // Find the nearest tweet with a marker.
    let tweets = this.aaronsJourney.tweets;
    var markedTweet = this;
    let count = 0;
    while(count++ < tweets.length && !markedTweet.marker) {
      markedTweet = markedTweet.getNextTweet(-1);
    }
    return markedTweet;
  }
}

class AaronsJourney {
  constructor() {
    this.map = null;
    this.polyline = null;
    this.tweets = [];
  }

  initMap() {
    this.map = new google.maps.Map(document.getElementById("map"), {
      // Center on the US
      center: { lat: 39, lng: -95 },
      zoom: 4,
      keyboardShortcuts: false,
    });
  }

  getMarkedTweets() {
    return _.select(this.tweets, function(tweet) { return tweet.lat_lng; });
  }

  showNextTweet(delta) {
    let nextTweet;
    if(Tweet.lastVisibleTweet) {
      nextTweet = Tweet.lastVisibleTweet.getNextTweet(delta);
    } else {
      nextTweet = this.tweets[0];
    }
    if(nextTweet) {
      nextTweet.showInfo();
    }
  }

  addTweetsJson(newTweetsJson) {
    this.tweets = this.tweets.concat(newTweetsJson.map(function(tweetJson) { return new Tweet(this, tweetJson); }.bind(this)));
    this.tweets.sort(function(a, b) { return a.date - b.date; });

    let getMarkedTweets = this.getMarkedTweets();
    let path = _.pluck(getMarkedTweets, 'lat_lng');
    if(this.polyline) {
      // If we'd already set a polyline, remove it before creating a new one.
      this.polyline.setMap(null);
    }
    this.polyline = new google.maps.Polyline({
      path: path,
      geodesic: true,
      strokeColor: '#FF0000',
      strokeOpacity: 1.0,
      strokeWeight: 2
    });
    this.polyline.setMap(this.map);
  }
}

let aaronsJourney = new AaronsJourney();
$(function() {

  let foundTweetIds = {};
  function doGrabTweets(maxTweetId) {
    $.ajax('https://zaos6o2edd.execute-api.us-west-2.amazonaws.com/prod/getAaronTweets', {
        type: "get",
        data: {
          count: 10,
          max_id: maxTweetId,
        },
      })
      .done(function(newTweetsJson, textStatus, jqXHR) {
        newTweetsJson = _.filter(newTweetsJson, function(tweet) { return !foundTweetIds[tweet.id]; });
        newTweetsJson.forEach(function(newTweet) { foundTweetIds[newTweet.id] = true; });
        if(newTweetsJson.length > 0) {
          // If we actually found any new tweets, go ahead and map them, and then query for more.
          aaronsJourney.addTweetsJson(newTweetsJson);
          let lastTweet = newTweetsJson[newTweetsJson.length - 1];
          doGrabTweets(lastTweet.id);
        }
      })
      .fail(function(jqXHR, textStatus, errorThrown) {
        throw new Error(errorThrown);
      });
  }
  doGrabTweets();

  $(window).on("keydown", function(e) {
    if(e.which == 37) { // left arrow key
      aaronsJourney.showNextTweet(-1);
    } else if(e.which == 39) { // right arrow key
      aaronsJourney.showNextTweet(1);
    }
  });

  $('#previousTweet').click(function() {
    aaronsJourney.showNextTweet(-1);
  });

  $('#nextTweet').click(function() {
    aaronsJourney.showNextTweet(1);
  });
});

window.initMap = function() { aaronsJourney.initMap(); };

})();
