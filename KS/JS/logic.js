//var shapes for drawing country outlines
//var elon for elon data
//var years for years
var list = Object.keys(shapes);

var selectBox, option, i;

selectBox = document.getElementById("selCountry");

for (i in list) {
   option = document.createElement("option");
   option.textContent = list[i];
   option.value = list[i];
   selectBox.add(option);
}

//var happy for default response variable
//vars freedom and GDP for alternate response variables
console.log(shapes)
console.log(freedom)
console.log(elon)
