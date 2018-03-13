import React, {Component} from 'react'


export default class Bars extends Component {
  constructor(props) {
    super(props);
  }

  render() {

    const {scales, margins, data, svgDimensions} = this.props;
    const {xScale, yScale} = scales;
    const {width} = svgDimensions;

    const detractorBars = (
      data.map(datum =>
        <rect
          key={datum.segment + 'detractor'}
          x={xScale(-datum.detractors - 0.5 * datum.neutral)}
          y={yScale(datum.segment)}
          height={yScale.bandwidth()}
          width={datum.detractors * (width - margins.left)/200}
          fill={'#F44336'}
        />,
      )
    );
    const neutralBars = (
      data.map(datum =>
        <rect
          key={datum.segment + 'neutral'}
          x={xScale(-0.5*datum.neutral)}
          y={yScale(datum.segment)}
          height={yScale.bandwidth()}
          width={datum.neutral * (width - margins.left)/200}
          fill={'#9E9E9E'}
        />
      )
    );
    const promoterBars = (
      data.map(datum =>
        <rect
          key={datum.segment + 'promoter'}
          x={xScale(0.5*datum.neutral)}
          y={yScale(datum.segment)}
          height={yScale.bandwidth()}
          width={datum.promoters * (width - margins.left)/200}
          fill={'#4CAF50'}
        />
      )
    );
    const npsCircle=(
      data.map(datum =>
        <circle
          fill="white"
          key={datum.segment + 'npscircle'}
          cx={xScale(datum.nps_score)}
          cy={yScale(datum.segment) + 0.5 * yScale.bandwidth()}
          r={0.4 * yScale.bandwidth()}
        />
      )
    );
    const npsText = (
      data.map(datum =>
        <text
          key={datum.segment + 'npsscore'}
          x={xScale(datum.nps_score)}
          y={yScale(datum.segment) + 0.6 * yScale.bandwidth()}
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