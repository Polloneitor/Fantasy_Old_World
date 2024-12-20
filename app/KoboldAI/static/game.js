/// JAVASCRIPT FUNCTIONS ///////
////////////////////////////////
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function draw(ctx, x, y, b, l) {
  ctx.fillRect(x, y, b, l);
}

function createArray(length) {
  var arr = new Array(length || 0),
    i = length;

  if (arguments.length > 1) {
    var args = Array.prototype.slice.call(arguments, 1);
    while (i--) arr[length - 1 - i] = createArray.apply(this, args);
  }

  return arr;
}

///////////////////////////////////////
/// FANTASY OLD WORLD FUNCTIONS ///////
///////////////////////////////////////
function player_action(action) {
  switch (action) {
    case 0:
      return "Pause"
    case 1:
      return "Move"
    case 2:
      return "Look"
    case 3:
      return "Attack"
    case 4:
      return "Defend"
  }
}

function typenature(color) {
  let color_text = ""
  let tileInfo = ""
  //console.log(color)
  if (color == "black") {
    color_text = "Pisas un terreno de tierra, y se siente firme y seguro de caminar."
    tileInfo = "stone"
  } else if (color == "green") {
    color_text = "Empiezas a navegarte cerca de un bosque, las hojas cubren el sol sobre de ti."
    tileInfo = "grass"
  } else if (color == "cyan") {
    color_text = "No hay ninguna nube arriba de ti, ahora el mundo está tan abierto para ti."
    tileInfo = null
  } else if (color == "yellow") {
    color_text = "Un camino de tierra está sobre tus pies, empieza a moverte a un lugar claro."
    tileInfo = "dirt"
  } else if (color == "brown") {
    color_text = "Estás caminando sobre lodo, díficil es para moverte, pues tu tobillo y ropa empieza a pesar cada vez más que te mancha en tu piel."
    tileInfo = "mud"
  } else if (color == "blue") {
    color_text = "Agua está en el suelo, no conoces que tan profundo es."
    tileInfo = "water"
  } else {
    color_text = null
    tileInfo = null
  }
  return { color_text, tileInfo }
}

function boardTravel(board) {
  //console.log(board)
  for (let i = 0; i < board.length; i++) {
    for (let j = 0; j < board[i].length; j++) {
      //console.log(board[i][j].tileImage);
      if (board[i][j].tileImage == null) {
        ctx.beginPath();
        ctx.fillStyle = board[i][j].color;
        draw(ctx, 128 * i, 128 * j, 128, 128)
        ctx.fill();
        ctx.closePath();
        //isIntersect(player, board[i][j])
      }
      else {
        //console.log(board[i][j].tileImage);
        let Image = document.getElementById(board[i][j].tileImage);
        //console.log(Image);
        ctx.drawImage(Image, board[i][j].x, board[i][j].y);
        //isIntersect(player, board[i][j])
      }
    }
  }
}
const canvas = document.getElementById("canvas")
const ctx = canvas.getContext("2d")
const colours = ["blue", "green", "yellow", "brown", "black"]

// 1 = Move, 2 = Look, 3 = Attack, 4 = Defend
let actionSelected = 0;
// time is a global variable that can be changed for actions in movement or actions that do not move up in the time.
let time = false
let quadrant = canvas.width * canvas.height;
let zone = 128; // Pixels
var board = createArray((1152 / zone), (896 / zone))
//console.log(board);
//console.log(quadrant / zone);

