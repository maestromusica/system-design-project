import React, {Component} from 'react'
import * as THREE from 'three'
const OrbitControls = require('three-orbit-controls')(THREE)

const adaptCoordinates = (
  {x, y, z, width, height, depth},
  {xCamera, yCamera, zCamera}
) => {
  // the 0, 0, 0 position is in fact the center of the box
  return {
    x: x + width/2 -xCamera/2 ,
    y: y + height/2 - yCamera/2,
    z: z + depth/2 - zCamera/2,
    width,
    height,
    depth
  }
}

let boxes = [{
  x: 0,
  y: 0,
  z: 0,
  width: 7,
  height: 4,
  depth: 10
}, {
  x: 7,
  y: 0,
  z: 0,
  width: 6,
  height: 4,
  depth: 9
}, {
  x: 13,
  y: 0,
  z: 0,
  width: 5,
  height: 4,
  depth: 8
}, {
  x: 0,
  y: 4,
  z: 0,
  width: 6,
  height: 3,
  depth: 8
}, {
  x: 6,
  y: 4,
  z: 0,
  width: 6,
  height: 3,
  depth: 8
}, {
  x: 12,
  y: 4,
  z: 0,
  width: 6,
  height: 3,
  depth: 8
}, {
  x: 0,
  y: 7,
  z: 0,
  width: 10,
  height: 2,
  depth: 4
}, {
  x: 0,
  y: 7,
  z: 4,
  width: 9,
  height: 2,
  depth: 3
}, {
  x: 10,
  y: 7,
  z: 0,
  width: 5,
  height: 2,
  depth: 3
}]

export default class Simulations extends Component {
  componentDidMount() {
    let scene = new THREE.Scene();
    let camera = new THREE.PerspectiveCamera( 75, window.innerWidth/window.innerHeight, 0.1, 1000 );
    let controls = new OrbitControls( camera );
    camera.position.set(0, 20, 10)
    controls.update()

    let renderer = new THREE.WebGLRenderer();
    renderer.setClearColor( 0xf0f0f0 );
    renderer.setSize( window.innerWidth / 2, window.innerHeight / 2 );
    document.getElementById('graph-sim').appendChild( renderer.domElement );
    
    camera.position.z = 5;
    renderer.render(scene, camera);
    const cameraSize = {
      x: 20,
      y: 10,
      z: 14
    }

    let geometry = new THREE.BoxGeometry(
      cameraSize.x,
      cameraSize.y,
      cameraSize.z
    )

    let geo = new THREE.EdgesGeometry( geometry ); // or WireframeGeometry( geometry )
    let mat = new THREE.LineBasicMaterial( { color: 0x000000, linewidth: 2 } );
    let wireframe = new THREE.LineSegments( geo, mat );
    wireframe.position.set(0, 0, 0);
    wireframe.name = 'container';
    scene.add( wireframe );

    const itemMaterial = new THREE.MeshNormalMaterial({
      transparent: true,
      opacity: 0.8,
      // color: 0x000000,
      overdraw: 0.5,
      polygonOffset: true,
      polygonOffsetFactor: 1, // positive value pushes polygon further away
      polygonOffsetUnits: 1
    })

    boxes = boxes.map(box => {
      return adaptCoordinates(box, {
        xCamera: cameraSize.x,
        yCamera: cameraSize.y,
        zCamera: cameraSize.z
      })
    }).map((box, id) => {
      box.id = id
      return box
    })

    let pos = 0
    function addToScene() {
      if(pos < boxes.length) {
        const box = boxes[pos]
        const itemGeometry = new THREE.BoxGeometry(box.width, box.height, box.depth)
        let cube = new THREE.Mesh(itemGeometry, itemMaterial)
        cube.position.set(box.x, box.y, box.z)
        cube.name = box.id
        pos += 1
        scene.add(cube)

        let geo = new THREE.EdgesGeometry(cube.geometry)
        let mat = new THREE.LineBasicMaterial({color: 0x888888, linewidth: 100})
        let wireframe = new THREE.LineSegments(geo, mat)
        cube.add(wireframe);
      }
      else {
        window.clearInterval(intervalID)
      }
    }

    var intervalID = setInterval(addToScene, 300)

    function animate() {
      requestAnimationFrame( animate );
      // required if controls.enableDamping or controls.autoRotate are set to true
      controls.update();
      renderer.render( scene, camera );
    }

    animate();
  }

  render() {
    var aspectratio = this.props.width / this.props.height;
    var cameraprops = {
      fov: 10,
      aspect: aspectratio,
      near: 1,
      far: 5000,
      position: new THREE.Vector3(0, 0, 600),
      lookat: new THREE.Vector3(0, 0, 0)
    }

    return (
      <div id="graph-sim"></div>
    )
    }
  }
