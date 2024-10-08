import { Component, ElementRef, OnInit } from '@angular/core';
import * as d3 from 'd3';

// Define a type for your score data
interface ScoreData {
  date: Date;
  score: number;
}

@Component({
  selector: 'app-score-oscillator',
  templateUrl: './score-oscillator.component.html',
  styleUrls: ['./score-oscillator.component.scss']
})
export class ScoreOscillatorComponent implements OnInit {
  private margin = { top: 50, right: 50, bottom: 60, left: 60 };
  private width = 800 - this.margin.left - this.margin.right;
  private height = 400 - this.margin.top - this.margin.bottom;

  constructor(private elementRef: ElementRef) {}

  ngOnInit() {
    const fakeData: [string, number][] = [
      ["2024-10-01", 3],
      ["2024-10-02", 7],
      ["2024-10-03", 4],
      ["2024-10-04", 6],
      ["2024-10-05", 2],
      ["2024-10-06", 5],
      ["2024-10-07", 6],
      ["2024-10-08", 3],
      ["2024-10-09", 7],
      ["2024-10-10", 4],
      ["2024-10-11", 2],
      ["2024-10-12", 6],
      ["2024-10-13", 5],
      ["2024-10-14", 3],
      ["2024-10-15", 7],
      ["2024-10-16", 4],
      ["2024-10-17", 2],
      ["2024-10-18", 6],
      ["2024-10-19", 5],
      ["2024-10-20", 7],
      ["2024-10-21", 4],
      ["2024-10-22", 2],
      ["2024-10-23", 6],
      ["2024-10-24", 3],
      ["2024-10-25", 5],
      ["2024-10-26", 6],
      ["2024-10-27", 7],
      ["2024-10-28", 4],
      ["2024-10-29", 3],
      ["2024-10-30", 6],
      ["2024-10-31", 2],
      ["2024-11-01", 5],
      ["2024-11-02", 6],
      ["2024-11-03", 3],
      ["2024-11-04", 7],
      ["2024-11-05", 4],
      ["2024-11-06", 2],
      ["2024-11-07", 6],
      ["2024-11-08", 5],
      ["2024-11-09", 3],
      ["2024-11-10", 7],
      ["2024-11-11", 4],
      ["2024-11-12", 2],
      ["2024-11-13", 6],
      ["2024-11-14", 5],
      ["2024-11-15", 7],
      ["2024-11-16", 4],
      ["2024-11-17", 2],
      ["2024-11-18", 6],
      ["2024-11-19", 3],
      ["2024-11-20", 5],
      ["2024-11-21", 6],
      ["2024-11-22", 7],
      ["2024-11-23", 4],
      ["2024-11-24", 3],
      ["2024-11-25", 6],
      ["2024-11-26", 2],
      ["2024-11-27", 5],
      ["2024-11-28", 7],
      ["2024-11-29", 3],
      ["2024-11-30", 4]
    ];
    
    

    this.createChart(fakeData);
  }

