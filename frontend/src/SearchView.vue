<template>
  <section class="ui centered center aligned main container">
    <div class="middle aligned row">
      <div class="column" id="name-header">
        <h1 class="ui inverted header">HUEMAN</h1>
        <h3 class="sub header light-text">A COLOR-AWARE IMAGE MANAGER</h3>
      </div>
    </div>
    <div class="middle aligned row mx-auto">
      <div class="middle aligned column mx-auto">
        <table class="ui very basic collapsing inverted table mx-auto">
          <tr>
            <td class="small-width">
              <div class="ui field">
                <label class="light-text">
                  Category
                </label>
              </div>
            </td>
            <td class="large-width" colspan="3">
              <div class="ui selection search inverted fluid dropdown" id="search-dropdown-category">
                <input name="country" type="hidden">
                <i class="dropdown icon"></i>
                <div class="default text">
                  All
                </div>
                <div class="menu">
                  <div class="item">
                    All
                  </div>
                  <div class="item" v-for="item in categoryItems">
                    {{ item }}
                  </div>
                </div>
              </div>
            </td>
          </tr>
          <tr>
            <td class="small-width">
              <div class="ui field">
                <label class="light-text">
                  Tags
                </label>
              </div>
            </td>
            <td class="large-width" colspan="3">
              <div class="ui fluid multiple selection search dropdown" id="search-dropdown-tags">
                <input name="tags" type="hidden">
                <i class="dropdown icon">
                </i>
                <div class="default text">
                  None
                </div>
                <div class="menu">
                  <div class="item" v-for="item in tagItems">
                    {{ item }}
                  </div>
                </div>
              </div>
            </td>
          </tr>
          <tr class="computer-only">
            <td rowspan="3" valign="top">
              <div class="ui field">
                <label class="light-text">
                  Color palette
                </label>
              </div>
            </td>
            <td>
              <div class="color-input ui icon input">
                <input class="input-color-primary jscolor {required:false, hash:true}"
                       placeholder="Primary">
                <i class="theme icon"></i>
              </div>
            </td>
            <td rowspan="3">
              <div id="holder"
                   class="ui center aligned raised compact inverted segment"
                   @dragover.stop.prevent="onHolderDragOver()"
                   @dragleave.prevent="onHolderDragLeave()"
                   @drop.prevent="onHolderDrop($event)">
                <p>
                  <b>
                    <label class="light-text">Drop an image here to extract its color palette...<br>or</label>
                  </b>
                </p>
                <button id="button-upload-image-computer" class="ui small basic inverted icon button"
                        @click="onUploadButtonClicked()">
                  <i class="upload icon"></i>
                </button>
              </div>
            </td>
          </tr>
          <tr class="computer-only">
            <td class="collapsing pad-left-11px">
              <div class="color-input ui icon input">
                <input class="input-color-secondary jscolor {required:false, hash:true}"
                       placeholder="Secondary">
                <i class="theme icon"></i>
              </div>
            </td>
          </tr>
          <tr class="computer-only">
            <td class="collapsing pad-left-11px">
              <div class="color-input ui icon input">
                <input class="input-color-tertiary jscolor {required:false, hash:true}"
                       placeholder="Tertiary">
                <i class="theme icon"></i>
              </div>
            </td>
          </tr>
          <tr class="touch-only">
            <td class="small-width">
              <div class="ui field">
                <label class="light-text">
                  Color palette
                </label>
              </div>
            </td>
            <td colspan="3">
              <div class="ui mx-auto form">
                <div class="field">
                  <div class="ui buttons">
                    <button
                      class="input-color-primary ui inverted icon button jscolor {value:'FF5050', valueElement:null, required:false, width:77, padding:5}">
                      <i class="theme icon"></i>
                    </button>
                    <button
                      class="input-color-secondary ui inverted icon button jscolor {value:'78FF7D', valueElement:null, required:false, width:77, padding:5}">
                      <i class="theme icon"></i>
                    </button>
                    <button
                      class="input-color-tertiary ui inverted icon button jscolor {value:'15B1FF', valueElement:null, required:false, width:77, padding:5}">
                      <i class="theme icon"></i>
                    </button>
                    <button class="ui inverted icon button"
                            id="button-upload-image-touch"
                            @click="onUploadButtonClicked()">
                      <i class="image icon"></i>
                    </button>
                  </div>
                </div>
              </div>
            </td>
          </tr>
        </table>
        <button class="ui primary inverted button" @click="onSearchButtonClicked()">Search</button>
      </div>
      <input id="file-input"
             type="file"
             name="name"
             style="display: none;"
             accept="image/*"
             @change.stop.prevent="onFileChange($event)"/>
    </div>
  </section>
