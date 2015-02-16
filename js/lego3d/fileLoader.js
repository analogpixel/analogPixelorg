// given an array of colors, and a color
// find out what color is closest to that color and return it
function findCloseColor(colors,r,g,b) {

    minDist = -1;
    returnColors = [-1,-1,-1];
    
    for (var i=0; i < colors.length; i++) {
        var color = colors[i];
        var testR = color[1][0];
        var testG = color[1][1];
        var testB = color[1][2];
        
        var d = Math.sqrt(  Math.pow((r - testR),2) +
                            Math.pow((g - testG),2) +
                            Math.pow((b - testB),2) );
        
        if (minDist == -1 || d < minDist) {
            minDist = d;
            returnColors = [testR, testG,testB];
        }
    }
    
    return returnColors;
}

// find the color is closest to the colors that lego has in their basic set
function createLegoColors() {
    var n = guiData.imageWidth * guiData.imageHeight * 4;
    
    for (var i=0; i <n; i+=4) {
        var r = imagePixelData.data[i];
        var g = imagePixelData.data[i+1];
        var b = imagePixelData.data[i+2];
        var a = imagePixelData.data[i+3];
        
        var c = findCloseColor(legoColors,r,g,b);
        
        imagePixelData.data[i] = c[0];
        imagePixelData.data[i+1] = c[1];
        imagePixelData.data[i+2] = c[2];
        
    }
    
    document.getElementById("mycanvas").getContext("2d").putImageData(imagePixelData,0,0);
}

function posterize(nl) {
    var numLevels = clamp(nl, 2, 256);
    var numAreas = 256 / numLevels;
    var numValues = 256 / (numLevels-1);
    var r, g, b;
    var n = guiData.imageWidth * guiData.imageHeight * 4;
    var prog, lastProg = 0;

    for (i=0;i<n;i+=4) {
        
            imagePixelData.data[i]   = numValues * ((imagePixelData.data[i] / numAreas)>>0);
            imagePixelData.data[i+1] = numValues * ((imagePixelData.data[i+1] / numAreas)>>0); 
            imagePixelData.data[i+2] = numValues * ((imagePixelData.data[i+2] / numAreas)>>0); 
        
            imagePixelData.data[i+3] = imagePixelData.data[i+3];
    }
    
    document.getElementById("mycanvas").getContext("2d").putImageData(imagePixelData,0,0);
}

function clamp(val, min, max) {
        return Math.min(max, Math.max(min, val));
    }
        
function buildTextures() {
     for (var x=0; x < guiData.imageWidth; x++) {
        for (var y=0; y < guiData.imageHeight; y++) {
            
            var key = makePixelKey( getPixel(x,y) );
            
            if (! (key in  meshColors) ) {
               
                //meshColors[key] = new THREE.MeshLambertMaterial(
                 meshColors[key] = new THREE.MeshPhongMaterial(
                    {
                        color: new THREE.Color(r/255, g/255, b/255 ) ,
                        specular: new THREE.Color( .2,.2,.2),
                        shininess:guiData.shine,
                        shading: THREE.FlatShading
                    }
                );
               
            }
        }
     }
}

function handleFileSelect(evt) {
    $("#uploader").css("visibility","hidden");
    $("#uploader").css("display","none");
    preFolder.close();
    postFolder.open();
    
    // create a html5 fileReader object to read the file in
    var reader = new FileReader();

    // javascript closures??
    // Setup an event to fire when the data is loaded 
    reader.onload = ( function(theFile) {    
        var fileName = theFile.name;
        
        return function(event) {
            // create a new HTML image element we can work with
            loadImage = new Image();
            
            // When the image is loaded, when we assign the src,
            // this function will be called
            loadImage.onload = function() {
                // copy that image onto the canvas object
                $("#mycanvas").css("width", guiData.imageWidth);
                $("#mycanvas").css("height", guiData.imageHeight);
                document.getElementById("mycanvas").getContext("2d").drawImage(loadImage, 0,0, guiData.imageWidth,guiData.imageHeight);
                imagePixelData = document.getElementById("mycanvas").getContext("2d").getImageData(0,0,guiData.imageWidth,guiData.imageHeight);
                
                
                switch (guiData.colorType) {
                
                    case "posterize":
                        posterize(guiData.posterizeLevel);
                        break;
                    case "lego": 
                        createLegoColors();
                        break;
                }
                
                buildTextures(); // build a texture for each color 
                buildShapes(); // what brick goes where
                init(); // ok, lets kick off the rendering
            }
            
            // set the image src to the data we loaded with the fileReader
            loadImage.src = 'data:image/jpeg;base64,' + btoa(event.target.result);
            
            
        };
    })(evt.target.files[0]);
    
    // kick of the entire process by reading the file that was selected
    // by the user from the file selection widget
    reader.readAsBinaryString( evt.target.files[0] );
}