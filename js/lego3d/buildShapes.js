// does a shape [w,h, name] fit at x,y
function shapeFit(x,y,s) {
    var matchColor = getPixel(x,y).toString();
    
    for (var xx=x; xx < x + s[0]; xx++) {
	for (var yy=y; yy < y+ s[1]; yy++) {
	    
	    // if we are outside of bounds return false
	    if (xx >= guiData.imageWidth || yy >= guiData.imageHeight) { return false; }
	    
	    // if the color doesn't match the first pixel then return false
	    if ( getPixel(xx,yy).toString() != matchColor) { return false;}
	    
	    // if the space isn't blank then return false because it's full
	    if (layout[xx][yy] != -1) { return false; }
	}
    }
    // all the blocks are free, this can fit
    return true;
}

// place a shape in this position
function fillShape(x,y,s,m) {
     
     for (var xx=x; xx < x + s[0]; xx++) {
	for (var yy=y; yy < y+ s[1]; yy++) {
	    layout[xx][yy] = -2;   
	}
     }
     
     // set the 0,0 position to the name of the part
     layout[x][y] = s[2];
}

// where does each block go in the drawing
function buildShapes() {
    
    //Clear the array out 
    for (var x=0; x < guiData.imageWidth; x++) {
	var t = [];
	for (var y=0; y < guiData.imageHeight; y++) {
	    t.push(-1);
	}
	layout.push(t);
    }
    
    // layout[x][y]
    for (var x=0; x < guiData.imageWidth; x++) {
       for (var y=0; y < guiData.imageHeight; y++) {
	    // if this space is empty, then find the biggest block to fill it
	    if (layout[x][y] == -1) {
		// loop through each shape
		for (var s=0; s < shapes.length; s++) {
		    if (shapeFit(x,y,shapes[s])) {
			fillShape(x,y,shapes[s]);
		    }
		}
	    }
       }
    }
    
}