</template>

<script>
  import * as Vibrant from 'node-vibrant';
  import jscolor from './assets/scripts/jscolor.min';
  import { eventBus } from './main';
  import { serverURLs } from './assets/scripts/urls';

  export default {
    data() {
      return {
//        browseViewMounted: false,
        categoryItems: [],
        tagItems: [],
        searchParams: {
          primaryColor: '',
          secondaryColor: '',
          tertiaryColor: '',
          selectedCategory: '',
          selectedTags: []
        }
      };
    },
    mounted() {
      $(this.$el).find('.ui.dropdown').dropdown();
      this.$http.get(serverURLs['FETCH-SEARCH-DATA']).then(
        response => {
          let result = response.body;
          this.categoryItems = result['categoryItems'];
          this.tagItems = result['tagItems'];
        }, response => {
          console.log('The response was bad');
        }
      );
    },
    methods: {
      onSearchButtonClicked() {
        this.searchParams.primaryColor = document.getElementsByClassName('input-color-primary')[0].value;
        this.searchParams.secondaryColor = document.getElementsByClassName('input-color-secondary')[0].value;
        this.searchParams.tertiaryColor = document.getElementsByClassName('input-color-tertiary')[0].value;
        this.searchParams.selectedCategory = $(this.$el).find('#search-dropdown-category').dropdown('get value');
        if (this.searchParams.selectedCategory.toLowerCase() == 'all') {
          this.searchParams.selectedCategory = '';
        }
        let selTags = [],
          activeTags = document.getElementById('search-dropdown-tags').getElementsByClassName('label');
        for (let x of activeTags)
          selTags.push(x.innerText.trim());
        this.searchParams.selectedTags = selTags;

        let promise = this.$http.post(serverURLs.SEARCH, this.searchParams);
        eventBus.$emit('searchClicked', promise);
      },
      onUploadButtonClicked() {
        $('#file-input').click();
      },
      onFileChange(e) {
        if (e.target.files.length > 0) {
          let elHolder = document.getElementById('holder');
          elHolder.classList.add('loading');
          let file = e.target.files[0];
          if (this.isFileValid(file)) {
            this.processFile(file);
          }
          elHolder.classList.remove('loading');
        }
      },
      onHolderDrop(e) {
        let file = e.dataTransfer.files[0],
          elHolder = document.getElementById('holder'),
          elBUIC = document.getElementById('button-upload-image-computer');
        if (this.isFileValid(file)) {
          elHolder.classList.add('inverted', 'loading');
          elBUIC.classList.add('inverted');
          this.processFile(file);
          elHolder.classList.remove('loading');
        } else {
          elHolder.classList.add('inverted');
          elBUIC.classList.add('inverted');
        }
      },
      onHolderDragOver() {
        document.getElementById('holder').classList.remove('inverted');
        document.getElementById('button-upload-image-computer').classList.remove('inverted');
      },
      onHolderDragLeave() {
        document.getElementById('holder').classList.add('inverted');
        document.getElementById('button-upload-image-computer').classList.add('inverted');
      },
      processFile(file) {
        let fileURL = window.URL.createObjectURL(file);
        this.paletteFromImage(fileURL);
      },
      paletteFromImage(f) {
        let v = new Vibrant(f);
        v.getPalette((err, palette) => {
          if (err === null) {
            if (palette['Vibrant']) {
              let elsInputs = document.getElementsByClassName('input-color-primary');
              elsInputs[0].jscolor.fromRGB(...(palette['Vibrant']._rgb));
              elsInputs[1].jscolor.fromRGB(...(palette['Vibrant']._rgb));
            }
            if (palette['DarkVibrant']) {
              let elsInputs = document.getElementsByClassName('input-color-secondary');
              elsInputs[0].jscolor.fromRGB(...(palette['DarkVibrant']._rgb));
              elsInputs[1].jscolor.fromRGB(...(palette['DarkVibrant']._rgb));
            }
            if (palette['LightVibrant']) {
              let elsInputs = document.getElementsByClassName('input-color-tertiary');
              elsInputs[0].jscolor.fromRGB(...(palette['LightVibrant']._rgb));
              elsInputs[1].jscolor.fromRGB(...(palette['LightVibrant']._rgb));
            }
          } else {
            console.log(err);
          }
        });
      },
      isFileValid(file) {
        let fileExtensionRange = '.jpg .jpeg .png .gif .bmp',
          MAX_SIZE = 5,  // MB
          postfix = file.name.substr(file.name.lastIndexOf('.')),
          size = file.size;

        if (fileExtensionRange.indexOf(postfix.toLowerCase()) > -1) {
          if (size > 1024 * 1024 * MAX_SIZE) {
            this.$toasted.error('Maximum file size is ' + MAX_SIZE + 'MB.', {
              theme: "primary",
              position: "top-center",
              duration: 2000,
              fitToScreen: true,
            });
          } else {
            return true;
          }
        } else {
          this.$toasted.error('Allowed file types are: ' + fileExtensionRange.split(' ').join(', ') + '', {
            theme: "primary",
            position: "top-center",
            duration: 3000,
            fitToScreen: true,
          });
        }
        return false;
      },
    },
    created() {

    }
  }
