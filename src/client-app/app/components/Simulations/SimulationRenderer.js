import React, {Component} from 'react'
import * as THREE from 'three'
const OrbitControls = require('three-orbit-controls')(THREE)
import {adaptCoordinates} from '../../utils/simulation'
import {Button} from '../../styled/components'
import {
  Section,
  SectionTitle
} from '../../styled/section'
import {Radio} from 'antd'
const RadioGroup = Radio.Group

const itemMaterial = new THREE.MeshNormalMaterial({
  transparent: true,
  opacity: 0.8,
  // color: 0x000000,
  overdraw: 0.5,
  polygonOffset: true,
  polygonOffsetFactor: 1, // positive value pushes polygon further away
  polygonOffsetUnits: 1
})

const hiddenMaterial = new THREE.MeshNormalMaterial({
  transparent: true,
  opacity: 0.2,
  // color: 0x000000,
  overdraw: 0.5,
  polygonOffset: true,
  polygonOffsetFactor: 1, // positive value pushes polygon further away
  polygonOffsetUnits: 1
})

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
    simulationOngoing: false,
    simulationFinished: false,
    level: -1
  }

  _resetLevel(level) {
    this.state.boxes[level].forEach(id => {
      let box = this.state.scene.getObjectByName(id)
      box.material = itemMaterial
    })
  }

  _hideLevel(level) {
    this.state.boxes[level].forEach(id => {
      let box = this.state.scene.getObjectByName(id)
      box.material = hiddenMaterial
    })
  }

  _showLevel(level) {
    const numOfLvls = this.state.boxes.length
    if(level === -1) {
      // this means we should show all levels
      for(let i=0; i<numOfLvls; i++) {
        this._resetLevel(i)
      }
    }
    else {
      for(let i=0; i<numOfLvls; i++) {
        if(i == level) {
          this._resetLevel(i)
        }
        else {
          console.log(i)
          this._hideLevel(i)
        }
      }
    }
  }

  _cleanRenderer(cb) {
    this.state.boxes.forEach(level => {
      level.forEach(id => {
        const box = this.state.scene.getObjectByName(id)
        this.state.scene.remove(box)
      })
    })
    this.setState({
      boxes: []
    }, () => {
      cb.call(this)
    })
  }

  _addBoxesToRenderer() {
    let boxes = this.props.boxes

    let pos = 0
    boxes = boxes.map(level => {
      return level.map(box => {
        return adaptCoordinates(box, {
          xCamera: this.state.cameraSize.x,
          yCamera: this.state.cameraSize.y,
          zCamera: this.state.cameraSize.z
        })
      })
    }).map(level => {
      return level.map(box => {
        box.id = pos++
        return box
      })
    })

    let flattenedBoxes = []
    boxes.forEach(level => {
      level.forEach((box, id) => {
        flattenedBoxes.push(box)
      })
    })

    pos = 0

    const addToScene = () => {
      if(pos < flattenedBoxes.length) {
        const box = flattenedBoxes[pos]
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
          simulationOngoing: false,
          simulationFinished: true
        })
      }
    }
    var intervalID

    this.setState({
      simulationOngoing: true,
      boxes: boxes.map(level => level.map(box => box.id))
    }, () => {
      intervalID = setInterval(addToScene, 300)
    })
  }

  componentDidMount() {
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
    let levels = []

    if(this.state.simulationFinished) {
      let numOfLvls = this.state.boxes.length
      for(let i=0; i<numOfLvls; i++) {
        levels.push(
          <Radio value={i} onClick={ev => {
            this.setState({
              level: i
            }, () => {
              this._showLevel(i)
            })
          }} key={i}>
            Level {i}
          </Radio>
        )
      }
      levels.push(
        <Radio value={-1} onClick={ev => {
          this.setState({
            level: -1
          })
          this._showLevel(-1)
        }} key={-1}>
          All levels
        </Radio>
      )
    }
    else {
      levels = null
    }

    return (
      <Section>
        <SectionTitle>Simulations</SectionTitle>
        <Button onClick={ev => {
          this._cleanRenderer(() => {
            this.setState({
              simulationOngoing: true,
              simulationFinished: false,
              level: -1
            })
            this._addBoxesToRenderer()
          })
        }} disabled={this.state.simulationOngoing}>
          Start mocked simulation
        </Button>
        {this.state.simulationFinished ? (
          <RadioGroup value={this.state.level}>
            {levels}
          </RadioGroup>
        ) : (
          null
        )}
        <div id="graph-sim"></div>
      </Section>
    )
  }
}
