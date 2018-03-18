import React, { Component } from 'react'
import { scaleBand, scaleLinear } from 'd3-scale'
import Axes from './Axes';
import ClientBars from './ClientBars';

class Chart extends Component {
  constructor() {
    super();
    // scaleBand domain should be an array of specific values
    this.yScale = scaleBand();
    // scaleLinear domain required at least two values, min and max
    this.xScale = scaleLinear();
  }

  render() {
    let { data }= this.props;

    const margins = { top: 20, right: 20, bottom: 50, left: 120 };
    const svgDimensions = { width: this.props.width, height: this.props.height };

    const xScale = this.xScale
      .domain([-100, 100])
      .range([margins.left, svgDimensions.width - margins.right]);

    const yScale = this.yScale
      .padding(0.3)
      .domain(data.map(d => d.survey))
      .range([svgDimensions.height - margins.bottom, margins.top]);


    return (
      <svg width={svgDimensions.width} height={svgDimensions.height}>
        <Axes
          scales={{ xScale, yScale }}
          margins={margins}
          svgDimensions={svgDimensions}
          axisLabel={'Percent of Clients'}
        />
        <ClientBars
          scales={{ xScale, yScale }}
          margins={margins}
          data={data}
          svgDimensions={svgDimensions}
        />
      </svg>
    )
  }
}

export default Chart;