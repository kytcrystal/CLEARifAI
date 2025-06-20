import React, { useEffect, useRef } from "react";
import * as echarts from "echarts";

function RadarChart({ values }) {
  const chartRef = useRef(null);

  useEffect(() => {

    if (!values) return;

    const chart = echarts.init(chartRef.current);

    const option = {
      title: {
        // text: "CLEAR Radar Chart",
        left: "left",
        textStyle: {
          fontSize: 20,
          color: "white"
        },
      },
      backgroundColor: "#21264c",
      tooltip: {},
      radar: {
        indicator: [
          { name: "C", max: 1 },
          { name: "L", max: 1 },
          { name: "E", max: 1 },
          { name: "A", max: 1 },
          { name: "R", max: 1 },
        ],
        radius: "80%",
        center: ['50%', '50%']
      },
      series: [
        {
          name: "CLEAR Scores",
          type: "radar",
          data: [
            {
              value: Object.values(values),
              name: "Meeting Score",
              areaStyle: {
                color: "rgba(100, 149, 237)",
              },
              lineStyle: {
                color: "cornflowerblue",
              },
              symbol: "circle",
              symbolSize: 6,
              itemStyle: {
                color: "cornflowerblue",
              },
            },
          ],
        },
      ],
    };

    chart.setOption(option);

    // Resize on container size change
    const handleResize = () => chart.resize();
    window.addEventListener("resize", handleResize);

    return () => {
      chart.dispose();
      window.removeEventListener("resize", handleResize);
    };
  }, [values]);

  return (
    <div
      ref={chartRef}
      style={{
        width: "100%",
        maxWidth: "600px",
        height: "400px",
        margin: "1rem auto",
      }}
    />
  );
}

export default RadarChart;