class actor {
  constructor() {
    this.state = {
      x: 0,
      y: 0,
      vx: 0,
      vxr: 0,
      vxl: 0,
      vy: 0,
      inTileid: 0,
      inTilecolor: "",
      height: 64,
      width: 64,
      limitXr: canvas.width,
      limitXl: 0,
      limitY: canvas.height,
      img: document.getElementById("warrior"),
      direction: 0,
      coordx: 0,
      coordy: 0,
      roundX: 0,
      roundY: 0,
      data: {}
    }
  }
  updateMovement(time) {
    let rounded_x = Math.floor(this.state.coordx);
    let rounded_y = Math.floor(this.state.coordy);
    ctx.beginPath();
    ctx.fillStyle = "purple";

    switch (this.state.direction) {
      case 1:
        if (this.state.coordy > 0) {
          //console.log("move up")
          this.state.coordy = this.state.coordy - 0.5;
          rounded_y = Math.floor(rounded_y);
          this.state.y += this.state.vy;
          this.state.roundX = rounded_x;
          this.state.roundY = rounded_y;
          this.isIntersect(board[rounded_x][rounded_y - 1], time)
        }
        break;
      case 2:
        if (this.state.coordy < board[0].length - 0.5) {
          //console.log("move down")
          this.state.coordy = this.state.coordy + 0.5
          rounded_y = Math.floor(rounded_y)
          this.state.y += this.state.vy;
          this.state.roundX = rounded_x;
          this.state.roundY = rounded_y;
          this.isIntersect(board[rounded_x][rounded_y + 1], time)
        }
        break;
      case 3:
        if (this.state.coordx > 0) {
          //console.log("move left")
          this.state.coordx = this.state.coordx - 0.5
          rounded_x = Math.floor(rounded_x);
          this.state.x += this.state.vx;
          this.state.x += this.state.vxl;
          this.state.roundX = rounded_x;
          this.state.roundY = rounded_y;
          if (rounded_x - 0.5 > 0) { this.isIntersect(board[rounded_x - 1][rounded_y], time) }

        }
        break;
      case 4:
        //console.log("move right")
        if (this.state.coordx < board.length - 0.5) {
          this.state.coordx = this.state.coordx + 0.5
          rounded_x = Math.floor(rounded_x);
          this.state.x += this.state.vx;
          this.state.x += this.state.vxr;
          this.state.roundX = rounded_x;
          this.state.roundY = rounded_y;
          if (rounded_x + 1 < board.length) { this.isIntersect(board[rounded_x + 1][rounded_y], time) }
        }
        break;
    }
    draw(ctx, this.state.x, this.state.y, 64, 64)
    ctx.fill();
    ctx.fillStyle = "white";
    ctx.closePath();
    ctx.drawImage(this.state.img, this.state.x, this.state.y);
    this.Proyect(this.state.direction)
    console.log("x: " + this.state.x + " y: " + this.state.y)
  }
  Proyect(direction) {
    switch (direction) {
      case 1:
        ctx.beginPath();
        ctx.globalAlpha = 0.4;
        ctx.fillStyle = "white";
        draw(ctx, this.state.x, this.state.y - 64, 64, 64)
        ctx.fill();
        ctx.closePath();
        break;
      case 2:
        ctx.beginPath();
        ctx.globalAlpha = 0.4;
        ctx.fillStyle = "white";
        draw(ctx, this.state.x, this.state.y + 64, 64, 64)
        ctx.fill();
        ctx.closePath();
        break;
      case 3:
        ctx.beginPath();
        ctx.globalAlpha = 0.4;
        ctx.fillStyle = "white";
        draw(ctx, this.state.x - 64, this.state.y, 64, 64)
        ctx.fill();
        ctx.closePath();
        break;
      case 4: -
        ctx.beginPath();
        ctx.globalAlpha = 0.4;
        ctx.fillStyle = "white";
        draw(ctx, this.state.x + 64, this.state.y, 64, 64)
        ctx.fill();
        ctx.closePath();
        break;
    }
    ctx.globalAlpha = 1.0;
  };
  isIntersect(b, time) {
    if (time != false) {
      if (b != undefined) {
        if (
          (this.state.x < b.x + b.width &&
            this.state.x + 64 > b.x &&
            this.state.y < b.y + b.height &&
            this.state.y + 64 > b.y)
        ) {
          this.state.inTileid = b.entity_id;
          b.owned = true;
          console.log("Before: " + this.state.inTilecolor);
          if (this.state.inTilecolor != b.color) {
            console.log("x: " + b.x, "y: " + b.y, "ID: " + b.entity_id)
            this.state.inTilecolor = b.color;
            game_text = "Te alejas del lugar que estuviste;"+b.test_text;
            dosubmitGame(game_text);
          }
          console.log("after: " + this.state.inTilecolor);
        }
      }
    }
  }
  setData(dataset) {
    this.state.data = dataset
  }
  getState() {
    return this.state
  }
  getData() {
    return this.state.data
  }
}
var player = new actor();
let tileId = 0;
let tileType = "";

