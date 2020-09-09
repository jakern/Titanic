window.onload = (event) => {
  ctlBuzz = document.getElementById("buzzer");
  ctlBuzz.load();
  ctlEnd = document.getElementById("end-noise");
  ctlEnd.load();
};

var myID, roomVal, nameVal, ctlBuzz;
var uList = new Map();

var username = document.getElementById("name");
var room = document.getElementById("room");
// room.addEventListener("change", changeRoom);
// username.addEventListener("change", update);
roomVal = room.value;
nameVal = username.value;

const button = document.getElementById("cup");
var pouring = -1;
// event listeners
button.addEventListener("mousedown", pourStart);
button.addEventListener("mouseup", pourStop);

button.addEventListener("touchstart", pour);
button.addEventListener("keydown", pour);


// handle socket events
var socket = io.connect("http://" + document.domain + ":" + location.port);

socket.on("connect", () => {
  socket.emit("new_connect");
});

socket.on("new_connect", msg => {
  console.log("msg", msg);
  myID = msg['id'];
  console.log("My ID is " + myID);
});

socket.on("pour", msg => {
    document.querySelector("#counter").innerHTML = msg['fill'];
    setPour(msg['fill']);
});

socket.on("beep", msg => {
  console.log("got beep", msg);
  ctlBuzz.play()
});

socket.on("join_room", msg => {
  console.log("joined", msg);
  socket.emit("here", {
    "id": myID,
    "room": roomVal,
    "name": nameVal
  });
});

socket.on("here", msg => {
  console.log("here", msg);
  var ul = document.getElementById("userlist")
  var id_list = Array.from(ul.children, x => x.getAttribute('data-id'));
  if ( ! id_list.includes(msg['id']) ) {
    addUser(msg['user'], msg['id']);
  }
});

socket.on("leave_room", msg => {
  console.log("left", msg);
  removeUser(msg['id'])
});

socket.on("game_over", loser => {
  // finish pouring
  const event = new Event('mouseup');
  button.dispatchEvent(event);

  var l = document.getElementById("liquor");
  var s = document.getElementById("shotglass");
  l.style.height = 0;
  l.style.top = 0;
  s.style.top = '250px';

  ctlEnd.play();
  alert("GAME OVER: " + loser);
});

function createID() {
  console.log("createID");
  return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
    (
      c ^
      (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))
    ).toString(16)
  );
}

function pourStart(e) {
  if(pouring == -1)  //Prevent multimple loops!
    pouring = setInterval(pour, 50 /*execute every 100ms*/);
}

function pourStop(e) {
  console.log("stop pour");
  if(pouring!=-1) {  //Only stop if exists
    clearInterval(pouring);
    pouring=-1;
  }
}

function pour() {
  console.log("send pour");
  socket.emit("pour", {
    "id": myID,
    "room": roomVal,
    "name": nameVal
  });
}

function changeRoom() {

  socket.emit("leave_room",{
    "id": myID,
    "room": roomVal,
    "name": nameVal
  });
  roomVal = document.getElementById("room").value;
  socket.emit("join_room",{
    "id": myID,
    "room": roomVal,
    "name": nameVal
  });
}

function joinRoom() {
  roomVal = document.getElementById("room").value;
  nameVal = document.getElementById("name").value;

  document.getElementById("cover").style.display = "none";
  document.getElementById("cup").style.display = "block";

  socket.emit("join_room",{
    "id": myID,
    "room": roomVal,
    "name": nameVal
  });
}

function addUser(user, id) {
  uList.set(id, user);

  if (uList.size > 1) {
    var ul = document.getElementById("userlist")
    ul.innerHTML = "";

    var sorted = Array.from(uList.keys()).sort()
    console.log(sorted)
    for (var u of sorted) {
      var li = document.createElement("li");
      var node = document.createTextNode(uList.get(u));
      li.appendChild(node);
      li.setAttribute("data-id", u)
      ul.appendChild(li);
    }
  }
}

function removeUser(id) {
  var ul = document.getElementById("userlist");
  ul.querySelector("li[data-id='"+ id + "']").remove();
}

function setPour(amt) {
  var l = document.getElementById("liquor")
  l.style.height = amt + "%"
  l.style.top = (100-amt) + "%"
}
