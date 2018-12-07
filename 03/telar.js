const fs = require('fs');

const CLAIM_REGEX = /#(\d+) @ (\d+),(\d+): (\d+)x(\d+)/;

function parseClaims(claims) {
  return claims.map(claim => {
    if (claim.length == 0) return null;
    const groups = claim.match(CLAIM_REGEX);
    return {
      claim_id: parseInt(groups[1]),
      x: parseInt(groups[2]),
      y: parseInt(groups[3]),
      width: parseInt(groups[4]),
      height: parseInt(groups[5]),
    };
  }).filter(claim => claim != null);
}

function countConflicts(claims) {
  let array = new Array(1000).fill(0).map(() => new Array(1000).fill(0).map(() => []));
  let validClaims = claims.map(claim => claim.claim_id);
  claims.forEach(({ claim_id, x, y, width, height }) => {
    for (let i = x; i < x + width; i++) {
      for (let j = y; j < y + height; j++) {
        if (array[i][j].length > 0) {
          if (validClaims.indexOf(claim_id) != -1) {
            validClaims.splice(validClaims.indexOf(claim_id), 1);
          }
          array[i][j].forEach(invalidClaim => {
            if (validClaims.indexOf(invalidClaim) != -1) {
              validClaims.splice(validClaims.indexOf(invalidClaim), 1);
            }
          });
        }
        array[i][j].push(claim_id);
      }
    }
  });
  // return array.reduce((acumulador, fila) => {
  //   return fila.filter(celda => celda.length > 1).length + acumulador;
  // }, 0);
  return validClaims;
}

fs.readFile('claims.txt', (err, data) => {
  if (err) {
    throw err;
  }
  let claims = parseClaims(data.toString().split('\n'));
  let totalConflicts = countConflicts(claims);
  console.log(totalConflicts);
});
