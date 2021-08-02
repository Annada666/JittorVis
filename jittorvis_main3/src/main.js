import Vue from 'vue'
import App from './App.vue'
import * as d3 from 'd3'
// import * as d3 from '../public/lib/d3.v4.min'
import {ColorManager} from './js/ColorManager'
import * as tool from './js/tools'
import {DAGLayout} from "@/js/Layout";



Vue.config.productionTip = false
Vue.prototype.$d3 = d3;
Vue.prototype.$color_manager = new ColorManager();
Vue.prototype.$tool = tool;
Vue.prototype.$DAGLayout = DAGLayout;

new Vue({
  render: h => h(App),
}).$mount('#app')
