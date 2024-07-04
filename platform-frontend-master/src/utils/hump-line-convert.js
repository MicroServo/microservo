export const toHump = function(name) {
  return name.replace(/_(\w)/g, function(all, letter) {
    return letter.toUpperCase()
  })
}

export const toLine = function(name) {
  return name.replace(/([A-Z])/g, '_$1').toLowerCase()
}
