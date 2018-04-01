import React from 'react'
import {
  Section
} from '../../styled/section'

import {
  Button
} from '../../styled/components'

const Controls = ({vision, thread, actions}) => {
  let rendered = null
  const startCapturingBtn = (
    <Button
      onClick={ev => {
        actions.processRequest()
      }}
      disabled={vision.waiting}
      loading={vision.waiting}
      type="primary"
    >
      Start capturing
    </Button>
  )

  const endSorting = (
    <Button onClick={ev => {
      actions.endSorting()
    }} type="danger">
      End current sorting
    </Button>
  )

  const startSortingBtn = (
    <Button onClick={ev => {
      actions.resumeSorting()
    }}>
      Start
    </Button>
  )

  const resumeSortingBtn = (
    <Button onClick={ev => {
      actions.resumeSorting()
    }}>
      Resume
    </Button>
  )

  const pauseSortingBtn = (
    <Button onClick={ev => {
      actions.pauseSorting()
    }}>
      Pause
    </Button>
  )

  return (
    <Section>
      {vision.sorting ? (
        <div>
          {!thread.locked ? (
            <Button loading disabled type="primary">Sorting</Button>
          ) : (null)}
          {(() => {
            if(!thread.locked) {
              return pauseSortingBtn
            }
            else {
              if(thread.locked && vision.startBtnPressed) {
                return resumeSortingBtn
              }
              else {
                return startSortingBtn
              }
            }
          })()}
          {endSorting}
        </div>
      ) : (
        <div>
          {!vision.processing || vision.waiting
            ? startCapturingBtn
            : null
          }
        </div>
      )}
    </Section>
  )
}

export default Controls