</script>

<style lang="scss" scoped>
  @import 'assets/styles/common';

  /* =============== GENERAL TAGS =============== */
  body,
  .top.fixed.menu {
    max-width: 100vw;
  }

  /* =============== GENERIC CLASSES =============== */
  .pad-left-11px {
    padding-left: 11px !important;
  }

  .light-text {
    color: $light-color !important;
  }

  .mx-auto {
    margin-left: auto !important;
    margin-right: auto !important;
  }

  /* =============== STRUCTURE SELECTORS =============== */
  td[valign="top"] {
    padding-top: 21px;
  }

  .main.container {
    padding-top: 15vh;
  }

  #holder {
    display: table;
    border: 2px dashed grey;
    min-width: 159px;
    max-width: 159px;
    min-height: 161px;
    max-height: 161px;
    transition: border 0.3s, color 0.3s;
  }

  /* =============== MEDIA QUERIES =============== */
  @media screen and (max-width: $phone-breakpoint) {
    * {
      font-size: 13px;
      font-weight: 400;
    }

    table.ui.table {
      padding-bottom: 5vh;
    }

    tr {
      padding-top: 0 !important;
      padding-bottom: 0 !important;
    }

    table.ui.table tr.computer-only {
      display: none !important;
    }

    .very-small-width {
      max-width: 80px !important;
    }

    .small-width {
      max-width: 30vw !important;
    }

    .large-width {
      min-width: 290px !important;
      width: 290px !important;
      max-width: 290px !important;
    }

    .color-input {
      max-width: 130px;
      padding-right: 0 !important;
      margin-right: 0 !important;
    }

    .ui.inverted.button.jscolor {
      font-size: 13px;
      padding-left: 1em;
      padding-right: 1em;
      min-width: 77px;
      max-width: 77px;
    }

    #name-header {
      h1 {
        font-size: 3.5em;
        margin-bottom: 0 !important;
      }
      h3 {
        margin-top: 3px;
        font-size: 1em;
        font-weight: 300;
      }
      padding-bottom: 10vh;
    }
  }

  @media screen and (min-width: $phone-breakpoint + 1px) {
    table.ui.table {
      padding-bottom: 5vh;
    }

    table.ui.table tr.touch-only {
      display: none !important;
    }

    .small-width {
      max-width: 9em !important;
    }

    .large-width {
      min-width: 23em !important;
      width: 23em !important;
      max-width: 23em !important;
    }

    .color-input {
      min-width: 130px;
      width: 130px;
      max-width: 130px;
    }

    #name-header {
      h1 {
        font-size: 6em;
        margin-bottom: 0 !important;
      }
      h3 {
        margin-top: 3px;
        font-size: 1.4em;
        font-weight: 300;
      }
      padding-bottom: 5vh;
    }
  }

</style>
