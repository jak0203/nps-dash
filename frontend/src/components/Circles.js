import React, {Component} from 'react';


export default class Circles extends Component {
  render() {
    const {scales, data } = this.props;
    const {xScale, yScale} = scales;

    const circles = (
      data.map(datum =>
        <circle
          fill={(datum.delta_from_2016 < 0 ) ? '#F44336' : '#4CAF50'}
          key={datum.client}
          cx={xScale(datum.nps_score)}
          cy={yScale(datum.products) + 0.5 * yScale.bandwidth()}
          r={(Math.abs(datum.delta_from_2016) / 100) * yScale.bandwidth()}
          stroke='black'
          strokeWidth={1}
        />
      )
    );

    return (
      <g>
        {circles}
      </g>
    )
  }
}