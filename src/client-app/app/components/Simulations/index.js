import React, {Component} from 'react'
import * as THREE from 'three'
const OrbitControls = require('three-orbit-controls')(THREE)

export default class Simulations extends Component {
  state = {

  }

  componentDidMount() {
    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera( 75, window.innerWidth/window.innerHeight, 0.1, 1000 );
    var controls = new OrbitControls( camera );
    camera.position.set(0, 20, 100)
    controls.update()

    var renderer = new THREE.WebGLRenderer();
    renderer.setClearColor( 0xf0f0f0 );
    renderer.setSize( window.innerWidth / 2, window.innerHeight / 2 );
    document.getElementById('graph-sim').appendChild( renderer.domElement );

    // var geometry = new THREE.BoxGeometry( 1, 1, 1 );
    // var material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
    // var cube = new THREE.Mesh( geometry, material );
    // scene.add( cube );

    camera.position.z = 5;
    renderer.render(scene, camera);

    var geometry = new THREE.BoxGeometry(20, 20, 20);
    var geo = new THREE.EdgesGeometry( geometry ); // or WireframeGeometry( geometry )
    var mat = new THREE.LineBasicMaterial( { color: 0x000000, linewidth: 2 } );
    var wireframe = new THREE.LineSegments( geo, mat );
    wireframe.position.set(0, 0, 0);
    wireframe.name = 'container';
    scene.add( wireframe );

    // pack two items
    var itemGeometry = new THREE.BoxGeometry(4, 4, 4)
    var itemMaterial = new THREE.MeshNormalMaterial({
      transparent: true, opacity: 0.6
    })
    var cube = new THREE.Mesh(itemGeometry, itemMaterial)
    cube.position.set(-8, -8, -8)
    cube.name = "1"
    scene.add(cube)

    var cube2 = new THREE.Mesh(itemGeometry, itemMaterial)
    cube2.position.set(-4, -8, -8)
    cube2.name="2"
    scene.add(cube2)


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
    var cameraprops = {fov : 75, aspect : aspectratio,
      near : 1, far : 5000,
      position : new THREE.Vector3(0,0,600),
      lookat : new THREE.Vector3(0,0,0)};

      return (
        <div id="graph-sim"></div>
      )
    }
  }
