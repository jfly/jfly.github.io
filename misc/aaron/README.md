# Aaron's Journey

## Directions
- `cd lambda`
  - `npm install`
  - Populate `.env` with your Twitter application's CONSUMER_KEY and CONSUMER_SECRET (available [here](https://apps.twitter.com/app/8983262/keys))
  - `zip -r ../dist/lambda.zip .` and upload it at <https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions/getAaronTweets>.

## Test it out locally
- `cd lambda`
- `node -e "require('./index').handler({}, { succeed: console.log })"`

## Areas for improvement
- Could look into <https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions/getAaronTweets>.
