//+ Jonas Raoni Soares Silva
//@ http://jsfromhell.com/array/shuffle [v1.0]
function shuffle(o){ //v1.0
    for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
    return o;
};

function getJsonFromUrlParams(params) {
    var query = params.substr(1);
    var data = query.split("&");
    var result = {};
    for(var i=0; i<data.length; i++) {
        var item = data[i].split("=");
        result[item[0]] = item[1];
    }
    return result;
}

angular.module('myapp').directive('focusOn', function() {
   return function(scope, elem, attr) {
      scope.$watch(attr.focusOn, function(newValue, oldValue) {
          if(newValue) {
              // This element isn't necessarily visible yet,
              // so we wait a moment.
              setTimeout(function() {
                  elem[0].focus();
                  elem[0].select();
              }, 0);
          }
      });
   };
});

function MemoryGameCtrl($scope, $timeout, angularFireCollection) {
    var DUPLICATE_CARD_COUNT = 2;
    var HIGH_SCORE_LIST_SIZE = 10;

    $scope.cardNames = []
    for(var i = 0; i < AMGTCategories.length; i++) {
        var cat = AMGTCategories[i];
        for(var j = 0; j < cat.images.length; j++) {
           $scope.cardNames.push(cat.images[j]);
        }
    }

    // We're hardcoding a 5x4 size game.
    //$scope.cardCount = $scope.cardNames.length;
    $scope.cardCount = 10;

    var allHighScoresRef = new Firebase("https://american-history-game.firebaseio.com/highScores");
    var highScoresRef = allHighScoresRef.child($scope.cardCount);
    var highScoresView = highScoresRef.startAt().limit(HIGH_SCORE_LIST_SIZE);
    $scope.highScores = angularFireCollection(highScoresView);

    try {
        $scope.name = localStorage.getItem("name") || "";
    } catch(e) {
        console.log(e);
        $scope.name = "";
    }
    $scope.$watch("name", function() {
        localStorage.setItem("name", $scope.name);
    }, true);

    $scope.showHighScores = false;
    $scope.showWelcomeScreen = true;
    $scope.myScore = null;


    function initialize() {
        $scope.cards = [];
        var cardNamesCopy;
        cardNamesCopy = $scope.cardNames.slice(0, parseInt($scope.cardCount));
        for(var i = 0; i < cardNamesCopy.length; i++) {
            for(var n = 0; n < DUPLICATE_CARD_COUNT; n++) {
                var card = {};
                card.name = cardNamesCopy[i];
                card.visible = false;
                card.found = false;
                card.animating = false;
                card.url = "images/cards/AM GT" + card.name + ".png";
                card.urlCss = { 'background-image': 'url("images/cards/AM GT ' + card.name + '.png")' };

                $scope.cards.push(card);
            }
        }
        shuffle($scope.cards);

        $scope.startTime = null;
        $scope.now = null;
        $scope.endTime = null;
        $scope.visibleCards = [];
    }
    initialize();

    $scope.play = function() {
        initialize();
        $scope.showHighScores = false;
        $scope.showWelcomeScreen = false;
    };

    $scope.getElapsedTime = function() {
        if($scope.startTime === null) {
            return null;
        }
        var end = ($scope.endTime !== null ? $scope.endTime : $scope.now );
        if(end === null) {
            return 0;
        }
        var elapsed = (end - $scope.startTime)/1000.0;
        return Math.max(0, elapsed);
    };
    var tick = function() {
        $scope.now = Date.now();
        $timeout(tick, 500);
    };
    $timeout(tick, 500);

    $scope.cardClicked = function(card) {
        if(card.animating || card.visible) {
            return;
        }
        if($scope.startTime === null) {
            $scope.startTime = Date.now();
        }
        if($scope.visibleCards.length > 0) {
            // If the user has already selected a card, check
            // if this is the same kind.
            var alreadySelectedCard = $scope.visibleCards[0];
            if(alreadySelectedCard.name == card.name) {
                card.visible = true;
                $scope.visibleCards.push(card);
            } else {
                // 1. Flip this card over, so the user can see it.
                // 2. Make it obvious to the user that these cards don't match.
                var animatingCards = [];
                $scope.visibleCards.push(card);
                while($scope.visibleCards.length > 0) {
                    var newCard = $scope.visibleCards.pop();
                    newCard.visible = true;
                    newCard.wrongChoice = true;
                    newCard.animating = true;
                    animatingCards.push(newCard);
                }
                // 3. Wait for animation to complete, then flip all the cards
                //    back upside down.
                $timeout(function() {
                    for(var i = 0; i < animatingCards.length; i++) {
                        var newCard = animatingCards[i];
                        newCard.visible = false;
                        newCard.wrongChoice = false;
                        newCard.animating = false;
                    }
                }, animationTime);
                return;
            }
        } else {
            card.visible = true;
            $scope.visibleCards.push(card);
        }

        if($scope.visibleCards.length == DUPLICATE_CARD_COUNT) {
            // The user just found a set! We can make these cards disappear.
            while($scope.visibleCards.length > 0) {
                var newCard = $scope.visibleCards.pop();
                newCard.found = true;
            }
        }

        if($scope.remainingCards().length == 0) {
            $scope.endTime = Date.now();
            $timeout(function() {
                $scope.showHighScores = true;
                var elapsed = $scope.getElapsedTime();
                $scope.myScore = {
                    name: $scope.name,
                    value: elapsed
                };
                $scope.addHighScore($scope.myScore);
            }, animationTime);
        }
    };
    
    $scope.$watch("name", function(newValue, oldValue) {
        if($scope.myScore && $scope.newHighScoreRef) {
            $scope.myScore.name = newValue;
            $scope.newHighScoreRef.child("name").set(newValue);
        }
    });

    $scope.isHighScore = function(score) {
        return 
        if(!score) {
            return false;
        }
        var hsList = $scope.highScores;
        if(hsList.indexOf(score) >= 0) {
            // this score is already a high score;
            return true;
        }
        var worstHighScore = hsList[hsList.length-1];
        return hsList.length < HIGH_SCORE_LIST_SIZE || score.value < worstHighScore.value;
    };
    $scope.newHighScoreRef = null;
    $scope.addHighScore = function(score) {
        $scope.newHighScoreRef = highScoresRef.push();
        $scope.newHighScoreRef.setWithPriority(score, score.value);
    };
    $scope.remainingCards = function() {
        return $scope.cards.filter(function(card) { return !card.found; });
    };
}
