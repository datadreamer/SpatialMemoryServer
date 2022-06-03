const http = require('http');
const path = require('path');
const fs = require('fs');

function handleRequest(req, res) {
  // What did we request?
  let pathname = req.url;

  // If blank let's ask for index.html
  if (pathname == '/') {
    pathname = '/image.html';
  }

  // Ok what's our file extension
  let ext = path.extname(pathname);

  // Map extension to file type
  const typeExt = {
    '.html': 'text/html',
    '.js':   'text/javascript',
    '.css':  'text/css'
  };

  // What is it?  Default to plain text
  let contentType = typeExt[ext] || 'text/plain';

  fs.readFile(__dirname + pathname,
    function (err, data) {
      if (err) {
        res.writeHead(500);
        return res.end('Error loading ' + pathname);
      }
      res.writeHead(200,{ 'Content-Type': contentType });
      res.end(data);
    }
  );
};


let server = http.createServer(handleRequest);
server.listen(8080);

console.log('Server started on port 8080');
