//Diccionario para guardar si se puede colisionar o no
//Si el usuario va en dirección a una puerta abierta las colisiones se desactivan.
var door_dict = {
"salon-d": true,
"outside-d": true,
"door-kit": true,
"bed1-d": true,
"bed2-d": true,
"bath1-d": true,
"bed3-d": true,
"bath2-d": true
};


function enable_camera_collisions(d){
  const entries = Object.entries(d);
  var collisions = true;
  for (const [key, value] of entries) {
    if (!value){
      collisions = false
    } 
  }
  console.log("Se habilitan las colisiones", collisions)
  const camera = document.querySelector("#camera");
  const cameraObject3D = camera.object3D;
  cameraObject3D.el.components["camera-movement"].data.collisions = collisions;

}

AFRAME.registerComponent("door-test", {
    schema: {
        rotation: { type: "string", default: "0 90 0" }, // Default open rotation
        proximityDistance: { type: "number", default: 5},
        opened: { type: "boolean", default: false}
      },

    init: function () {
      // Initial rotation of the door
      this.element = this.el;
      var el = this.el
      this.closedRotation = this.element.getAttribute("rotation"); // Modify this to suit your door's closed state
      this.element.addEventListener('click', this.toggleDoor.bind(this))
      

      
    },

    toggleDoor: function (event) {
        console.log("SaltaEvent", event);
        var cursor = event.detail.cursorEl.getAttribute("id")
        console.log(cursor);
        if (cursor !== "front-cursor"){
          return
        }
        camera = document.querySelector("#camera");
        const doorObject3D = this.el.object3D;
        const cameraObject3D = camera.object3D;
        //console.log(this.el)
        // Get the world positions of the camera and door
        const doorPosition = new THREE.Vector3();
        const cameraPosition = new THREE.Vector3();
        doorObject3D.getWorldPosition(doorPosition);
        cameraObject3D.getWorldPosition(cameraPosition);
        const distance = cameraPosition.distanceTo(doorPosition);
        var cursor = document.querySelector("#front-cursor").components.raycaster
        var intersection = cursor.getIntersection(this.el);
        //console.log(intersection);
        console.log(distance, this.data.proximityDistance);
        if (distance <= this.data.proximityDistance){
            if (this.data.opened) {
                console.log("CIERRA");
                this.el.removeAttribute("animation");
                this.el.setAttribute("animation", {property: "rotation", to: this.closedRotation, dur: 500, easing: "linear"});
            } else {
               console.log("ABRE");
                this.el.removeAttribute("animation");
                this.el.setAttribute("animation", {property: "rotation", to: this.data.rotation, dur: 500,  easing: "linear"});
                
                //this.el.setAttribute("rotation", this.data.rotation);
            }
        

            // Toggle the state
            this.data.opened = !this.data.opened;
        }
    },
  });


  AFRAME.registerComponent('raycaster-collide', {
    schema: {
      intersecting: { type: "boolean", default: false}
    },
    init: function () {
      this.timer = 0;
      var self = this
      this.el.addEventListener('raycaster-intersected', function (evt) {
        
        if (!this.components["raycaster-collide"].data.intersecting){
          var el = evt.target;
    // May get two intersection events per tick; same element, different faces.
          self.evt = evt;
          //console.log(evt);
          this.components["raycaster-collide"].data.intersecting = true;
          //console.log('raycaster-intersected ' + el.outerHTML);
          el.setAttribute('material', 'color', '#7f7');
        }
      });

      this.el.addEventListener('raycaster-intersected-cleared', function (evt) {
        if (this.components["raycaster-collide"].data.intersecting){
          self.evt = null;
          this.components["raycaster-collide"].data.intersecting = false;
          var el = evt.target;
          console.log("DEJA DE INTERSECTAR")
          const door_id = el.getAttribute("id")
          console.log(door_id)
          if (door_id.indexOf("invisible") !== -1) {
                  var real_door_s = door_id.split("-")
                  var real_door_id = real_door_s[1] + "-" + real_door_s[2];
                  console.log("------- DEJA DE INTERSECTAR CON PUERTA INVISIBLE --------", real_door_id)
                  door_dict[real_door_id] = true;
                  enable_camera_collisions(door_dict);

          } else {
            console.log(el.object3D)
          }
    // May get two intersection events per tick; same element, different faces.
          //console.log('raycaster-intersected-cleared ' + el.outerHTML);
          el.setAttribute('material', 'color', '#f77');
        }
      }); 
        // Add a listener for the 'tick' event to periodically check intersection.
      //this.el.addEventListener('tick', this.checkIntersection.bind(this));


    },
    tick: function (time, timedelta) {
      
      this.timer += timedelta;
      if (this.timer >= 1000){
      //console.log(this.el.getAttribute("id"))
      //console.log(this.data.intersecting);
      // Perform your periodic intersection check logic here.
      // For example, you can check the intersection status and take action.
        if (this.data.intersecting) {
          //console.log("Intersectando")
          //console.log(this)
          //console.log(this.el.components["door-test"]["data"]["opened"]);
          // Element is currently intersecting the raycaster.
          // Add your code to handle this scenario.

          const intersection = this.evt.detail.el.components.raycaster.getIntersection(this.el);
          if (intersection) {
            //console.log("INTERSECTANDO", intersection)
            var id_door = this.el.getAttribute("id")
            var proximity;
            if (id_door.indexOf("invisible") !== -1) {
              proximity = 5;
            } else {
               proximity = 2
            }
            
            camera = document.querySelector("#camera");
            const cameraObject3D = camera.object3D;
            const doorObject3D = this.el.object3D;
            const doorPosition = new THREE.Vector3();
            const cameraPosition = new THREE.Vector3();
           // console.log(doorObject3D)
            doorObject3D.getWorldPosition(doorPosition);
           // console.log(doorPosition);
            cameraObject3D.getWorldPosition(cameraPosition);
            const distance = cameraPosition.distanceTo(doorPosition);
            //console.log(distance)
            //console.log(proximity)
            if (distance < proximity) {

              if (id_door.indexOf("invisible") !== -1) {
                  //disable_collisions
                  var real_door_s = id_door.split("-")
                  var real_door_id = real_door_s[1] + "-" + real_door_s[2];
                  //console.log("------- INTERSECTANDO CON PUERTA INVISIBLE --------", real_door_id)
                  var real_door = document.querySelector("#" + real_door_id)
                  const opened_door = real_door.object3D.children[0].el.components["door-test"].data.opened
                  //console.log(opened_door)
                  if (opened_door) {
                    door_dict[real_door_id] = false;
                    cameraObject3D.el.components["camera-movement"].data.collisions = false;
                  }
              } else {
                var is_opened = this.el.components["door-test"].data.opened
              //console.log(is_opened)
              if (is_opened){
                camera.setAttribute('wasd-controls', {});
              } else {
                //console.log("CHOCANDO")
                var impulseStrength = 0.5; // Adjust the impulse strength as needed
                var point = intersection.point
                var cameraPos = camera.getAttribute("position")
                var direction = new THREE.Vector3().subVectors(point, cameraPos);
                direction.setY(0);
                var impulse = new THREE.Vector3().copy(direction).multiplyScalar(-impulseStrength);
                var new_pos = {
                  x: cameraPos.x + impulse.x,
                  y: cameraPos.y + impulse.y,
                  z: cameraPos.z + impulse.z,
                }
                camera.setAttribute("animation", {property: "position", to: new_pos, dur: 100, easing: "linear"});
              }
              }
              
            }



          }

        } else {
         
          camera = document.querySelector("#camera");
            const cameraObject3D = camera.object3D;
            //console.log("No intersectando", cameraObject3D.el.components["camera-movement"].data.collisions)
          // Element is not intersecting the raycaster.
          // Add your code to handle this scenario.
        }

        //const cameraEl= document.querySelector("#camera").object3D.el; 

        
        this.checkDirection();

        this.timer = 0
      }
    },

    checkDirection: function(){
        /*const doorEl = this.el.object3D
        var doorPosition;
        doorPosition = this.el.object3D.getWorldPosition(new THREE.Vector3());
        const windowPosition = new THREE.Vector3(doorPosition.x, doorPosition.y, doorPosition.z)
        var doorRotation = doorEl.parent.el.getAttribute("rotation");
        console.log(doorEl);
        console.log("ROTACION PUERTA: ", doorRotation)
        
        const windowHeight = 2.3
        const windowWidth = 1.1


        const camera2 = document.querySelector("#camera");
        const cameraPosition = camera2.getAttribute("position");
        const cameraRotation = camera2.getAttribute("rotation");

        const pitch = THREE.MathUtils.degToRad(cameraRotation.x);
        const yaw = THREE.MathUtils.degToRad(cameraRotation.y);

        const direction = new THREE.Vector3(
          -Math.sin(yaw) * Math.cos(pitch),
          Math.sin(pitch),
          -Math.cos(yaw) * Math.cos(pitch)
        );

        const holePosition = new THREE.Vector3(doorPosition.x, doorPosition.y, doorPosition.z); // Replace with the actual position
        const holeWidth = 1.1; // Replace with the actual width
        const holeHeight = 2.3; // Replace with the actual height

        const holeRotation = new THREE.Euler(THREE.MathUtils.degToRad(doorRotation.x), THREE.MathUtils.degToRad(doorRotation.y), THREE.MathUtils.degToRad(doorRotation.z), 'YXZ'); // Set rotation to "0 180 0"

        const holeRotationMatrix = new THREE.Matrix4();
        holeRotationMatrix.makeRotationFromEuler(holeRotation);

        const directionInverseRotated = direction.clone().applyEuler(holeRotation.clone().invert());

        const holeMin = new THREE.Vector3(
          holePosition.x - holeWidth / 2,
          holePosition.y - holeHeight / 2,
          holePosition.z
        ).applyMatrix4(holeRotationMatrix);

        const holeMax = new THREE.Vector3(
          holePosition.x + holeWidth / 2,
          holePosition.y + holeHeight / 2,
          holePosition.z
        ).applyMatrix4(holeRotationMatrix);

        const t = (
          (holeMin.x - cameraPosition.x) / directionInverseRotated.x,
          (holeMin.y - cameraPosition.y) / directionInverseRotated.y,
          (holeMin.z - cameraPosition.z) / directionInverseRotated.z
        );

        const intersectionPoint = new THREE.Vector3(
          cameraPosition.x + t * directionInverseRotated.x,
          cameraPosition.y + t * directionInverseRotated.y,
          cameraPosition.z + t * directionInverseRotated.z
        );

        const isInsideHole =
        intersectionPoint.x >= holeMin.x &&
        intersectionPoint.x <= holeMax.x &&
        intersectionPoint.y >= holeMin.y &&
        intersectionPoint.y <= holeMax.y;

        console.log("-----------TESTING -------------")
      console.log(this.el)
      console.log("CAMERA POSITION", cameraPosition)
      console.log("DIRECCION", direction)
      console.log("POSICION PUERTA", doorPosition)
      console.log("INTRSECCION", intersectionPoint);
      console.log("MIN", holeMin)
      console.log("MAX", holeMax)       
        
        if (isInsideHole) {
          console.log("The line intersects with the rotated hole in the wall.");
        } else {
          console.log("The line does not intersect with the rotated hole in the wall.");
        }*/

        /*const camera2= document.querySelector("#camera")
        // Get the position and rotation of the camera
        const position = camera2.getAttribute("position");
        const rotation = camera2.getAttribute("rotation");*/

        //A solution that nearly works
        // Convert rotation to radians
      // Convert rotation to radians
      /*const pitch = THREE.MathUtils.degToRad(rotation.x);
      const yaw = THREE.MathUtils.degToRad(rotation.y);

      // Calculate the direction vector
      const direction2 = new THREE.Vector3(
        -Math.sin(yaw) * Math.cos(pitch),
        -Math.sin(pitch),
        -Math.cos(yaw) * Math.cos(pitch)
      );

      const holePosition = new THREE.Vector3(doorPosition.x, doorPosition.y, doorPosition.z); // Replace with the actual position
      const holeWidth = 1.1; // Replace with the actual width
      const holeHeight = 2.3; // Replace with the actual height


      // Calculate the minimum and maximum coordinates of the hole's bounding box
      const holeMin = new THREE.Vector3(
        holePosition.x - holeWidth / 2,
        holePosition.y - holeHeight / 2,
        holePosition.z
      );
      const holeMax = new THREE.Vector3(
        holePosition.x + holeWidth / 2,
        holePosition.y + holeHeight / 2,
        holePosition.z
      );
      console.log("HOLE MAX ")
      console.log(holePosition);
      console.log(doorPosition)
      console.log(holeMax)
      const tx = (holePosition.x - position.x) / direction2.x;
      const ty = (holePosition.y - position.y) / direction2.y;
      const tz = (holePosition.z - position.z) / direction2.z;
      
      // Use the smallest non-negative t to get the intersection point
      let t = null;
      
      if (tx >= 0 && (t === null || tx < t)) {
        t = tx;
      }
      if (ty >= 0 && (t === null || ty < t)) {
        t = ty;
      }
      if (tz >= 0 && (t === null || tz < t)) {
        t = tz;
      }
      var intersectionPoint = new THREE.Vector3(
        position.x + t * direction2.x,
        position.y + t * direction2.y,
        position.z + t * direction2.z
      );

      const isInsideHole =
              intersectionPoint.x >= holeMin.x &&
              intersectionPoint.x <= holeMax.x &&
              intersectionPoint.y >= holeMin.y &&
              intersectionPoint.y <= holeMax.y;

      console.log("-----------TESTING -------------")
      console.log(this.el)
      console.log("CAMERA POSITION", position)
      console.log("DIRECCION", direction2)
      console.log("POSICION PUERTA", doorPosition)
      console.log("INTRSECCION", intersectionPoint);
      console.log("MIN", holeMin)
      console.log("MAX", holeMax)       
      intersectionPoint.y = 1.6
      const distanceToIntersection = position.distanceTo(doorPosition);  
      console.log("DISTANCIA", distanceToIntersection)
      var is_opened = this.el.components["door-test"].data.opened
      if (isInsideHole) {
        console.log("The line intersects with the hole in the wall.");
      } else {
        console.log("The line does not intersect with the hole in the wall.");
      }*/


    }


  });


  AFRAME.registerComponent('raycaster-wall', {
    schema: {
      intersecting: { type: "boolean", default: false}
    },
    init: function () {
      this.timer = 0;
      var self = this
      this.el.addEventListener('raycaster-intersected', function (evt) {
        //console.log(self);
        if (!self.data.intersecting){
          var el = evt.target;
    // May get two intersection events per tick; same element, different faces.
          self.evt = evt;
          //console.log(evt);
          self.data.intersecting = true;
          //console.log('raycaster-intersected ' + el.outerHTML);
          //el.setAttribute('material', 'color', '#7f7');
        }
      });

      this.el.addEventListener('raycaster-intersected-cleared', function (evt) {
        if (self.data.intersecting){
          self.evt = null;
          self.data.intersecting = false;
          var el = evt.target;
    // May get two intersection events per tick; same element, different faces.
          //console.log('raycaster-intersected-cleared ' + el.outerHTML);
        }
      }); 


    },
    tick: function (time, timedelta) {
    
      this.timer += timedelta;
      if ((this.timer >= 1000) && (this.evt)){
        /*console.log("----------------");
        console.log(this.evt);
        console.log(this.data.intersecting);
        console.log("-------------------");*/
      // Perform your periodic intersection check logic here.
      // For example, you can check the intersection status and take action.
        if (this.data.intersecting) {
          //console.log("Intersectando")
          //console.log(this)
          //console.log(this.el.components["door-test"]["data"]["opened"]);
          // Element is currently intersecting the raycaster.
          // Add your code to handle this scenario.
          //console.log(this.el)
          //console.log(this.evt.detail.el.components.raycaster)
          const intersection = this.evt.detail.el.components.raycaster.getIntersection(this.el);
          if (intersection) {
            const proximity = 1.25;
            camera = document.querySelector("#camera");
            //console.log(camera.object3D);
            const cameraObject3D = camera.object3D;
            const doorObject3D = this.el.object3D;
            /*console.log("LOG TESTING");
            console.log(doorObject3D);*/
            var obj;
            for (let i = 0; i < doorObject3D.children.length; i++) {
              if (doorObject3D.children[i].type === "Mesh") {
                obj = doorObject3D.children[i];
              }
            }
          
            const doorPosition = new THREE.Vector3();
            const cameraPosition = new THREE.Vector3();
            /*console.log("ANTES DEL FALLO");
            console.log(doorObject3D)*/
            //const obj = doorObject3D.children[0];
            const test = new THREE.Box3().setFromObject(obj)
            doorObject3D.getWorldPosition(doorPosition);
            cameraObject3D.getWorldPosition(cameraPosition);
            /*console.log("LOG TESTING");
            console.log(doorObject3D);
            console.log(doorPosition);
            console.log(cameraPosition);
            console.log(test)*/
            const closestPoint = new THREE.Vector3()
            const minPoint = new THREE.Vector3(test.min.x, test.min.y, test.min.z);
            const maxPoint = new THREE.Vector3(test.max.x, test.max.y, test.max.z);
            closestPoint.copy(cameraPosition)
            closestPoint.clamp(minPoint, maxPoint)
            const distance = cameraPosition.distanceTo(closestPoint);
            /*console.log(distance)
            console.log(proximity)*/
            //console.log("---camera position ----")
            //console.log(cameraPosition);
            const direction2 = new THREE.Vector3().subVectors(doorPosition, cameraPosition);
            //console.log("A VER", cameraObject3D.el.components["camera-movement"].data.prevPosition);
            const velocity = new THREE.Vector3().subVectors(cameraPosition, cameraObject3D.el.components["camera-movement"].data.prevPosition);
            const dotProduct = velocity.dot(direction2);
            if (dotProduct > 0) {
              console.log("Moving towards the wall.");
            } else {
              console.log("Not moving towards the wall.");
            }
        

            //console.log("DISTANCE:", distance)
      
            //console.log("MOVIMIENTO", movement);
            if ((distance < proximity) && (dotProduct > 0)) {
          
              
                console.log("CHOCANDO");
                var impulseStrength = 0.5; // Adjust the impulse strength as needed
                var point = intersection.point
                var cameraPos = camera.getAttribute("position")
                var direction = new THREE.Vector3().subVectors(point, cameraPos);
                direction.setY(0);
                var impulse = new THREE.Vector3().copy(direction).multiplyScalar(-impulseStrength);
                var new_pos = {
                  x: cameraPos.x + impulse.x,
                  y: cameraPos.y + impulse.y,
                  z: cameraPos.z + impulse.z,
                }
                camera.setAttribute("animation", {property: "position", to: new_pos, dur: 100, easing: "linear"});
              }
          }

        } else {
          //console.log("No intersectando")
          // Element is not intersecting the raycaster.
          // Add your code to handle this scenario.
        }
        this.timer = 0
      }
    },
  });