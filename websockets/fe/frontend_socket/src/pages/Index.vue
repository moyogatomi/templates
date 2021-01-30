<template>
  <q-page class="">
    <div class="q-ma-md text-h6">
      <q-badge color="black">
        Websockets &nbsp;

        <!-- <q-icon
          name="wifi"
          class="text-green"
          v-if="test.isConnected === true"
          style="font-size: 1.5em;"
        />
        <q-icon name="wifi" class="text-red" style="font-size: 1.5em;" v-else />
        -->
        <q-spinner-bars
          color="green"
          style="font-size: 1.5em;"
          v-if="test.isConnected === true"
        />
        <q-spinner-puff color="red" style="font-size: 1.5em;" v-else />
      </q-badge>
      <q-btn @click="create_task"> Create Task</q-btn>
    </div>

    <div class="row">
      <div class="col-8">
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
                    :label="make_percentage(item.progress)"
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
                <q-icon name="check_circle" color="green" size="2em" />
              </div>
              <div class="text-orange" v-if="item.state === 'received'">
                <q-spinner-orbit color="blue" size="2em" />
              </div>
              <div class="text-orange" v-if="item.state === 'queued'">
                <q-spinner-box color="blue" size="2em" />
              </div>
            </q-item-section>
          </q-item>
        </q-list>
      </div>
      <div class="col-4">
        <div>
          Logs
        </div>
        <q-scroll-area style="height: 700px">
          <div>
            <q-list>
              <q-item v-for="(item, index) in logs" :key="index">
                <q-item-section>
                  <q-item-label overline
                    >{{ item.message_type }}: {{ item.task_id }}</q-item-label
                  >
                  <q-item-label>state: {{ item.state }}</q-item-label>
                  <q-item-label caption lines="2"
                    >progress: {{ item.progress }}%</q-item-label
                  >
                </q-item-section>

                <q-item-section side top>
                  <q-item-label caption>{{ item.timestamp }}</q-item-label>
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
                    <q-icon name="check_circle" color="green" size="2em" />
                  </div>
                  <div class="text-orange" v-if="item.state === 'received'">
                    <q-spinner-orbit color="blue" size="2em" />
                  </div>
                  <div class="text-orange" v-if="item.state === 'queued'">
                    <q-spinner-box color="blue" size="2em" />
                  </div>
                </q-item-section>
              </q-item>

              <q-separator spaced inset />
            </q-list>
          </div>
        </q-scroll-area>
      </div>
    </div>
  </q-page>
</template>

<script>
import axios from 'axios'

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
    },
    make_percentage (val) {
      return String(val) + ' %'
    },
    create_task () {
      axios
        .get('http://localhost:8000/create_task')
        .then(response => {
          console.log(response)
        })
        .catch(e => {
          console.log(e)
        })
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
    },
    logs: {
      get () {
        return this.$store.state.socket.logs
      },
      set () {
        return 0
      }
    }
  }
}
</script>
