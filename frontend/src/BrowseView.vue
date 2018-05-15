<template>
  <section class="ui centered center aligned main container">
    <div class="ui dimmer">
      <div class="ui text medium loader">Loading</div>
    </div>
    <div class="ui inverted header" id="no-results-text" v-if="noResults">
      Search returned no results...
    </div>
    <div class="ui four centered stackable cards">
      <div class="ui link card" v-for="card in cards">
        <a class="image" :href="getImageSource(card.fileName)">
          <img :src="getImageSource(card.fileName)">
        </a>
        <div class="content">
          <h4 class="ui dividing header">
            <p>{{ card.caption }}</p>
            <div class="sub header">{{ card.category }}</div>
          </h4>
          <div class="description">
            <div class="ui tag small labels">
              <a class="ui label" v-for="tag in card.tags">
                {{ tag }}
              </a>
            </div>
          </div>
        </div>
        <div class="extra content">
          <a>
            <span class="ui basic label" :style="'background-color:' + card.primaryColor">
              {{ card.primaryColor }}
            </span>
            <span class="ui basic label" :style="'background-color:' + card.secondaryColor">
              {{ card.secondaryColor }}
            </span>
            <span class="ui basic label" :style="'background-color:' + card.tertiaryColor">
              {{ card.tertiaryColor }}
            </span>
          </a>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
  import { eventBus } from './main';
  import  { serverURLs } from './assets/scripts/urls';

  export default {
    data() {
      return {
        cards: [],
        noResults: false,
      }
    },
    props: ['propSearchResultsPromise'],
    methods: {
      getImageSource(filename) {
        return serverURLs['GET-IMAGE'] + filename;
      },
      loadResults() {
        this.cards = [];
        this.setLoading(true);
        this.propSearchResultsPromise.then(
          response => {
            this.cards = response.body;
            if (!this.cards.length)
              this.noResults = true;
          }, response => {
            console.log('The response was bad');
          }
        );
        this.setLoading(false);
      },
      setLoading(enabled) {
        let elDimmer = document.getElementsByClassName('dimmer')[0];
        if (enabled) {
          elDimmer.classList.add('active');
        } else {
          elDimmer.classList.remove('active');
        }
      }
    },
    activated () {
      this.loadResults();
    }
  }
</script>

<style lang="scss" scoped>
  @import "assets/styles/common";

  .main.container {
    padding-top: 15vh;
  }

  #no-results-text {
    @media screen and (max-width: $phone-breakpoint) {
      margin-top: 5vh;
      font-size: 1em;
    }
    @media screen and (min-width: $phone-breakpoint + 1px) {
      margin-top: 5vh;
      font-size: 2em;
    }
  }
</style>
