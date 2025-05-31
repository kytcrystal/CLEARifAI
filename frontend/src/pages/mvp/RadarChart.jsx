import React, { useEffect, useRef } from "react";
import * as echarts from "echarts";

function RadarChart({ values }) {
  const chartRef = useRef(null);

  useEffect(() => {
    console.log("Radar values:", values);

    if (!values) return;

    const chart = echarts.init(chartRef.current);

    const option = {
      title: {
        text: "CLEAR Radar Chart",
        left: "center",
        textStyle: {
          fontSize: 22,
        },
      },
      backgroundColor: "#f0f0f0",
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
        margin: "2rem auto",
      }}
    />
  );
}

export default RadarChart;
