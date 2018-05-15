$(document).ready(function() {
    $(".ui.dropdown").dropdown();

    var holder = $("#holder");
    
    holder.on("drop", function(e) {
        e.preventDefault();
        var file = e.originalEvent.dataTransfer.files[0];
        if (is_file_valid(file)) {
            $(this).addClass("inverted");
            $(this).addClass("loading");
            $("#button-upload-image").addClass("inverted");
            var reader = new FileReader();
            reader.onload = function(file) {
                do_vibrant(reader.result);
            };
            reader.readAsDataURL(file);
        } else {
            $(this).addClass("inverted");
            $("#button-upload-image").addClass("inverted");
        }
    });

    holder.on("dragover", function(e) {
        e.stopPropagation();
        e.preventDefault();
        $(this).removeClass("inverted");
        $("#button-upload-image").removeClass("inverted");
    });

    holder.on("dragleave", function(e) {
        e.preventDefault();
        $(this).addClass("inverted");
        $("#button-upload-image").addClass("inverted");
    });

    $("#button-upload-image").on("click", function() {
        $("#file-input").click();
    });

    $("#file-input").change(function(e) {
        e.stopPropagation();
        e.preventDefault();
        var reader = new FileReader();
        reader.onload = function(file) {
            do_vibrant(reader.result);
        }
        if (this.files.length > 0) {
            if(is_file_valid(this.files[0])) {
                $("#holder").addClass("loading");
                reader.readAsDataURL(this.files[0]);
            }
        }
    });
});

function is_file_valid (file) {
    var fileExtentionRange = ".jpg .jpeg .png .gif .bmp";
    var MAX_SIZE = 30; // MB

    var postfix = file.name.substr(file.name.lastIndexOf("."));
    size = file.size

    if (fileExtentionRange.indexOf(postfix.toLowerCase()) > -1) {
        if (size > 1024 * 1024 * MAX_SIZE ) {
            alert("Error! Maximum file size is " + MAX_SIZE + " MB.");
        } else {
            return true
        }
    } else {
        alert("Error! Allowed file types are: " + fileExtentionRange.split(" ").join(", ") + "");
    }
    return false
}

function do_vibrant(img_data) {
    var img = document.createElement("img");
    img.setAttribute("src", img_data);
    img.setAttribute("id", "vibrant-img");
    img.setAttribute("class", "ui small image");
    img.addEventListener("load", function() {
        var vibrant = new Vibrant(img, 256, 5);
        var swatches = vibrant.swatches();
        // var palette = [];
        // for (var swatch in swatches)
        //     if (swatches.hasOwnProperty(swatch) && swatches[swatch])
        //      palette.push(swatches[swatch].getHex());
        if (swatches["Vibrant"])
            document.getElementById("input-color-primary").jscolor.fromString(swatches["Vibrant"].getHex());
        if (swatches["DarkVibrant"])
            document.getElementById("input-color-secondary").jscolor.fromString(swatches["DarkVibrant"].getHex());
        if (swatches["LightVibrant"])
            document.getElementById("input-color-tertiary").jscolor.fromString(swatches["LightVibrant"].getHex());
        $("#holder").removeClass("loading");
    });
}

function setup_page() {
    
}