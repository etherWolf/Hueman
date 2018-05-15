// import jQuery from 'jquery'
import '../semantic/dist/semantic.css'
import '../semantic/dist/semantic.js';
import './assets/styles/base.scss';
import Vue from 'vue';
import VueResource from 'vue-resource'
import App from './App.vue';
import Toasted from 'vue-toasted';

Vue.use(VueResource);
Vue.use(Toasted);

export const eventBus = new Vue();

new Vue({
  el: '#app',
  render: h => h(App)
});
