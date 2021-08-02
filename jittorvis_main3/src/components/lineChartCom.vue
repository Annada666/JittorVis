<template>
<div id="lineChartCom">
  <div id="StatisticPanel">
    <div id="StatisticComponent"></div>
  </div>
</div>
</template>

<script>
export default {
  name: "lineChartCom",
  props:['data_selected', 'is_resized'],
  data(){
    return{
      WIDTH: 0,
      HEIGHT: 0,
      origin_point : {
        'x': 0,
        'y': 0
      },
      margins: ({
        top: 30,
        right: 50,
        bottom: 10,
        left: 40
     }),
      NUM_ALL_X_TICKS: 5,
      NUM_ALL_Y_TICKS: 5,
      num_y_ticks: 5,
      num_x_ticks: 5,
      x_tick_values: [],
      y_tick_values: [],
      all_data: [],
      duration: 2000,
      line_chart: {},
      posX: null,
      posY: null,
    }
  },
  mounted() {
    var that = this;
    that.__init();
    that.init_svg();

  },
  watch: {

    data_selected: {
      handler(newVal){
        if(newVal.is_data_loaded == true){
          this.clear_previous_data();
          this.get_statistics_data();
          this.generate_line_chart();
          this.remove_chart();
          this.create_chart();
          this.update_chart();
        }
      },
      immediate: true,
      deep: true
    },
    is_resized: {
      handler(newVal){
        // console.log('line:', newVal);
        if(newVal == true){
          this.remove_svg();
          this.__init();
          this.init_svg();
          this.clear_previous_data();
          this.get_statistics_data();
          this.generate_line_chart();
          this.remove_chart();
          this.create_chart();
          this.update_chart();
        }
      }
    }
  },
  methods:{


    clear_previous_data(){
      this.x_tick_values = [];
      this.y_tick_values = [];
      this.num_x_ticks = this.NUM_ALL_X_TICKS;
      this.num_y_ticks = this.NUM_ALL_Y_TICKS;
    },
    get_statistics_data(){
      this.all_data = [];
      var statistics = this.data_selected.all_data['statistics'];
      for (var i=0;i < statistics['iter'].length; i++){
        console.log(this.data_selected.selected);
        this.all_data.push({x: statistics['iter'][i], y: statistics[this.data_selected.selected][i]});
      }
      console.log(this.all_data);
    },

    __init(){
      var that = this;
      var d3 = that.$d3;
      that.WIDTH = document.body.clientWidth - 180;
      console.log(that.WIDTH);
      that.HEIGHT = parseInt(d3.selectAll('#StatisticComponent')
          .style("height"));
      var width = that.WIDTH;
      var height = that.HEIGHT;
      var margins = that.margins;
      // that.WIDTH = window.innerWidth;
      // that.HEIGHT = window.innerHeight;
      var odiv=document.getElementById('StatisticComponent');
      that.origin_point.x = odiv.getBoundingClientRect().top;
      that.origin_point.y = odiv.getBoundingClientRect().left;

      var svg = d3.selectAll('#StatisticComponent')
          .append("svg")
          .attr('id', 'statisticView')
          .attr("viewBox", [0, 0, width, height])
          .attr('width', width)
          .attr('height', height);
      svg.append("svg:clipPath")
          .attr("id", "clip")
          .append('svg:rect')
          .attr("id", "clip-rect")
          .attr('x', margins.left)
          .attr('y', margins.top)
          .attr('width', width - (margins.left + margins.right + margins.left))
          .attr('height', height - (margins.top+margins.top+margins.bottom))
          .attr('pointer-events', 'none');
      svg.append("svg:clipPath")
          .attr("id", "clip_x_axis")
          .append('svg:rect')
          .attr("id", "clip-x-rect_axis")
          .attr('x', margins.left - 5)
          .attr('y', height - margins.bottom - margins.top - 5)
          .attr('width', width - (margins.left + margins.right + margins.left) + 20)
          .attr('height', 30)
          .attr('pointer-events', 'none');
      svg.append("svg:clipPath")
          .attr("id", "clip_y_axis")
          .append('svg:rect')
          .attr("id", "clip-y-rect_axis")
          .attr('x', 0)
          .attr('y', margins.top - 5)
          .attr('width', margins.left)
          .attr('height', height - (margins.top+margins.top+margins.bottom) + 10)
          .attr('pointer-events', 'none');


        const chart = svg.append("g")
            .attr('class', 'lines')
            .attr("clip-path", "url(#clip)");
        const x_chart = svg.append("g")
            .attr('class', 'x_axis_lines')
            .attr("clip-path", "url(#clip_x_axis)");
        const y_chart = svg.append("g")
            .attr('class', 'y_axis_lines')
            .attr("clip-path", "url(#clip_y_axis)");
      },
    init_svg(){
      var that = this;
      var width = that.WIDTH;
      var height = that.HEIGHT;
      var margins = that.margins;
      var svg = that.$d3.selectAll('#StatisticComponent')
          .selectAll("#statisticView");
      var chart = svg.selectAll('.lines');
      var x_chart = svg.selectAll('.x_axis_lines');
      var y_chart = svg.selectAll('.y_axis_lines');
        x_chart.append("g")
            .attr('id', 'gxLabel')
            .attr('stroke-width', 2)
            .attr("class", "axis")
            .attr("transform", `translate(0,${height - (margins.bottom + margins.top)})`)
            .style("color", that.$color_manager.text_color);
        chart.append("g")
            .attr('id', 'gridXLabel')
            .attr("transform", `translate(0,${height - (margins.bottom + margins.top)})`)
            .style("stroke-dasharray",("3,3"))
            .style("color", that.$color_manager.text_color)
            .style("opacity", "0.5");
        // x axis
        svg.append('path')
            .attr('id', 'op_schedule_axis-x')
            .style('stroke', that.$color_manager.text_color)
            .style('stroke-width', 2);
        svg.append('path')
            .attr('id', 'op_schedule_axis-x-arrow')
            .style('stroke', that.$color_manager.text_color)
            .style('fill', that.$color_manager.text_color)
            .style('stroke-width', '2px');
        svg.append('text')
            .attr('id', 'op_schedule_axis-x-label')
            .attr('x', width - (margins.right + margins.left) + 25)
            .attr('y', height - (margins.bottom + margins.top))
            .style("user-select", "none")
            .attr('font-size', '15px')
            .attr('font-family', 'Arial')
            .attr('dominant-baseline', 'central')
            .style('fill', that.$color_manager.text_color);

        y_chart.append("g")
            .attr('id', 'gyLabel')
            .attr('stroke-width', 2)
            .attr("class", "axis")
            .attr("transform", `translate(${margins.left},0)`)
            .style("color", that.$color_manager.text_color);
        chart.append("g")
            .attr('id', 'gridYLabel')
            .attr("transform", `translate(${margins.left},0)`)
            .style("stroke-dasharray",("3,3"))
            .style("color", that.$color_manager.text_color)
            .style("opacity", "0.5");
        svg.selectAll('.axis path').style("stroke", that.$color_manager.text_color);
        svg.selectAll('.axis line').style("stroke", that.$color_manager.text_color);


        // y axis
        svg.append('path')
            .attr('id', 'op_schedule_axis-y')
            .style('stroke', that.$color_manager.text_color)
            .style('stroke-width', 2);
        svg.append('path')
            .attr('id', 'op_schedule_axis-y-arrow')
            .style('stroke', that.$color_manager.text_color)
            .style('fill', that.$color_manager.text_color)
            .style('stroke-width', "2px");
        svg.append('text')
            .attr('id', 'op_schedule_axis-y-label')
            .attr('x', margins.left + 6)
            .attr('y', margins.top - 20)
            .style("user-select", "none")
            .attr('font-size', '15px')
            .attr('font-family', 'Arial')
            .attr('dominant-baseline', 'hanging')
            .style('fill', that.$color_manager.text_color);
        var chart = svg.selectAll('.lines');

      var mouseG = chart.append("g")
          .attr('id', 'mouseOverlay')
          .attr("class", "mouse-over-effects");

      chart.append("path")
          .attr("class", "mouse-line")
          .style("stroke", "black")
          .style("stroke-width", "1px")
          .style('visibility', 'hidden');
      mouseG.append('svg:rect')
          .attr('id', 'mouse-rect')
          .attr('x', margins.left)
          .attr('y', margins.top)
          .attr('width', width - (margins.left + margins.right + margins.left))
          .attr('height', height - (margins.top+margins.top+margins.bottom))
          .attr('fill', 'none')
          // .style("stroke", "black")
          .attr('pointer-events', 'all');
      var labelGroup = mouseG.append("g")
          .attr("class", "label_group")
          .attr('pointer-events', 'none');
      labelGroup.append("circle")
          .attr("r", 5)
          .attr("class", "data_circle")
          .style("stroke", "#0000ff")
          .style("fill", "none")
          .style("stroke-width", "2px")
          .style('visibility', 'hidden');
      document.addEventListener('mouseup', that.line_chart['onMouseUp'])
      document.addEventListener('keydown', (e) => {
        if(e.keyCode === 17) that.line_chart['MOUSE_DATA'].onCTRLKeyDown = true;
      })
      document.addEventListener('keyup', (e) => {
        if(e.keyCode === 17) {
          console.log("Olmadı");
          that.line_chart['MOUSE_DATA'].onCTRLKeyDown = false;
        }
      })
    },
    generate_line_chart(){
      var that = this;
      var data = that.all_data;
      var d3 = that.$d3;
      var width = that.WIDTH;
      var height = that.HEIGHT;
      var margins = that.margins;

      //compute x, y axis tick values
      var max_x = d3.max(data, d => d.x), min_x = d3.min(data, d => d.x);
      var max_y = d3.max(data, d => d.y);
      if(that.data_selected.selected == 'accuracy'){
        max_y = 1;
      }
      var i;
      var x_space = parseInt((max_x - min_x + 1) / that.num_x_ticks);
      if(x_space === 0){
        x_space = 1;
      }
      var y_space = (max_y - 0) / that.num_y_ticks;
      var y_space = (max_y - 0) / that.num_y_ticks;

      for(i = min_x;i <= max_x;i += x_space){
        that.x_tick_values.push(i);
      }
      if(that.x_tick_values[that.x_tick_values.length - 1] != max_x){
        that.x_tick_values.push(max_x);
      }
      if(that.x_tick_values[0] != 0 && that.x_tick_values[0] != 1){
        that.x_tick_values.unshift(0);
      }
      for(i = 0;i <= max_y;i += y_space){
        that.y_tick_values.push(i.toFixed(2));
      }
      if(that.y_tick_values[that.y_tick_values.length - 1] != max_y.toFixed(2)){
        that.y_tick_values.push(max_y.toFixed(2));
      }
      var x = d3.scaleLinear()
          .domain([0, d3.max(data, d => d.x)])
          .range([margins.left, width - (margins.right + margins.left)]);
      var rawLine = d3.line()
          .x(d => x(d.x))
          .y(d => y(d.y));
      var smoothLine = d3.line()
          .curve(d3.curveBasis)
          .x(d => x(d.x))
          .y(d => y(d.y));
      that.line_chart['smoothLine'] = smoothLine;
      var y = d3.scaleLinear()
          .domain([d3.max(data, d => d.y),0 ])
          .range([margins.top, height - (margins.bottom + margins.top)]);
      if(that.data_selected.selected == 'accuracy'){
        y = d3.scaleLinear()
          .domain([1,0 ])
          .range([margins.top, height - (margins.bottom + margins.top)]);
      }
      that.line_chart['x'] = x;
      that.line_chart['y'] = y;
      var xAxis = d3.axisBottom(x)
          .tickValues(that.x_tick_values);
      var make_x_gridlines = d3.axisBottom(x)
          .tickValues(that.x_tick_values)
          .tickSize(-(height - (margins.bottom + margins.top + margins.top )))
          .tickFormat("");
      var make_y_gridlines = d3.axisLeft(y)
          .tickValues(that.y_tick_values)
          .tickSize(-(width - (margins.left + margins.left + margins.right)))
          .tickFormat("");
      var yAxis = d3.axisLeft(y)
          .tickValues(that.y_tick_values)
          .tickFormat(y_space === 0.1? d3.format('.1f') : d3.format('.2f'));
      that.line_chart['xAxis'] = xAxis;
      that.line_chart['yAxis'] = yAxis;
      that.line_chart['make_x_gridlines'] = make_x_gridlines;
      that.line_chart['make_y_gridlines'] = make_y_gridlines;
      that.line_chart['rawLine'] = rawLine;

      that.line_chart['MOUSE_DATA']=({isMouseDown:false, onCTRLKeyDown:false, selectChart:null});
      var onMouseUp = function () {
        that.line_chart['MOUSE_DATA'].isMouseDown = false;
        that.line_chart['MOUSE_DATA'].firstIndex = undefined;
      }
      var onMouseDown = function () {
        that.line_chart['MOUSE_DATA'].isMouseDown = true;
        // updateSelect([]);
      }

      var onDrag = function () {
        // let selectChart = MOUSE_DATA.selectChart;
        let firstIndex = that.line_chart['MOUSE_DATA'].firstIndex;
        let currentIndex = that.line_chart['MOUSE_DATA'].index;

        if(firstIndex == null) {
          return;
        }
        if(firstIndex === currentIndex) {
          return;
        }
        let minInx = Math.min(currentIndex, firstIndex);
        let maxInx = Math.max(currentIndex, firstIndex) + 1;
        let newData = data.slice(minInx, maxInx);
      }

      var mouseMove = function () {
        var mouse = d3.pointer(event);
        const mouseLength = that.line_chart['x'].invert(mouse[0]);
        const bisect = d3.bisector(d => d.x).right;
        const xIndex = bisect(data, mouseLength, 0);
        if(xIndex >= data.length){
          return ;
        }
        let pos = data[xIndex];
        let posY = that.line_chart['y'](pos.y);
        let posX = that.line_chart['x'](pos.x);
        that.posX = posX;
        that.posY = posY;

        var callout = (g, value) => {
        if (!value) return g.style("display", "none");
        g.style("display", null)
            .style("pointer-events", "none")
            .style("font", "10px sans-serif");
        const path = g.selectAll("path")
            .data([null])
            .join("path")
            .attr("fill", "white")
            .attr("stroke", "black");
        const text = g.selectAll("text")
            .data([null])
            .join("text")
            .call(text => text
                .selectAll("tspan")
                .data(value)
                .join("tspan")
                .text(d => d));
        var {x, y, width: w, height: h} = text.node().getBBox();
        text.attr("transform", `translate(${-w / 2},${15 - y})`);
        path.attr("d", `M${-w / 2 - 10},5H-5l5,-5l5,5H${w / 2 + 10}v${h + 20}h-${w + 20}z`);
      };
        var formatX = function (x) {
          return x.toLocaleString("en", {
            Iteration: "short",
          });
        }
        svg.on("touchmove mousemove", function(event) {
          svg.selectAll('#tooltip').attr("transform", `translate(${posX},${posY})`)
              .call(callout, `Iteration:${pos.x},${that.data_selected.selected}:${pos.y.toFixed(2)}`);
        });
        svg.on("touchend mouseleave", () => svg.selectAll('#tooltip').call(callout, null));

        d3.select(".mouse-line")
            .attr("d", function() {
              var d = "M" + posX + "," + (height - (margins.top + margins.bottom))
              d += "L" + posX + "," + margins.top;
              return d;
            })
            .style('visibility', 'visible');
        d3.select('.data_circle')
            .style('visibility', 'visible');


        if(that.line_chart['MOUSE_DATA'].onCTRLKeyDown) {
          that.line_chart['MOUSE_DATA'].index = xIndex;
          if(that.line_chart['MOUSE_DATA'].onCTRLKeyDown && that.line_chart['MOUSE_DATA'].isMouseDown) {
            if(that.line_chart['MOUSE_DATA'].firstIndex === undefined) {
              that.line_chart['MOUSE_DATA'].firstIndex = xIndex;
              console.log("İlk nokta");
            }
            onDrag();
          }
        }
        d3.select('.label_group')
            .attr("transform", `translate(${posX},${posY})`);

      }
      that.line_chart['mouseMove'] = mouseMove;
      that.line_chart['onMouseDown'] = onMouseDown;
      that.line_chart['onMouseUp'] = onMouseUp;
      var zoomed = function (event){
        if(that.line_chart['MOUSE_DATA'].onCTRLKeyDown) {
          return;
        }

        d3.select('.data_circle')
            .attr("r", 7 / event.transform.k)
            .style("stroke-width", 2 / event.transform.k);

        d3.select('#mouseOverlay #mouse-rect')
          .attr('x', that.margins.left)
          .attr('y', that.margins.top)
          .attr('width', that.WIDTH - (that.margins.left + that.margins.right + that.margins.left))
          .attr('height', that.HEIGHT - (that.margins.top+that.margins.top+that.margins.bottom));
        d3.select('.mouse-line')
            .style("stroke-width", 1 / event.transform.k)
            .attr("transform", 'translate('+event.transform.x+',0) scale('+event.transform.k+',1)')
            .attr("d", function() {
              var d = "M" + that.posX + "," + (that.HEIGHT - (that.margins.top + that.margins.bottom))
              d += " " + that.posX + "," + that.margins.top;
              return d;
            })
        d3.select('.rawLine')
            .attr("transform", event.transform)
            .style("stroke-width", 2 / event.transform.k);
        d3.select('#mouseOverlay')
            .attr("transform", event.transform);
        d3.select('#gxLabel')
            .call(xAxis.scale(event.transform.rescaleX(x)));
        d3.select('#gridXLabel')
            .call(make_x_gridlines.scale(event.transform.rescaleX(x)));
        d3.select('#gyLabel')
            .call(yAxis.scale(event.transform.rescaleY(y)));
        d3.select('#gridYLabel')
            .call(make_y_gridlines.scale(event.transform.rescaleY(y)));

      };
      var zoom = d3.zoom()
          .scaleExtent([1, 5])
          .translateExtent([[0, 0], [width, height]])
          .on("zoom", zoomed);
      var svg = d3.selectAll('#StatisticComponent')
          .selectAll("#statisticView")
          .call(zoom);

    },
    update_chart(){
        var that = this;
        var margins = that.margins;
        var width = that.WIDTH;
        var height = that.HEIGHT;
        var svg = that.$d3.selectAll('#StatisticComponent')
          .selectAll("#statisticView");
        var chart = svg.selectAll('.lines');

        svg.selectAll('.x_axis_lines').selectAll('#gxLabel')
            .transition()
            .duration(that.duration)
            .call(that.line_chart['xAxis'])
        svg.selectAll('#gridXLabel')
            .transition()
            .duration(that.duration)
            .call(that.line_chart['make_x_gridlines'])
        chart.selectAll('#op_schedule_axis-x')
            .transition()
            .duration(that.duration)
            .attr('d', that.$tool.default.path_d([
                [width - (margins.right + margins.left),
                  height - (margins.bottom + margins.top)],
              [width - (margins.right + margins.left) + 20,
                height - (margins.bottom + margins.top)]]));
        chart.selectAll('#op_schedule_axis-x-arrow')
            .transition()
            .duration(that.duration)
            .attr('d', that.$tool.default.arrow_path_d(width - (margins.right + margins.left) + 11, height - (margins.bottom + margins.top) - 3, 9, 6, 'right'));
        chart.selectAll('#op_schedule_axis-x-label')
            .transition()
            .duration(that.duration)
            .text('Iteration');

        svg.selectAll('.y_axis_lines').selectAll('#gyLabel')
            .transition()
            .duration(that.duration)
            .call(that.line_chart['yAxis'])
        svg.selectAll('#gridYLabel')
            .transition()
            .duration(that.duration)
            .call(that.line_chart['make_y_gridlines'])
        chart.selectAll('#op_schedule_axis-y')
            .transition()
            .duration(that.duration)
            .attr('d', that.$tool.default.path_d([
                [margins.left, margins.top],
              [margins.left, margins.top - 10]]))
                .style('stroke', that.$color_manager.text_color)
                .style('stroke-width', 2);

        chart.selectAll('#op_schedule_axis-y-arrow')
            .transition()
            .duration(that.duration)
            .attr('d', that.$tool.default.arrow_path_d(margins.left - 3, margins.top - 15, 6, 9, 'top'));


        chart.selectAll('#op_schedule_axis-y-label')
            .transition()
            .duration(that.duration)
            .text(that.data_selected.selected);


        var rawLineChart = chart
            .selectAll('.rawLine')
            .data([that.all_data]);
        rawLineChart.transition()
            .duration(that.duration)
            .attr('d', that.line_chart['rawLine'] );
      },
    create_chart(){
        var that = this;
        var svg = that.$d3.selectAll('#StatisticComponent')
          .selectAll("#statisticView");
        var margins = that.margins;
        var width = that.WIDTH;
        var height = that.HEIGHT;
        var chart = svg.selectAll('.lines');
        svg.selectAll('.x_axis_lines').selectAll('#gxLabel')
            .call(that.line_chart['xAxis']);
        chart.selectAll('#gridXLabel')
            .call(that.line_chart['make_x_gridlines']);
        // x axis
        svg.selectAll('#op_schedule_axis-x')
            .attr('d', that.$tool.default.path_d([
                [width - (margins.right + margins.left),
                  height - (margins.bottom + margins.top)],
              [width - (margins.right + margins.left) + 20,
                height - (margins.bottom + margins.top)]]));

        svg.selectAll('#op_schedule_axis-x-arrow')
            .attr('d', that.$tool.default.arrow_path_d(width - (margins.right + margins.left) + 11, height - (margins.bottom + margins.top) - 3, 9, 6, 'right'));
        svg.selectAll('#op_schedule_axis-x-label')
            .text('Iteration');

        svg.selectAll('.y_axis_lines').selectAll('#gyLabel')
            .call(that.line_chart['yAxis']);
        chart.selectAll('#gridYLabel')
            .call(that.line_chart['make_y_gridlines']);

        // y axis
        svg.selectAll('#op_schedule_axis-y')
            .attr('d', that.$tool.default.path_d([
                [margins.left, margins.top],
              [margins.left, margins.top - 10]]))
                .style('stroke', that.$color_manager.text_color)
                .style('stroke-width', 2);
        svg.selectAll('#op_schedule_axis-y-arrow')
            .attr('d', that.$tool.default.arrow_path_d(margins.left - 3, margins.top - 15, 6, 9, 'top'));
        svg.selectAll('#op_schedule_axis-y-label')
            .text(that.data_selected.selected);


        let rawLineChart = chart
            .selectAll('.rawLine')
            .data([that.all_data]);
        rawLineChart.enter().append('path')
            .attr('class','rawLine')
            .attr('id', function (d){
              return `rawLine_${that.data_selected.selected}`;
            })
            .attr('fill', 'none')
            .attr('stroke', that.$color_manager.darker_default_color)
            .attr('stroke-width', "3px")
            .style("opacity", "0.2");

      var mouseG = svg.selectAll("#mouseOverlay");

      mouseG.selectAll('rect')
          .on('mousemove', that.line_chart['mouseMove'])
          .on('mousedown', that.line_chart['onMouseDown']);
      svg.selectAll(".mouse-line")
          .style('visibility', 'hidden');
      var labelGroup = mouseG.selectAll(".label_group");
      labelGroup.selectAll(".data_circle")
          .style("stroke", "#0000ff")
          .style('visibility', 'hidden');

      var tooltip = svg.append('g')
          .attr('id','tooltip');


    },

    remove_chart(){
        var that = this;
        var svg = that.$d3.selectAll('#StatisticComponent')
          .selectAll("#statisticView");
        var chart = svg.selectAll('.lines');

        chart.selectAll('#gyLabel')
            .exit().transition().duration(that.duration).style('opacity', 0);
        chart.selectAll('#gridYLabel')
            .exit().transition().duration(that.duration).style('opacity', 0);
        chart.selectAll('#op_schedule_axis-y')
            .exit().transition().duration(that.duration).style('opacity', 0);

        chart.selectAll('#op_schedule_axis-y-arrow')
            .exit().transition().duration(that.duration).style('opacity', 0);

        chart.selectAll('#op_schedule_axis-y-label')
            .exit().transition().duration(that.duration).style('opacity', 0);
        const rawLineChart = svg.selectAll('.lines')
            .selectAll('.rawLine')
            .data([that.all_data]);
        rawLineChart.exit().transition().duration(that.duration).style('opacity', 0);

    },
    remove_svg(){
      var that = this;
      var svg = that.$d3.selectAll('#StatisticComponent').selectAll('#statisticView').remove();
      // svg.exit().style('opacity',0);
    }
  }
}
</script>

<style>
#lineChartCom{
    background: white;
    height: 150px;
    flex-direction: row;
    width: 100%;
    box-shadow: inset 0 1px 3px 3px rgb(0 0 0 / 25%);
    z-index: 1;
    box-sizing: border-box;
}
#StatisticPanel {
    display: flex;
    flex-direction: row;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
}
#StatisticComponent{
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    overflow:hidden;
}
</style>