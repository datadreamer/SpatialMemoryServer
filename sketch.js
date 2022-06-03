var data = [];
var images = [];
var currentImage = 0;

function setup(){
  var canvas = createCanvas(windowWidth, windowHeight);
  canvas.parent("sketch");
  frameRate(60);
  imageMode(CENTER);

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    console.log("Geolocation is not supported by this browser.");
  }

}

function draw(){
  background(0);
  if(images[currentImage] != null){
    image(images[currentImage], width/2, height/2);
    fill(0,200);
    rect(0, height-70, width, 70);
    fill(255);
    textSize(22);
    text(data[currentImage].title, 20, height-40);
    textSize(16);
    text("Distance: "+ data[currentImage].dist + "m", 20, height-15);
  }
}

function windowResized(){
  resizeCanvas(windowWidth, windowHeight);
}

function showPosition(position){
  var lat = position.coords.latitude;
  var lon = position.coords.longitude;
  console.log(lat +", "+ lon);
  // load JSON data from the API
  loadJSON("api.py?action=local&lat="+lat+"&lon="+lon, listLoaded);
}

function listLoaded(list){
  console.log(list);
  for(var i=0; i<list.length; i++){
    //data[list[i].item_id] = list[i];
    data.push(list[i]);
    // load images
    loadImage("api.py?action=photo&id="+list[i].item_id+"&sh="+height+"&sw="+width, imageLoaded);
  }
}

function imageLoaded(img){
  images.push(img);
}

function mousePressed(){
  if(mouseX < width/2){
    if(currentImage > 0){
      currentImage--;
    }
  } else {
    if(currentImage < images.length-1){
      currentImage++;
    }
  }
  console.log(currentImage, data[currentImage].item_id);
}
