import React, {Component} from 'react'


export default class Bars extends Component {
  constructor(props) {
    super(props);
  }

  render() {

    const {scales, margins, data, svgDimensions} = this.props;
    const {xScale, yScale} = scales;
    // const {width} = svgDimensions;

    const detractorBars = (
      data.map(datum =>
        <rect
          key={datum.segment + 'detractor'}
          x={margins.left}
          y={yScale(datum.segment)}
          height={yScale.bandwidth()}
          width={scales.xScale(datum.detractors) - margins.left}
          fill={'#F44336'}
        />,
      )
    );
    const neutralBars = (
      data.map(datum =>
        <rect
          key={datum.segment + 'neutral'}
          x={xScale(datum.detractors)}
          y={yScale(datum.segment)}
          height={yScale.bandwidth()}
          width={scales.xScale(datum.neutral) - margins.left}
          fill={'#9E9E9E'}
        />
      )
    );
    const promoterBars = (
      data.map(datum =>
        <rect
          key={datum.segment + 'promoter'}
          x={xScale(datum.detractors) + xScale(datum.neutral) - margins.left}
          y={yScale(datum.segment)}
          height={yScale.bandwidth()}
          width={scales.xScale(datum.promoters) - margins.left}
          fill={'#4CAF50'}
        />
      )
    );
    return (
      <g>
        {detractorBars}
        {neutralBars}
        {promoterBars}
      </g>
    )
  }
}