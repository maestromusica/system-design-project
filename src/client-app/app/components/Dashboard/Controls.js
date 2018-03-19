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

    }} type="danger">
      End current sorting
    </Button>
  )

  const startSortingBtn = (
    <Button onClick={ev => {

    }}>
      Start
    </Button>
  )

  const pauseSortingBtn = (
    <Button onClick={ev => {

    }}>
      Pause
    </Button>
  )

  return (
    <Section>
      {vision.sorting ? (
        <div>
          {thread.name == "vision" && !thread.locked
            ? pauseSortingBtn
            : startSortingBtn
          }
          {endSorting}
        </div>
      ) : (
        <div>
          {!vision.processing || vision.waiting ? (
            {startCapturingBtn}
          ) : (
            null
          )}
        </div>
      )}
    </Section>
  )
}

export default Controls
