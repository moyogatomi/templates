<template>
  <q-page class="">
    <div class="text-h6">
      <q-badge color="black">
        Websocket
        <q-icon
          name="wifi"
          class="text-green"
          v-if="test.isConnected === true"
          style="font-size: 1.5em;"
        />
        <q-icon name="wifi" class="text-red" style="font-size: 1.5em;" v-else />
      </q-badge>
      <q-btn @click="send_message" v-if="false">click</q-btn>
    </div>
    <div>
      <q-list>
        <q-item v-for="(item, key) in tasks" :key="key">
          <q-item-section>
            <q-item-label>Task number: {{ key }}</q-item-label>
            <q-linear-progress
              size="25px"
              :value="item.progress / 100"
              color="blue"
              class="q-mt-sm"
            >
              <div class="absolute-full flex flex-center">
                <q-badge
                  color="white"
                  text-color="accent"
                  :label="String(item.progress)"
                />
              </div>
            </q-linear-progress>
          </q-item-section>

          <q-item-section side top>
            <q-item-label caption>{{ item.state }}</q-item-label>
            <q-space />

            <div class="text-orange" v-if="item.state === 'started'">
              <q-spinner-bars color="primary" size="2em" />
            </div>
            <div class="text-orange" v-if="item.state === 'in progress'">
              <q-spinner-clock color="primary" size="2em" />
            </div>

            <div class="text-orange" v-if="item.state === 'computing'">
              <q-spinner-gears color="orange" size="2em" />
            </div>

            <div class="text-orange" v-if="item.state === 'done'">
              <q-spinner-cube color="green" size="2em" />
            </div>
          </q-item-section>
        </q-item>
      </q-list>
    </div>
  </q-page>
</template>

<script>
export default {
  name: 'PageIndex',
  data () {
    return {}
  },
  methods: {
    datas () {
      this.websocketStorage = 5
    },
    send_message () {
      this.test = this.$store.state.socket
      this.$socket.sendObj({ Hello: 'data' })
    }
  },
  computed: {
    websocketStorage: {
      get () {
        return this.$store.state.websocketStorage.socket
      },
      set (val) {
        this.$store.commit('websocketStorage/updatestorage', val)
      }
    },
    test: {
      get () {
        return this.$store.state.socket
      },
      set () {
        return 0
      }
    },
    tasks: {
      get () {
        return this.$store.state.socket.message
      },
      set () {
        return 0
      }
    }
  }
}
</script>