for (let i = 0; i < board.length; i++) {
  for (let j = 0; j < board[i].length; j++) {
    let random = Math.floor(Math.random() * colours.length)
    let text = ""
    text = typenature(colours[random])
    board[i][j] = {
      entity_id: tileId,
      color: colours[random],
      test_text: text.color_text,
      tileImage: text.tileInfo,
      x: 128 * (i),
      y: 128 * (j),
      width: 128,
      height: 128,
      owned: false
    }
    tileId = tileId + 1;
  }
}

function updateWorld() {
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  boardTravel(board);
  player.updateMovement(time);
  ctx.font = "30px Arial";
  ctx.fillStyle = "white";
  ctx.fillText("Action Selected: " + player_action(actionSelected), 10, 40);
}

/////////////////////////
// GAME INITIALIZATION //
/////////////////////////

sleep(1000).then(() => {
  player.setData(get_demo_player())
  player.isIntersect(board[0][0])
  console.log(player.getData())
  //console.log(player.state.da ta)
  //console.log(getEffects())
  //console.log(getSkills())
  //console.log(getTalents())
  //console.log(getCareers())
  //console.log(getItems())
  updateWorld()
})


///////////////////////
// KEY INPUT READING //
///////////////////////

//Direction is a value attached to the key listener. Up 1, Down 2, Left 3, Right 4. 
sleep(1000).then(() =>
  addEventListener("keydown", function (e) {
    if (e.repeat === true) { return };
    switch (e.code) {
      case 'Digit0':
        actionSelected = 0;
        time = false;
        requestAnimationFrame(updateWorld);
        break;

      case 'Digit1':
        actionSelected = 1;
        time = false;
        requestAnimationFrame(updateWorld);
        break;

      case 'Digit2':
        actionSelected = 2;
        time = false;
        requestAnimationFrame(updateWorld);
        break;

      case 'Digit3':
        actionSelected = 3;
        time = false;
        requestAnimationFrame(updateWorld);
        break;

      case 'Digit4':
        actionSelected = 4;
        time = false;
        requestAnimationFrame(updateWorld);
        break;
    }

    switch (actionSelected) {
      case 1:
        switch (e.code) {
          case 'KeyD':
            if (player.state.direction == 1 || player.state.direction == 2) {
              player.state.direction = 4; player.state.vxr = 64; player.state.vy = 0; time = true; requestAnimationFrame(updateWorld); break;
            } else {
              player.state.direction = 4; player.state.vxr = 64; time = true; requestAnimationFrame(updateWorld); break;
            }
          case 'KeyA':
            if (player.state.direction == 1 || player.state.direction == 2) {
              player.state.direction = 3; player.state.vxl = -64; player.state.vy = 0; time = true; requestAnimationFrame(updateWorld); break;
            } else {
              player.state.direction = 3; player.state.vxl = -64; time = true; requestAnimationFrame(updateWorld); break;
            }

          case 'KeyS':
            if (player.state.direction == 3 || player.state.direction == 4) {
              player.state.direction = 2; player.state.vy = 64; player.state.vxr = 0; player.state.vxl = 0; time = true; requestAnimationFrame(updateWorld); break;
            } else {
              player.state.direction = 2; player.state.vy = 64; time = true; requestAnimationFrame(updateWorld); break;
            }

          case 'KeyW':
            if (player.state.direction == 3 || player.state.direction == 4) {
              player.state.direction = 1; player.state.vy = -64; player.state.vxr = 0; player.state.vxl = 0; time = true; requestAnimationFrame(updateWorld); break;
            } else {
              player.state.direction = 1; player.state.vy = -64; time = true; requestAnimationFrame(updateWorld); break;
            }
        } break;
      case 2:
        switch (e.code) {
          case 'KeyD':
            if (player.state.direction == 1 || player.state.direction == 2) {
              player.state.direction = 4; time = true; requestAnimationFrame(updateWorld); break;
            } else {
              player.state.direction = 4; time = true; requestAnimationFrame(updateWorld); break;
            }
          case 'KeyA':
            if (player.state.direction == 1 || player.state.direction == 2) {
              player.state.direction = 3; time = true; requestAnimationFrame(updateWorld); break;
            } else {
              player.state.direction = 3; time = true; requestAnimationFrame(updateWorld); break;
            }

          case 'KeyS':
            if (player.state.direction == 3 || player.state.direction == 4) {
              player.state.direction = 2; time = true; requestAnimationFrame(updateWorld); break;
            } else {
              player.state.direction = 2; time = true; requestAnimationFrame(updateWorld); break;
            }

          case 'KeyW':
            if (player.state.direction == 3 || player.state.direction == 4) {
              player.state.direction = 1; time = true; requestAnimationFrame(updateWorld); break;
            } else {
              player.state.direction = 1; time = true; requestAnimationFrame(updateWorld); break;
            }
        } break;
    }

  }))

