/*
export function someMutation (state) {
}
*/
export const updatestorage = (state, msg) => {
  state.wss = msg
}

export const SOCKET_ONOPEN = (state, event) => {
  this.prototype.$socket = event.currentTarget
  state.socket.isConnected = true
}
export const SOCKET_ONCLOSE = (state, event) => {
  state.socket.isConnected = false
}
export const SOCKET_ONERROR = (state, event) => {
  console.error(state, event)
}
// default handler called for all methods
export const SOCKET_ONMESSAGE = (state, message) => {
  console.log('I am in an event')
  state.socket.message = message
}
// mutations for reconnect methods
export const SOCKET_RECONNECT = (state, count) => {
  console.info(state, count)
}
export const SOCKET_RECONNECT_ERROR = state => {
  state.socket.reconnectError = true
}
