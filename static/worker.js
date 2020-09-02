importScripts("socket.io.js");
var socket = io.connect("http://" + "localhost" + ":" + location.port);
// socket = new WebSocket("ws://localhost:5000/");
self.addEventListener(
  "message",
  function(e) {
    self.postMessage({ func: "start" });
    console.log(e.data);
    // doDraw();
    while (true) {
      socket.emit("start", {
        data: "User"
      });
    }
  },
  false
);
