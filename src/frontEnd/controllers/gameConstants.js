//global variables
var bgW = 7;
var bgH = bgW/1.163;
var circleR = bgH/(2*6.0);
var boundaryX = bgW;
var boundaryY = bgH;
var error = circleR * 0.75;

//for col
var colUnit = bgW / 7.0;
var colCenterCoords = [0-colUnit*3, 0-colUnit*2, 0-colUnit*1, 0, colUnit*1, colUnit*2, colUnit*3];

//for row
var rowUnit = bgH / 6.0;
var rowCenterCoords = [0+rowUnit*2.5, 0+rowUnit*1.5, 0+rowUnit*0.5, 0-rowUnit*0.5, 0-rowUnit*1.5,0-rowUnit*2.5];

