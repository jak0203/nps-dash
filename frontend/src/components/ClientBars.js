import React, {Component} from 'react';

export default class ClientBars extends Component {
  render() {
    const {scales, margins, data, svgDimensions} = this.props;
    const {xScale, yScale} = scales;
    const {width} = svgDimensions;

    const negativeBars = (
      data.map(datum =>
        <rect
        key={datum.survey + 'negative'}
        x={xScale(-datum.percent_clients_negative)}
        y={yScale(datum.survey)}
        width={datum.percent_clients_negative * (width - margins.left)/200}
        height={yScale.bandwidth()}
        fill={'#F44336'}
        />
      )
    );
    const positiveBars = (
      data.map(datum =>
      <rect
        key={datum.survey + 'positive'}
        x={xScale(0)}
        y={yScale(datum.survey)}
        width={datum.percent_clients_positive * (width - margins.left)/200}
        height={yScale.bandwidth()}
        fill={'#4CAF50'}
        />
      )
    );
  return (
    <g>
      {negativeBars}
      {positiveBars}
    </g>
  )
  }

}