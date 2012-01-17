
function $(name) {
    return document.getElementById(name);
}

function draggingMouseDown(e) {
    var elt = e.target;
    if (elt.id != 'diagram') {
        return;
    }

    window.startX = parseInt(elt.style.left);
    window.startY = parseInt(elt.style.top);
    if (!window.startX) {
        window.startX = 0;
    }
    if (!window.startY) {
        window.startY = 0;
    }
    window.mouseX = e.clientX;
    window.mouseY = e.clientY;
    window.dragElt = elt;

    document.onmousemove = draggingMouseMove;
}
function draggingMouseMove(e) {
    var elt = window.dragElt;
    if (!elt) {
        return;
    }
    elt.style.left = (window.startX + (e.clientX - window.mouseX)) + 'px';
    elt.style.top  = (window.startY + (e.clientY - window.mouseY)) + 'px';
}
function draggingMouseUp(e) {
    window.dragElt = null;
    document.onmousemove = null;
}

function loaded() {
    fetchDataAndUpdateDisplay($('system-selector'));
    updateMap();
    document.onmousedown = draggingMouseDown;
    document.onmouseup = draggingMouseUp;
}

function fetchDataAndUpdateDisplay(selector) {
    // Launch the request for the data. This is JSONP, purely because I'm a lazy
    // bum and I want something that works locally too
    var url = 'data/' + selector.value + '.js';
    var fetcher = document.createElement('script');
    fetcher.setAttribute('src', url);
    document.getElementsByTagName('head')[0].appendChild(fetcher);
}

function updateDisplay() {
    paint();
}

// The JSONP callback for the choose-a-system selector
function hereItIs(text, xmin, ymin, xmax, ymax, centerlat, centerlon) {
    window.lastFetchedData = {'obj' : text,
                              'xmin' : xmin,
                              'ymin' : ymin,
                              'xmax' : xmax,
                              'ymax' : ymax};
    paint();
}

function updateMap() {
    var zoom = $('scale-slider').value;
    var imgsrc = 'http://maps.googleapis.com/maps/api/staticmap?center=';
    imgsrc += encodeURIComponent($('map-selector').value);
    imgsrc += '&zoom=' + zoom + '&sensor=false&size=640x640';
    $('gmap').src = imgsrc;
}

function paint() {
    var context = $('diagram').getContext('2d');

    if (!window.lastFetchedData) {
        return;
    }

    var lines = window.lastFetchedData.obj;
    var xmin = window.lastFetchedData.xmin;
    var ymin = window.lastFetchedData.ymin;
    var xmax = window.lastFetchedData.xmax;
    var ymax = window.lastFetchedData.ymax;

    // Google Maps zoom level x is our "zoom level" x-16.
    var gzoomlevel = $('scale-slider').value;
    var zoomfactor = Math.pow(2, gzoomlevel - 16);

    var xspan = xmax - xmin;
    var yspan = ymax - ymin;
    context.canvas.width = zoomfactor * xspan;
    context.canvas.height = zoomfactor * yspan;
    context.canvas.style.left = '0px';
    context.canvas.style.top = '0px';

    // Functions to convert the meter-offset data into pixel coordinates
    var xconv = function (pt) { return (pt[0] - xmin) * zoomfactor; };
    var yconv = function (pt) { return (pt[1] - ymin) * zoomfactor; };

    // Clean slate
    context.clearRect(0, 0, context.canvas.width, context.canvas.height);

    // Line style settings
    context.lineCap = 'round';
    context.lineWidth = 3.0;

    // Aight let'z go
    for (var lineIndex = 0; lineIndex < lines.length; lineIndex++) {
        if ($('color-checkbox').checked) {
            context.strokeStyle = lines[lineIndex].color;
        } else {
            context.strokeStyle = 'black';
        }

        var pieces = lines[lineIndex].pieces;
        for (var ii = 0; ii < pieces.length; ii++) {
            var points = pieces[ii];
            var xs = points.map(xconv);
            var ys = points.map(yconv);
            context.beginPath();
            context.moveTo(xs[0], ys[0]);

            for (var jj = 0; jj < points.length; jj++) {
                context.lineTo(xs[jj], ys[jj]);
            }
            context.stroke();
        }
    }
}

