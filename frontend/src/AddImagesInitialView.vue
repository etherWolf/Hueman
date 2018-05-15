<template>
  <section class="ui centered center aligned main container">
    <div class="ui center aligned inverted segment">
      <div id="drop-holder" class="ui center aligned raised compact inverted segment"
           @dragover.stop.prevent="onHolderDragOver()"
           @dragleave.prevent="onHolderDragLeave()"
           @drop.prevent="onHolderDrop($event)">
        <p class="light-text">Drop images here...</p>
        <input class="file-input"
               type="file"
               name="name"
               style="display: none;"
               accept="image/*"
               @change.stop.prevent="onFileChange($event)"
               multiple>
      </div>
      <div class="ui horizontal inverted divider">
        Or
      </div>
      <button class="ui inverted labeled primary icon button"
              @click="onUploadButtonClicked()">
        Browse...
        <i class="upload icon"></i>
      </button>
    </div>
  </section>
</template>

<script>
  import {eventBus} from './main';
  import {serverURLs} from './assets/scripts/urls';

  export default {
    data() {
      return {
        filesList: [],
      };
    },
    methods: {
      onUploadButtonClicked() {
        this.$el.getElementsByClassName('file-input')[0].click();
      },
      onFileChange(e) {
        if (e.target.files.length > 0) {
          let elHolder = document.getElementById('drop-holder');
          elHolder.classList.add('loading');
          document.getElementsByTagName('button')[0].disabled = true;
          this.processFiles(e.target.files);
          elHolder.classList.remove('loading');
        }
      },
      onHolderDrop(e) {
        let elHolder = document.getElementById('drop-holder'),
          elBUIC = document.getElementsByTagName('button')[0];
        elHolder.classList.add('inverted', 'loading');
        elBUIC.classList.add('inverted');
        elBUIC.disabled = true;
        this.processFiles(e.dataTransfer.files);
        elHolder.classList.remove('loading');
      },
      onHolderDragOver() {
        document.getElementById('drop-holder').classList.remove('inverted');
        document.getElementsByTagName('button')[0].classList.remove('inverted');
      },
      onHolderDragLeave() {
        document.getElementById('drop-holder').classList.add('inverted');
        document.getElementsByTagName('button')[0].classList.add('inverted');
      },
      processFiles(files) {
        let promises = [];
        for (let file of files) {
          if (this.isFileValid(file)) {
            let formData = new FormData();
            formData.append('file', file);
            promises.push(this.$http.post(serverURLs.UPLOAD, formData, {
              headers: {
                'Content-Type': 'multipart/form-data',
              }
            }));
          }
        }

        Promise.all(promises).then(responses => {
          this.filesList = [];
          for (let response of responses)
            this.filesList.push(response.body);
          if (this.filesList.length > 0) {
            eventBus.$emit('filesProcessingDone', this.filesList);
          }
          else
            this.$toasted.error('No valid files found!', {
              theme: "primary",
              position: "top-center",
              duration: 3000,
              fitToScreen: true,
            });
        }, responses => {
          for (let response of responses) {
            console.log('The response was bad');
            console.log(response);
          }
        });
      },
      isFileValid(file) {
        let fileExtensionRange = '.jpg .jpeg .png .gif .bmp',
          MAX_SIZE = 15,  // MB
          postfix = file.name.substr(file.name.lastIndexOf('.')),
          size = file.size;

        if (fileExtensionRange.indexOf(postfix.toLowerCase()) > -1) {
          return size <= 1024 * 1024 * MAX_SIZE;
        } else {
          return false;
        }
      },
    }
  }
</script>

<style lang="scss" scoped>
  @import 'assets/styles/common';

  #drop-holder {
    margin-left: auto;
    margin-right: auto;
    display: table;
    border: 2px dashed grey;
    transition: border 0.3s, color 0.3s;

    @media screen and (max-width: $phone-breakpoint) {
      min-width: 60vw;
      max-width: 60vw;
      min-height: 20vh;
      max-height: 20vh;
      p {
        margin-top: 6vh;
      }
    }

    @media screen and (min-width: $phone-breakpoint + 1px) {
      min-width: 500px;
      max-width: 500px;
      min-height: 200px;
      max-height: 200px;
      p {
        margin-top: 75px;
      }
    }
  }

  .main.container {
    padding-top: 15vh;
  }
</style>