  private createChart(data: [string, number][]) {
    const parseDate = d3.timeParse("%Y-%m-%d");

    const parsedData: ScoreData[] = data.map(d => ({
      date: parseDate(d[0]) || new Date(),
      score: +d[1]
    }));

    const container = d3.select(this.elementRef.nativeElement).select("#chart");

    this.width = parseInt(container.style("width"), 10) - this.margin.left - this.margin.right;
    this.height = parseInt(container.style("height"), 10) - this.margin.top - this.margin.bottom;

    const svg = d3.select("#chart")
      .append("svg")
      .attr("width", this.width + this.margin.left + this.margin.right)
      .attr("height", this.height + this.margin.top + this.margin.bottom)
      .attr("color", "whitesmoke")
      .append("g")
      .attr("transform", `translate(${this.margin.left}, ${this.margin.top})`); // Adjusted transform to account for margins

    const x = d3.scaleTime().range([0, this.width]);
    const y = d3.scaleLinear().range([this.height, 0]);

    const valueline = d3.line<ScoreData>()
      .x(d => x(d.date))
      .y(d => y(d.score));

    x.domain(d3.extent(parsedData, d => d.date) as [Date, Date]);
    y.domain([1, 7]);

    svg.append("rect")
      .attr("width", this.width)
      .attr("height", this.height)
      .style("fill", "black")
      .style("pointer-events", "all")
      .on("mousemove", (event) => {
        const [mouseX, mouseY] = d3.pointer(event);
      
        const bisectDate = d3.bisector((d: ScoreData) => d.date).left;
        const x0 = x.invert(mouseX);
        const i = bisectDate(parsedData, x0);
      
        const d0 = parsedData[i - 1];
        const d1 = parsedData[i];
        const dClosest = x0.getTime() - d0.date.getTime() > d1.date.getTime() - x0.getTime() ? d1 : d0;
      
        const closestX = x(dClosest.date);
        const closestY = y(dClosest.score);
      
        // Update the crosshair lines
        svg.selectAll(".vertical-crosshair-line")
          .data([closestX, closestY])
          .join("line")
          .attr("class", "vertical-crosshair-line")
          .attr("stroke", "white")
          .attr("stroke-dasharray", "5, 5")
          .attr("stroke-width", 1)
          .style("opacity", 1)
          .attr("x1", closestX)
          .attr("y1", 0)
          .attr("x2", closestX)
          .attr("y2", this.height);
      
        svg.selectAll(".horizontal-crosshair-line")
          .data([closestY])
          .join("line")
          .attr("class", "horizontal-crosshair-line")
          .attr("stroke", "white")
          .attr("stroke-dasharray", "5, 5")
          .attr("stroke-width", 1)
          .style("opacity", 1)
          .attr("x1", 0)
          .attr("y1", closestY)
          .attr("x2", this.width)
          .attr("y2", closestY);
      
        // Calculate tooltip position and shift left if it's near the right edge
        const tooltipWidth = 100 + tooltipPadding.left + tooltipPadding.right;
        const tooltipX = closestX + 10;
      
        const adjustedTooltipX = tooltipX + tooltipWidth > this.width
          ? closestX - tooltipWidth - 10 // Shift to the left if the tooltip goes beyond the chart width
          : tooltipX;
      
        // Update the tooltip
        tooltipRect
          .attr("x", adjustedTooltipX)
          .attr("y", closestY - 40)
          .style("opacity", 1);
      
        tooltipDateText
          .attr("x", adjustedTooltipX + tooltipPadding.left)
          .attr("y", closestY - 25 + tooltipPadding.top)
          .text(`Date: ${d3.timeFormat("%Y-%m-%d")(dClosest.date)}`)
          .style("opacity", 1);
      
        tooltipScoreText
          .attr("x", adjustedTooltipX + tooltipPadding.left)
          .attr("y", closestY - 10 + tooltipPadding.top)
          .text(`Score: ${dClosest.score}`)
          .style("opacity", 1);
      });

    // Add highlighted areas below score 2
    svg.append("rect")
      .attr("x", 0)
      .attr("y", y(2))
      .attr("width", this.width) // Ensure width matches the chart width
      .attr("height", this.height - y(2)) // height from score 2 to the bottom
      .attr("fill", "rgba(191, 0, 255, 0.2)").style("pointer-events", "none");; // Red with transparency

    // Add highlighted areas above score 6
    svg.append("rect")
      .attr("x", 0)
      .attr("y", 0)
      .attr("width", this.width) // Ensure width matches the chart width
      .attr("height", y(6)) // height from the top to score 6
      .attr("fill", "rgba(191, 0, 255, 0.2)").style("pointer-events", "none");; // Green with transparency

    // Line Color
    svg.append("path")
      .data([parsedData])
      .attr("class", "line")
      .attr("d", valueline)
      .attr("fill", "none")
      .attr("stroke", "#BF00FF") // Purple
      .attr("stroke-width", 1); // Reduced stroke width

    // Add red dots for scores ≥ 6 or ≤ 2
    parsedData.forEach(d => {
      if (d.score >= 6 || d.score <= 2) {
        svg.append("circle")
          .attr("cx", x(d.date)) // X position based on the date
          .attr("cy", y(d.score)) // Y position based on the score
          .attr("r", 3) // Radius of the dot
          .attr("fill", "#FF6601"); // Fill color
      }
    });

    const xAxis = svg.append("g")
      .attr("transform", `translate(0,${this.height})`)
      .call(d3.axisBottom(x).tickFormat(d => d instanceof Date ? d3.timeFormat("%Y-%m-%d")(d) : ''));

    // Set the color of the x-axis ticks to white
    xAxis.selectAll("text").attr("fill", "white");

    const yAxis = svg.append("g").call(d3.axisLeft(y));

    // Set the color of the y-axis ticks to white
    yAxis.selectAll("text").attr("fill", "white");

    svg.append("text")
      .attr("transform", `translate(${this.width / 2},${this.height + 40})`)
      .attr("fill", "white")
      .style("text-anchor", "middle")
      .text("Date");

    svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", -40)
      .attr("x", -this.height / 2)
      .attr("fill", "white")
      .style("text-anchor", "middle")
      .text("Score");

    const tooltipPadding = { top: 4, right: 2, bottom: 4, left: 11 };

    const tooltipRect = svg.append("rect")
      .attr("class", "tooltip-rect")
      .attr("width", 100 + tooltipPadding.left + tooltipPadding.right)
      .attr("height", 35 + tooltipPadding.top + tooltipPadding.bottom)
      .attr("fill", "purple") // Light Lavender for tooltip
      .attr("rx", 5)
      .attr("ry", 5)
      .style("opacity", 0);

    const tooltipDateText = svg.append("text")
      .attr("class", "tooltip-text")
      .attr("fill", "white")
      .style("font-size", "10px")
      .style("opacity", 0);

    const tooltipScoreText = svg.append("text")
      .attr("class", "tooltip-text")
      .attr("fill", "white")
      .style("font-size", "10px")
      .style("opacity", 0);

    svg.on("mouseout", function () {
      tooltipRect.style("opacity", 0);
      tooltipDateText.style("opacity", 0);
      tooltipScoreText.style("opacity", 0);

      svg.selectAll(".vertical-crosshair-line").style("opacity", 0);
      svg.selectAll(".horizontal-crosshair-line").style("opacity", 0);
    });
  }
}
