$fn=400;
kerf = 0.4;
thickness = 4;
thickness_front = 4;
height_front = 50;
fillet = 3;
front_slot_width = 0.6;
front_stand_width = 2.5;
front_pin_width = 2;

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

module front(width=150, height=height_front){
   linear_extrude(thickness){
        difference(){
            square([width,height-2*thickness]);
            for(i=[0:200]){
                translate([2*i*front_stand_width, front_stand_width, 0]) square([front_slot_width, height-2*thickness]);
            }
            translate([front_stand_width,-2,0]) for(i=[0:200]){
                translate([2*i*front_stand_width, 0, 0]) square([front_slot_width, height-2*thickness]);
            }
        }
        for(i=[0:28]){
            translate([i*2*(front_stand_width)-front_slot_width+front_stand_width*2,-thickness,0]) square([front_pin_width, thickness]);
        }
        for(i=[0:29]){
            translate([i*2*(front_stand_width)+front_stand_width-front_slot_width,height-2*thickness,0]) square([front_pin_width, thickness]);
        }
   }
}

module lasercut(){
    offset(delta=kerf/2) {
        projection() {
            front();
        }
    }
}
//lasercut();
main_plate();
//front();
