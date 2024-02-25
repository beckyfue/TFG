AFRAME.registerComponent('camera-listener', {
    init: function () {
      // Get a reference to the camera element with wasd-controls
      const camera = document.querySelector('[camera][wasd-controls]');
  
      // Listen for keydown events on the document
      document.addEventListener('keydown', (event) => {
        if (event.key === 'a') {
           // event.stopPropagation();
           // event.preventDefault();
          // Customize the 'a' key behavior here
            console.log("Custom 'a' key action");
          // You can add your own functionality here
        } else if (event.key === 's') {
          // Customize the 's' key behavior here
          console.log("Custom 's' key action");
          // You can add your own functionality here
        } else if (event.key === 'd') {
          // Customize the 'd' key behavior here
          console.log("Custom 'd' key action");
          // You can add your own functionality here
        }
      });
    }
  });

 


  AFRAME.registerComponent('camera-movement', {
    schema: {
      movement: { type: "vec3"}, // Default open rotation
      prevPosition: { type: "vec3"},
      collisions: { type: "boolean", default: true}
    },
    init: function(){
      this.timer = 0;
      this.data.movement = new THREE.Vector3();
      this.data.prevPosition = new THREE.Vector3();
    },
  
    tick: function(time, timedelta) {
        this.timer += timedelta;
        if (this.timer>=1000) {
          var cameraEntity = this.el;
          const currentPosition = cameraEntity.object3D.getWorldPosition(new THREE.Vector3());
          //const vector = new THREE.Vector3(this.data.prevPosition.x, this.data.prevPosition.y, this.data.prevPosition.z);
          const velocity = currentPosition.clone().sub(this.data.prevPosition);
          var movementDirection = new THREE.Vector3();
          if (velocity.length() > 0) {
            velocity.normalize();
            movementDirection.copy(velocity);
          } else {
            movementDirection = this.data.movement;
           // movementDirection.set(0, 0, 1); // Default direction (e.g., forward)
          }
         
          this.data.prevPosition.copy(currentPosition);
          movementDirection.setY(1.6);
          //console.log('Movement Direction:', movementDirection);
          this.data.movement.copy(movementDirection);
          this.timer = 0
      }
    }
  
  });

AFRAME.registerComponent('modify-materials', {
    init: function () {
      // Wait for model to load.
      this.el.addEventListener('model-loaded', () => {
        // Grab the mesh / scene.
        const obj = this.el.getObject3D('mesh');
        // Go over the submeshes and modify materials we want.
        obj.traverse(node => {
          if (node.name.indexOf('ship') !== -1) {
            node.material.color.set('red');
          }
        });
      });
    }
  });