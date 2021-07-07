$fn=400;
kerf = 0.4;
thickness = 4;
fillet = 3;

module main_plate(){
    linear_extrude(thickness){
        offset(-fillet) offset(fillet) offset(fillet) offset(-fillet) {
            square([100,80]);
            difference(){
                translate([50,0,0]) resize([140,60]) circle(d=140);
                translate([-20,0,0]) square([140,50]);
            }
        }
    }
}

module front(width=80, height=40){
   linear_extrude(thickness){
        difference(){
            square([width,height]);
            for(i=[0:20]){
                translate([4*i, 2, 0]) square([1, height]);
            }
            translate([2,-2,0]) for(i=[0:20]){
                translate([4*i, 0, 0]) square([1, height]);
            }
        }
   }
}

module lasercut(){
    offset(delta=kerf/2) {
        projection() {
//            site();
//            translate([b_height+lc_slot,0,0]) site();
//            translate([b_height*2+lc_slot*2,0,0]) back();
//            translate([b_height*2+lc_slot*2,b_height+lc_slot,0]) back();
//            translate([b_length,b_length+lc_slot,0]) rotate([0,0,90]) bottom();
        }
    }
}
//main_plate();
front();
