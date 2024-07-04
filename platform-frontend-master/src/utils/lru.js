class LRUCache extends Map {
  constructor(capacity, map) {
    super(map)
    this.capacity = capacity || 100
  }
  set(key, value) {
    if (this.has(key)) {
      this.delete(key)
    } else {
      if (this.size >= this.capacity) {
        this.delete(this.keys().next().value)
      }
    }
    return super.set(key, value)
  }
  get(key) {
    if (this.has(key)) {
      const value = super.get(key)
      this.delete(key)
      super.set(key, value)
      return value
    } else return undefined
  }
}

export default LRUCache
