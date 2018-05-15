<template>
  <section class="ui centered middle center aligned main fluid container">

    <!--TODO: Try this experimental shit-->
    <!--<div class="ui move up reveal">-->
    <!--<div class="visible content">-->
    <!--</div>-->
    <!--<div class="hidden content">-->
    <!--</div>-->
    <!--</div>-->


    <!--<div class="ui inverted tiny teal progress">-->
    <!--:data-value="currentIndex"-->
    <!--:data-total="totalItems">-->
    <!--<div class="bar hidden"></div>-->
    <!--<div class="inverted label"> {{ currentIndex }} of {{ totalItems }} </div>-->
    <!--</div>-->

    <div class="ui inverted header" style="color:#696969">This page is still under construction!</div>
    <div class="ui stackable two column centered middle center aligned grid" id="main-grid">
      <div class="middle aligned column">
        <div class="ui segments">
          <div class="ui inverted segment" id="main-image-box">
            <img class="ui centered big middle aligned image"
                 id="main-image"
                 :src="currentData.filePath">
          </div>
          <div class="ui segment zero-padding zero-border">
            <div class="ui horizontal segments zero-margin zero-border">
              <div class="ui basic segment zero-border"
                   id="primary-color-segment"
                   :style="'background-color: ' + currentData.primaryColor">
              </div>
              <div class="ui basic segment zero-border"
                   id="secondary-color-segment"
                   :style="'background-color: ' + currentData.secondaryColor">
              </div>
              <div class="ui basic segment zero-border"
                   id="tertiary-color-segment"
                   :style="'background-color: ' + currentData.tertiaryColor">
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Shocked by the number of  px-300s? Well that was what finally defeated Semantic UI's weirdly !important rules -->
      <div class="middle aligned column px-300">
        <div class="ui form px-300">
          <div class="field px-300">
            <div class="ui input px-300">
              <input placeholder="Caption for this image..." id="input-caption">
            </div>
          </div>

          <div class="field px-300">
            <div class="ui selection search dropdown px-300" id="add-images-dropdown-category">
              <!--<input name="category" type="hidden">-->
              <i class="dropdown icon"></i>
              <div class="default text">
                Category
              </div>
              <div class="menu">
                <!--<div class="ui action input"-->
                <!--data-content="Categories that you don't use for any image will be discarded">-->
                <!--<input placeholder="Add a new category..." id="input-add-cat">-->
                <!--<button class="ui button" @click="addCat()">-->
                <!--Add-->
                <!--</button>-->
                <!--</div>-->
                <div class="item" v-for="item in categoryItems" :data-value="item">
                  {{ item }}
                </div>
              </div>
            </div>
          </div>

          <div class="field px-300">
            <div class="ui multiple selection search dropdown px-300" id="add-images-dropdown-tags">
              <!--<input name="tags" type="hidden">-->
              <i class="dropdown icon">
              </i>
              <div class="default text">
                Tags
              </div>
              <div class="menu">
                <!--<div class="ui action input" data-content="Tags that you don't use for any image will be discarded">-->
                <!--<input placeholder="Add a new tag..." id="input-add-tag">-->
                <!--<button class="ui button" @click="addTag()">-->
                <!--Add-->
                <!--</button>-->
                <!--</div>-->
                <div class="item" v-for="item in tagItems">
                  {{ item }}
                </div>
              </div>
            </div>
          </div>

          <div class="ui hidden divider"></div>

          <div class="centered divided row px-300">
            <div class="ui buttons px-300">
              <button class="ui left labeled icon red inverted button" @click="onDiscardButtonClicked()">
                <i class="close icon"></i>
                Discard
              </button>
              <div class="or">
              </div>
              <button class="ui right labeled icon green inverted button" @click="onUploadButtonClicked()">
                <i class="right arrow icon"></i>
                Accept
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
  import * as Vibrant from 'node-vibrant';
  import { serverURLs } from './assets/scripts/urls';

  export default {
    data() {
      return {
        currentIndex: 0,
        totalItems: 0,
        currentData: {
          fileName: '',
          filePath: '',
          primaryColor: '',
          secondaryColor: '',
          tertiaryColor: '',
        },
//        TODO: Async palette getter
//        nextData: {
//          primaryColor: '',
//          secondaryColor: '',
//          tertiaryColor: '',
//        },
        categoryItems: [],
        tagItems: [],
        filesListGen: null,
      };
    },
    props: ['propFilesList'],
    mounted() {
      $(this.$el).find('.ui.dropdown').dropdown({
        allowAdditions: true
      });
      $(this.$el).find('.progress').progress();
//      $(this.$el).find('.action.input').popup({
//        on: 'hover',
//        delay: {
//          show: 0,
//          hide: 50
//        }
//      });
      this.totalItems = this.propFilesList.length;
      this.loadNextDataSet();
    },
    methods: {
//      addCat() {
//        let el = $(this.$el).find('#input-add-cat');
//        console.log(el);
//        if (el.value !== '') {
//          this.categoryItems.unshift(el.value);
//          console.log(el.value);
//        }
//      },
//      addTag () {
//        let el = $(this.$el).find('#input-add-tag');
//        if (el.value !== '') {
//          this.tagItems.unshift(el.value);
//          console.log(el.value);
//        }
//      },
      onUploadButtonClicked() {
        let els = document.getElementsByTagName('button');
        for (let el of els)
          el.disabled = true;
        els[1].classList.add('loading');
        let selCat = $(this.$el).find('#add-images-dropdown-category').dropdown('get value');
        let selTags = [],
          activeTags = document.getElementById('add-images-dropdown-tags').getElementsByClassName('label');
        for (let x of activeTags) {
          selTags.push(x.innerText.trim());
        }
        let obj = {
          fileName: this.currentData.fileName,
          caption: document.getElementById('input-caption').value,
          category: selCat,
          tags: selTags,
          primaryColor: this.currentData.primaryColor,
          secondaryColor: this.currentData.secondaryColor,
          tertiaryColor: this.currentData.tertiaryColor,
        };
        this.$http.post(serverURLs['POST-DATA'], obj).then(
          response => {
            for (let el of els)
              el.disabled = false;
            els[1].classList.remove('loading');
          }, response => {
            for (let el of els)
              el.disabled = false;
            els[1].classList.remove('loading');
            console.log('the response was bad.');
          }
        );
        this.loadNextDataSet();
      },
      onDiscardButtonClicked() {
        this.$http.delete(serverURLs['DELETE-IMAGE'] + this.currentData.fileName);
        this.loadNextDataSet();
      },
      loadNextDataSet() {
        if (this.currentIndex === this.propFilesList.length)
          return false;
        this.$http.get(serverURLs['FETCH-SEARCH-DATA']).then(
          response => {
            this.categoryItems = response.body['categoryItems'];
            this.tagItems = response.body['tagItems'];
          }, response => {
            console.log('The response was bad');
          }
        );
        document.getElementById('input-caption').value = '';
        $(this.$el).find('#add-images-dropdown-category').dropdown('restore defaults');
        $(this.$el).find('#add-images-dropdown-tags').dropdown('restore defaults');
        this.categoryItems = [];
        this.tagItems = [];
        this.currentData.fileName = this.propFilesList[this.currentIndex++];
        this.currentData.filePath = serverURLs['GET-IMAGE'] + this.currentData.fileName;
        let v = new Vibrant(this.currentData.filePath);
        v.getPalette((err, palette) => {
          if (!err) {
//            TODO: Need to think about the else of these ifs. And above all, is this check even required in the new library?
            if (palette['Vibrant']) {
              this.currentData.primaryColor = this.rgbToHex(...(palette['Vibrant']._rgb));
            }
            if (palette['DarkVibrant']) {
              this.currentData.secondaryColor = this.rgbToHex(...(palette['DarkVibrant']._rgb));
            }
            if (palette['LightVibrant']) {
              this.currentData.tertiaryColor = this.rgbToHex(...(palette['LightVibrant']._rgb));
            }
          } else {
            console.log(err);
          }
        });
      },
      rgbToHex(r, g, b) {
        return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
      },
    }
  }
</script>

<style lang="scss" scoped>
  @import "assets/styles/common";

  .zero-padding {
    padding: 0 !important;
  }

  .zero-margin {
    margin: 0 !important;
  }

  .zero-border {
    border: 0 !important;
  }

  .ui.action.input {
    width: unset !important;
    margin-right: 1em !important;
  }

  .main.container {
    padding-top: 15vh;
  }

  #main-image {
    /*max-height: 100%;*/
  }

  #main-image-box {
    background-color: darken($dark-color, 20);
  }

  #main-grid {
    margin-left: auto;
    margin-right: auto;
  }

  #primary-color-segment {
    border-bottom-left-radius: 3px;
  }

  #tertiary-color-segment {
    border-bottom-right-radius: 3px;
  }

  @media screen and (max-width: $phone-breakpoint) {
    #main-image-box {
      max-height: 90vh;
    }
  }

  @media screen and (min-width: $phone-breakpoint + 1px) {
    .px-300 {
      min-width: 300px;
      max-width: 300px;
    }

    #main-image-box {
      min-height: 60vh;
      max-height: 60vh;
    }

    #main-grid {
      margin-left: 0;
      margin-right: 0;
    }
  }
</style>
