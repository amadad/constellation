var color = d3.scaleOrdinal(d3.schemeCategory10);
var width = window.innerWidth;
var height = window.innerHeight;

var svgContainer = d3.select("body").append("svg")
.attr("width", width)
.attr("height", height)


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

d3.json("all-vectors(no verbs).json", function(error, data) {
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
    let who = d.brand;
    if (who == "swappa") {
      let posX = map(d.vec[0],-61.02, 58.57,50,width-70);
      //let posX = map(d.vec[0],-61.02, 58.57,50,800);
      let posY = map(d.vec[1],-65.39, 78.06,50,height-50);
      d.pos = [posX,posY];
      return posX
    } else if (who == "bestbuy") {
      let posX = map(d.vec[0],-61.02, 58.57,50,width-70);
      //let posX = map(d.vec[0],-61.02, 58.57,850,width-70);
      let posY = map(d.vec[1],-65.39, 78.06,50,height-50);
      d.pos = [posX,posY];
      return posX
    }
  })
  .attr("cy", function (d) {
    let posY = map(d.vec[1],-65.39, 78.06,50,height-50);
    return posY
  })
  .attr("r", function (d) {
    let who = d.brand;
    if (who == "swappa") {
      let radius = map(d.frequency,1568,17840,2,15);
      return radius;
    } else if (who == "bestbuy") {
      let radius = map(d.frequency,51,252,2,15);
      return radius;
    }
  })
  // .attr("stroke","black")
  .style('fill', function (d) {
    let who = d.brand;
    if (who == "swappa") {
      return '#44974e';
    } else if (who == "bestbuy") {
      return '#1549b7';
    }
  });

  var count = 0;
  while (count < data.length) {
    let centroid = data[count];

    for (let i = 1; i < data.length; i++) {
      let next = data[i];

      let d = dist(centroid.pos[0],centroid.pos[1],next.pos[0],next.pos[1]);
      if (d < 40) {
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
      return d.pos[0]+5
    })
    .attr("dy", function (d) {
      return d.pos[1]-10
    })
    .text(function(d){return d.keyword})
    .style("font-size", "10px")

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
