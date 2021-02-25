<template>
  <div class="outter">
    <div class="title"> Music Ind </div>
    <div class="content">
      <NetworkGraph v-bind="graphData" />
    </div>
  </div>
</template>

<script>
import NetworkGraph from '@/components/NetworkGraph'
import {DemoElements, DemoConfig} from '@/demo.js'

export default {
  name: 'MusicInd',
  components: {
    NetworkGraph,
  },
  computed: {
    a: function () {return 2  },

    graphData: function () {

      return {elements:DemoElements, config:DemoConfig}
    }

  }
}

</script>

<style>

.outter{
  margin-left: 2rem;
  margin-right: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.title{
  font-size:3rem;
  width:100%;
  text-align: center;
}
.content{
  border:3px solid darkgrey;
  border-radius: 4px;
  width: 80%;
  height: 800px;
}

</style>
