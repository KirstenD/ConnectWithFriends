//global variables
var bgW = 8.25;
var bgH = 6;
var circleR = bgH/(2*5.0);
var boundaryX = bgW;
var boundaryY = bgH;
var error = circleR * 0.75;

//for col
var colUnit = bgW / 7.0;
var colCenterCoords = [0-colUnit*3, 0-colUnit*2, 0-colUnit*1, 0, colUnit*1, colUnit*2, colUnit*3];

//for row
var rowUnit = bgH / 5.0;
var rowCenterCoords = [0+rowUnit*2, 0+rowUnit*1, 0, 0-rowUnit*1, 0-rowUnit*2];

//[-]update board locally 
function updateBoard(){
    var geometry2 = new THREE.CircleGeometry(circleR, 35);
    var material2 = new THREE.MeshBasicMaterial( { color: 0xffffff } );
    material2.map    = THREE.ImageUtils.loadTexture('../images/RedToken.png')
    var gameToken2 = new THREE.Mesh( geometry2, material2 );
    //alert(geometry2.id);
    gameToken2.name = "a";
    gameToken2.position.y = -1;
    scene.add( gameToken2 );
}
//setInterval(updateBoard, 3000);

//transfer position in 3D world into array indexes
function posToArrayIndex(pos){
    var x = pos.x;//x is the column in this game!!!!!!!!!!!
    var y = pos.y;//y is the row in this game!!!!!!!!!!!
    var i;
    var retI;
    var retJ;
    for (i=0;i<colCenterCoords.length;i++){
        if (x> colCenterCoords[i]-error && x < colCenterCoords[i]+error ){
            retJ = i;
        }
    }

    for (i=0;i<rowCenterCoords.length;i++){
        if (y> rowCenterCoords[i]-error && y < rowCenterCoords[i]+error ){
            retI = i;
        }
    }
    return [retI,retJ];
}

//handle mouse click event
document.addEventListener( 'click', onDocumentMouseClick, false );
function onDocumentMouseClick( event ) {
    //document coords to  3D space coords: http://stackoverflow.com/questions/13055214/mouse-canvas-x-y-to-three-js-world-x-y-z
    var vector = new THREE.Vector3();
    vector.set(
            ( event.clientX / window.innerWidth ) * 2 - 1,
            - ( event.clientY / window.innerHeight ) * 2 + 1,
            0.5 );
    vector.unproject( camera );
    var dir = vector.sub( camera.position ).normalize();
    var distance = - camera.position.z / dir.z;
    var pos = camera.position.clone().add( dir.multiplyScalar( distance ) );

    var index = posToArrayIndex(pos);

    if (typeof(index[0]) != "undefined" && typeof(index[1]) != "undefined"){
        //creating object based on this 
        var geometry2 = new THREE.CircleGeometry(circleR, 35);
        var material2 = new THREE.MeshBasicMaterial( { color: 0xffffff } );
        material2.map    = THREE.ImageUtils.loadTexture('../images/BlackToken.png')
        var gameToken2 = new THREE.Mesh( geometry2, material2 );
        //alert(geometry2.id);
        gameToken2.name = "t" + index[0] + index[1];
        gameToken2.position.x = colCenterCoords[index[1]];
        gameToken2.position.y = rowCenterCoords[index[0]];
        scene.add( gameToken2 );

    }else{
        alert(index[0]+" "+index[1]);
    }


    //alert(scene.getObjectByName("aa"));

    //scene.getObjectByName("aa").translateY(-0.1);
//scene.traverse (function (object)
//{
//        if (object.name === 'aa'){
//            object.position.x = 1;
//            //while  (object.position.y > -(boundaryY/2.0 - circleR)){
//                //object.translateY(-0.1);
//            //}
//        }
//            // do what you want with it.
//});

}


//for background image. i.e. the game board
var bg = new THREE.Mesh(
        new THREE.PlaneGeometry(bgW , bgH),
        new THREE.MeshBasicMaterial({map: THREE.ImageUtils.loadTexture('../images/Connect4Board.png')})
        );

// The bg plane shouldn't care about the z-buffer.
bg.material.depthTest = false;
bg.material.depthWrite = false;

var bgScene = new THREE.Scene();
var bgCam = new THREE.Camera();
var bgCam = new THREE.PerspectiveCamera( 75, window.innerWidth/window.innerHeight, 0.1, 1000 );
bgScene.add(bgCam);
bgScene.add(bg);
bgCam.position.z = 5;


//for the tokens
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 75, window.innerWidth/window.innerHeight, 0.1, 1000 );

var renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

var geometry = new THREE.CircleGeometry(circleR, 35);
var material = new THREE.MeshBasicMaterial( { color: 0xffffff } );
material.map    = THREE.ImageUtils.loadTexture('../images/RedToken.png')
var gameToken = new THREE.Mesh( geometry, material );
geometry.name = "aa";
scene.add( gameToken );

camera.position.z = 5;

var render = function () {
    requestAnimationFrame( render );

    //gameToken.rotation.x += 0.1;
    //gameToken.rotation.y += 0.1;

    if (gameToken.position.y > -(boundaryY/2.0 - circleR)){
        gameToken.translateY( -0.1 );
    }
    //if (typeof(scene.getObjectById("6")) != "undefined"){
        //scene.getObjectByName("aa").translateY(-0.1);
        //alert("g");
    //}
    //alert(scene.getObjectByName("aa"));//.translateY( -0.1 );
    //alert(typeof(scene.getObjectByName("aa")) == "undefined");


    renderer.autoClear = false;
    renderer.clear();
    renderer.render(bgScene, bgCam);
    renderer.render(scene, camera);
};
render();
