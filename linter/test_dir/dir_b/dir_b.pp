class psycclient::class {
  case $facts['networking']['hostname'] {
    /pspctrilab/ : { include itsclient::x2goserver }
  }
}
