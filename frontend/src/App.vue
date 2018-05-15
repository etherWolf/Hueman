<template>
  <div>
    <header id="navbar" class="ui secondary pointing top fixed inverted menu">
      <a :class="currentView === 'app-search-view' ? 'active item' : 'item'"
         @click="setCurrentView('app-search-view')">
        Search
      </a>
      <a v-if="isBrowseViewInitialized"
         :class="currentView === 'app-browse-view' ? 'active item' : 'item'"
         @click="setCurrentView('app-browse-view')">
        Results
      </a>
      <div class="right item">
        <a class="ui inverted button"
           :class="{'active': currentView === 'app-add-images-view'}"
           @click="setCurrentView('app-add-images-view')">
          Add images
        </a>
      </div>
    </header>
    <keep-alive>
      <component :is="currentView" :propSearchResultsPromise="propSearchResultsPromise"></component>
    </keep-alive>
  </div>
</template>

<script>
  import SearchView from './SearchView.vue';
  import BrowseView from './BrowseView.vue';
  import AddImagesView from './AddImagesView.vue';
  import AddImagesFinalizeView from './AddImagesFinalizeView.vue'
  import { eventBus } from './main';

  export default {
    data() {
      return {
        currentView: 'app-search-view',
        isBrowseViewInitialized: false,
        propSearchResultsPromise: null,
      };
    },
    components: {
      'app-search-view': SearchView,
      'app-browse-view': BrowseView,
      'app-add-images-view': AddImagesView,
      'app-add-images-finalize-view': AddImagesFinalizeView,
    },
    methods: {
      setCurrentView(data) {
        if (data === 'app-browse-view')
          this.isBrowseViewInitialized = true;
        this.currentView = data;
      },
      onSearchClicked(data) {
        this.propSearchResultsPromise = data;
        this.setCurrentView('app-browse-view');
      }
    },
    mounted() {
      eventBus.$on('searchClicked', data => this.onSearchClicked(data));
    }
  }
</script>

<style lang="scss" scoped>
  @import 'assets/styles/common';

  #navbar {
    background-color: #1B1B1B;
  }

  /* =============== MEDIA QUERIES =============== */
  @media screen and (max-width: $phone-breakpoint) {
    #navbar {
      padding-left: 1.1em;
      padding-top: .5em;
    }
  }

  @media screen and (min-width: $phone-breakpoint + 1px) {
    #navbar {
      padding: 1.5em 2em 0 3.1em;
    }
  }

</style>
