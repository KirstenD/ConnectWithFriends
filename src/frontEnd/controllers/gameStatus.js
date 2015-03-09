//put status updates in a separate file

function updateStatus(stalemate,turn,winner){
    updateStatusHelper("turn",turn);
    updateStatusHelper("stalemate",stalemate);
    updateStatusHelper("winner",winner);

}

function updateStatusHelper(name,arg){
    if (typeof(scene.getObjectByName(name)) != "undefined"){
        scene.remove((scene.getObjectByName(name)));
    }
    //create image
    var bitmap = document.createElement('canvas');
    var g = bitmap.getContext('2d');
    bitmap.width = 100;
    bitmap.height = 100;
    g.font = 'Bold 15 Arial';

    var text;
    var xpos = 0;
    var ypos = 0;
    if (name == "turn"){
        var turn = arg;
        console.log(turn);
        if (turn == whoami()){
            text = "Your turn";
            g.fillStyle = 'yellow';
        }else{
            text = "Wait";
            g.strokeStyle = 'red';
        }
        xpos = bgW/2.0 + bgW/5.0;
        ypos = bgH/2.0 - bgH/4.0;
    }else if (name == "stalemate"){
        var sm = arg;
        console.log(sm);
        if (sm == false){
            text = "On going"
            g.fillStyle = 'yellow';
        }else{
            text = "Draw!"
            g.strokeStyle = 'red';
        }
        xpos = bgW/2.0 + bgW/5.0;
        ypos = -bgH/2.0 + bgH/4.0;
    }else if (name == "winner"){
        var winner = arg;
        console.log(winner);
        if (winner == null){

        }else if (winner == whoami()){
            text = "You win!"
            g.fillStyle = 'yellow';
            scene.remove((scene.getObjectByName("stalemate")));
        }else{
            text = "You lose!"
            g.strokeStyle = 'red';
            scene.remove((scene.getObjectByName("stalemate")));
        }
        xpos = bgW/2.0 + bgW/5.0;
        ypos = 0;
    }


    g.fillText(text, 0, 15);
    g.strokeText(text, 0, 15);
    // canvas contents will be used for a texture
    var texture = new THREE.Texture(bitmap) 
    texture.needsUpdate = true;

    var pGeo = new THREE.PlaneGeometry(bgW/4.0 , bgH/4.0);
    var pGeoMat = new THREE.MeshBasicMaterial({map: texture});
    var stat = new THREE.Mesh(pGeo, pGeoMat);
    stat.name = name;
    stat.position.x = xpos;
    stat.position.y = ypos;
    scene.add(stat);
}


//TODO: not used 
function updateOpponent(name){
    if (typeof(scene.getObjectByName(name)) != "undefined"){
        scene.remove((scene.getObjectByName(name)));
    }
    //create image
    var bitmap = document.createElement('canvas');
    var g = bitmap.getContext('2d');
    bitmap.width = 100;
    bitmap.height = 100;
    g.font = 'Bold 15 Arial';
    var text = "Playing with: "+name;

    g.fillStyle = 'yellow';
    g.fillText(text, 0, 15);
    g.strokeStyle = 'red';
    g.strokeText(text, 0, 15);
    // canvas contents will be used for a texture
    var texture = new THREE.Texture(bitmap) 
    texture.needsUpdate = true;

    var pGeo = new THREE.PlaneGeometry(bgW/4.0 , bgH/4.0);
    var pGeoMat = new THREE.MeshBasicMaterial({map: texture});
    var stat = new THREE.Mesh(pGeo, pGeoMat);
    stat.name = name;

    xpos = -bgW/2.0 - bgW/3.0;
    ypos = bgH/2.0 - bgH/4.0;
    stat.position.x = xpos;
    stat.position.y = ypos;
    scene.add(stat);
}
