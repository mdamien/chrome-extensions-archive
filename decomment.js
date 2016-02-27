var vm = require('vm');
var util = require('util');

var data = '';

process.stdin.resume();
process.stdin.setEncoding('utf8');

process.stdin.on('data', function(chunk) {
	data += chunk;
});

process.stdin.on('end', function() {
	var script = new vm.Script('result = '+data);
	script.runInThisContext(script);
	console.log(JSON.stringify(result, null, 2));
});