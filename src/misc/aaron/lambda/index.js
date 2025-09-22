#!/usr/bin/env node
"use strict";

require("dotenv").load({ silent: true });

var async = require('async');
var request = require('request');
var querystring = require('querystring');

var MAX_TWEETS_DEFAULT = 10;
var MAX_SIMULTANEOUS_REQUESTS = 10;
var CONSUMER_KEY = process.env.CONSUMER_KEY;
var CONSUMER_SECRET = process.env.CONSUMER_SECRET;
var BEARER_TOKEN = new Buffer(CONSUMER_KEY + ":" + CONSUMER_SECRET).toString("base64");

exports.handler = function(event, context) {
  var maxTweets = event.count || MAX_TWEETS_DEFAULT;
  request.post('https://api.twitter.com/oauth2/token', {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
      'Authorization': 'Basic ' + BEARER_TOKEN,
    },
    form: {
      grant_type: 'client_credentials',
    }
  }, function(error, response, body) {
    if(error) {
      throw new Error(error);
    }
    body = JSON.parse(body);
    if(body.token_type !== "bearer") {
      throw new Error("Unrecognized token_type: " + body.token_type);
    }
    var accessToken = body.access_token;

    var queryParams = {
      count: maxTweets,
      screen_name: 'Aaron2Phipps',
      user_id: '123145688',
    };
    if(event.since_id) {
      queryParams.since_id = event.since_id;
    }
    if(event.max_id) {
      queryParams.max_id = event.max_id;
    }
    var queryStr = querystring.stringify(queryParams);
    request.get('https://api.twitter.com/1.1/statuses/user_timeline.json?' + queryStr, {
      headers: {
        'Authorization': 'Bearer ' + accessToken,
      },
    }, function(error, response, body) {
      if(error) {
        throw new Error(error);
      }
      var tweets = JSON.parse(body);
      var asyncTasks = [];
      tweets.forEach(function(tweet) {

        var parseGoogleMapsUrl = function(googleMapsUrl) {
					var floatReg = "-?[0-9]+\.[0-9]+";
					var lat_long = googleMapsUrl.match("(" + floatReg + "),(" + floatReg + ").*");
					if(lat_long) {
						tweet.latitude = parseFloat(lat_long[1]);
            tweet.longitude = parseFloat(lat_long[2]);
          }
        };

				var tinyurlMatch = tweet.text.match("(http://is.gd/[^\\s]*)");
				var googleMapsUrlMatch = tweet.text.match("(http://maps.google.com/[^\\s]*)");
        if(googleMapsUrlMatch) {
          parseGoogleMapsUrl(googleMapsUrlMatch[0]);
        } else if(tinyurlMatch) {
          asyncTasks.push(function(done) {
            request({ url: tinyurlMatch[0], followRedirect: false }, function(e, response) {
              var googleMapsUrl = response.request.response.headers.location;
              parseGoogleMapsUrl(googleMapsUrl);
              done();
            });
          });
        }

        var imageUrls = tweet.text.match(/http:\/\/twitgoo.com[^\s]*/gi);
        if(imageUrls) {
          tweet.image_urls = [];
          imageUrls.forEach(function(imageUrl) {
            asyncTasks.push(function(done) {
              request({ url: imageUrl, followRedirect: false }, function(e, response) {
                var imageUrl = response.request.response.headers.location;
                tweet.image_urls.push(imageUrl);
                done();
              });
            });
          });
        }
      });

      async.parallelLimit(asyncTasks, MAX_SIMULTANEOUS_REQUESTS, function(error) {
        if(error) {
          throw new Error(error);
        }

        context.succeed(tweets);
      });
    });
  });
};
