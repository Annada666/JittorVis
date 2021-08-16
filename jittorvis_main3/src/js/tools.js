export default {
    path_d,
    arrow_path_d,
    process_duplicated_brother_var_nodes,
    compute_edges,
    get_exploring_node_level_and_height,
    short_title,
    filter_exploring_nodes,
    sgn,
    get_exploring_height_of_node,
    get_exploring_height_of_edge,
    one_edge,
    init_network_click_menu,
    set_content_of_tooltip,
    init_interactions,
    init_drag_for_info_tip_div,
    plus_path_d,
    create_units,
    add_intro,
}
function add_intro() {
    introJs("#app").setOptions({
        disableInteraction: true,
        steps: [{
          intro: "Welcome to JittorVis!"
        }, {
          element: document.querySelector('#ControlPanel'),
          intro: "Click here to toggle different views"
        },
        {
            element: document.querySelector('#treeViewCom'),
            intro: "This is the navigation view."
        },
        {
            element: document.querySelector('.tree-btn'),
            intro: "Each leaf node represents a computational node in the computational graph."
        },
        {
            element: document.querySelector('.tree-btn'),
            intro: "Click one intermediate node to selected its computational nodes."
        },
        {
            element: document.querySelector('#graphCom'),
            intro: "This is the graph structure view, which shows the graph structure of selected computational nodes."
        },
        {
            element: document.querySelector('#graphCom'),
            intro: "Each rectangle represents a computational node."
        },
        {
            element: document.querySelector('#graphCom'),
            intro: "Each link represents data flows among computational nodes."
        },{
            element: document.querySelector('body'),
            intro: "Start to explore your model in JittorVis!"
        },
        ],
      }).start();
}

function create_units(time_cost, max_time_cost, width, max_unit_num, start_x) {
    let unit_width = width / max_unit_num;
    let time_width = time_cost / max_time_cost * width;
    let unit_num = Math.ceil(time_width / unit_width);
    let unit = [];
    for (let i = 0;i < unit_num - 1;i++) {
        unit.push({
            'x': start_x + i * unit_width,
            'width': unit_width - 1
        });
    }
    unit.push({
        'x': start_x + (unit_num - 1) * unit_width,
        'width': Math.max(1, unit_width - 1 - (unit_num * unit_width - time_width))
    });
    return unit;
}
function plus_path_d(start_x, start_y, width, height, k) {
    let sum_k = 2 * k + 1;
    let x = [start_x, start_x + k / sum_k * width, start_x + (k + 1) / sum_k * width, start_x + width];
    let y = [start_y, start_y + k / sum_k * height, start_y + (k + 1) / sum_k * height, start_y + height];
    let d = `M${x[0]},${y[1]}`;
    d += `L${x[1]},${y[1]}`;
    d += `L${x[1]},${y[0]}`;
    d += `L${x[2]},${y[0]}`;
    d += `L${x[2]},${y[1]}`;
    d += `L${x[3]},${y[1]}`;
    d += `L${x[3]},${y[2]}`;
    d += `L${x[2]},${y[2]}`;
    d += `L${x[2]},${y[3]}`;
    d += `L${x[1]},${y[3]}`;
    d += `L${x[1]},${y[2]}`;
    d += `L${x[0]},${y[2]}`;
    d += `L${x[0]},${y[1]}`;
    return d;
}
function init_interactions(that) {
    window.show_topbar = 1
    $('#info-remove-btn').on('click', function () {
        that.$d3.selectAll('#info-tip-div').transition().duration(self.duration).style('opacity', 0)
            .style('width', `0px`)
            .style('top', `-100px`)
            .style('left', `-100px`);
        that.$d3.selectAll('#info-tip-content')
            .transition().duration(500)
            .style('width', `0px`);
        that.hide_detail_info();
    });

    init_drag_for_info_tip_div(that);
}
function init_drag_for_info_tip_div(that) {
    let dv = document.getElementById('info-tip-title');
    let tdv = document.getElementById('info-tip-div');
    let dv1 = document.getElementById('info-tip-title-text');
    let x = 0;
    let y = 0;
    let l = 0;
    let t = 0;
    let isDown = false;
    //鼠标按下事件
    dv.onmousedown = function(e) {
        //获取x坐标和y坐标
        x = e.clientX;
        y = e.clientY;

        //获取左部和顶部的偏移量
        l = tdv.offsetLeft;
        t = tdv.offsetTop;
        //开关打开
        isDown = true;
        //设置样式
        dv.style.cursor = 'grabing';
        dv1.style.cursor = 'grabing';
    };
    //鼠标移动
    window.onmousemove = function(e) {
        if (isDown == false) {
            return;
        }
        //获取x和y
        var nx = e.clientX;
        var ny = e.clientY;
        //计算移动后的左偏移量和顶部的偏移量
        var nl = nx - (x - l);
        var nt = ny - (y - t);

        tdv.style.left = nl + 'px';
        tdv.style.top = nt + 'px';
    };
    //鼠标抬起事件
    window.onmouseup = function() {
        //开关关闭
        isDown = false;
        dv.style.cursor = 'grab';
        dv1.style.cursor = 'grab';
    };
    that.$d3.selectAll('#info-tip-div')
        .style('opacity', 0);
}
function set_content_of_tooltip(that, attrs) {
    that.$d3.selectAll('#info-tip-div')
        .style('width', `${attrs.width}px`)
        .style('left', `${attrs.left}px`)
        .style('top', `${attrs.top}px`).style("overflow","hidden")
        // .style("position","absolute").style("z-index","300").style("display","block").style("border","1px ridge #bbb").style("border-radius","10px");
    that.$d3.selectAll('#info-tip-content')
        .style('width', `${attrs.width}px`);
    that.$d3.selectAll('#info-tip-title-text')
        .style('width', `${attrs.width - 24}px`);
    that.$d3.selectAll('#info-tip-div')
        .transition().duration(500)
        .style('opacity', attrs.opacity);
    that.$d3.selectAll('#info-tip-content')
        .transition().duration(500);
    $('#info-tip-title-text').text(attrs['title']);
    let values = attrs.values;
    let innerhtml = '';
    for (let key in values) {
        let value = values[key];
        // innerhtml += `${key}:<p style=\"margin-left: 20px;\">${value}</p>`;
        innerhtml += `<p>${key}: ${value}</p>`;
    }
    $('#info-tip-content')[0].innerHTML = innerhtml;
}

