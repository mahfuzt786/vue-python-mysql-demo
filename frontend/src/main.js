import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import CoreuiVue from '@coreui/vue'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import axios from 'axios'
import VueAxios from 'vue-axios'
import JsonViewer from 'vue-json-viewer'
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS
import '@coreui/coreui/dist/css/coreui.min.css';
import { CIcon } from '@coreui/icons-vue';

Vue.config.productionTip = false

console.log('CoreuiVue:', CoreuiVue);

Vue.use(VueAxios, axios)
Vue.use(JsonViewer)
Vue.use(CoreuiVue)
Vue.use(CIcon)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
