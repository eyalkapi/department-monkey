const puppeteer = require('puppeteer');
const fs = require('fs');


module.exports.buildDiagramSVG = async(json) => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Point to a version of go.js, either a local file or one on the web at a CDN
    await page.addScriptTag({
      url: 'https://unpkg.com/gojs'
    });

    // Create HTML for the page:
    page.setContent('<div id="diagram" style="border: solid 1px black; width:400px; height:400px"></div>');

    // Set up a Diagram, and return the result of makeImageData:
    const imageData = await page.evaluate(() => {
        var $ = go.GraphObject.make;
    
        var diagram = $(go.Diagram, "diagram",
        {
          "animationManager.isEnabled": false,
          "undoManager.isEnabled": true  // enable undo & redo
        });
  
        // define a simple Node template
        diagram.nodeTemplate =
        $(go.Node, "Auto",  // the Shape will go around the TextBlock
            $(go.Shape, "RoundedRectangle", { strokeWidth: 0 },
            new go.Binding("fill", "color")),
            $(go.TextBlock,
            { margin: 8 },
            new go.Binding("text", "key"))
        );
                
        let servers = {
            myDB: {
                groups: ['DB'],
                platform: 'linux',
                technology: ['mongoDB'],
                description: 'a db.'
            },
            myZB: {
                groups: ['DB'],
                platform: 'linux',
                technology: ['mongoDB'],
                description: 'a db.' 
            }
        }

        let links = {
            dbToZb: {
                source: 'myDB',
                destination: 'myZB',
                ports: [80,443],
                protocols: ['HTTP']
            },
        }

        let nodes = [];
        let edges = [];

        for (let [name, properties] of Object.entries(servers)) {
            nodes.push({
                key: name,
                color: "red",
                ...properties
            })
        }

        for (let [key, props] of Object.entries(links)) {
            edges.push({
                from: props.source,
                to: props.destination
            })
        }

        diagram.model = new go.GraphLinksModel(nodes,edges);

        return diagram.makeImageData();
    });

    console.log(imageData);
    createImage(imageData)
}

function createImage(data) {
    const path = 'a-' + Date.now() + '.png';
    const base64 = data.replace(/^data:image\/\w+;base64,/, "");//Remove the front part of the image base64 code data:image/png;base64
    const dataBuffer = new Buffer(base64, 'base64'); //Convert the base64 code into a buffer object,
    fs.writeFile(path, dataBuffer, function(err){//write file with fs
        if(err){
            console.log('bruhror');
        }else{
            console.log('Write successfully!');
        }
    })
}