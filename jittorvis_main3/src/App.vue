<template>
  <div id="app">
     <panel-row1-com :data_loaded="data_loaded" :is_resized="is_window_resized"></panel-row1-com>
     <panel-row2-com :data_loaded="data_loaded" :is_resized="is_window_resized"></panel-row2-com>
  </div>
</template>

<script>
import panelRow1Com from "@/components/panelRow1Com";
import panelRow2Com from "@/components/panelRow2Com";
import axios from "axios";

export default {
  name: 'App',
  components: {
    panelRow1Com,
    panelRow2Com,
  },

  created() {
    this.getData();
  },

  data(){
    return {
      data_loaded: {
        is_data_loaded: false,
        all_data: null,
      },
      is_window_resized: false,
    }
  },
  mounted() {
    var that = this;
    window.onresize = function (){
      return (() => {
        window.screenWidth = document.body.clientWidth;
        window.screenHeight = document.body.clientHeight;
        that.$forceUpdate();
        that.$nextTick(() => {
          that.is_window_resized = true;
        });
        that.is_window_resized = false;
      })();
    }
  },
  methods:{
    getData(){
      const path = 'http://166.111.80.25:5010/api/process';
      // const path = 'http://localhost:5009/api/process';
      var that = this;
      axios.get(path).then(function (response) {
        var msg = response.data.data;
        var statistic_data = msg;
        if(response.status === 200){
          that.data_loaded = {
            is_data_loaded: true,
            all_data: statistic_data
          };
          console.log('Success ' + response.status + ', ' + response.data + ', ' + msg);
        }
        else {
          alert('An error occurred!');
        }
        }).catch(function (error) {
          alert('Error ' + error);
        })
    }
  }
}
</script>

<style >
#app {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  min-height:500px;
  overflow-x: hidden;
  overflow-y: hidden;
  position: relative;
  box-sizing: border-box;
}
</style>
