
import React, { Component } from 'react'
import { scaleBand, scaleLinear } from 'd3-scale'
import Axes from './Axes';
import Bars from './Bars';

class Chart extends Component {
  constructor() {
    super();
    // scaleBand domain should be an array of specific values
    this.yScale = scaleBand();
    // scaleLinear domain required at least two values, min and max
    this.xScale = scaleLinear();
  }

  render() {
    let { nps_data }= this.props;

    const margins = { top: 20, right: 20, bottom: 50, left: 100 };
    const svgDimensions = { width: this.props.width, height: this.props.height };

    const xScale = this.xScale
      .domain([-100, 100])
      .range([margins.left, svgDimensions.width - margins.right]);

    const yScale = this.yScale
      .padding(0.3)
      .domain(nps_data.reverse().map(d => d.survey))
      .range([svgDimensions.height - margins.bottom, margins.top]);

    return (
      <svg width={svgDimensions.width} height={svgDimensions.height}>
        <Axes
          scales={{ xScale, yScale }}
          margins={margins}
          svgDimensions={svgDimensions}
        />
        <Bars
          scales={{ xScale, yScale }}
          margins={margins}
          data={nps_data}
          svgDimensions={svgDimensions}
        />
      </svg>
    )
  }
}

export default Chart;