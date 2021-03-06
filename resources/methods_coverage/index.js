'use strict';

function getURLParameter(name) {
  return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search) || [null, ''])[1].replace(/\+/g, '%20')) || null;
}

var UNIQUE_MODE = (getURLParameter('UNIQUE_MODE') || 'true') === 'true';
var OVER_ABSOLUTE_TOTAL = (getURLParameter('OVER_ABSOLUTE_TOTAL') || 'true') === 'true';

console.log(UNIQUE_MODE, OVER_ABSOLUTE_TOTAL);

function to100P(x, ndecimals) {
  return (x * 100).toFixed(ndecimals || 0);
}

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

  layout.update
  .selectAll(".label")
  .style("font-size", "16px")

  layout.enter
  .append("text")
  .attr("class", "sublabel1")
  .style("fill", "#666")
  .attr("text-anchor", "middle")
  .filter(function (d) { return d.sets in textCentres; })
  .text(function(d) {
    if (d.sets.length === 1) {
      return "" + to100P(d.percentage) + "% (" + d.size + ")";
    }
    else {
      return "";
    }
  })
  .style("font-size", "14px")
  .attr("dy", "18")
  .attr("x", function(d) { return Math.floor(textCentres[d.sets].x);})
  .attr("y", function(d) { return Math.floor(textCentres[d.sets].y);});


  layout.enter
  .append("text")
  .attr("class", "sublabel2")
  .style("fill", "#666")
  .attr("text-anchor", "middle")
  .filter(function (d) { return d.sets in textCentres; })
  .text(function(d) {
    if (d.sets.length === 1) {
      return "" + to100P(d.per_singular) + "% (" + d.num_singular + ")";
    }
    else {
      return "";
    }
  })
  .style("font-size", "14px")
  .attr("dy", "36")
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

function jsonpToVennSets(jsonp, corpus_name, filter_f, subclass) {

  var map_f = UNIQUE_MODE ? (x => x.substring(x.lastIndexOf('|')+1)) : (x => x);

  var a = jsonp.A.results.filter(filter_f).map(map_f);
  var b = jsonp.B.results.filter(filter_f).map(map_f);
  var c = jsonp.C.results.filter(filter_f).map(map_f);

  var A = new Set(a);
  var B = new Set(b);
  var C = new Set(c);

  var AiB = intersect2(A, B);
  var AiC = intersect2(A, C);
  var BiC = intersect2(B, C);

  var AiBiC = intersect3(A, B, C);

  var AuB = new Set([...a, ...b]); //union
  var AuC = new Set([...a, ...c]); //union
  var BuC = new Set([...b, ...c]); //union
  var AuBuC = new Set([...a, ...b, ...c]); //union

  var A_BuC = new Set([...a].filter(x => !BuC.has(x)));
  var B_AuC = new Set([...b].filter(x => !AuC.has(x)));
  var C_AuB = new Set([...c].filter(x => !AuB.has(x)));

  if (OVER_ABSOLUTE_TOTAL) {
    var which_counts;
    if (corpus_name === "Var120") {
      which_counts = (UNIQUE_MODE) ? jsonp.Var120_uniq_counts : jsonp.Var120_counts;
    }
    else if (corpus_name === 'SetsKnown(Balanced)') {
      throw new Error('Approximation for calculating total size not implemented yet');

      // which_counts = (UNIQUE_MODE) ? jsonp.Var120_uniq_counts : jsonp.Var120_counts;
      // //Approximation
      // which_counts = JSON.parse(JSON.stringify(which_counts));
      // which_counts[subclass] = which_counts[subclass] * 3;
    }
    else {
      which_counts = (UNIQUE_MODE) ? jsonp.uniq_counts : jsonp.counts;
    }

    var total_number = which_counts[subclass];

    if (total_number < AuBuC.size) {
      console.log(a, b, c);
      console.log(AuBuC);
      throw new Error("This cannot be: " + total_number + " < " + AuBuC.size + " -- " + subclass);
    }
  }
  else {
    //over methods' combined results (smaller number)
    var total_number = AuBuC.size
  }

  var sets = [ //not unique percentages
    {sets: ['A'], size: A.size, label: jsonp.A.label, percentage: A.size / total_number, num_singular: A_BuC.size, per_singular: A_BuC.size / total_number},
    {sets: ['B'], size: B.size, label: jsonp.B.label, percentage: B.size / total_number, num_singular: B_AuC.size, per_singular: B_AuC.size / total_number},
    {sets: ['C'], size: C.size, label: jsonp.C.label, percentage: C.size / total_number, num_singular: C_AuB.size, per_singular: C_AuB.size / total_number},
    {sets: ['A','B'], size: AiB.size},
    {sets: ['A','C'], size: AiC.size},
    {sets: ['B','C'], size: BiC.size},
    {sets: ['A','B','C'], size: AiBiC.size}
  ];

  return sets;
}

