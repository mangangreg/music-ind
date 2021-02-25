<template>
  <div class="wrapper">
    <cytoscape ref="cy" :config="config" >
      <cy-element
        v-for="def in elements"
        :key="`${def.data.id}`"
        :definition="def"
      />
    </cytoscape>

  </div>
</template>

<script>
export default {
  name: 'NetworkGraph',
  props: {
    elements: Array,
    config: Object
  },

  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      config
    }
  }
}
</script>

<style scoped>
.wrapper{
  width:100%;
  height:100%;
}
</style>
