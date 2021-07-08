$fn=400;
kerf = 0.4;
thickness = 4;
thickness_front = 4;
height_front = 50;
fillet = 3;
front_slot_width = 0.6;
front_stand_width = 2.5;
front_pin_width = 2;
bore_d = 3.3;

module main_plate(){
    linear_extrude(thickness){
        //offset(-fillet) offset(fillet) offset(fillet) offset(-fillet) {
            difference(){
                square([100,80]);
                translate([8.625+1.375,2.625+1.375,0]) circle(d=bore_d);
                translate([94.625+1.375,2.625+1.375,0]) circle(d=bore_d);
                translate([94.625+1.375,60.625+1.375,0]) circle(d=bore_d);
                translate([8.625+1.375,60.625+1.375,0]) circle(d=bore_d);

                // h bruecke
                translate([3,3,0]) circle(d=bore_d);
                translate([3,40,0]) circle(d=bore_d);
                translate([40,40,0]) circle(d=bore_d);
                translate([40,3,0]) circle(d=bore_d);

                // spannungswandler
                // kein größerer Kopf als 4.5 im Durchmesser
                translate([5.025+1.475,17.275+1.475,0]) circle(d=bore_d);
                translate([35.225+1.475,1.025+1.475,0]) circle(d=bore_d);



            }
            difference(){
                translate([50,50,0]) circle(d=180);
                translate([-40,0,0]) square([240,200]);
            }
        //}
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
