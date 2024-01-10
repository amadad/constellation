var color = d3.scaleOrdinal(d3.schemeCategory10);
var width = window.innerWidth;
var height = window.innerHeight;

var svgContainer = d3.select("body").append("svg")
.attr("width", width)
.attr("height", height)

console.log("hi")

var x = d3.scaleLinear()
.domain([0,width])
.range([0, width]);

svgContainer
.append("g")
.attr("transform", "translate(0,"+(0)+")")
.call(d3.axisBottom(x));

var y = d3.scaleLinear()
.domain([0, height])
.range([0, height]);

svgContainer
.append("g")
.attr("transform", "translate(0,0)")
// .attr("stroke","grey")
.call(d3.axisRight(y));

d3.json("all-vectors.json", function(error, data) {
  if (error) throw error;
  //console.log(data);

  var elem = svgContainer.selectAll("g myCircleText")
  .data(data)

  /*Create and place the "blocks" containing the circle and the text */
  var elemEnter = elem.enter()
  .append("g")

  /*Create the circle for each block */
  var circle = elemEnter.append("circle")
  .attr("cx", function (d) {
    let posX = map(d.vec[0],-175.81, 239.65,50,width-200);
    let posY = map(d.vec[1],-173.3, 179.29,50,height-50);
    d.pos = [posX,posY];
    return posX
  })
  .attr("cy", function (d) {
    let posY = map(d.vec[1],-173.3, 179.29,50,height-50);
    return posY
  })
  .attr("r", function (d) {
    let radius = map(d.frequency,4,9,2,15);
    return radius;
  })
  // .attr("stroke","black")
  .style('fill', function (d) {
    let who = d.brand;
    if (who == "michelin") {
      return '#005b90ff';
    } else if (who == "tireCo") {
      return '#cc4125ff';
    } else if (who == "telematic") {
      return '#e69138ff';
    }
  });

  var count = 0;
  while (count < data.length) {
    let centroid = data[count];

    for (let i = 1; i < data.length; i++) {
      let next = data[i];

      let d = dist(centroid.pos[0],centroid.pos[1],next.pos[0],next.pos[1]);
      if (d < 110) {
        // Create a horizontal link from the first node to the second
        const link = d3.linkHorizontal()({
          source: [centroid.pos[0],centroid.pos[1]],
          target: [next.pos[0],next.pos[1]]
        });

        // Append the link to the svg element
        elemEnter.append('path')
        .attr('d', link)
        .attr('stroke', '#727272')
        .attr("stroke-width", 0.009 )
        .attr('fill', 'none');
      }
    }
      count ++;
    }

    /* Create the text for each block */
    elemEnter.append("text")
    .attr("class", "keywords")
    .attr("dx", function (d) {
      return d.pos[0] + Math.random() * -7;
    })
    .attr("dy", function (d) {
      return d.pos[1] + Math.random() * -10
    })
    .text(function(d){return d.topic})
    .style("font-size", "12px")

  });

  function map(n, start1, stop1, start2, stop2) {
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2;
  }
  function dist (x1, y1, x2, y2) {
    var deltaX = Math.abs(x2 - x1);
    var deltaY = Math.abs(y2 - y1);
    var dist = Math.sqrt(Math.pow(deltaX, 2) + Math.pow(deltaY, 2));
    return (dist);
  };
