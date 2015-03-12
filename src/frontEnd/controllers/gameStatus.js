//put status updates in a separate file, player2 is to check if the second player has joined
function updateStatus(stalemate,turn,winner,player2){
    updateStatusHelper("turn",turn,player2);
    updateStatusHelper("stalemate",stalemate,player2);
    updateStatusHelper("winner",winner,player2);

}

function updateStatusHelper(name,arg,player2){
    if (typeof(scene.getObjectByName(name)) != "undefined"){
        scene.remove((scene.getObjectByName(name)));
    }
    //create image
    var bitmap = document.createElement('canvas');
    var g = bitmap.getContext('2d');
    bitmap.width = 100;
    bitmap.height = 100;
    g.font = 'Bold 20 Arial';

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
            g.fillStyle = 'red';
        }
        xpos = bgW/2.0 + bgW/5.0;
        ypos = bgH/2.0 - bgH/4.0;
    }else if (name == "stalemate"){
        var sm = arg;
        console.log(sm);
        console.log(player2);
        if (sm == false && player2 == null){
            text = "Queuing.."
            //g.strokeStyle = 'red';
            g.fillStyle = 'red';
        }else if (sm == false){
            text = "In game"
            g.fillStyle = 'yellow';
        }else{
            text = "Draw!"
            g.fillStyle = 'red';
            //g.strokeStyle = 'red';
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
            g.fillStyle = 'red';
            //g.strokeStyle = 'red';
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

function updateOpponent(player1,player2){
    var name = "opp";
    if (typeof(scene.getObjectByName(name)) != "undefined"){
        return;
        //scene.remove((scene.getObjectByName("opp")));
    }
    if (player2 == null){
        return;
    }
    //create image
    if (player2 != null){
        var bitmap = document.createElement('canvas');
        var g = bitmap.getContext('2d');
        bitmap.width = 190;
        bitmap.height = 100;
        g.font = 'Bold 18 Arial';

        var opp;
        var oppName;
        if ( player1 == whoami() ){
            opp = player2;
        }else{
            opp = player1;
        }

        var token = getCookie("token");
        
        xmlhttp=new XMLHttpRequest();
        xmlhttp.open("GET",HOST+"accounts/"+opp +"/",false); //ending / is necessary, otherwise the redirecting is bad
        xmlhttp.setRequestHeader("Authorization","Token "+token);
        xmlhttp.send();
        if (xmlhttp.status == 200){
            var player = JSON.parse(xmlhttp.responseText);
            oppName = player.username;
            var text = "Against: " + oppName;

            g.fillStyle = 'white';
            g.fillText(text, 0, 15);
            g.strokeText(text, 0, 15);
            // canvas contents will be used for a texture
            var texture = new THREE.Texture(bitmap) 
                texture.needsUpdate = true;
            var pGeo = new THREE.PlaneGeometry(bgW/4.0 , bgH/4.0);
            var pGeoMat = new THREE.MeshBasicMaterial({map: texture});
            var stat = new THREE.Mesh(pGeo, pGeoMat);
            stat.name = name;

            xpos = -bgW/2.0 - bgW/5.0;
            ypos = bgH/2.0 - bgH/4.0;
            //ypos = 0;
            stat.position.x = xpos;
            stat.position.y = ypos;
            scene.add(stat);
            
        }else{
            console.log("error in updateOpponent:" + xmlhttp.responseText);
        }
    }
}

