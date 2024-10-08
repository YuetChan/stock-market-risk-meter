import { Injectable, EventEmitter } from '@angular/core';
import * as d3 from 'd3';

@Injectable({
  providedIn: 'root',
})
export class D3Service {
  constructor() {}

  // // Create force-directed graph simulation
  // getForceDirectedGraph(nodes, links) {
  //   const simulation = d3
  //     .forceSimulation(nodes)
  //     .force(
  //       'link',
  //       d3.forceLink(links).id((d: any) => d.id).distance(200)
  //     )
  //     .force('charge', d3.forceManyBody().strength(-400))
  //     .force('center', d3.forceCenter(400 / 2, 400 / 2));

  //   return simulation;
  // }

  // applyZoomableBehaviour(svg, container) {
  //   const zoom = d3.zoom().on('zoom', function (event) {
  //     container.attr('transform', event.transform);
  //   });

  //   svg.call(zoom);
  // }

  // applyDraggableBehaviour(node, simulation) {
  //   const dragStarted = (event, d) => {
  //     if (!event.active) simulation.alphaTarget(0.3).restart();
  //     d.fx = d.x;
  //     d.fy = d.y;
  //   };

  //   const dragged = (event, d) => {
  //     d.fx = event.x;
  //     d.fy = event.y;
  //   };

  //   const dragEnded = (event, d) => {
  //     if (!event.active) simulation.alphaTarget(0);
  //     d.fx = null;
  //     d.fy = null;
  //   };

  //   node.call(d3.drag().on('start', dragStarted).on('drag', dragged).on('end', dragEnded));
  // }
}
