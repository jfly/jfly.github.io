//+ Jonas Raoni Soares Silva
//@ http://jsfromhell.com/array/shuffle [v1.0]
function shuffle(o){ //v1.0
    for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
    return o;
};

function CardCtrl($scope, $timeout) {
    var cardNames = []
    for(var i = 0; i < AMGTCategories.length; i++) {
        var cat = AMGTCategories[i];
        //if(i != 2) { continue; }
        for(var j = 0; j < cat.images.length; j++) {
           cardNames.push(cat.images[j]);
        }
    }


    var DUPLICATE_CARD_COUNT = 2;
    function initialize() {
        $scope.cards = [];
        for(var n = 0; n < DUPLICATE_CARD_COUNT; n++) {
            for(var i = 0; i < cardNames.length; i++) {
                var card = {};
                card.name = cardNames[i];
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
    $scope.getElapsedTimeStr = function() {
        var elapsed = $scope.getElapsedTime();
        if(elapsed === null) {
            return "Click any card to start";
        }
        if($scope.endTime === null) {
            return Math.floor(elapsed);
        } else {
            return elapsed.toFixed(2);
        }
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
                alert("You finished in " + $scope.getElapsedTimeStr() + " seconds.");
                initialize();
            }, animationTime);
        }
    };
    $scope.remainingCards = function() {
        return $scope.cards.filter(function(card) { return !card.found; });
    };
}
