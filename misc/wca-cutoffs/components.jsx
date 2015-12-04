(function() {

let SOLVES_TO_MAKE_CUTOFF = 2;
let SOLVES_IN_ROUND = 5

let SolveTd = React.createClass({
  render() {
    let solveTime = this.props.solveTime;
    let cls = classNames({
      'text-right': true,
      "would-not-have-happened": solveTime.wouldNotHaveHappened,
      "would-have-DNFed": solveTime.wouldHaveDNFed,
    });
    return (
      <td className={cls}>
        {jChester.solveTimeToStopwatchFormat(solveTime)}
      </td>
    );
  },
});

let ResultRow = React.createClass({
  render() {
    let result = this.props.result;
    return (
      <tr>
        <td title={result.name}>{result.name}</td>
        {result.solves.map((solveTime, i) => <SolveTd key={i} solveTime={solveTime} />)}
      </tr>
    );
  },
});

let ResultsTable = React.createClass({
  render() {
    return (
      <div className="table-responsive">
        <table className="table table-striped table-condensed table-nonfluid">
          <thead>
            <tr>
              <th>Name</th>
              <th colSpan={SOLVES_IN_ROUND}>Solves</th>
            </tr>
          </thead>
          <tbody>
            {this.props.results.map((result, i) => <ResultRow key={i} result={result} />)}
          </tbody>
        </table>
      </div>
    );
  },
});

let RoundAnalysis = React.createClass({
  render() {
    let results = this.props.results.map(result => {
      let madeCutoff = (
        !this.props.cutoff ||
        _.any(result.solves.slice(0, SOLVES_TO_MAKE_CUTOFF), solveTime => solveTime.millis <= this.props.cutoff.millis)
      );
      let cumulativeTimeSpentMillis = 0;
      let solves = result.solves.map((solveTime, i) => {
        let wouldNotHaveHappened = !madeCutoff && i >= SOLVES_TO_MAKE_CUTOFF;
        let wouldHaveDNFed = this.props.timeLimit && solveTime.millis > this.props.timeLimit.millis;
        if(wouldHaveDNFed) {
          solveTime = this.props.timeLimit;
        }

        if(this.props.cumulativeTimeLimit) {
          if(cumulativeTimeSpentMillis > this.props.cumulativeTimeLimit.millis) {
            wouldNotHaveHappened = true;
          } else {
            cumulativeTimeSpentMillis += solveTime.millis;
            if(cumulativeTimeSpentMillis > this.props.cumulativeTimeLimit.millis) {
              wouldHaveDNFed = true;
              let millisOver = cumulativeTimeSpentMillis - this.props.cumulativeTimeLimit.millis;
              solveTime = { millis: solveTime.millis - millisOver, decimals: 2 };
            }
          }
        }
        return _.extend({}, solveTime, { wouldNotHaveHappened, wouldHaveDNFed });
      });
      return {
        name: result.name,
        solves: solves,
      }
    });

    let allSolves =  _(results).pluck('solves').flatten().value();
    let wouldHaveDNFedSolves = allSolves.filter(solve => solve.wouldHaveDNFed);

    let totalMillisSolving = _(allSolves).filter(solve => !solve.wouldNotHaveHappened).sum(solve => solve.millis);

    var isSuccessfulSolve = solve => !solve.wouldHaveDNFed && !solve.wouldNotHaveHappened;
    let resultsBySuccessfulSolveCount = _.groupBy(results, result => {
      return result.solves.filter(isSuccessfulSolve).length;
    });

    let resultsWithAnAverage = (resultsBySuccessfulSolveCount[4] || []).concat(resultsBySuccessfulSolveCount[5] || []);

    return (
      <div>
        <ul>
          {_.range(SOLVES_IN_ROUND + 1).map(solveCount => {
            return (
              <li key={solveCount}>
                {solveCount} solves: {(resultsBySuccessfulSolveCount[solveCount] || []).length} people
              </li>
            )
          })}
          <li>
            {results.length} people spent a total of
            {' '}{jChester.solveTimeToStopwatchFormat({ millis: totalMillisSolving, decimals: 2 })}{' '}
            doing {allSolves.filter(isSuccessfulSolve).length} successful solves
          </li>
          <li>
            {wouldHaveDNFedSolves.length} DNFs
            due to (cumulative and not cumulative) time limit
            led to {jChester.solveTimeToStopwatchFormat({ millis: _.sum(wouldHaveDNFedSolves, solve => solve.millis), decimals: 2 })} "wasted" time
          </li>
          <li>
            {resultsWithAnAverage.length} people got an average, {results.length - resultsWithAnAverage.length} did not
          </li>
        </ul>

        <ResultsTable results={results} />
      </div>
    );
  },
});

wca_cutoffs.components = wca_cutoffs.components || {};
wca_cutoffs.components.RoundAnalysis = RoundAnalysis;

})();
