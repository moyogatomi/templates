import Vue from 'vue'
import Vuex from 'vuex'

// import example from './module-example'
import websocketStorage from './websocket_storage'

Vue.use(Vuex)

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Store instance.
 */

export default function (/* { ssrContext } */) {
  const Store = new Vuex.Store({
    modules: {
      websocketStorage
    },
    state: {
      socket: {
        isConnected: false,
        message: {},
        reconnectError: false
      }
    },
    mutations: {
      SOCKET_ONOPEN (state, event) {
        console.log('Open')
        Vue.prototype.$socket = event.currentTarget
        state.socket.isConnected = true
      },
      SOCKET_ONCLOSE (state, event) {
        console.log('Hello, Closed')
        state.socket.isConnected = false
      },
      SOCKET_ONERROR (state, event) {
        console.error(state, event)
      },
      // default handler called for all methods
      SOCKET_ONMESSAGE (state, message) {
        console.log('Hello, got message')
        const key = Object.keys(message)[0]

        Vue.set(state.socket.message, key, message[key])
      },
      // mutations for reconnect methods
      SOCKET_RECONNECT (state, count) {
        console.info(state, count)
      },
      SOCKET_RECONNECT_ERROR (state) {
        state.socket.reconnectError = true
      }
    },
    // enable strict mode (adds overhead!)
    // for dev mode and --debug builds only
    strict: process.env.DEBUGGING
  })

  return Store
}
