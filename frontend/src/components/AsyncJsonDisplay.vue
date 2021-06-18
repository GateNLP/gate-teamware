<template>
  <div>
    <b-button block @click="toggleJsonDisplay" variant="outline-primary" class="mb-1">
      <b-icon-chevron-down v-if="!doShow"></b-icon-chevron-down>
      <b-icon-chevron-up v-else></b-icon-chevron-up>
      {{ btnText }}
    </b-button>
    <b-collapse v-model="doShow">
      <b-skeleton-wrapper :loading="loading">
        <template #loading>
          <b-card>
            <b-skeleton width="85%"></b-skeleton>
            <b-skeleton width="55%"></b-skeleton>
            <b-skeleton width="70%"></b-skeleton>
          </b-card>
        </template>

        <b-card>
          <vue-json-pretty :data="data"></vue-json-pretty>
        </b-card>


      </b-skeleton-wrapper>

    </b-collapse>


  </div>

</template>

<script>
import VueJsonPretty from 'vue-json-pretty';
import 'vue-json-pretty/lib/styles.css';

export default {
  name: "AsyncJsonDisplay",
  components: {
    VueJsonPretty
  },
  data() {
    return {
      data: null,
      loading: false,
      doShow: false,
    }
  },
  computed: {
    btnText() {
      if (this.doShow) {
        return this.hideText
      } else {
        return this.showText
      }
    }

  },
  props: {
    fetchFunction: {
      type: Function,
      default: null
    },
    fetchParam: {
      default: null
    },
    showText: {
      type: String,
      default: "Show JSON"
    },
    hideText: {
      type: String,
      default: "Hide JSON"
    }
  },
  methods: {
    async setShow(show) {
      this.doShow = show
    },
    async setLoading(loading) {
      this.loading = loading
    },
    async toggleJsonDisplay() {
      this.doShow = !this.doShow
      if (this.doShow) {
        this.setShow(true)
        this.setLoading(true)

        try {
          this.data = await this.fetchFunction(this.fetchParam)

        } catch (e) {
          console.exception(e)
        }

        this.setLoading(false)

      } else {
        this.setShow(false)
        this.setLoading(false)

      }

    }

  }

}
</script>

<style scoped>

</style>
