// Constants
var PERIOD = 10;

// Variables
var time = 0;
var travel = 0;

var startLaunch = false;

// Shapes
var background = new Path.Rectangle(view.bounds);
background.fillColor = new Color(1, 0, 0);

var backgroundLayer = project.activeLayer;
var starLayer = new Layer();
var flameLayer = new Layer();
var surfaceLayer = new Layer();

surfaceLayer.activate();
var earth = new Raster('png-earth');
earth.position = view.center;
earth.scale(view.bounds.size.height/earth.bounds.size.height);

var innerFlame = new Path({
    segments: [[0, -50], [100, 20], [25, 185], [-25, 185], [-100, 20]],
    fillColor: 'orange',
    closed: true
});
innerFlame.scale(view.bounds.size.height/2000);
//innerFlame.translate(new Point(0,view.bounds.size.height/3);
innerFlame.smooth();
innerFlame.position = view.center + new Point(0, view.bounds.size.height/3);
outerFlame = innerFlame.clone();
outerFlame.fillColor = 'red';
outerFlame.scale(1.5);
outerFlame.bringToFront();
innerFlame.bringToFront();

// Backend data
var drawing_id = -1;
var other_drawings = [];

// Keyframes
var duration = [5, 0.1, 8, 5, 5, 20, 10, 0.1]
var starsOpacity = [0, 0, 0, 0.1, 1, 1, 1, 0, 0];
var starsSpeed = [0, 0, 80, 120, 130, 130, 130, 0, 0];
var starsAngle = [90, 90, 90, 90, 90, 90, 270, 270, 270];
var backgroundGradientTop = [
	new Color(0.33, 0.8, 1),
	new Color(0.33, 0.8, 1),
	new Color(0.33, 0.8, 1),
	new Color(0, 0.5, 0.71),
	new Color(0, 0, 0),
	new Color(0, 0, 0),
	new Color(0, 0, 0),
	new Color(0.37, 0.33, 0.3),
	new Color(0.37, 0.33, 0.3)
];
var backgroundGradientBot = [
	new Color(0.81, 0.91, 1),
	new Color(0.81, 0.91, 1),
	new Color(0.81, 0.91, 1),
	new Color(0.33, 0.8, 1),
	new Color(0, 0, 0),
	new Color(0, 0, 0),
	new Color(0, 0, 0),
	new Color(0.68, 0.52, 0.37),
	new Color(0.68, 0.52, 0.37)
];
var flameSize = [0, 0, 1, 1, 0, 0, 0, 1, 0];
var earthTop = [0, 0, 0, 5, 5, 5, 5, 5, 5];
var marsTop = [1, 1, 1, 1, 1, 1, 1, 1, 0];

// Functions

// InterPolated KeyFrame
function ipkf(array) {
	var baseTravel = Math.floor(travel);
	if (baseTravel != duration.length) {
		var invProgress = travel % 1;
		var progress = 1-invProgress;
		return array[baseTravel]*progress + array[baseTravel+1]*invProgress;
	} else {
		return array[baseTravel];
	}
}

function drawBackground() {
	background.fillColor = {
		gradient: {
            stops: [ipkf(backgroundGradientBot), ipkf(backgroundGradientTop)]
        },
        origin: background.bounds.bottomCenter,
        destination: background.bounds.topCenter
	};	
}

function drawSurfaces() {
	earth.position = view.center + new Point(0, view.bounds.size.height*ipkf(earthTop));
	if (ipkf(earthTop)>1) {
		earth.opacity = 0;
	}
	//mars.position = view.center + new Point(view.bounds.size.height*ipkf(marsTop), 0);
}

starLayer.activate();
var moveStars = new function() {
	// The amount of symbol we want to place;
	var count = 50;

	// Create a symbol, which we will use to place instances of later:
	var path = new Path.Circle({
		center: [0, 0],
		radius: 5,
		fillColor: 'white'
	});

	var symbol = new Symbol(path);

	// Place the instances of the symbol:
	for (var i = 0; i < count; i++) {
		// The center position is a random point in the view:
		var center = Point.random() * view.size;
		var placed = symbol.place(center);
		placed.scale(i / count + 0.01);
		placed.data = {
			vector: new Point({
				angle: Math.random() * 360,
				length : (i / count) * Math.random() / 5
			})
		};
	}

	var vector = new Point({
		angle: 45,
		length: 0
	});

	function keepInView(item) {
		var position = item.position;
		var viewBounds = view.bounds;
		if (position.isInside(viewBounds))
			return;
		var itemBounds = item.bounds;
		if (position.x > viewBounds.width + 5) {
			position.x = -item.bounds.width;
		}

		if (position.x < -itemBounds.width - 5) {
			position.x = viewBounds.width;
		}

		if (position.y > viewBounds.height + 5) {
			position.y = -itemBounds.height;
		}

		if (position.y < -itemBounds.height - 5) {
			position.y = viewBounds.height
		}
	}

	return function(vector) {
		// Run through the active layer's children list and change
		// the position of the placed symbols:
		var layer = project.activeLayer;
		for (var i = 0; i < count; i++) {
			var item = layer.children[i];
			var size = item.bounds.size;
			var length = vector.length / 10 * size.width / 10;
			item.position += vector.normalize(length) + item.data.vector;
			keepInView(item);
			item.opacity = ipkf(starsOpacity);
		}
	};
};

window.setSceneData = function(drawing_id, other_drawings){
	window.drawing_id = drawing_id;
	drawing_id = drawing_id;
	window.other_drawings = other_drawings;
	other_drawings = other_drawings;
	startLaunch = true;
	setTimeout(function() {
		new Audio('/static/countdown.mp3').play()
	}, 1000);
}

view.onResize = function(event) {
	background.bounds = view.bounds;
};

view.onFrame = function(event) {

	time = event.time;
	var transition = false;

	if (startLaunch){
		if (travel < duration.length) {
			var oldTravel = travel;
			travel += event.delta/duration[Math.floor(travel)];
			if (Math.floor(oldTravel)<Math.floor(travel)) {
				transition = true;
			}
		} else if (travel != duration.length) {
			travel = duration.length;
		}
	}

	if (transition) {
		console.log(Math.floor(travel));
		switch(Math.floor(travel)) {
		  case 0:
		    // code block
		    break;
		  case 1:
		    new Audio('/static/launch.mp3').play()
		    break;
		  default:
		    // code block
		}
	}

	innerFlame.scale(1+0.01*Math.sin(event.time*25));
	outerFlame.scale(1+0.01*Math.cos(event.time*25));

	// Draw layers
	backgroundLayer.activate();
	drawBackground();
	starLayer.activate();
	var starsVector = new Point(1,0);
	starsVector *= ipkf(starsSpeed);
	starsVector.angle = ipkf(starsAngle);
	moveStars(starsVector);
	surfaceLayer.activate();
	drawSurfaces();
	flameLayer.activate();
	innerFlame.opacity = ipkf(flameSize);
	outerFlame.opacity = ipkf(flameSize);
};