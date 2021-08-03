import "gojs"

var $ = go.GraphObject.make;

var myDiagram =
  $(go.Diagram, "maane-hagana",
    { // enable Ctrl-Z to undo and Ctrl-Y to redo
      "undoManager.isEnabled": true
    });

// Create the Diagram's Model:
var nodeDataArray = [
    { key: 1, text: "Alpha", color: "lightblue" },
    { key: 2, text: "Beta", color: "orange" },
    { key: 3, text: "Gamma", color: "lightgreen", group: 5 },
    { key: 4, text: "Delta", color: "pink", group: 5 },
    { key: 5, text: "Epsilon", color: "green", isGroup: true }
    ];
var linkDataArray = [
    { from: 1, to: 2, color: "blue" },
    { from: 2, to: 2 },
    { from: 3, to: 4, color: "green" },
    { from: 3, to: 1, color: "purple" }
    ];

myDiagram.model = new go.GraphLinksModel(nodeDataArray, linkDataArray);