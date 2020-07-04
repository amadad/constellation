var svg = d3.select("svg"),
width = svg.attr("width"),
height = svg.attr("height");

var color = d3.scaleOrdinal(d3.schemeCategory10);
//.distance(15).strength(1)
var simulation = d3.forceSimulation()
.force("link", d3.forceLink().id(function(d) { return d.id; }).distance(40).strength(1))
//.force('collision', d3.forceCollide().radius(-500))
.force("charge", d3.forceManyBody().strength(-5))
//.force("charge", function(d, i) { return i==0 ? -10000 : -500;})
.force("center", d3.forceCenter(width / 2, height / 2));

d3.json("all_clusters-1.json", function(error, graph) {
  if (error) throw error;

  var link = svg.append("g")
  .attr("class", "links")
  .selectAll("line")
  .data(graph.links)
  .enter().append("line")
  .attr("stroke-width", function(d) { return 0.5 });

  var node = svg.append("g")
  //.attr("class", "nodes")
  .selectAll(".node")
  .data(graph.nodes)
  .enter().append("g")
  .attr("class", function (d) {
    return "node";
  })

var circles = node.append("circle")
.attr("r", function (d) {
  if (d.what == "topic") {
    return 20
  } else {
    return 2
  }
})
//.attr("fill", function(d) { return color(d.group); })
.style("fill", function (d) {
  let who = d.brand;
  if (who == "schwab") {
    return '#45a0db';
  } else if (who == "tda") {
    return '#5eb43d';
  }
})
.call(d3.drag()
.on("start", dragstarted)
.on("drag", dragged)
.on("end", dragended));

// var squares = d3.selectAll(".alcohol").append("rect")
// .attr("width", function (d) {
//   let width = map(d.frequency,1,79,4,12);
//   return width
// })
// .attr("height", function (d) {
//   let height = map(d.frequency,1,79,4,12);
//   return height
// })
// .attr("fill", function(d) { return color(d.group); })
// .call(d3.drag()
// .on("start", dragstarted)
// .on("drag", dragged)
// .on("end", dragended));

var lables = node.append("text")
.text(function(d) {
    return d.id;
})
.style("fill", function (d) {
  if (d.what == "topic") {
    return "#000";
  } else {
    return "#828282";
  }
})
//.style("font-size", "8px")
.style("font-size", function (d) {
  if (d.what != "topic") {
    return "7px";
  } else {
    return "10px";
  }
})
.attr('x', function (d) {
  if (d.what != "topic") {
    return 6;
  } else {
    return -6;
  }
})
.attr('y', function (d) {
  if (d.what != "topic") {
    return 3;
  } else {
    return 3;
  }
})

node.append("title")
.text(function(d) { return d.id; });

simulation
.nodes(graph.nodes)
.on("tick", ticked);

simulation.force("link")
.links(graph.links);

function ticked() {
  link
  .attr("x1", function(d) { return d.source.x; })
  .attr("y1", function(d) { return d.source.y; })
  .attr("x2", function(d) { return d.target.x; })
  .attr("y2", function(d) { return d.target.y; });

  node
  .attr("transform", function(d) {
    return "translate(" + d.x + "," + d.y + ")";
    //return "translate(" + (d.x < 10 ? dx = 10 : d.x > 90 ? d.x = 90 : d.x) + "," + (d.y < 10 ? d.y = 10 : d.y > 90 ? d.y = 90 : d.y) + ")"
  })
}
});

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

function map(n, start1, stop1, start2, stop2) {
  return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2;
}