function init_network_click_menu(that) {
    let nextwork_menu = [{
            name:'detail info',
            title:'detail info',
            fun:function(){
                that._show_detail_info();
            }
        }];
    $('.node_main_rect_g').contextMenu(nextwork_menu, {'mouseClick':'right','triggerOn':'click'});
    $('.var_node_group').contextMenu(nextwork_menu, {'mouseClick':'right','triggerOn':'click'});
}
function one_edge(points) {
    // return bundle_line(points);
    // return line(points);
    // return B_spline(points);

//     points = handle_points(points);
    let len = points.length;
    if (len === 0) { return "" }
    let start = `M ${points[0].x} ${points[0].y}`,
        vias = [];

    const getInter = (p1, p2, n) => {
        return `${p1.x * n + p2.x * (1 - n)} ${p1.y * n + p2.y * (1 - n)}`
    };

    const getCurve = (points) => {
        let vias = [],
            len = points.length;
        const ratio = 0.5;
        for (let i = 0; i < len - 2; i++) {
            let p1, p2, p3, p4, p5;
            if (i === 0) {
                p1 = `${points[i].x} ${points[i].y}`
            } else {
                p1 = getInter(points[i], points[i + 1], ratio)
            }
            p2 = getInter(points[i], points[i + 1], 1 - ratio);
            p3 = `${points[i + 1].x} ${points[i + 1].y}`;
            p4 = getInter(points[i + 1], points[i + 2], ratio);
            if (i === len - 3) {
                p5 = `${points[i + 2].x} ${points[i + 2].y}`
            } else {
                p5 = getInter(points[i + 1], points[i + 2], 1 - ratio)
            }
            let cPath = `M ${p1} L${p2} Q${p3} ${p4} L${p5}`;
            vias.push(cPath);
        }
        return vias
    };
    vias = getCurve(points);
    let pathData = `${start}  ${vias.join(' ')}`;
    return pathData;
}

function filter_exploring_nodes(exploring_nodes) {
    let new_exploring_nodes = [];
    exploring_nodes.forEach(function (d) {
        if (d.exploring_height >= 0) {
            new_exploring_nodes.push(d);
        }
    });
    return new_exploring_nodes;
}
function get_exploring_height_of_edge(edge) {
    let start_exploring_height = edge.startNode.exploring_height,
        end_exploring_height = edge.endNode.exploring_height;

    if (start_exploring_height === end_exploring_height) {
        edge.exploring_height = start_exploring_height;
    }
    else {
        edge.exploring_height = -2;
    }
}
function get_exploring_height_of_node(d, all_nodes) {
    if (d.parent === -1) {
        d.exploring_height = -1;
    }
    else {
        let exploring_height = all_nodes[d.parent].exploring_height;
        d.exploring_height = -1;
        if (exploring_height < 3) {
            d.exploring_height = exploring_height;
        }
    }
}
function sgn(x) {
    if (x > 0) {
        return 1;
    }
    else if(x === 0) {
        return 0;
    }
    else {
        return -1;
    }
}
function short_title(title, max_size) {
    let short_dic = {
        'array': 'arr',
        'binary': 'bi',
        'subtract': 'sub',
        'divide': 'div',
        'broadcast': 'bcast'
    };
    let short_title = title;
    for (let key in short_dic) {
        short_title = short_title.replace(key, short_dic[key]);
    }
    if (short_title.length > max_size) {
        short_title = short_title.slice(0, max_size - 2) + '··';
    }
    // console.log(title, 'to', short_title);
    return short_title;
}