function draw(jsonp, corpus_name, filter_f) {
  filter_f = filter_f || (_ => true);

  var htmlElement = document.createElement("div");

  //var title_node = document.createElement("h1");
  //title_node.appendChild(document.createTextNode(corpus_name));
  //htmlElement.appendChild(title_node);

  var table = document.createElement("table");
  var tr1 = document.createElement("tr");
  var tr1_c1 = document.createElement("td");
  var tr1_c2 = document.createElement("td");
  tr1.appendChild(tr1_c1);
  tr1.appendChild(tr1_c2);
  table.appendChild(tr1);

  var tr2 = document.createElement("tr");
  var tr2_c1 = document.createElement("td");
  var tr2_c2 = document.createElement("td");
  tr2.appendChild(tr2_c1);
  tr2.appendChild(tr2_c2);
  table.appendChild(tr2);

  drawVennDiagram(tr1_c1, jsonpToVennSets(jsonp, corpus_name, (x => filter_f(x)), "All"), "All @ " + corpus_name);
  drawVennDiagram(tr1_c2, jsonpToVennSets(jsonp, corpus_name, (x => filter_f(x) && x.includes('|e_2|0|')), "ST"), "ST @ " + corpus_name);
  drawVennDiagram(tr2_c1, jsonpToVennSets(jsonp, corpus_name, (x => filter_f(x) && x.includes('|e_2|1|')), "NL"), "NL @ " + corpus_name);
  drawVennDiagram(tr2_c2, jsonpToVennSets(jsonp, corpus_name, (x => filter_f(x) && x.includes('|e_2|2|')), "SST"), "SST @ " + corpus_name);

  htmlElement.appendChild(table);
  htmlElement.appendChild(document.createElement("hr"));

  var root_canvas = document.getElementById("venn");
  root_canvas.appendChild(htmlElement);
}

//---------------------------------------------------------------------------------------------------------------

draw(nala_discoveries, 'nala_discoveries');
draw(SetsKnown, 'SetsKnown');

// draw(SetsKnown, 'Var120', (x => /^\d+\|\d\d-/.test(x))); //Unique pattern for Var120, as in: '3034663|05-Discussion-p02-p2|411,422|e_2|0|p.Lys618Ala'
//
// var SetsKnownBalancedAccepted = new Set();
// var SetsKnownBalancedAll = SetsKnown.A.results.concat(SetsKnown.B.results.concat(SetsKnown.C.results));
//
// SetsKnownBalancedAll.forEach(function(x) {
//   var sizeVar120 = (UNIQUE_MODE) ? SetsKnown.Var120_uniq_counts.TOTAL : SetsKnown.Var120_counts.TOTAL; //Smallest of all 3 corpora
//
//   //Var120
//   if (x.includes('-')) {
//     SetsKnownBalancedAccepted.add(x);
//   }
//   //nala-known
//   else if (x.includes('s1')) {
//     var bar = sizeVar120 / ((UNIQUE_MODE) ? SetsKnown.nala_known_uniq_counts.TOTAL : SetsKnown.nala_known_counts.TOTAL);
//     if (Math.random() < bar) {
//       SetsKnownBalancedAccepted.add(x);
//     }
//   }
//   //SETH
//   else {
//     var bar = sizeVar120 / ((UNIQUE_MODE) ? SetsKnown.SETH_uniq_counts.TOTAL : SetsKnown.SETH_counts.TOTAL);
//     if (Math.random() < bar) {
//       SetsKnownBalancedAccepted.add(x);
//     }
//   }
// });
//
// draw(SetsKnown, 'SetsKnown(Balanced)', (x => SetsKnownBalancedAccepted.has(x)));
