<template>
<div id="panelRow2Com">
  <div id="NetworkPanel">
    <div id="NetworkComponent">
      <div id="treeViewBackground">
        <div id="treeViewCom">
        </div>
      </div>
      <div id="graphViewBackground">
        <div id="graphCom">
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: "panelRow2Com",
  data() {
    return {
      CHECK_INIT: false,
      TREE_WIDTH: 0,
      GRAPH_WIDTH: 0,
      INIT_TREE_WIDTH: 0,
      INIT_HEIGHT: 0,
      last_tree_scale: 0,
      HEIGHT: 0,
      margins: {
        left: 30,
        right: 30,
        gap: 20,
        top: 0,
        bottom: 30,
        line_height: 183,
        margin_top: 3,
      },

      margin_tree:{ top: 65, right: 70, bottom: 45, left: 70 },
      rightbottom_area_hidden: false,
      data: {},
      defaultVal: {
        margin: {top: 5, right: 5, bottom: 5, left: 5},
        events: {}
      },
      all_nodes: null,
      all_edges: null,
      moveto: null,
      chart: null,
      guideview: null,
      treeview: null,
      zoom: null,
      op_nodes: null,
      nodes : [],
      curr_all_nodes : [],
      exploring_nodes : [],
      edges : [],
      curr_all_edges : [],
      time_cost_height : 0,
      visconfig : {},
      title_height : 20,
      node_width : 120,
      node_height : 36,
      node_expand_width : 240,
      node_expand_height : 166,
      var_node_r : 8,
      time_cost_unit_number : 10,
      duration : 500,
      remove_duration : 500,
      explore_btn_width : 18,
      exploring_level_delta : 10,
      expand_btn_width : 20,
      update_layout : false,
      focus_node_index : -1,
      main_group: null,
      legend_group: null,
      exploring_node_map: null,
      exploring_cover_map: null,
      edge_map: null,
      node_map: null,
      render_legend: null,
      righttop_area: null,
      leftbottom_area: null,
      rightbottom_area: null,
      lefttop_area: null,
      zoom_tree: null,
    }
  },
  props:['data_loaded', 'is_resized'],
  watch:{
    is_resized: {
      handler(newVal) {
        this.resize();
      }
    },
    data_loaded: {
      handler(newVal){
        if(newVal.is_data_loaded == true){
          // console.log('data loaded again!');
            this.redraw(newVal.all_data['network']);
            this.$tool.default.init_interactions(this);
            if(!this.CHECK_INIT){
              this.$tool.default.add_intro();
              this.CHECK_INIT = true;
            }
          }
        },
      immediate: true,
      deep: false
      }
    },

  mounted() {
    this.__init();
  },
  methods:{
    __init(){
      var self = this;
      var d3 = self.$d3;
      var margins = self.margins;
      self.TREE_WIDTH = (document.body.clientWidth - margins.left - margins.right) * 0.35 - margins.gap * 2;
      self.HEIGHT = document.body.clientHeight - margins.line_height - margins.bottom - margins.margin_top - margins.gap * 2;
      self.INIT_TREE_WIDTH = self.TREE_WIDTH;
      self.INIT_HEIGHT = self.HEIGHT;

      self.GRAPH_WIDTH = (document.body.clientWidth - margins.left - margins.right) * 0.65 - margins.gap * 2;


      self.chart = d3.selectAll('#graphCom')
                .append('svg')
                .attr('id', 'networkView')
                .attr('width', self.GRAPH_WIDTH)
                .attr('height', self.HEIGHT);
      d3.selectAll('#NetworkComponent').attr('height', self.HEIGHT);
      var background = self.chart.append("g")
          .attr("class", "background");
      background.append("rect")
          .attr('id', 'background-rect')
          .attr("width", self.GRAPH_WIDTH)
          .attr("height", self.HEIGHT)
          .attr("fill", "white")//color_manager.default_color)
          .style("opacity", .1);
      self.lefttop_area = background.append("g")
          .attr("class", "lefttop")
          .attr("transform", `translate(20, 20)`);
      self.righttop_area = background.append("g")
          .attr("class", "righttop")
          .attr("transform", `translate(${self.GRAPH_WIDTH - 100}, 20)`);
      self.leftbottom_area = background.append("g")
          .attr("class", "leftbottom")
          .attr("transform", `translate(20, ${self.HEIGHT - 100})`);
      self.lefttop_area.append("text")
          .attr('id','graph_label')
          .attr("x", 0)
          .attr("y", 20)
          .attr("text-anchor", "start")
          .attr("font-size", "24px")
          .attr("font-family", "Arial")
          .attr("fill", self.$color_manager.disable_color)
          .text("GRAPH STRUCTURE");

      self.rightbottom_area_hidden = false
      self.render_legend = () => {
        const legend_height = Math.max(160, self.GRAPH_WIDTH / 5, self.HEIGHT / 3.5);
        const legend_width = legend_height * 0.9;
        const margin = 10;
        background.selectAll("g.rightbottom").remove()
        self.rightbottom_area = background.append("g")
                    .attr("class", "rightbottom")
                    .attr("transform", `translate(${self.GRAPH_WIDTH
                        - (self.rightbottom_area_hidden ? 0 : legend_width)
                        - margin * 2}, ${self.HEIGHT - legend_height - margin * 2})`)
        self.rightbottom_area.append("image")
                    .attr("href", "/legend.png")
                    //.attr("clip-path", )
                    .attr("width", legend_width)
                    .attr("height", legend_height)
        self.rightbottom_area.append("rect")
                    .attr("x", -margin)
                    .attr("y", -margin)
                    .attr("width", legend_width + margin * 2)
                    .attr("height", legend_height + margin * 2)
                    .attr("stroke", self.$color_manager.disable_color)
                    .attr("stroke-width", 2)
                    .attr("fill", "none")
                    .attr("opacity", .5)

        self.rightbottom_area.append("text")
                    .attr("x", legend_width)
                    .attr("y", -24)
                    .attr("text-anchor", "end")
                    .attr("font-size", "24px")
                    .attr("fill", self.$color_manager.disable_color)
                    .text("LEGEND")


        self.rightbottom_area.append("text")
                    .attr("x", -10)
                    .attr("y", -24)
                    .attr("text-anchor", "start")
                    .attr("font-size", "24px")
                    .attr("fill", self.$color_manager.disable_color)
                    .attr("opacity", .5)
                    .text(self.rightbottom_area_hidden ? "◀" : "▶")//
                    .on("mouseover", function() {
                        d3.select(this).attr("opacity", 1)
                      // self.rightbottom_area.select("#arrow").attr("opacity", 1)
                    })
                    .on("mouseout", function() {
                        d3.select(this).attr("opacity", .5)
                      // self.rightbottom_area.select("#arrow").attr("opacity", .5)
                    })
                    .on("click", function(){
                        self.rightbottom_area_hidden = !self.rightbottom_area_hidden
                        self.render_legend()
                    })
            }
            self.render_legend()
      var backbtn = self.righttop_area.append("g")
                .attr("class", "back")
                .attr("transform", "translate(0, 0) scale(0.75)")
                .attr("opacity", .6)
                .on("mouseover", function(){
                    d3.select(this).attr("opacity", 1)
                })
                .on("mouseout", function(){
                    d3.select(this).attr("opacity", .5)
                })
                .on("click", function(){
                    self.moveTo(null)
                })

      backbtn.append("rect")
                .attr("width", 80)
                .attr("height", 60)
                .attr("fill", "white")
                .attr("stroke", self.$color_manager.disable_color)
                .attr("stroke-width", 3.5)
                .attr("rx", 5)
                .attr("ry", 5)

      backbtn.append("polygon")
                .attr("transform", "translate(10,0) scale(0.15)")
                .attr("points", "384,170.667 81.707,170.667 158.187,94.187 128,64 0,192 128,320 158.187,289.813 81.707,213.333 384,213.333")
                .attr("fill", self.$color_manager.disable_color)

      self.main_group = self.chart.append('g').attr('class', 'main_group');
      self.legend_group = self.chart.append('g').attr('class', 'legend_group');
      self.exploring_node_map = self.main_group.append('g').attr('class', 'exploring_node_map');
      self.exploring_cover_map = self.main_group.append('g').attr('class', 'exploring_cover_map');
      self.edge_map = self.main_group.append('g').attr('class', 'edge_map');
      self.node_map = self.main_group.append('g').attr('class', 'node_map');


      var zoomed = function (event) {
        self.main_group
            .attr("transform", event.transform);

      }
      self.zoom = d3.zoom()
          .on("zoom", zoomed);
      self.chart.call(self.zoom);

      // Define the arrowhead marker variables
      self.edge_map.append('defs')
                .append('marker')
                    .attr('id', 'edge-arrow')
                    .attr('viewBox', '0 -10 15 15')
                    .attr('refX', 15)
                    .attr('refY', 0)
                    .attr('markerWidth', 15)
                    .attr('markerHeight', 15)
                    .attr('markerUnits', 'userSpaceOnUse') // disable the effect of stroke width on the arrow
                    .attr('orient', 'auto')
                .append('path')
                    .attr('d', 'M0,-5 L10,0 L0,5Z')
                    .style('fill', '#999')

      self.legend_group = self.chart.append('g').attr('class', 'legend_group');

      self.guideview = d3.selectAll("#treeViewCom")
          .append('svg')
          .attr('id', 'guideview')
          .attr('width', self.TREE_WIDTH)
          .attr('height', self.HEIGHT);
      const svg = d3.selectAll("#treeViewCom").selectAll('#guideview')
                .style("font", "15px sans-serif")
                .style("user-select", "none")

      self.treeview = svg.append("g").attr("class","tree_view")

      const canvas = self.treeview.append("g").attr("id","tree_canvas")
                .attr("transform", `translate(${self.margin_tree.left},${self.margin_tree.top})`)


      const gLink = canvas.append("g").attr("id",'tree_link')
                .attr("fill", "none")
                .attr("stroke", "#555")
                .attr("stroke-opacity", 0.4)
                .attr("stroke-width", 1.5);

      const gNode = canvas.append("g").attr("id",'tree_node')
                .attr("cursor", "pointer")
                .attr("pointer-events", "all");
      var zoomed_tree = function (event) {
        gLink
            .attr("transform", event.transform);

        gNode
            .attr("transform", event.transform);
        // self.last_tree_scale = event.transform;
      }
      self.zoom_tree = d3.zoom()
          .on("zoom", zoomed_tree);
      self.guideview.call(self.zoom_tree);
       const guide_background = self.guideview.append("g")
           .attr("class", "background");
       var guide_lefttop_area = guide_background.append("g")
           .attr("class", "lefttop")
           .attr("transform", `translate(20, 20)`);
       guide_lefttop_area.append("text")
                .attr("x", 0)
                .attr("y", 20)
                .attr("text-anchor", "start")
                .attr("font-size", "24px")
                .attr("font-family", "Arial")
                .attr("fill", self.$color_manager.disable_color)
                .text("NAVIGATION");

       self.nodes = [];
            self.curr_all_nodes = [];
            self.exploring_nodes = [];
            self.edges = [];
            self.curr_all_edges = [];
            self.time_cost_height = 0;

            self.title_height = 20;
            self.node_width = 120;
            self.node_height = 36;
            self.node_expand_width = 240;
            self.node_expand_height = 166;
            self.var_node_r = 8;
            self.time_cost_unit_number = 10;
            self.duration = 500;
            self.remove_duration = 500;
            self.explore_btn_width = 18;
            self.exploring_level_delta = 10;
            self.expand_btn_width = 20;
            self.update_layout = false;
            self.focus_node_index = -1;
    },
    resize: function () {
            let self = this;
            var margins = self.margins;
            var d3 = self.$d3;
            self.TREE_WIDTH = (document.body.clientWidth - margins.left - margins.right) * 0.35 - margins.gap * 2;
            self.HEIGHT = document.body.clientHeight - margins.line_height - margins.bottom - margins.margin_top - margins.gap * 2;
            self.GRAPH_WIDTH = (document.body.clientWidth - margins.left - margins.right) * 0.65 - margins.gap * 2;

            self.chart
                .attr('width', self.GRAPH_WIDTH)
                .attr('height', self.HEIGHT);
            self.guideview
                .attr('width', self.TREE_WIDTH)
                .attr('height', self.HEIGHT)
            d3.selectAll('#NetworkComponent').attr('height', self.HEIGHT);

            self.chart.selectAll(".background").selectAll('background-rect')
                .attr("width", self.GRAPH_WIDTH)
                .attr("height", self.HEIGHT)
                .attr("fill", "white")
            self.righttop_area
                .attr("transform", `translate(${self.GRAPH_WIDTH - 100}, 20)`)
            self.righttop_area.selectAll(".back").selectAll('rect')
                .attr("width", 80)
                .attr("height", 60)
            self.leftbottom_area
                .attr("transform", `translate(20, ${self.HEIGHT - 100})`)
            self.rightbottom_area
                .attr("transform", `translate(${self.GRAPH_WIDTH - 120}, ${self.HEIGHT - 120})`);
            self.render_legend()

            var scale_tree = function () {
             // let scale = Math.min(self.HEIGHT / self.INIT_HEIGHT, self.TREE_WIDTH / self.INIT_TREE_WIDTH)\
              let scale;
              if(self.HEIGHT === self.INIT_HEIGHT)
                scale =  self.TREE_WIDTH / self.INIT_TREE_WIDTH;
              else if(self.TREE_WIDTH === self.INIT_TREE_WIDTH)
                scale =  self.HEIGHT / self.INIT_HEIGHT;
              else scale = Math.min(self.HEIGHT / self.INIT_HEIGHT, self.TREE_WIDTH / self.INIT_TREE_WIDTH);
             //  console.log(scale);
               self.treeview.attr('transform', `scale(${ self.last_tree_scale * scale})`)

            }
            scale_tree();
            self._generate_chart();
        },
    getNodetree: function() {

      let self = this
      const nodes = JSON.parse(JSON.stringify(self.all_nodes))
      nodes.forEach(node => {
        node.parent = null
      })
      nodes.forEach(node => {
        node.children = node.children.map(id => nodes[id])
        node.children.forEach(child => {
          child.father = node
        })
      })
      let root = {
        title: 'model',
        index: -1,
        children: nodes.filter(d => !d.father)
      }
      function visit(x) { //深度优先遍历
        x.size = 11
        for (let ch of x.children) {
          if (x.title != 'model') {
            self.all_nodes[ch.index].depth = self.all_nodes[x.index].depth + 1
          } else {
            self.all_nodes[ch.index].depth = 0
          }
          visit(ch)
          //self.all_nodes[ch.index].father = self.all_nodes[x.index]
          x.size += ch.size
        }
        if (x.title != 'model') {
          if (x.children.length == 0) {
            self.all_nodes[x.index].treenodes = [x.index]
          } else {
            self.all_nodes[x.index].treenodes = [x.index].concat(...x.children.map(e => self.all_nodes[e.index].treenodes))
          }
        }
        if (x.children.length <= 2)
          x.subnodes = [].concat(...x.children.map(d => d.children.length == 0 ? [d.index] : d.children.map(e => e.index)))
        else
          x.subnodes = [].concat(...x.children.map(d => [d.index]))
      }
      visit(root)
      nodes.push(root)
      nodes.forEach(node => {
        let next = []
        for (let i = 0; i < node.children.length; ++i) {
          next.push([])
          node.children[i].visited = false
        }
        for (let i = 0; i < node.children.length; ++i) {
          for (let j = i + 1; j < node.children.length; ++j) {
            if (node.children[i].next.indexOf(node.children[j].index) != -1) {
              next[i].push(j)
            } else if (node.children[j].next.indexOf(node.children[i].index) != -1) {
              next[j].push(i)
            }
          }
        }
        let orders = []
        let toposort = (x) => {
          if (node.children[x].visited) return
          node.children[x].visited = true
          for (let y of next[x]) {
            toposort(y)
          }
          orders.push(x)
        }
        for (let i = 0; i < node.children.length; ++i) {
          if (node.children[i].visited) continue
          toposort(i)
        }
        if (node.index != -1 && !self.all_nodes[node.index].attrs.shape && node.children.length > 0) {
          let current = self.all_nodes[node.index]
          let target = self.all_nodes[node.children[orders[0]].index] // 子节点中逆拓扑排序的第一个节点
          for (let i = 0; i < orders.length; ++i) {
            if (self.all_nodes[node.children[orders[i]].index].attrs.has_feature) {
              target = self.all_nodes[node.children[orders[i]].index]
              break
            }
          }
          current.attrs.has_feature = target.attrs.has_feature
          current.attrs.enable_expand = target.attrs.enable_expand
          current.attrs.shape = target.attrs.shape
          current.attrs.var_node_id = target.attrs.var_node_id
        }
        orders = orders.reverse()
        node.children = orders.map(i => node.children[i])
        let counts = {}
        for (let i = 0; i < node.children.length; ++i) {
          if (node.children[i].children.length == 0) {
            if (node.children[i].title == '') {
              node.children[i].title = node.children[i].type
            }
            counts[node.children[i].title] = (counts[node.children[i].title] || 0) + 1
          }
        }
        let newarr = []
        for (let i = 0; i < node.children.length; ++i) { // array * 10
          if (node.children[i].children.length == 0 && counts[node.children[i].title] > 1) {
            newarr.push({
              title: `${node.children[i].title} * ${counts[node.children[i].title]}`,
              nodes: node.children.filter(d => d.title == node.children[i].title),
              size: counts[node.children[i].title],
              index: node.children[i].index,
              children: [],
            })
            counts[node.children[i].title] = 0
          } else if (node.children[i].children.length > 0 || counts[node.children[i].title] == 1) {
            newarr.push(node.children[i])
          }
        }
        if (newarr.length > 20) {
          const arr1 = newarr.filter(d => d.children.length > 0)
          const arr2 = newarr.filter(d => d.children.length == 0)
          newarr = arr1.concat(arr2.slice(0, 15))
          newarr[newarr.length - 1].others = arr2.slice(10) //
          newarr[newarr.length - 1].title = newarr[newarr.length - 1].title + " ..."
        }
        node.children = newarr
      })
      return root
    },

    renderTree: function(nodetree) {
      const self = this
      var d3 = self.$d3;
      const margin = self.margin_tree;
      const diagonal = d3.linkHorizontal().x(d => d.y).y(d => d.x)
      const dx = 30
      const dy = 200
      const width = d3.selectAll("#treeViewCom").selectAll('#guideview').attr("width")
      const tree = d3.tree().nodeSize([dx, dy])
      const root = d3.hierarchy(nodetree)
      // console.log(root);
      let nodeSet = new Set(self.all_nodes.map(d => d.index))
      function expand(x) {
        x.focus = true
        if (nodeSet.has(x.data.index)) { //只展开第一层子节点？
          return
        }
        if (!x.children) {
          x.children = x._children
        }
        if (!x.children) {
          return
        }
        for (let ch of x.children) {
          expand(ch)
        }
      }
      function focus(x) {
        root.descendants().forEach((d, i) => {
          d._children = d._children || d.children
          d.focus = false
          if (d.depth >= 2) d.children = null;
        })
        expand(x)
        while (x) {
          x.children = x._children || x.children
          x = x.parent
        }
      }
      let last
      function moveTo(x) {
        last = x

        const back = d3.selectAll('#graphCom #networkView .background .righttop').select("g.back")
        const lbarea = d3.selectAll('#graphCom #networkView .background .leftbottom')
        lbarea.selectAll("*").remove()
        if (x.parent) {
          back.select("rect").attr("stroke", self.$color_manager.darker_default_color)
          back.select("polygon").attr("fill", self.$color_manager.darker_default_color)
          lbarea.append("text")
              .attr("dy", 40)
              .attr("fill", self.$color_manager.darker_text_color)
              .attr("font-size", "24px")
              .attr("font-style", "italic")
              .text(self.infopath(x.data.index))
          lbarea.append("text")
              .attr("dy", 72)
              .attr("fill", self.$color_manager.darker_text_color)
              .attr("font-size", "24px")
              .attr("font-style", "italic")
              .text(x.data.subnodes.length + ' nodes')
              // .text(x.subnodes.length + ' nodes')
        } else {
          back.select("rect").attr("stroke", self.$color_manager.disable_color)
          back.select("polygon").attr("fill", self.$color_manager.disable_color)
        }
        x.children = x._children;
        // const idx = x.subnodes
        const idx = x.data.subnodes
        // console.log(idx);
        nodeSet = new Set(idx)
        focus(x)
        self.curr_all_nodes = idx.map(x => self.all_nodes[x]);
        self.nodes = self.$tool.default.process_duplicated_brother_var_nodes(self.curr_all_nodes, self.all_edges);
        [self.nodes, self.curr_all_edges] = self.$tool.default.compute_edges(self.nodes, self.all_edges, self.all_nodes)
        self._generate_chart();
        update(x)
      }
      self.moveTo = (idx) => {
        if (idx === null) {
          if (last.parent)
            moveTo(last.parent)
          else
            moveTo(root)
          return
        }
        for (let i = 0; i < root.descendants().length; ++i) {
          if (root.descendants()[i].data.index == idx) {
            moveTo(root.descendants()[i])
            return
          }
        }
      }

      root.x0 = dy / 2;
      root.y0 = 0;
      root.descendants().forEach((d, i) => {
        d.id = i;
        d._children = d.children;
        d.focus = nodeSet.has(d.data.index)
        if (d.depth >= 2) d.children = null;
      });

      const svg = d3.selectAll("#treeViewCom").selectAll('#guideview')

      const height = svg.attr("height")

      self.treeview = svg.selectAll(".tree_view")

      const canvas = self.treeview.selectAll("#tree_canvas")
                .attr("transform", `translate(${margin.left},${margin.top})`)

      const gLink = canvas.selectAll("#tree_link")
                .attr("fill", "none")
                .attr("stroke", "#555")
                .attr("stroke-opacity", 0.4)
                .attr("stroke-width", 1.5);

      const gNode = canvas.selectAll("#tree_node")
      function update(source) {
                const duration = d3.event && d3.event.altKey ? 2500 : 250;
                const nodes = root.descendants().reverse();
                const links = root.links();

                // Compute the new tree layout.
                tree(root);

                let left = root;
                let right = root;
                let bottom = root;
                root.eachBefore(node => {
                    if (node.x < left.x) left = node;
                    if (node.x > right.x) right = node;
                    if (node.y > bottom.y) bottom = node;
                });

                let left_x = left.x
                let right_x = right.x
                let real_height = right_x - left_x
                // let real_width = bottom.y
                let real_width = bottom.y + bottom.data.title.length * 17 // font size?
                let offset_x = Math.max(((height - margin.top - margin.bottom) - real_height) / 2 - left_x + margin.top, -left.x + margin.top)
                let offset_y = (bottom.y + 2 * dy > width) ? 0 : ((bottom.y + 2 * dy - width) / 2);
                let scale = Math.min((height - margin.top - margin.bottom) / real_height, (width - margin.left - margin.right) / real_width)
                if (scale < 1) {
                    self.treeview.attr('transform', `scale(${scale})`)
                }
                  self.last_tree_scale = scale;
                self.INIT_TREE_WIDTH = self.TREE_WIDTH;
                self.INIT_HEIGHT = self.HEIGHT;

                self.treeview
                    .transition().duration(1000)
                    .call(self.zoom_tree.translateTo, self.TREE_WIDTH * 0.5, self.HEIGHT * 0.5)

                root.eachBefore(node => {
                    node.x += offset_x
                    node.y -= offset_y
                })

                const transition = svg.transition()
                    .duration(duration)
                    .tween("resize", window.ResizeObserver ? null : () => () => svg.dispatch("toggle"));

                // Update the nodes…
                const node = gNode.selectAll("g")
                    .data(nodes, d => d.id);

                // Enter any new nodes at the parent's previous position.
                const nodeEnter = node.enter().append("g")
                    .attr("transform", d => `translate(${source.y0},${source.x0})`)
                    .attr("fill-opacity", 0)
                    .attr("stroke-opacity", 0)
                    .on("click", (i, d) => {
                        if (!d.children) {
                            moveTo(d)
                        } else {
                            d.children = null
                            if (d.parent)
                                moveTo(d.parent)
                            else
                                moveTo(root)
                        }
                    });

                nodeEnter.append("circle")
                    .attr("class", "tree-btn")
                    .attr("r", 3.5)
                    .attr("fill", d => nodeSet.has(d.data.index) ? self.$color_manager.tree_highlight_color : self.$color_manager.tree_default_color)
                    .attr("stroke-width", 10);

                nodeEnter.append("line").attr("class", "hline")
                nodeEnter.append("line").attr("class", "vline")

                nodeEnter.append("text")
                    .attr("dy", "0.31em")
                    .attr("x", d => d._children ? -6 : 6)
                    .attr("text-anchor", d => d._children ? "end" : "start")
                    .attr("font-size", "21px")
                    .text(d => d.data.title)
                    .clone(true).lower()
                    .attr("stroke-linejoin", "round")
                    .attr("stroke-width", 3)
                    .attr("stroke", "white");

                // Transition nodes to their new position.
                const nodeUpdate = node.merge(nodeEnter).transition(transition)
                    .attr("transform", d => `translate(${d.y},${d.x})`)
                    .attr("fill-opacity", 1)
                    .attr("stroke-opacity", 1)

                nodeUpdate
                    .select("circle")
                    .attr("r", d => d._children && d._children.length > 0 ? 5 : 3.5)
                    .attr("fill", d => {
                        return d.focus ? self.$color_manager.tree_highlight_color : self.$color_manager.tree_default_color
                    })

                const glyph_r = 3

                nodeUpdate
                    .select("line.vline")
                    .attr("x1", -glyph_r)
                    .attr("y1", 0)
                    .attr("x2", glyph_r)
                    .attr("y2", 0)
                    .attr("stroke", "white")
                    .attr("stroke-width", d => (d._children && d._children.length > 0) ? 2 : 0)

                nodeUpdate
                    .select("line.hline")
                    .attr("x1", 0)
                    .attr("y1", -glyph_r)
                    .attr("x2", 0)
                    .attr("y2", glyph_r)
                    .attr("stroke", "white")
                    .attr("stroke-width", d => (!d.children && d._children && d._children.length > 0) ? 2 : 0)

                // Transition exiting nodes to the parent's new position.
                const nodeExit = node.exit().transition(transition).remove()
                    .attr("transform", d => `translate(${source.y},${source.x})`)
                    .attr("fill-opacity", 0)
                    .attr("stroke-opacity", 0);

                // Update the links…
                const link = gLink.selectAll("path")
                    .data(links, d => d.target.id);

                // Enter any new links at the parent's previous position.
                const linkEnter = link.enter().append("path")
                    .attr("d", d => {
                        const o = { x: source.x0, y: source.y0 };
                        return diagonal({ source: o, target: o });
                    })

                // Transition links to their new position.
                link.merge(linkEnter).transition(transition)
                    .attr("d", diagonal)
                    .attr("stroke", d => {
                        return d.target.focus ? self.$color_manager.tree_highlight_color : self.$color_manager.tree_default_color
                    })

                // Transition exiting nodes to the parent's new position.
                link.exit().transition(transition).remove()
                    .attr("d", d => {
                        const o = { x: source.x, y: source.y };
                        return diagonal({ source: o, target: o });
                    });

                // Stash the old positions for transition.
                root.eachBefore(d => {
                    d.x0 = d.x;
                    d.y0 = d.y;
                });
            }
      moveTo(root)
    },
    redraw: function (data) {
      let self = this;
      if (data) {
        self.data = data;
        // self.settings.data = data;
        let all_nodes = data['nodes'];
        let root = data['root'];
        let all_edges = data['edges'];
        all_nodes.forEach(d => {
          if (d.title.length > 20) {
            d.title = "block"
          } else if (d.title == '') {
            d.title = d.type + '_init'
          }
          if (d.attrs.var_node_id != -1 && d.attrs.has_feature) {
            d.attrs.enable_expand = 1
          } else {
            d.attrs.enable_expand = 0
          }
          d.pre = []
          d.next = []
        })
        all_edges.forEach(e => {
          e.start = e.start_stack[e.start_stack.length - 1]
          e.end = e.end_stack[e.end_stack.length - 1]
          for (let x of e.start_stack) {
            for (let y of e.end_stack) {
              all_nodes[y].pre.push(x)
              all_nodes[x].next.push(y)
            }
          }
        })
        self.all_nodes = all_nodes
        self.all_edges = all_edges
        self.curr_all_nodes = root.map(x => all_nodes[x]);

        const nodetree = self.getNodetree()
        self.nodes = self.$tool.default.process_duplicated_brother_var_nodes(self.curr_all_nodes, all_edges);
        [self.nodes, self.curr_all_edges] = self.$tool.default.compute_edges(self.nodes, self.all_edges, self.all_nodes)
        self.curr_all_edges = self.edges;
        all_nodes.forEach(function (node) {
          node.expand = false;
          node.expand_info = 'feature_map';
          node.exploring = false;
          node.name = `${node.index}`;
          if (node.is_var) {
            node.w = self.var_node_r * 2;
            node.h = self.var_node_r * 2;
          }
          else {
            node.w = self.node_width;
            node.h = self.node_height;
          }
          node.op_highlight = [];
        });
        self.renderTree(nodetree)
        self._generate_chart();
            }
        },
    infopath(idx) {
      let d = this.all_nodes[idx]
      let info = []
      for (let x = d; x && x.title != 'model'; x = this.all_nodes[x.parent]) {
        if (x.attrs && x.attrs.name) {
          info.push(x.attrs.name)
        } else {
          info.push(x.title)
        }
        if (x.parent == null || x.parent == undefined) {
          break
        }
      }
      info = info.reverse()
      return info.join('/')
    },

    _generate_chart: function () {
            let self = this;
            let data = self.data;

            let all_nodes = data['nodes'];
            let nodes = self.nodes;
            let edges = self.curr_all_edges;

            self.$DAGLayout(nodes, edges, (x, y) => [x, y]);
            let current_width = Math.max(...nodes.map(d => d.x)) + 100;
            let current_height = Math.max(...nodes.map(d => d.y)) + 50;
            const scale = Math.min((self.GRAPH_WIDTH - 80) / current_width, (self.HEIGHT - 120) / current_height)

            if (current_width > self.GRAPH_WIDTH) {
                self.chart
                    .transition().duration(1000)
                    .call(self.zoom.translateTo, current_width * 0.5, current_height * 0.5)
                    .delay(2000)
                    .transition().duration(1000)
                    .call(self.zoom.scaleTo, scale)
            } else {
                self.chart
                    .transition().duration(1000)
                    .call(self.zoom.translateTo, current_width * 0.5, current_height * 0.5)
                    .delay(2000)
                    .transition().duration(1000)
                    .call(self.zoom.scaleTo, Math.min(scale, 1.25))
            }

            nodes.forEach(node => {
                node.x += self.defaultVal.margin.left;
            });

            self.$tool.default.get_exploring_node_level_and_height(self, all_nodes, self.exploring_nodes);
            self.nodes = nodes;
            self.curr_all_edges = edges;
            self.op_nodes = [];
            self.nodes.forEach(function (node) {
                if (node.is_var) { //-----
                    // node.y += self.time_cost_height / 2;
                }
                else {
                    self.op_nodes.push(node);
                }
            });
        },
    _create_panelRow2: function () {
            let self = this;
            self._create_network_node();

            let paths = self.edge_map.selectAll('.network_edge')
                .data(self.edges, function (d) {
                    return `${d.start}-${d.end}`;
                });

            const line = self.$d3.line()
                .x(d => d.x)
                .y(d => d.y)
                .curve(self.$d3.curveBasis)

            paths.enter()
                .append('path')
                .attr('class', 'network_edge')
                .attr('id', function (d) {
                    return `network_edge_${d.start}-${d.end}`;
                })
                .attr('d', function (d) {
                    return line(d.points);
                })
                .attr('marker-end', 'url(#edge-arrow)')
                .style('stroke', self.$color_manager.edge_color)
                .style('stroke-width', '4px')
                .style('opacity', 0)
                .style('fill', 'none');

            self.$tool.default.init_network_click_menu(self);
        },
    _update_panelRow2: function () {
            let self = this;
            self._update_network_node();

            let paths = self.edge_map.selectAll('.network_edge')
                .data(self.edges, function (d) {
                    return `${d.start}-${d.end}`;
                });
            paths.transition()
                .duration(self.duration)
                .attr('d', function (d) {
                    return self.$tool.default.one_edge(d.points);
                })
                .style('opacity', .66)
        },
    _remove: function () {
            let self = this;
            let groups = self.node_map.selectAll('.op_node_group')
                .data(self.op_nodes, function (d) {
                    return d.name;
                });
            let exploring_cover_rects = self.exploring_cover_map.selectAll('.exploring_node_rect')
                .data(self.op_nodes, function (d) {
                    return d.name;
                });

            let paths = self.edge_map.selectAll('.network_edge')
                .data(self.edges, function (d) {
                    return `${d.start}-${d.end}`;
                });



            groups.exit()
                .transition()
                .duration(self.remove_duration)
                .style('opacity', 0);
            exploring_cover_rects.exit()
                .transition()
                .duration(self.remove_duration)
                .style('opacity', 0);
            // op_highlight_rect.exit()
            //     .transition()
            //     .duration(self.remove_duration)
            //     .style('opacity', 0);
            paths.exit()
                .transition()
                .duration(self.remove_duration)
                .style('opacity', 0);

            setTimeout(() => {
                groups.exit().remove();
                exploring_cover_rects.exit().remove();
                paths.exit().remove();
                // op_highlight_rect.exit().remove();
            }, self.remove_duration);
        },
    _create_network_node: function () {
            let self = this;
            let groups = self.node_map.selectAll('.op_node_group')
                .data(self.op_nodes, function (d) {
                    return d.name;
                })
            let g_groups = groups.enter()
                .append('g')
                .attr('class', 'op_node_group')
                .attr('id', function (d) {
                    return `op_node_group_${d.name}`;
                })
                .attr('cursor', "pointer")
                .attr('transform', function (d) {
                    return `translate(${d.x - d.w / 2},${d.y - d.h / 2})`;
                })
                .style('opacity', 0)
                .on("mouseenter", function (i, d) {
                    if (d.level > 0) {
                        self.node_map.selectAll(`.node_plus_btn_g_${d.name}`).transition().duration(self.duration).style('opacity', 1);
                    }
                    else {
                        self.node_map.selectAll(`.node_plus_btn_g_${d.name}`).transition().duration(self.duration).style('opacity', 0.5);
                    }
                    if (!d.attrs.enable_expand) return
                    self.node_map.selectAll(`#node_rect_${d.name}`)
                        .transition().duration(self.duration * 0.2)
                        .style('stroke', self.$color_manager.brother_node_highlight_color)
                        .style('stroke-width', 3)
                })
                .on("mouseleave", function (i, d) {
                    self.node_map.selectAll(`.node_plus_btn_g_${d.name}`).transition().duration(self.duration).style('opacity', 0);
                    self.node_map.selectAll(`.node_minus_btn_g_${d.name}`).transition().duration(self.duration).style('opacity', 0);

                    if (!d.attrs.enable_expand) return
                    self.node_map.selectAll(`#node_rect_${d.name}`)
                        .transition().duration(self.duration * 0.2)
                        .style('stroke', self.$color_manager.darker_default_color)
                        .style('stroke-width', 2);
                });

            g_groups.append('rect')
                .attr('class', 'node_background')
                .attr('id', function (d) {
                    return `node_background_${d.name}`;
                })
                .attr('cursor', "pointer")
                .attr('x', 0)
                .attr('y', 0)
                .attr('width', function (d) {
                    return d.w;
                })
                .attr('height', function (d) {
                    return d.h;
                })
                .style('fill', 'transparent');
            let main_rect_g = g_groups.selectAll('.node_main_rect_g').data(function (d) {
                return [d];
            });
            let main_rect_g_g = main_rect_g.enter().append('g')
                .attr('class', 'node_main_rect_g')
                .attr('id', function (d) {
                    return `node_main_rect_g_${d.name}`;
                })
                .attr('cursor', "pointer")
                .on("click", function (i, d) {
                    if (d.attrs.has_feature) {
                        d.expand = !d.expand;
                        if (d.expand) {
                            d.w = self.node_expand_width;
                            d.h = self.node_expand_height;
                        }
                        else {
                            d.w = self.node_width;
                            d.h = self.node_height;
                        }
                        self._generate_chart();
                    }

                })
                .on('mouseenter', function (i, d) {
                    self.focus_node_index = d.index;
                });
            main_rect_g_g.selectAll('.node_rect').data(function (d) {
                return [d];
            }).enter().append('rect')
                .attr('class', 'node_rect')
                .attr('id', function (d) {
                    return `node_rect_${d.name}`;
                })
                .attr('cursor', "pointer")
                .attr('x', 0)
                .attr('y', self.time_cost_height)
                .attr('stroke-dasharray', d => d.status == 'inner' ? '10,0' : '10')
                .attr('rx', d => d.children && d.children.length > 0 ? d.h / 4 : 0)
                .attr('ry', d => d.children && d.children.length > 0 ? d.h / 4 : 0)
                .attr('width', function (d) {
                    return d.w;
                })
                .attr('height', function (d) {
                    return d.h// - self.time_cost_height * 2;
                })
                .style('fill', function (d) {
                    return self.$color_manager.lighter_default_color
                })
                .style('stroke', function (d) {
                    return self.$color_manager.darker_default_color;
                })
                .style('stroke-width', 2);



            main_rect_g_g.append('text')
                .attr('class', 'node_name_text')
                .attr('id', function (d) {
                    return `node_name_text_${d.name}`;
                })
                .text(function (d) {
                    let title = d.title;
                    if (d.expand) {
                        if (title.length > 15) {
                            return self.$tool.default.short_title(title, 15);
                        }
                        return title;
                    }
                    return self.$tool.default.short_title(title, 8);
                })
                .attr("font-size", "22px")
                .attr("fill", self.$color_manager.darker_default_color)
                .attr('cursor', "pointer")
                .attr('x', function (d) {
                  // console.log(d.title,' ',d.w, ' ', self.expand_btn_width);
                    if (d.expand) {
                        return (d.w - self.expand_btn_width) / 2;
                    }
                    return d.w / 2;
                })
                .attr('y', function (d) {
                    if (d.expand) {
                        return self.title_height / 2 + self.time_cost_height;
                    }
                    return d.h / 2;
                })
                .style("text-anchor", "middle")
                .style("user-select", "none")
                .style('dominant-baseline','central')

            main_rect_g_g.append('image')
                .attr('class', 'node_expand_image')
                .attr('id', function (d) {
                    return `node_expand_image_${d.name}`;
                })
                .attr('cursor', "pointer")
                .attr('x', function (d) {
                    return d.w / 20;
                })
                .attr('y', function (d) {
                    return (d.h + 19 * (self.title_height + self.time_cost_height)) / 20;
                })
                .attr('width', function (d) {
                    return 0;
                })
                .attr('height', function (d) {
                    return 0;
                })
                .style('opacity', function (d) {
                    return 0;
                });

            let btn_g = g_groups.append('g')
                .attr('class', 'node_btn_g')
                .attr('transform', function (d) {
                    return `translate(${d.w - self.explore_btn_width},0)`;
                });

            let plus_btn_g = btn_g.append('g')
                .attr('class', function (d) {
                    return `node_plus_btn_g_${d.name}`;
                })
                .attr('cursor', "pointer")
                .style('opacity', 0)
                .on("mouseenter", function (i, d) {
                    if (d.level > 0) {
                        self.node_map.selectAll(`#node_plus_btn_rect_${d.name}`)
                            .transition()
                            .duration(self.duration)
                            .style('fill', self.$color_manager.node_btn_highlight_background_color);
                    }
                })
                .on("mouseleave", function (i, d) {
                    if (d.level > 0) {
                        self.node_map.selectAll(`#node_plus_btn_rect_${d.name}`)
                            .transition()
                            .duration(self.duration)
                            .style('fill', 'white');
                    }
                })
                .on("click", function (i, d) {
                    self.moveTo(d.index)
                });
            plus_btn_g.append('circle')
                .attr('class', 'node_btn_rect')
                .attr('id', function (d) {
                    return `node_plus_btn_rect_${d.name}`;
                })
                .attr('cx', 4)
                .attr('cy', self.time_cost_height + self.explore_btn_width / 2 + 3)
                .attr('r', self.explore_btn_width / 2 - 2)
                .style('stroke', d => d.children.length > 0 ? self.$color_manager.darker_default_color : "white")//color_manager.default_color)
                .style('stroke-width', 1.5)
                .style('fill', 'white');

            plus_btn_g.append('path')
                .attr('class', 'node_btn_path')
                .attr('transform', `translate(${-self.explore_btn_width / 2},${self.explore_btn_width})`)
                .attr('id', function (d) {
                    return `node_plus_btn_path_${d.name}`;
                })
                .attr('d', function (d) {
                    return self.$tool.default.plus_path_d(self.explore_btn_width / 2, self.time_cost_height - self.explore_btn_width / 2 - 1, self.explore_btn_width / 2 - 1, self.explore_btn_width / 2 - 1, 1.5);
                })
                .attr('cursor', "pointer")
                .style('fill', function (d) {
                    if (d.children.length > 0) {
                        return self.$color_manager.darker_default_color
                    }
                    return "white"//color_manager.default_color;
                });

            let expand_btn_g = g_groups.append('g')
                .attr('class', 'node_expand_btn_g')
                .attr('transform', function (d) {
                    if (d.expand) {
                        return `translate(${d.w - self.expand_btn_width + 1},${self.time_cost_height})`;
                    }
                    return `translate(${d.w},${self.time_cost_height})`;
                })
                .style('opacity', function (d) {
                    if (d.expand) {
                        return 1;
                    }
                    return 0;
                });

                let activation_matrix_btn_g = expand_btn_g.append('g')
                .attr('class', function (d) {
                    return `node_expand_activation_matrix_btn_g`;
                })
                .attr('id', function (d) {
                    return `node_expand_activation_matrix_btn_g_${d.name}`;
                })
                .attr('cursor', "pointer")
                .on("mouseenter", function (i, d) {
                    if (d.expand_info !== 'activation_matrix') {
                        self.node_map.selectAll(`#node_expand_activation_matrix_btn_rect_${d.name}`)
                            .transition()
                            .duration(self.duration)
                            .style('fill', self.$color_manager.expand_btn_highlight_color);
                    }
                })
                .on("mouseleave", function (i, d) {
                    if (d.expand_info !== 'activation_matrix') {
                        self.node_map.selectAll(`#node_expand_activation_matrix_btn_rect_${d.name}`)
                            .transition()
                            .duration(self.duration)
                            .style('fill', self.$color_manager.default_color);
                    }
                })
                .on("click", function (i, d) {
                    if (d.expand_info !== 'activation_matrix') {
                        d.expand_info = 'activation_matrix';
                        self._update_network_node();
                        self.node_map.selectAll(`#node_expand_activation_matrix_btn_g_${d.name}`).raise();
                    }
                });

            activation_matrix_btn_g.append('rect')
                .attr('class', 'node_expand_activation_matrix_btn_rect')
                .attr('id', function (d) {
                    return `node_expand_activation_matrix_btn_rect_${d.name}`;
                })
                .attr('x', 0)
                .attr('y', 0)
                .attr('rx', 2)
                .attr('ry', 2)
                .attr('width', function (d) {
                    if (d.expand) {
                        return self.expand_btn_width;
                    }
                    return 0;
                })
                .attr('height', function (d) {
                    if (d.expand) {
                        return (d.h - self.time_cost_height * 2) * 0.7;
                    }
                    return 0;
                })
                .style('stroke', self.$color_manager.default_color)
                .style('stroke-width', 1)
                .style('fill', function (d) {
                    if (d.expand_info === 'activation_matrix') {
                        return self.$color_manager.expand_btn_highlight_color;
                    }
                    return self.$color_manager.default_color
                });
            activation_matrix_btn_g.append('g')
                .attr('class', 'node_expand_activation_matrix_btn_text_g')
                .attr('transform', function (d) {
                    return `rotate(90 0 0) translate(${(d.h - self.time_cost_height * 2) * 0.35}, ${-self.expand_btn_width / 2})`;
                })
                .append('text')
                .attr('class', 'node_expand_activation_matrix_btn_text')
                .attr('id', function (d) {
                    return `node_expand_activation_matrix_btn_text_${d.name}`;
                })
                .attr('cursor', "pointer")
                .attr('x', 0)
                .attr('y', 0)
                .style("user-select", "none")
                .style('text-anchor', 'middle')
                .style('dominant-baseline', 'central')
                .style('font-size', '12px')
                .style('font-family', 'Arial');
            let feature_map_btn_g = expand_btn_g.append('g')
                .attr('class', function (d) {
                    return `node_expand_feature_map_btn_g`;
                })
                .attr('id', function (d) {
                    return `node_expand_feature_map_btn_g_${d.name}`;
                })
                .attr('transform', function (d) {
                    return `translate(0, ${(d.h - self.time_cost_height * 2) * 0.3})`;
                })
                .attr('cursor', "pointer")
                .on("mouseenter", function (i, d) {
                    if (d.expand_info !== 'feature_map') {
                        self.node_map.selectAll(`#node_expand_feature_map_btn_rect_${d.name}`)
                            .transition()
                            .duration(self.duration)
                            .style('fill', self.$color_manager.expand_btn_highlight_color);
                    }
                })
                .on("mouseleave", function (i, d) {
                    if (d.expand_info !== 'feature_map') {
                        self.node_map.selectAll(`#node_expand_feature_map_btn_rect_${d.name}`)
                            .transition()
                            .duration(self.duration)
                            .style('fill', self.$color_manager.default_color);
                    }
                })
                .on("click", function (i, d) {
                    if (d.expand_info !== 'feature_map') {
                        d.expand_info = 'feature_map';
                        self._update_network_node();
                        self.node_map.selectAll(`#node_expand_feature_map_btn_g_${d.name}`).raise();
                    }
                });
            feature_map_btn_g.append('rect')
                .attr('class', 'node_expand_feature_map_btn_rect')
                .attr('id', function (d) {
                    return `node_expand_feature_map_btn_rect_${d.name}`;
                })
                .attr('x', 0)
                .attr('y', 0)
                .attr('rx', 2)
                .attr('ry', 2)
                .attr('width', function (d) {
                    if (d.expand) {
                        return self.expand_btn_width;
                    }
                    return 0;
                })
                .attr('height', function (d) {
                    if (d.expand) {
                        return (d.h - self.time_cost_height * 2) * 0.7;
                    }
                    return 0;
                })
                .style('stroke', self.$color_manager.default_color)
                .style('stroke-width', 1)
                .style('fill', function (d) {
                    if (d.expand_info === 'feature_map') {
                        return self.$color_manager.expand_btn_highlight_color;
                    }
                    return self.$color_manager.default_color
                });
            feature_map_btn_g.append('g')
                .attr('class', 'node_expand_feature_map_btn_text_g')
                .attr('transform', function (d) {
                    return `rotate(90 0 0) translate(${(d.h - self.time_cost_height * 2) * 0.35}, ${-self.expand_btn_width / 2})`;
                })
                .append('text')
                .attr('class', 'node_expand_feature_map_btn_text')
                .attr('id', function (d) {
                    return `node_expand_feature_map_btn_text_${d.name}`;
                })
                .attr('cursor', "pointer")
                .attr('x', 0)
                .attr('y', 0)
                .style("user-select", "none")
                .style('text-anchor', 'middle')
                .style('dominant-baseline', 'central')
                .style('font-size', '12px')
                .style('font-family', 'Arial');


            let extra_info = g_groups.append('g')
                .attr('class', 'extra_info')

            extra_info.append('text')
                .attr('class', 'shape')
                .attr("font-size", "13px")


            let max_time_cost = 0;
            self.op_nodes.forEach(node => {
                if (node.time_cost > max_time_cost) {
                    max_time_cost = node.time_cost;
                }
            });

            let exploring_cover_rects = self.exploring_cover_map.selectAll('.exploring_node_rect')
                .data(self.op_nodes, function (d) {
                    return d.name;
                });

            exploring_cover_rects.enter().append('rect')
                .attr('class', 'exploring_node_rect')
                .attr('id', function (d) {
                    return `exploring_node_rect_${d.name}`;
                })
                .attr('cursor', "pointer")
                .attr('x', function (d) {
                    return d.x - d.w / 2 - self.exploring_level_delta / 2;
                })
                .attr('y', function (d) {
                    return d.y - d.h / 2 - self.exploring_level_delta / 2;
                })
                .style('rx', function (d) {
                    return self.exploring_level_delta;
                })
                .style('ry', function (d) {
                    return self.exploring_level_delta;
                })
                .attr('width', function (d) {
                    return d.w + self.exploring_level_delta;
                })
                .attr('height', function (d) {
                    return d.h + self.exploring_level_delta;
                })
                .style('opacity', 0)
                .style('fill', 'transparent');

        },
    _update_network_node: function () {
            let self = this;
            let groups = self.node_map.selectAll('.op_node_group')
                .data(self.op_nodes, function (d) {
                    return d.name;
                });
            groups.transition()
                .duration(self.duration)
                .style('opacity', 1)
                .attr('transform', function (d) {
                    return `translate(${d.x - d.w / 2},${d.y - d.h / 2})`;
                });

            groups.selectAll('.node_background').data(function (d) {
                return [d];
            }).transition()
                .duration(self.duration)
                .attr('width', function (d) {
                    return d.w;
                })
                .attr('height', function (d) {
                    return d.h;
                });

            let main_rect_g = groups.selectAll('.node_main_rect_g').data(function (d) {
                return [d];
            });

            main_rect_g.selectAll('.node_rect').data(function (d) {
                return [d];
            }).transition()
                .duration(self.duration)
                .attr('width', function (d) {
                    if (d.expand) {
                        return d.w - self.expand_btn_width;
                    }
                    return d.w;
                })
                .style('fill', function (d) {
                    return self.$color_manager.get_color_by_exploring_height(d.exploring_height);
                })
                .attr('stroke-dasharray', d => d.status == 'inner' ? '10,0' : '10')//----?
                .attr('height', function (d) {
                    return d.h - self.time_cost_height * 2;
                });

            main_rect_g.selectAll('.node_name_text').data(function (d) {
                return [d];
            }).transition()
                .duration(self.duration)
                .attr('x', function (d) {
                    if (d.expand) {
                        return (d.w - self.expand_btn_width) / 2;
                    }
                    return d.w / 2;
                })
                .attr('y', function (d) {
                    if (d.expand) {
                        return self.title_height / 2 + self.time_cost_height;
                    }
                    return d.h / 2;
                })
                .text(function (d) {
                    let title = d.title;
                    if (d.expand) {
                        if (title.length > 15) {
                            return self.$tool.default.short_title(title, 15);
                        }
                        return title;
                    }
                    return self.$tool.default.short_title(title, 8);
                });

            main_rect_g.selectAll('.node_expand_image').data(function (d) {
                return [d];
            }).transition()
                .duration(self.duration)
                .attr('x', function (d) {
                    if (d.expand) {
                        return (d.w - self.expand_btn_width) / 20;
                    }
                    return d.w / 20;
                })
                .attr('y', function (d) {
                    return (d.h + 19 * (self.title_height + self.time_cost_height)) / 20;
                })
                .attr('width', function (d) {
                    if (d.expand) {
                        return (d.w - self.expand_btn_width) * 0.9;
                    }
                    return 0;
                })
                .attr('height', function (d) {
                    if (d.expand) {
                        return (d.h - self.title_height - self.time_cost_height * 2) * 0.9;
                    }
                    return 0;
                })
                .attr("xlink:href", function (d) {

                    return d.attrs.enable_expand ?
                        `http://166.111.80.25:5010/api/get_image?dataset=default&data_id=${d.index}&var_node_id=${d.attrs.var_node_id}&shape=${d.attrs.shape}&image_type=${d.expand_info}` :
                        ''
                })
                .style('opacity', function (d) {
                    if (d.expand) {
                        return 1;
                    }
                    return 0;
                });

            groups.selectAll('.node_btn_g').data(function (d) {
                return [d];
            }).transition()
                .duration(self.duration)
                .attr('transform', function (d) {
                    if (d.expand) {
                        return `translate(${d.w - self.explore_btn_width - self.expand_btn_width},0)`;
                    }
                    return `translate(${d.w - self.explore_btn_width},0)`;
                });

            groups.selectAll('.node_expand_btn_g').data(function (d) {
                return [d];
            }).transition()
                .duration(self.duration)
                .attr('transform', function (d) {
                    if (d.expand) {
                        return `translate(${d.w - self.expand_btn_width + 1},${self.time_cost_height})`;
                    }
                    return `translate(${d.w},${self.time_cost_height})`;
                })
                .style('opacity', function (d) {
                    if (d.expand) {
                        return 1;
                    }
                    return 0;
                });


            groups.selectAll('.node_expand_btn_g')
                .selectAll('.node_expand_feature_map_btn_g')
                .data(function (d) {
                    return [d];
                }).transition()
                .duration(self.duration)
                .attr('transform', function (d) {
                    return `translate(0, ${(d.h - self.time_cost_height * 2) * 0.3})`;
                });

            groups.selectAll('.node_expand_btn_g')
                .selectAll('.node_expand_feature_map_btn_g')
                .selectAll('.node_expand_feature_map_btn_rect')
                .data(function (d) {
                    return [d];
                }).transition()
                .duration(self.duration)
                .attr('width', function (d) {
                    if (d.expand) {
                        return self.expand_btn_width;
                    }
                    return 0;
                })
                .attr('height', function (d) {
                    if (d.expand) {
                        return (d.h - self.time_cost_height * 2) * 0.7;
                    }
                    return 0;
                })
                .style('fill', function (d) {
                    if (d.expand_info === 'feature_map') {
                        return self.$color_manager.expand_btn_highlight_color;
                    }
                    return self.$color_manager.default_color
                });

            groups.selectAll('.node_expand_btn_g')
                .selectAll('.node_expand_feature_map_btn_g')
                .selectAll('.node_expand_feature_map_btn_text_g')
                .data(function (d) {
                    return [d];
                }).transition()
                .duration(self.duration)
                .attr('transform', function (d) {
                    return `rotate(90 0 0) translate(${(d.h - self.time_cost_height * 2) * 0.35}, ${-self.expand_btn_width / 2})`;
                });

            groups.selectAll('.node_expand_btn_g')
                .selectAll('.node_expand_feature_map_btn_g')
                .selectAll('.node_expand_feature_map_btn_text_g')
                .selectAll('.node_expand_feature_map_btn_text')
                .data(function (d) {
                    return [d];
                }).transition()
                .duration(self.duration)
                .text(function (d) {
                    if (d.expand) {
                        return 'feature map';
                    }
                    return '';
                });


            groups.selectAll('.node_expand_btn_g')
                .selectAll('.node_expand_activation_matrix_btn_g')
                .selectAll('.node_expand_activation_matrix_btn_rect')
                .data(function (d) {
                    return [d];
                }).transition()
                .duration(self.duration)
                .attr('width', function (d) {
                    if (d.expand) {
                        return self.expand_btn_width;
                    }
                    return 0;
                })
                .attr('height', function (d) {
                    if (d.expand) {
                        return (d.h - self.time_cost_height * 2) * 0.7;
                    }
                    return 0;
                })
                .style('fill', function (d) {
                    if (d.expand_info === 'activation_matrix') {
                        return self.$color_manager.expand_btn_highlight_color;
                    }
                    return self.$color_manager.default_color
                });

            groups.selectAll('.node_expand_btn_g')
                .selectAll('.node_expand_activation_matrix_btn_g')
                .selectAll('.node_expand_activation_matrix_btn_text_g')
                .data(function (d) {
                    return [d];
                }).transition()
                .duration(self.duration)
                .attr('transform', function (d) {
                    return `rotate(90 0 0) translate(${(d.h - self.time_cost_height * 2) * 0.35}, ${-self.expand_btn_width / 2})`;
                });

            groups.selectAll('.node_expand_btn_g')
                .selectAll('.node_expand_activation_matrix_btn_g')
                .selectAll('.node_expand_activation_matrix_btn_text_g')
                .selectAll('.node_expand_activation_matrix_btn_text')
                .data(function (d) {
                    return [d];
                })
                .transition()
                .duration(self.duration)
                .text(function (d) {
                    if (d.expand) {
                        return 'activation matrix';
                    }
                    return '';
                });

            self.node_map.selectAll(".op_node_group")
                .select(".extra_info")
                //.style("opacity", d => d.status == "inner" ? 1 : 0)

            self.node_map.selectAll(".op_node_group")
                .select(".extra_info")
                .select(".shape")
                .attr("fill", self.$color_manager.darker_default_color)
                .attr("dx", d => d.w / 2 + 10)
                .attr("dy", d => d.h + 15)
                .text(d => {
                    if (d.status == "outer") {
                        return self.infopath(d.index)
                    }
                    return d.attrs.shape ? `shape: [${d.attrs.shape.slice(1, d.attrs.shape.length - 2)}]` : `children: ${d.children.length}`
                })


            let max_time_cost = 0;
            self.op_nodes.forEach(node => {
                if (node.time_cost > max_time_cost) {
                    max_time_cost = node.time_cost;
                }
            });



            self.exploring_cover_map.selectAll('.exploring_node_rect')
                .data(self.op_nodes, function (d) {
                    return d.name;
                }).transition()
                .duration(self.duration)
                .attr('x', function (d) {
                    return d.x - d.w / 2 - self.exploring_level_delta / 2;
                })
                .attr('y', function (d) {
                    return d.y - d.h / 2 - self.exploring_level_delta / 2;
                })
                .style('rx', function (d) {
                    return self.exploring_level_delta;
                })
                .style('ry', function (d) {
                    return self.exploring_level_delta;
                })
                .attr('width', function (d) {
                    return d.w + self.exploring_level_delta;
                })
                .attr('height', function (d) {
                    return d.h + self.exploring_level_delta;
                })
                .style('fill', function (d) {
                    return self.$color_manager.brother_node_highlight_color;
                })
                .style('stroke', self.$color_manager.node_border_color)
                .style('stroke-width', 1);
        },
    show_detail_info(){
      this._show_detail_info();
    },
    _show_detail_info: function () {
            let self = this;
            if (self.focus_node_index !== -1) {
                let node = self.data['nodes'][self.focus_node_index];
                let keys = ['index', 'id', 'time_cost', 'title', 'type', 'code_path', 'line_num', 'name'];
                let add_keys = ['scope']; // different attributes to show -- pytorch model
                for (let key_index in add_keys){
                  var key = add_keys[key_index];
                  if(key in node){
                    keys.push(key);
                  }
                }
                let max_size = 100;
                let values = {};
                keys.forEach((key, i) => {
                    if (node[key] !== undefined && ('' + node[key]).length > 0) {
                        max_size = Math.max(max_size, (key + ': ' + node[key]).length);
                        values[key] = node[key];
                    }
                });
                for (let key in node.attrs) {
                    if (keys.indexOf(key) === -1) {
                        max_size = Math.max(max_size, (key + ': ' + node.attrs[key]).length);
                        values[key] = node.attrs[key];
                        keys.push(key);
                    }
                }

                let width = Math.min(500, max_size * 5);
                // let tdv = document.getElementById('info-tip-div');
                let tag_id = '';
                if (node.is_var) {
                    tag_id = `var_node_group_${node.index}`;
                }
                else {
                    tag_id = `op_node_group_${node.index}`;
                }
                let bbox = self.$d3.selectAll(`#${tag_id}`).node().getBoundingClientRect();
                let attrs = {
                    top: bbox.top,
                    left: bbox.left - width - 10,
                    opacity: 1,
                    width: width,
                    values: values,
                    title: `node: ${node.title}`
                };
                console.log(attrs);
                self.$tool.default.set_content_of_tooltip(self, attrs);
            }
        },


    _hide_detail_info: function () {
            let self = this;
        },

    hide_detail_info(){
      this._hide_detail_info();
    },
    _create_network_exploring_node: function () {
            let self = this;
            let exploring_nodes = self.$tool.default.filter_exploring_nodes(self.exploring_nodes);
            let groups = self.exploring_node_map.selectAll('.exploring_node_group')
                .data(exploring_nodes, function (d) {
                    return d.name;
                });
            let g_groups = groups.enter()
                .append('g')
                .attr('class', 'exploring_node_group')
                .attr('id', function (d) {
                    return `exploring_node_group_${d.name}`;
                })
                .style('opacity', 0)
                .attr('cursor', "pointer");
            g_groups.append('g').attr('class', 'exploring_node_bg_rect_g');
            g_groups.append('g').attr('class', 'exploring_node_bg_path_g');
            g_groups.append('g').attr('class', 'exploring_node_path_border_g');
            g_groups.append('g').attr('class', 'exploring_node_rect_g');
            g_groups.append('g').attr('class', 'exploring_node_path_g');


            let exploring_hull_paths = self.exploring_node_map.selectAll('.exploring_node_group')
                .selectAll('.exploring_node_bg_path_g')
                .selectAll('.exploring_hull_path')
                .data(function (d) {
                    return [d];
                });

            exploring_hull_paths.enter()
                .append('path')
                .attr('class', 'exploring_hull_path')
                .attr('id', function (d) {
                    return `exploring_hull_path_${d.index}`;
                })
                .attr('d', function (d) {
                    let path = '';
                    if (d.hull_points !== undefined) {
                        d.hull_points.forEach(points => {
                            path += spline(points);
                        });
                    }
                    return path;
                })
                .style('stroke-width', '1px')
                .style('opacity', '1')
                .style('stroke', self.$color_manager.node_border_color)
                .style('fill', function (d) {
                    return self.$color_manager.get_color_by_exploring_height(d.exploring_height);
                });

        },
    _update_network_exploring_node: function () {
            let self = this;
            let exploring_nodes = self.$tool.default.filter_exploring_nodes(self.exploring_nodes);
            let groups = self.exploring_node_map.selectAll('.exploring_node_group')
                .data(exploring_nodes, function (d) {
                    return d.name;
                });

            groups.transition()
                .duration(self.duration)
                .style('opacity', 1);

            self.exploring_node_map.selectAll('.exploring_node_group')
                .selectAll('.exploring_node_bg_path_g')
                .selectAll('.exploring_hull_path')
                .data(function (d) {
                    return [d];
                }).transition()
                .duration(self.duration)
                .attr('d', function (d) {
                    let path = '';
                    if (d.hull_points !== undefined) {
                        d.hull_points.forEach(points => {
                            path += spline(points);
                        });
                    }
                    return path;
                })
                .style('fill', function (d) {
                    return self.$color_manager.get_color_by_exploring_height(d.exploring_height);
                });

            groups.selectAll('.exploring_node_btn_g').data(function (d) {
                return [d];
            }).transition()
                .duration(self.duration)
                .attr('transform', function (d) {
                    return `translate(${d.del_btn_pos['x'] - self.explore_btn_width / 2},${d.del_btn_pos['y']})`;
                });
        },
    _repaint: function () {
            let self = this;

            let edges = [];
            let edge_dic = {};
            self.curr_all_edges.forEach(edge => {
                edge.points.forEach(point => {
                    point.x += self.defaultVal.margin.left;
                });

                if (!edge.isLong) {
                    let start_node = edge.startNode;
                    let end_node = edge.endNode;
                    if (edge_dic[start_node.index] === undefined) {
                        edge_dic[start_node.index] = {
                            'left_edge_index': [],
                            'right_edge_index': []
                        }
                    }
                    edge_dic[start_node.index]['right_edge_index'].push(edges.length);

                    if (edge_dic[end_node.index] === undefined) {
                        edge_dic[end_node.index] = {
                            'left_edge_index': [],
                            'right_edge_index': []
                        }
                    }
                    edge_dic[end_node.index]['left_edge_index'].push(edges.length);

                    let y_direction = self.$tool.default.sgn(end_node.y - start_node.y);
                    let reversed = false;
                    if (y_direction < 0) {
                        end_node = edge.startNode;
                        start_node = edge.endNode;
                        y_direction = 1;
                        reversed = true;
                    }
                    const margin = 10
                    if (self.update_layout) {
                        let points = [];

                        points.push({
                            'x': start_node.x,
                            'y': start_node.y - y_direction * margin
                        });
                        points.push({
                            'x': end_node.x,
                            'y': end_node.y + y_direction * margin
                        });

                        edge.points = points;
                    }
                    else if (reversed) {
                        edge.points.reverse();
                    }
                    edges.push(edge);
                }
            });
            edges.forEach(edge => {
                let start_node = edge.startNode;
                let end_node = edge.endNode;

                let x_direction = self.$tool.default.sgn(end_node.x - start_node.x);
                let reversed = false;
                if (x_direction < 0) {
                    reversed = true;
                }
            });
            self.edges = edges;

            self.op_nodes.forEach(node => {
                self.$tool.default.get_exploring_height_of_node(node, self.data.nodes);
            });
            self.edges.forEach(edge => {
                self.$tool.default.get_exploring_height_of_edge(edge);
            });
            self._remove();
            setTimeout(() => {
                // self._pre_update();
                setTimeout(() => {
                    self._update_panelRow2();
                    setTimeout(() => {
                        self._create_panelRow2();
                        self._update_panelRow2();
                    }, self.duration);
                }, self.duration);

            }, self.remove_duration);
        },
    repaint(){
      this._repaint();
    }
  }
}
</script>

