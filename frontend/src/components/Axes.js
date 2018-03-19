import React from 'react'
import Axis from './Axis'

import './Axis.css'

export default ({ scales, margins, svgDimensions, axisLabel, graphTitle }) => {
  const { height, width } = svgDimensions;

  const xProps = {
    orient: 'Bottom',
    scale: scales.xScale,
    translate: `translate(0, ${height - margins.bottom})`,
    tickSize: height - margins.top - margins.bottom,
  };

  const yProps = {
    orient: 'Left',
    scale: scales.yScale,
    translate: `translate(${margins.left}, 0)`,
    tickSize: width - margins.left - margins.right,
  };

  const xLabel = (
    <text
      textAnchor={'middle'}
      y={(height)}
      x={((width + margins.left)/2)}
          fontWeight={'bold'}
    >{axisLabel}</text>
  );

   const GraphTitle = (
    <text
      fontSize={18}
      textAnchor={'middle'}
      y={(margins.top - 5)}
      x={((width)/2)}
      fontWeight={'bold'}
    >{graphTitle}</text>
  );


  return (
    <g>
      <Axis {...xProps} />
      <Axis {...yProps} />
      {xLabel}
      {GraphTitle}
    </g>
  )
}