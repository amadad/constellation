// upload data
d3.json("backmarket-keywords.json", function(error, data) {
  if (error) throw error;
  data = data.sort(function (a, b) {
    return d3.ascending(a.frequency, b.frequency);
  })

  // set up svg using margin conventions - we'll need plenty of room on the left for labels
  var margin = {
    top: 10,
    right: 25,
    bottom: 80,
    left: 100
  };

  var width = window.innerWidth;
  var height = window.innerHeight;

  var svg = d3.select("body").append("svg")
  .attr("width", width)
  .attr("height", height)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // map data values to svg dimensions
  var x = d3.scale.linear()
  .range([0, width - 300])
  .domain([0, d3.max(data, function (d) {
    return d.frequency;
  })]);

  var y = d3.scale.ordinal()
  .rangeRoundBands([height - 40, 0], .2)
  .domain(data.map(function (d) {
    return d.keyword;
  }));

  //make y axis to show bar names
  var yAxis = d3.svg.axis()
  .scale(y)
  //no tick marks
  .tickSize(0)
  .orient("left");

  var gy = svg.append("g")
  .attr("class", "y axis")
  .call(yAxis)

  var bars = svg.selectAll(".bar")
  .data(data)
  .enter()
  .append("g")

  // append bar rects
  bars.append("rect")
  .attr("class", "bar")
  .attr("y", function (d) {
    return y(d.keyword);
  })
  .style('fill', function (d) {
    let who = d.brand;
    if (who == "swappa") {
      return '#44974e';
    } else if (who == "bestbuy") {
      return '#1549b7';
    } else if (who == "secondipity") {
      return '#85c842';
    } else if (who == "gazelle") {
      return '#ff8f34';
    } else if (who == "backmarket") {
      return '#000000';
    }
  })
  .attr("height", y.rangeBand())
  .attr("x", 0)
  .attr("width", function (d) {
    return x(d.frequency);
  });

  //add a value label to the right of each bar
  bars.append("text")
  .attr("class", "label")
  .style("font-size", "14px")
  //y position of the label is halfway down the bar
  .attr("y", function (d) {
    return y(d.keyword) + y.rangeBand() / 2 + 4;
  })
  //x position is 3 pixels to the right of the bar
  .attr("x", function (d) {
    return x(d.frequency) + 5;
  })
  .text(function (d) {
    let who = d.brand;
    if (who == "swappa") {
      return d.frequency;
    } else if (who == "bestbuy") {
      return d.original;
    } else if (who == "secondipity") {
      return d.frequency;
    } else if (who == "gazelle") {
      return d.frequency;
    } else if (who == "backmarket") {
      return d.frequency;
    }
  });
});
