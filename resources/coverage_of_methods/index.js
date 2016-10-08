'use strict';

function drawVennDiagram(sets, title) {

  var sub_div = document.createElement("div");

  var title_node = document.createElement("h3");
  title_node.appendChild(document.createTextNode(title));

  var sub_sub_div = document.createElement("div");

  sub_div.appendChild(title_node);
  sub_div.appendChild(sub_sub_div);

  var root_canvas = document.getElementById("venn");
  root_canvas.appendChild(sub_div);

  var chart = venn.VennDiagram();
  var div = d3.select(sub_div).datum(sets);
  var layout = chart(div);
  var textCentres = layout.textCentres;

  // add new sublabels (growing from middle)
  layout.enter
  .append("text")
  .attr("class", "sublabel")
  .text(function(d) { return "size " + d.size; })
  .style("fill", "#666")
  .style("font-size", "0px")
  .attr("text-anchor", "middle")
  .attr("dy", "0")
  .attr("x", chart.width() /2)
  .attr("y", chart.height() /2);

  // move existing
  layout.update
  .selectAll(".sublabel")
  .filter(function (d) { return d.sets in textCentres; })
  .text(function(d) {
    if (d.sets.length === 1) {
      return "" + d.size;
    }
    else {
      return "";
    }
  })
  .style("font-size", "10px")
  .attr("dy", "18")
  .attr("x", function(d) { return Math.floor(textCentres[d.sets].x);})
  .attr("y", function(d) { return Math.floor(textCentres[d.sets].y);});

}

//---------------------------------------------------------------------------------------------------------------

var sets = [
  {sets: ['A'], size: 12, label: 'tmVar'},
  {sets: ['B'], size: 12, label: 'SETH'},
  {sets: ['C'], size: 18, label: 'nala'},
  {sets: ['A','B'], size: 2},
  {sets: ['A','C'], size: 3},
  {sets: ['B','C'], size: 8},
  {sets: ['A','B','C'], size: 2}
];

drawVennDiagram(sets, 'papa');

drawVennDiagram(sets, 'pio');
