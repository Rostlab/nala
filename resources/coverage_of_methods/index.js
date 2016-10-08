'use strict';

function drawVennDiagram(htmlElement, sets, title) {

  var sub_div = document.createElement("div");

  var title_node = document.createElement("h3");
  title_node.appendChild(document.createTextNode(title));

  var sub_sub_div = document.createElement("div");

  sub_div.appendChild(title_node);
  sub_div.appendChild(sub_sub_div);

  var root_canvas = htmlElement;
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

function intersect2(set1, set2) {
  return new Set(
    [...set1].filter(x => set2.has(x))
  );
}

function intersect3(set1, set2, set3) {
  return intersect2(set1, intersect2(set2, set3));
}

function jsonpToVennSets(jsonp, filter_f) {
  filter_f = filter_f || (_ => true);

  var A = new Set(jsonp.A.results.filter(filter_f));
  var B = new Set(jsonp.B.results.filter(filter_f));
  var C = new Set(jsonp.C.results.filter(filter_f));

  var AiB = intersect2(A, B);
  var AiC = intersect2(A, C);
  var BiC = intersect2(B, C);

  var AiBiC = intersect3(A, B, C);

  var sets = [
    {sets: ['A'], size: A.size, label: jsonp.A.label},
    {sets: ['B'], size: B.size, label: jsonp.B.label},
    {sets: ['C'], size: C.size, label: jsonp.C.label},
    {sets: ['A','B'], size: AiB.size},
    {sets: ['A','C'], size: AiC.size},
    {sets: ['B','C'], size: BiC.size},
    {sets: ['A','B','C'], size: AiBiC.size}
  ];

  return sets;
}

function draw(jsonp, title_prefix, filter_f) {
  filter_f = filter_f || (_ => true);

  var div = document.createElement("div");
  var title_node = document.createElement("h1");
  title_node.appendChild(document.createTextNode(title_prefix));
  div.appendChild(title_node);

  drawVennDiagram(div, jsonpToVennSets(jsonp, (x => filter_f(x))), title_prefix + " TOTAL");
  drawVennDiagram(div, jsonpToVennSets(jsonp, (x => filter_f(x) && x.endsWith('0'))), title_prefix + " ST");
  drawVennDiagram(div, jsonpToVennSets(jsonp, (x => filter_f(x) && x.endsWith('1'))), title_prefix + " NL");

  var row = document.createElement("hr");
  div.appendChild(row);

  var root_canvas = document.getElementById("venn");
  root_canvas.appendChild(div);
}

//---------------------------------------------------------------------------------------------------------------

draw(nala_discoveries, 'nala_discoveries');
draw(SetsKnown, 'Var120', (x => x.includes('-')));
draw(SetsKnown, 'SetsKnown');
draw(SetsKnown, 'SetsKnown(Balanced)');
