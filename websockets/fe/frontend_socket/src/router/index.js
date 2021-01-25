// https://github.com/nathantsoi/vue-native-websocket
import Vue from 'vue'
import VueRouter from 'vue-router'
import routes from './routes'
import VueNativeSock from 'vue-native-websocket'
import websocketStorage from '../store/websocket_storage'
console.log(websocketStorage)
console.log('HELLO')

Vue.use(VueRouter)

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default ({ store, ssrContext }, inject) => {
  Vue.use(VueNativeSock, 'ws://localhost:8000/ws', {
    format: 'json',
    reconnection: true, // (Boolean) whether to reconnect automatically (false)
    reconnectionAttempts: 5, // (Number) number of reconnection attempts before giving up (Infinity),
    reconnectionDelay: 3000, // (Number) how long to initially wait before attempting a new (1000)
    store: store
  })

  const Router = new VueRouter({
    scrollBehavior: () => ({ x: 0, y: 0 }),
    routes,

    // Leave these as they are and change in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    mode: process.env.VUE_ROUTER_MODE,
    base: process.env.VUE_ROUTER_BASE
  })

  return Router
}
