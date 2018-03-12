import React, {Component} from 'react'
import * as THREE from 'three'
const OrbitControls = require('three-orbit-controls')(THREE)
import {adaptCoordinates} from '../../utils/simulation'
import {Button} from '../../styled/components'
import {
  Section,
  SectionTitle
} from '../../styled/section'

export default class SimulationRenderer extends Component {
  state = {
    scene: undefined,
    camera: undefined,
    cameraSize: {
      x: 20,
      y: 10,
      z: 14
    },
    boxes: [],
    simulationOngoing: false
  }

  _cleanRenderer(cb) {
    this.state.boxes.forEach(box => {
      const renderedBox = this.state.scene.getObjectByName(box)
      this.state.scene.remove(renderedBox)
    })
    this.setState({
      boxes: []
    }, () => {
      cb.call(this)
    })
  }

  _addBoxesToRenderer() {
    let boxes = this.props.boxes
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
        xCamera: this.state.cameraSize.x,
        yCamera: this.state.cameraSize.y,
        zCamera: this.state.cameraSize.z
      })
    }).map((box, id) => {
      box.id = id
      return box
    })

    let pos = 0
    const addToScene = () => {
      if(pos < boxes.length) {
        const box = boxes[pos]
        const itemGeometry = new THREE.BoxGeometry(box.width, box.height, box.depth)
        let cube = new THREE.Mesh(itemGeometry, itemMaterial)
        cube.position.set(box.x, box.y, box.z)
        cube.name = box.id
        pos += 1
        this.state.scene.add(cube)

        let geo = new THREE.EdgesGeometry(cube.geometry)
        let mat = new THREE.LineBasicMaterial({color: 0x888888, linewidth: 100})
        let wireframe = new THREE.LineSegments(geo, mat)
        cube.add(wireframe);
      }
      else {
        window.clearInterval(intervalID)
        this.setState({
          simulationOngoing: false
        })
      }
    }
    var intervalID

    this.setState({
      simulationOngoing: true,
      boxes: boxes.map(box => box.id)
    }, () => {
      intervalID = setInterval(addToScene, 300)
    })
  }

  componentDidMount() {
    let boxes = this.props.boxes

    let scene = new THREE.Scene();
    let camera = new THREE.PerspectiveCamera( 75, window.innerWidth/window.innerHeight, 0.1, 1000)
    let controls = new OrbitControls(camera, document.getElementById("graph-sim"))
    camera.position.set(0, 20, 10)
    controls.update()

    let renderer = new THREE.WebGLRenderer();
    renderer.setClearColor( 0xf0f0f0 );
    renderer.setSize( window.innerWidth / 2, window.innerHeight / 2 );
    document.getElementById('graph-sim').appendChild( renderer.domElement );

    camera.position.z = 5;
    renderer.render(scene, camera);

    let geometry = new THREE.BoxGeometry(
      this.state.cameraSize.x,
      this.state.cameraSize.y,
      this.state.cameraSize.z
    )

    let geo = new THREE.EdgesGeometry( geometry ); // or WireframeGeometry( geometry )
    let mat = new THREE.LineBasicMaterial( { color: 0x000000, linewidth: 2 } );
    let wireframe = new THREE.LineSegments( geo, mat );
    wireframe.position.set(0, 0, 0);
    wireframe.name = 'container';
    scene.add( wireframe );

    function animate() {
      requestAnimationFrame(animate);
      // required if controls.enableDamping or controls.autoRotate are set to true
      controls.update();
      renderer.render( scene, camera );
    }

    animate();

    this.setState({
      scene: scene
    })
  }

  componentWillUnmount() {
    let el = document.getElementById("graph-sim")
    el.outerHTML = ""
  }

  render() {
    return (
      <Section>
        <SectionTitle>Simulations</SectionTitle>
        <Button onClick={ev => {
          this._cleanRenderer(this._addBoxesToRenderer)
        }} disabled={this.state.simulationOngoing}>
          Start mocked simulation
        </Button>
        <div id="graph-sim"></div>
      </Section>
    )
  }
}
