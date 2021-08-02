<template>
<div id="panelRow1Com" ref="panelRow1">
  <div id="ControlPanel">
    <div id="statisticBtn">
      <span id="statisticBtnFont">Statistics</span>
<!--      {{metrics}}-->
<!--      {{sta_data}}-->
<!--      {{GLOBAL_DATA}}-->
    </div>
    <div id="statisticMenu">
      <select id="statisticItem" v-model="selected">
        <option id="statisticItemText" v-for="option in metrics" v-bind:value="option" :key="option">
          <span>
<!--            {{metrics_display[option]}}-->
            {{option}}
          </span>
        </option>
      </select>
      </div>
  </div>
<!--  <line-chart-com v-bind:selected_data="data" v-bind:selected="selected"></line-chart-com>-->
  <line-chart-com v-bind:data_selected="data_selected" :is_resized="is_resized_"></line-chart-com>
</div>
</template>

<script>
import lineChartCom from "@/components/lineChartCom";
export default {
  name: "panelRow1Com",
  components:{
    lineChartCom
  },
  props:['data_loaded', 'is_resized'],
  data(){
    return{
      metrics : [],
      selected : '',
      // selected_data: {},
      metrics_display: {},
      is_resized_: false,
      statisticItemDisplayLength : 10,
      data_selected: {
        is_data_loaded: false,
        all_data: null,
        selected: '',
      },
      // data: {},
    }
  },
  watch:{
    data_loaded: {
      handler(newVal){
        if(newVal.is_data_loaded == true){
          this.get_metrics();
          this.data_selected = {
            is_data_loaded: newVal.is_data_loaded,
            all_data: newVal.all_data,
            selected: this.selected,
          }
        }
      },
      immediate: true,
      deep: true
    },
    selected: {
      handler(newVal){
        // this.init_statistics();
        // this.get_metrics();
        this.selected = newVal;
        this.data_selected.selected = this.selected;
      },
      immediate: false,
    },
    is_resized: {
      handler(newVal) {
        this.is_resized_ = newVal;
      },
      // deep: true,
    }
  },
  // created() {
  //   // this.init_statistics();
  //   // this.get_metrics();
  //   this.metrics = ['loss', 'accuracy', 'precision', 'recall', 'memory'];
  //   this.selected = this.metrics[0];
  // },

  methods:{
    init_statistics(){
      // this.sta_data = this.$GLOBAL_DATA;
      this.metrics = ['loss', 'accuracy', 'precision', 'recall', 'memory'];
      // this.selected_data = this.sta_data; // notice the order, data first, then selected metrics
    },
    get_metrics(){
      let value = this.data_loaded.all_data['statistics']['value'];
      this.metrics = value['iter'].concat(value['time']);
      if(this.metrics.length > 0){
        this.selected = this.metrics[0];
      }
    },
    // get_data(){
    //   // alert(this.$sta_data);
    // }
  }
}
</script>

<style>
#panelRow1Com{
  display: flex;
  flex-direction: column;
  margin: 0 0 0 0;
  padding: 0 50px 0 50px ;
  box-sizing: border-box;
  background: rgb(0,0,0,5%);
}
#ControlPanel {
    /*justify-content: space-between;*/
    /*background: white;*/
    width: 100%;
    height: 33px;
    display: flex;
    flex-direction: row;
    /*box-shadow: inset 0 1px 3px 3px rgb(0 0 0 / 10%);*/
    box-sizing: border-box;
    z-index: 1;
    /*margin: 1px 3px 1px 3px;*/
}
#statisticBtn{
    float: left;
    background: white;
    height: 100%;/*-*/
    flex-direction: row;
    width: 100px;
    box-shadow: inset 0 1px 3px 3px rgb(0 0 0 / 10%);
    /*box-shadow:  inset 5px 0px 5px -5px rgb(0 0 0 / 25%), inset -5px 0px 5px -5px rgb(0 0 0 / 25%);*/
    z-index: 1;
    box-sizing: border-box;
}
#statisticBtnFont{
  position: relative;
  display: flex;
  font-size: 20px;
  font-weight: 400;
  /*line-height: 14px;*/
  /*text-align: left;*/
  -moz-text-size-adjust: 100%;
  align-items: center;
  justify-content: center;
  height: 100%;
  box-sizing: border-box;
  color: gray;
  /*font-family: "Arial";*/
}
#statisticMenu{
  float: right;
  /*background: white;*/
  height: 100%;/*-*/
  /*flex-direction: row;*/
  width: 100px;
  /*box-shadow: inset 0 1px 3px 3px rgb(0 0 0 / 10%);*/
  /*box-shadow:  inset 5px 0px 5px -5px rgb(0 0 0 / 25%), inset -5px 0px 5px -5px rgb(0 0 0 / 25%);*/
  z-index: 1;
  box-sizing: border-box;
  /*margin-right: 2px;*/
  /*position: relative;*/
  /*justify-content: flex-end;*/
  /*display: flex;*/
  margin-left:auto;
  /*flex-flow: row nowrap;*/
  /*justify-content: space-between;*/
}
#statisticItem{
  width: auto;
  height: 100%;
  box-sizing: border-box;

  padding: 0 2%;
  margin: 0;

  font-size: 15px;
  font-weight: 400;
  /*box-shadow: inset 0 1px 3px 3px rgb(0 0 0 / 10%);*/

  display: flex;
  align-items: center;
  justify-content: center;
  /*text-align: center;*/
  /*flex-direction: column;*/
  margin-left: auto;
  margin-right: auto;

  outline: none;
  text-align-last: center;
  text-align: center;
  font-family: "Arial";
}
#statisticItemText{
  /*text-indent: 2px;*/
  text-align:center;
  /*width: 100%;*/
  /*height: 100%;*/
  text-align-last: center;
  display: flex;
  outline: none;
  align-items: center;
  justify-content: center;
  margin-bottom: auto;
  margin-top: auto;
  position: relative;
  margin-left: auto;
  /*font-size: 20px;*/
  /*font-weight: 400;*/
  /*line-height: 14px;*/
  /*text-align: left;*/
  /*-moz-text-size-adjust: 100%;*/
  /*align-items: center;*/
  /*margin-bottom: 0;*/
  /*justify-content: center;*/
  /*height: 100%;*/
  /*margin-top: 5px;*/
  /*color: #87878a;*/
  box-sizing: border-box;
}
</style>