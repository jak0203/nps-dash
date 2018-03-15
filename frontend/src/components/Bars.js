import React, {Component} from 'react'


export default class Bars extends Component {
  render() {

    const {scales, margins, data, svgDimensions} = this.props;
    const {xScale, yScale} = scales;
    const {width} = svgDimensions;

    const detractorBars = (
      data.map(datum =>
        <rect
          key={datum.survey + 'detractor'}
          x={xScale(-datum.percent_detractors - 0.5 * datum.percent_neutral)}
          y={yScale(datum.survey)}
          height={yScale.bandwidth()}
          width={datum.percent_detractors * (width - margins.left)/200}
          fill={'#F44336'}
        />,
      )
    );
    const neutralBars = (
      data.map(datum =>
        <rect
          key={datum.survey + 'neutral'}
          x={xScale(-0.5*datum.percent_neutral)}
          y={yScale(datum.survey)}
          height={yScale.bandwidth()}
          width={datum.percent_neutral * (width - margins.left)/200}
          fill={'#9E9E9E'}
        />
      )
    );
    const promoterBars = (
      data.map(datum =>
        <rect
          key={datum.survey + 'promoter'}
          x={xScale(0.5*datum.percent_neutral)}
          y={yScale(datum.survey)}
          height={yScale.bandwidth()}
          width={datum.percent_promoters * (width - margins.left)/200}
          fill={'#4CAF50'}
        />
      )
    );
    const npsCircle=(
      data.map(datum =>
        <circle
          fill="white"
          key={datum.survey + 'npscircle'}
          cx={xScale(datum.nps_score)}
          cy={yScale(datum.survey) + 0.5 * yScale.bandwidth()}
          r={0.4 * yScale.bandwidth()}
        />
      )
    );
    const npsText = (
      data.map(datum =>
        <text
          key={datum.survey + 'npsscore'}
          x={xScale(datum.nps_score)}
          y={yScale(datum.survey) + 0.6 * yScale.bandwidth()}
          textAnchor={"middle"}
          fontSize={11}
        >{datum.nps_score}</text>
      )
    );

    return (
      <g>
        {detractorBars}
        {neutralBars}
        {promoterBars}
        {npsCircle}
        {npsText}
      </g>
    )
  }
}