<style>
/*@import "public/lib/css/flex.css"*/
#panelRow2Com{
  /*background: white;*/
  display: flex;
  flex-direction: column;
  margin: 0 0 0 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  padding: 0 30px 30px 30px ;
  box-sizing: border-box;
  background: rgb(0,0,0,5%);
}
#NetworkPanel {
  /*background: white;*/
  display: flex;
  flex-direction: row;
  margin-top: 3px;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}
#NetworkComponent {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 100%;
}
#treeViewBackground{
  width: 35%;
  height: 100%;
  float: left;
  /*box-shadow: 0 1px 3px 3px rgb(0 0 0 / 25%);*/
  /*background: rgb(32, 151, 246);*/
  border: 20px solid rgb(0,0,0,0%);
  /*border-top: 30px;*/
  box-sizing: border-box;
  /*border-radius:5px;*/

}
#graphViewBackground{
  /*background: #bbdefb;*/
  width: 65%;
  height: 100%;
  float: right;
  /*box-shadow: 0 1px 0px 3px rgb(0 0 0 / 25%);*/
  border: 20px solid rgb(0,0,0,0%);
  box-sizing: border-box;
}
#treeViewCom{
  width: 100%;
  height: 100%;
  border-radius:15px;
  background: white;
  box-sizing: border-box;
}
#graphCom{
  /*background: #bbdefb;*/
  width: 100%;
  height: 100%;
  border-radius: 15px;
  background: white;
  box-sizing: border-box;
}
</style>