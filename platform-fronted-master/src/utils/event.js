class EventManager {
  constructor() {
    this.eventMap = new Map()
  }
  addEventListener(eventName, func) {
    if (!this.eventMap.has(eventName)) this.eventMap.set(eventName, [])
    this.eventMap.get(eventName).push(func)
  }
  removeEventListener(eventName, func) {
    if (this.eventMap.has(eventName)) {
      this.eventMap.set(eventName, this.eventMap.get(eventName).filter((f) => f !== func))
    }
  }
  trigger(eventName, params) {
    if (this.eventMap.has(eventName)) {
      this.eventMap.get(eventName).forEach((func) => {
        func(params)
      })
    }
  }
}

export default EventManager
