var allowed = false;
addEventListener("keydown", function (e) {
    console.log(e.repeat); // If pressed more then once (in less then 1000ms) "true"
    if (e.repeat === true) return;
    if (e.code == 'KeyD') vxr = 10;
    if (e.code == 'KeyA') vxl = -10;
    if (e.code == 'KeyS') vy = 10;
    if (e.code == 'KeyW') vy = -10;
})

addEventListener("keyup", function (e) {
    console.log(e.repeat); // If pressed more then once (in less then 1000ms) "true"
    if (e.code == 'KeyD') vxr = 0;
    if (e.code == 'KeyA') vxl = 0;
    if (e.code == 'KeyS') vy = 0;
    if (e.code == 'KeyW') vy = 0;
})

