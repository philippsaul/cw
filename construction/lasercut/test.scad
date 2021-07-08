for(i=[0:18]){
    translate([25*cos(i*20),0,0]) rotate([0,0,i*20]) translate([25,0,0]) square([2,3], center=true);
}