addEventListener("keyup", function (e) {
  switch (e.code) {
    case 'KeyD':
      player.state.vxr = 0;
    case 'KeyA':
      player.state.vxl = 0;
    case 'KeyS':
      player.state.vy = 0;
    case 'KeyW':
      player.state.vy = 0;
  }
})


// TESTING //
//for (let i in images) {
//  ctx.beginPath();
//  ctx.fillStyle = images[i].color;
//  draw(ctx, images[i].x, images[i].y, images[i].width, images[i].height)
//  ctx.fill()
//  ctx.closePath();
//  //isIntersect(x, y, images[i])
//
//  //console.log('done')
//}
//for (let i = 0; i < board.length; i++) {
//  ctx.beginPath();
//  ctx.fillStyle = "green";
//  draw(ctx, 128 * i, 0, 128, 128)
//  ctx.fill()
//  ctx.closePath();
//  //console.log(i);
//  for (let j = 0; j < board[i].length; j++) {
//    ctx.beginPath();
//    ctx.fillStyle = "red";
//    draw(ctx, 128 * i, 128 * (j + 1), 128, 128)
//    ctx.fill()
//    ctx.closePath();
//    //console.log(j);
//  }
//
//  //console.log('done')
//}

//// create the rectangle
//var images = [];
//images.push({
//  entity_id: 1,
//  x: 310,
//  y: 310,
//  width: 64,
//  height: 64,
//  color: "green",
//  test_text: ('You enter through a forest')
//});
//
//images.push({
//  entity_id: 2,
//  x: 360,
//  y: 310,
//  width: 64,
//  height: 64,
//  color: "yellow",
//  test_text: ('Observas a una persona')
//});
//function playerMovement() {
//  ctx.beginPath();
//  ctx.fillStyle = "purple";
//  if ((x + vxr) <= limitXr - 64) {
//    x += vx;
//    x += vxr;
//  }
//
//  if ((x + vxl) >= limitXl) {
//    x += vx;
//    x += vxl;
//  }
//
//  if ((y + vy) <= limitY - 64 && (y + vy) >= 0) {
//    y += vy;
//  }
//  draw(ctx, x, y, 64, 64)
//  ctx.fill();
//  ctx.closePath();
//  ctx.drawImage(img, x, y);
//  console.log("x: " + x + " y: " + y)
//}

//let x = 0;
//let y = 0;
//let vx = 0;
//let vxr = 0;
//let vxl = 0;
//let vy = 0;
//let limitXr = canvas.width;
//let limitXl = 0;
//let limitY = canvas.height;
//let inTileid = 0;

//function isIntersect(a, b) {
//  if (
//    (a.x< b.x + b.width &&
//      a.x + 64 > b.x &&
//      a.y < b.y + b.height &&
//      a.y + 64 > b.y)
//  ) {
//    console.log("Before: " + tileType);
//
//    if (tileType != b.color) {
//      console.log("x: " + b.x, "y: " + b.y, "ID: " + b.entity_id)
//      b.owned = true;
//      a.inTileid = b.entity_id;
//      tileType = b.color;
//      game_text = b.test_text;
//      console.log("after: " + tileType);
//      //socket.send({ 'cmd': 'oldworldtest', 'data': '' });
//      return dosubmitGame(game_text);
//    }
//  }
//}

