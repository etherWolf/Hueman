<template>
  <div>
    <app-add-images-initial-view
      v-if="currentView === 'app-add-images-initial-view'">
    </app-add-images-initial-view>
    <app-add-images-finalize-view
      v-if="currentView === 'app-add-images-finalize-view'"
      :propFilesList="propFilesList">
    </app-add-images-finalize-view>
  </div>
</template>

<script>
  import { eventBus } from './main';
  import AddImagesInitialView from './AddImagesInitialView.vue';
  import AddImagesFinalizeView from './AddImagesFinalizeView.vue';

  export default {
    data() {
      return {
        currentView: 'app-add-images-initial-view',
        propFilesList: [],
      };
    },
    mounted() {
      eventBus.$on('filesProcessingDone', (e) => {
        this.propFilesList = e;
        this.currentView = 'app-add-images-finalize-view';
      });
    },
    components: {
      'app-add-images-initial-view': AddImagesInitialView,
      'app-add-images-finalize-view': AddImagesFinalizeView,
    }
  }
</script>
