try {
  document.querySelector('.main-footer div.float-right').remove()
} catch (e) {
  console.log(e)
}

try {
  document.querySelectorAll('textarea').forEach(e => e.setAttribute('rows', 3))
} catch (e) {
  console.log(e)
}