function path_d(points) {
    let res = `M${points[0][0]},${points[0][1]}`;
    for (let i = 1;i < points.length;i++) {
        res += `L${points[i][0]},${points[i][1]}`;
    }
    return res;
}
function arrow_path_d(start_x, start_y, width, height, direction) {
    let res = '';
    if (direction === 'left') {
        res += `M${start_x + width},${start_y}`;
        res += `L${start_x},${start_y + height / 2}`;
        res += `L${start_x + width},${start_y + height}`;
    }
    else if (direction === 'right') {
        res += `M${start_x},${start_y}`;
        res += `L${start_x + width},${start_y + height / 2}`;
        res += `L${start_x},${start_y + height}`;
    }
    else if (direction === 'top') {
        res += `M${start_x},${start_y + height}`;
        res += `L${start_x + width / 2},${start_y}`;
        res += `L${start_x + width},${start_y + height}`;
    }
    else if (direction === 'bottom') {
        res += `M${start_x},${start_y}`;
        res += `L${start_x + width / 2},${start_y + height}`;
        res += `L${start_x + width},${start_y}`;
    }
    return res;
}
function process_duplicated_brother_var_nodes(nodes, all_edges) {
    let res = [];
    let var_groups = {};
    let node_index = {};
    nodes.forEach(node=>{
        node_index[node.index] = true;
    });
    nodes.forEach(node=>{
        if (node.is_var) {
            let pre_edge_ids = node.pre, next_edge_ids = node.next;
            let pre_edges = pre_edge_ids.map(x=>all_edges[x]),
                next_edges = next_edge_ids.map(x=>all_edges[x]);

            let pre_node_ids = [],
                next_node_ids = [];
            pre_edges.forEach(edge=>{
                if (node_index[edge.start] !== undefined) {
                    pre_node_ids.push(edge.start);
                }
            });
            next_edges.forEach(edge=>{
                if (node_index[edge.end] !== undefined) {
                    next_node_ids.push(edge.end);
                }
            });
            pre_node_ids.sort();
            next_node_ids.sort();
            let var_key = pre_node_ids.join('$') + '->' + next_node_ids.join('$');
            if (var_groups[var_key] === undefined) {
                var_groups[var_key] = [];
            }
            node.children = [];
            var_groups[var_key].push(node);
        }
        else {
            res.push(node);
        }
    });

    for (let var_key in var_groups) {
        let var_nodes = var_groups[var_key];
        if (var_nodes.length > 1) {
            var_nodes[0].children = var_nodes.slice(1).map(x=>x.index);
        }
        res.push(var_nodes[0]);
    }
    return res;
}
function compute_edges(nodes, all_edges, all_nodes=[]) {
    let edges = [];
    let node_indexs = nodes.map(node => node.index)
    let nodeset = new Map()
    for (let idx of node_indexs) {
        nodeset.set(idx, 0)
        all_nodes[idx].status = 'inner'
    }
    let in_nodes = []
    let out_nodes = []
    let edgeset = new Set()
    let lca = node_indexs.slice(0)
    while (1) {
        let flag = 1
        for (let i = 0; i + 1 < lca.length; ++i) {
            if (lca[i] != lca[i + 1]) {
                flag = 0
                break
            }
        }
        if (flag) break
        for (let i = 0; i < lca.length; ++i) lca[i] = all_nodes[lca[i]].parent
    }
    lca = lca[0]
    const lca_depth = lca == -1 ? 0 : all_nodes[lca].depth

    for (let edge_index = 0; edge_index < all_edges.length; ++edge_index) {
        let edge = all_edges[edge_index]
        let start = edge.start
        let end = edge.end
        while (start != -1 && all_nodes[start].depth > lca_depth && (!nodeset.has(start) || nodeset.get(start) != 0)) {
            start = all_nodes[start].parent
        }
        while (end != -1 && all_nodes[end].depth > lca_depth && (!nodeset.has(end) || nodeset.get(end) != 0)) {
            end = all_nodes[end].parent
        }
        if ((!nodeset.has(start) || nodeset.get(start) != 0) && (!nodeset.has(end) || nodeset.get(end) != 0)) {
            continue
        }
        if (start == lca || end == lca || start == end) continue
        if (edgeset.has(start + ' ' + end)) continue
        edgeset.add(start + ' ' + end)
        if (!nodeset.has(start)) {
            nodeset.set(start, 1)
            in_nodes.push(start)
        }
        if (!nodeset.has(end)) {
            nodeset.set(end, 1)
            out_nodes.push(end)
        }
        let e = { start, end }
        edges.push(e)
    }
    const is_ancestor = (x, y) => {
        while (x != -1 && x != y) x = all_nodes[x].parent
        return x == y
    }
    const shrink = (nodes) => {
        let preserve_nodes = nodes.filter(d => is_ancestor(d, all_nodes[lca].parent))
        let left_nodes = nodes.filter(d => !is_ancestor(d, all_nodes[lca].parent))
        edges.forEach(d => {
            for (let e of left_nodes) {
                if (d.start == e && all_nodes[e].parent != -1) d.start = all_nodes[e].parent
                if (d.end == e && all_nodes[e].parent != -1) d.end = all_nodes[e].parent
            }
        })
//         left_nodes = [...new Set(left_nodes.map(d => all_nodes[d].parent).filter(d => d != -1))]
        left_nodes = [...new Set(left_nodes.map(d => all_nodes[d].parent!=-1? all_nodes[d].parent: d).filter(d => d != -1))]
        return preserve_nodes.concat(left_nodes)
    }
    if (in_nodes.length > 1) {
        in_nodes = shrink(in_nodes)
    }
    if (out_nodes.length > 1) {
        out_nodes = shrink(out_nodes)
    }

    in_nodes = in_nodes.map(d => all_nodes[d])
    out_nodes = out_nodes.map(d => all_nodes[d])
    in_nodes = in_nodes.concat(out_nodes)
    in_nodes.forEach(d => { d.status = 'outer' })
    nodes = nodes.concat(in_nodes)
    edgeset = new Set()
    let newedges = []
    for (let e of edges) {
        if (edgeset.has(e.start + ' ' + e.end)) continue
        edgeset.add(e.start + ' ' + e.end)
        newedges.push(e)
    }
    edges = newedges
    return [nodes, edges]
}
function get_exploring_node_level_and_height(that,all_nodes, exploring_nodes, time_cost_height) {
    let formData = new FormData();
    let node_keys = ['index', 'x', 'y', 'w', 'h', 'parent', 'children', 'id', 'pre', 'next', 'exploring', 'is_var', 'expand'];
    let new_all_nodes = all_nodes.map(node=>{
        let new_node = {};
        node_keys.forEach(key=>{
            new_node[key] = node[key];
        });
        new_node['node_top'] = new_node['y'] - new_node['h'] / 2;
        new_node['node_bottom'] = new_node['y'] + new_node['h'] / 2;
        new_node['node_left'] = new_node['x'] - new_node['w'] / 2;
        new_node['node_right'] = new_node['x'] + new_node['w'] / 2;
        if (!new_node['is_var'] && !new_node['expand']) {
            new_node['node_bottom'] -= time_cost_height;
        }
        return new_node;
    });
    let exploring_node_keys = ['index', 'x', 'y', 'w', 'h', 'parent', 'children', 'id', 'pre', 'next', 'exploring', 'is_var'];
    let new_exploring_nodes = exploring_nodes.map(node=>{
        let new_node = {};
        exploring_node_keys.forEach(key=>{
            new_node[key] = node[key];
        });
        return new_node;
    });
    formData.append('all_nodes', JSON.stringify(new_all_nodes));
    formData.append('exploring_nodes', JSON.stringify(new_exploring_nodes));

    let xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://166.111.80.25:5010/api/get_exploring_node_level_and_height', true);

    xhr.onload = function (e) {
        if (xhr.status === 200) {
            let response = JSON.parse(xhr.response);
            let exploring_nodes = response['exploring_nodes'];
            if (exploring_nodes.length > 0) {
                exploring_nodes.forEach(exploring_node=>{
                    all_nodes[exploring_node.index].exploring_height = exploring_node.exploring_height;
                    all_nodes[exploring_node.index].exploring_level = exploring_node.exploring_level;
                });
            }
            that.repaint();

        } else {
            alert('An error occurred!');
        }
    };
    xhr.send(formData);
}
