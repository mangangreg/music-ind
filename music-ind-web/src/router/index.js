import Vue from 'vue'
import Router from 'vue-router'
import MusicInd from '@/components/MusicInd'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: MusicInd
    }
  ]
})
